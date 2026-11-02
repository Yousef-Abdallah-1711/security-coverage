import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="security coverage-")
        self.base = Path(self.temp.name) / "安全 home"
        self.base.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_install_reinstall_and_uninstall_only_owned_files(self):
        lines = installer.install(ROOT, self.base, "claude")
        self.assertTrue((self.base / "skills/security-coverage/SKILL.md").is_file())
        self.assertTrue((self.base / "commands/security-assess.md").is_file())
        installer.install(ROOT, self.base, "claude")
        unrelated = self.base / "skills/other/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("keep", encoding="utf-8")
        installer.uninstall(self.base)
        self.assertFalse((self.base / "skills/security-coverage/SKILL.md").exists())
        self.assertTrue(unrelated.exists())

    def test_unowned_collision_fails_without_overwrite(self):
        dst = self.base / "commands/security-plan.md"
        dst.parent.mkdir(parents=True)
        dst.write_text("personal command", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            installer.install(ROOT, self.base, "claude")
        self.assertEqual(dst.read_text(encoding="utf-8"), "personal command")

    def test_modified_owned_file_is_preserved_on_uninstall(self):
        installer.install(ROOT, self.base, "claude")
        dst = self.base / "commands/security-implement.md"
        dst.write_text("user edit", encoding="utf-8")
        lines = installer.uninstall(self.base)
        self.assertEqual(dst.read_text(encoding="utf-8"), "user edit")
        self.assertTrue(any("modified" in line for line in lines))

    def test_codex_plugin_files_are_installed(self):
        installer.install(ROOT, self.base, "codex")
        self.assertTrue((self.base / "plugins/security-coverage/.codex-plugin/plugin.json").is_file())
        self.assertTrue((self.base / "plugins/security-coverage/skills/security-coverage/SKILL.md").is_file())

    def test_uninstall_is_repeatable(self):
        installer.install(ROOT, self.base, "claude")
        installer.uninstall(self.base)
        installer.uninstall(self.base)
        self.assertFalse((self.base / installer.MANIFEST).exists())

    def test_output_escapes_paths_not_representable_by_console_encoding(self):
        buffer = io.BytesIO()
        stream = io.TextIOWrapper(buffer, encoding="cp1252")
        installer.print_safe("Installed files to C:/安全", stream=stream)
        stream.flush()
        self.assertIn(b"C:/\\u5b89\\u5168", buffer.getvalue())

    def test_update_backs_up_prior_managed_version(self):
        installer.install(ROOT, self.base, "claude")
        managed = self.base / "commands/security-assess.md"
        old = managed.read_bytes()
        # Use a disposable source copy to model an upstream update.
        with tempfile.TemporaryDirectory() as source_dir:
            import shutil
            source = Path(source_dir)
            shutil.copytree(ROOT / "skills", source / "skills")
            shutil.copytree(ROOT / "commands", source / "commands")
            shutil.copytree(ROOT / ".codex-plugin", source / ".codex-plugin")
            changed = source / "commands/security-assess.md"
            changed.write_text(changed.read_text(encoding="utf-8") + "\nUpdate fixture.\n", encoding="utf-8")
            installer.install(source, self.base, "claude")
        self.assertNotEqual(managed.read_bytes(), old)
        backups = list((self.base / ".security-coverage-backups").rglob("security-assess.md"))
        self.assertTrue(backups)
        self.assertEqual(backups[0].read_bytes(), old)

    def test_partial_failure_rolls_back_new_files(self):
        original = installer.atomic_copy
        count = {"n": 0}
        def fail_second(src, dst):
            count["n"] += 1
            if count["n"] == 2:
                raise OSError("controlled fixture failure")
            original(src, dst)
        with mock.patch.object(installer, "atomic_copy", fail_second):
            with self.assertRaises(OSError):
                installer.install(ROOT, self.base, "claude")
        self.assertFalse((self.base / installer.MANIFEST).exists())
        self.assertFalse((self.base / "commands/security-assess.md").exists())

    def test_path_traversal_manifest_rejected(self):
        path = self.base / installer.MANIFEST
        path.write_text('{"files":{"../../outside":"' + "0" * 64 + '"}}', encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            installer.read_manifest(path)


if __name__ == "__main__":
    unittest.main()
