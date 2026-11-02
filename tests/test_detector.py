import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "security-coverage" / "scripts" / "detect_security_stack.py"
spec = importlib.util.spec_from_file_location("detector", SCRIPT)
detector = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = detector
spec.loader.exec_module(detector)


class DetectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_empty_repository_is_not_scanned(self):
        result = detector.detect(self.root)
        self.assertEqual(result["scan_status"], "NOT SCANNED")
        self.assertEqual(result["file_count"], 0)

    def test_next_react_and_express_fixtures(self):
        self.write("package.json", '{"dependencies":{"next":"15","react":"19","express":"5"}}')
        result = detector.detect(self.root)
        self.assertEqual(result["frameworks"]["Next.js"], ["package.json"])
        self.assertEqual(result["frameworks"]["React"], ["package.json"])
        self.assertEqual(result["frameworks"]["Express"], ["package.json"])
        self.assertEqual(result["states"]["frameworks"]["Next.js"]["status"], "DETECTED")

    def test_python_go_php_and_multistack(self):
        self.write("pyproject.toml", '[project]\ndependencies=["fastapi"]')
        self.write("main.py", "from fastapi import FastAPI")
        self.write("go.mod", "module sample\n")
        self.write("main.go", "package main\n")
        self.write("composer.json", '{"require":{"laravel/framework":"*"}}')
        self.write("index.php", "<?php echo 'ok';")
        result = detector.detect(self.root)
        self.assertIn("Python", result["languages"])
        self.assertIn("Go", result["languages"])
        self.assertIn("PHP", result["languages"])
        self.assertIn("FastAPI", result["frameworks"])
        self.assertIn("Laravel", result["frameworks"])

    def test_comment_noise_does_not_detect_generic_login_or_payment_words(self):
        self.write("app.py", "# TODO login payment dashboard\nprint('hello')\n")
        result = detector.detect(self.root)
        self.assertNotIn("auth_session", result["signals"])
        self.assertNotIn("payments", result["signals"])

    def test_large_file_warns_and_marks_incomplete(self):
        self.write("large.py", "x" * (detector.MAX_FILE_BYTES + 1))
        result = detector.detect(self.root)
        self.assertEqual(result["scan_status"], "INCOMPLETE SCAN")
        self.assertTrue(any("exceeds 2 MB" in item for item in result["warnings"]))

    def test_file_count_limit_warns_and_marks_incomplete(self):
        for name in ("a.py", "b.py", "c.py"):
            self.write(name, "print('ok')")
        with mock.patch.object(detector, "MAX_FILES", 2):
            result = detector.detect(self.root)
        self.assertEqual(result["scan_status"], "INCOMPLETE SCAN")
        self.assertTrue(any("Maximum file count" in item for item in result["warnings"]))

    def test_environment_flag_reports_path_without_reading_value(self):
        self.write(".env.production", "API_KEY=synthetic-test-value")
        result = detector.detect(self.root)
        self.assertIn("Environment file present: .env.production", result["risk_flags"])
        self.assertNotIn("synthetic-test-value", json.dumps(result))

    def test_symlink_escape_is_skipped(self):
        outside = self.root.parent / (self.root.name + "-outside.py")
        outside.write_text("stripe webhook", encoding="utf-8")
        try:
            (self.root / "external.py").symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is not available")
        try:
            result = detector.detect(self.root)
            self.assertNotIn("payments", result["signals"])
            self.assertTrue(any("Symlink outside" in item for item in result["warnings"]))
        finally:
            outside.unlink(missing_ok=True)

    def test_depth_limit_is_reported(self):
        self.write("/".join(["d"] * (detector.MAX_DEPTH + 2) + ["a.py"]), "print('ok')")
        result = detector.detect(self.root)
        self.assertEqual(result["scan_status"], "INCOMPLETE SCAN")
        self.assertTrue(any("depth" in item.lower() for item in result["warnings"]))

    def test_binary_is_skipped(self):
        path = self.root / "app.py"
        path.write_bytes(b"\x00\xffstripe")
        result = detector.detect(self.root)
        self.assertNotIn("payments", result["signals"])

    def test_unreadable_file_warning(self):
        path = self.write("app.py", "print('x')")
        original_open = Path.open
        intercepted = []
        def fail_open(file, *args, **kwargs):
            if file == path:
                intercepted.append(file)
                raise PermissionError("denied")
            return original_open(file, *args, **kwargs)
        with mock.patch.object(Path, "open", fail_open):
            result = detector.detect(self.root)
        self.assertEqual(intercepted, [path])
        self.assertEqual(result["scan_status"], "INCOMPLETE SCAN")
        self.assertTrue(any("Unreadable file" in item for item in result["warnings"]))

    def test_json_output_and_invalid_path_exit_codes(self):
        good = subprocess.run([sys.executable, str(SCRIPT), str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        self.assertEqual(json.loads(good.stdout)["schema_version"], 2)
        bad = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "missing")], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        invalid = subprocess.run([sys.executable, str(SCRIPT), "--unsupported"], capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 2)

    def test_swift_and_dart_extensions_are_counted(self):
        self.write("App.swift", "import Foundation")
        self.write("lib/main.dart", "void main() {}")
        result = detector.detect(self.root)
        self.assertIn("Swift", result["languages"])
        self.assertIn("Dart", result["languages"])

    def test_synthetic_fixture_yields_review_leads_without_claiming_vulnerabilities(self):
        fixture = ROOT / "tests/fixtures/vulnerable_app"
        result = detector.detect(fixture)
        self.assertEqual(result["scan_status"], "COMPLETE")
        self.assertIn("api_surface", result["signals"])
        self.assertIn("database", result["signals"])
        self.assertNotIn("vulnerabilities", result)
        source = (fixture / "app.py").read_text(encoding="utf-8")
        self.assertIn("SESSION_COOKIE_SECURE = False", source)
        self.assertIn('WHERE id = %s', source)


if __name__ == "__main__":
    unittest.main()
