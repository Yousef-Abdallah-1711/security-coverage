import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "security-coverage"


class ContractTests(unittest.TestCase):
    def test_only_one_discoverable_skill_and_frontmatter_valid(self):
        files = list(ROOT.rglob("SKILL.md"))
        self.assertEqual([p.relative_to(ROOT).as_posix() for p in files], ["skills/security-coverage/SKILL.md"])
        text = files[0].read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match)
        meta = yaml.safe_load(match.group(1))
        self.assertEqual(meta["name"], "security-coverage")
        self.assertTrue(meta["description"])
        self.assertLessEqual(len(meta["description"]), 1024)
        self.assertEqual(meta["license"], "MIT")
        self.assertEqual(meta["version"], "1.0.0")
        self.assertTrue(meta["summary"])
        self.assertTrue(meta["use_cases"])

    def test_skill_references_resolve_inside_package(self):
        body = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotRegex(body, r"(?:^|[(/])\.\./")
        for relative in re.findall(r"(?:references|templates|scripts)/[A-Za-z0-9_.-]+\.\w+", body):
            self.assertTrue((SKILL_ROOT / relative).is_file(), relative)
        for path in (SKILL_ROOT / "references").glob("*.md"):
            self.assertTrue(path.is_file())

    def test_templates_share_required_schema_terms(self):
        strategy = (SKILL_ROOT / "templates/SECURITY-STRATEGY.md").read_text(encoding="utf-8")
        plan = (SKILL_ROOT / "templates/SECURITY-PLAN.md").read_text(encoding="utf-8")
        tasks = (SKILL_ROOT / "templates/SECURITY-TASKS.md").read_text(encoding="utf-8")
        evidence = (SKILL_ROOT / "templates/SECURITY-EVIDENCE-LOG.md").read_text(encoding="utf-8")
        for field in ("ID", "Layer", "Severity", "Evidence", "Affected files", "Recommended action"):
            self.assertIn(field, strategy)
        for field in ("Source findings", "Acceptance criteria", "Verification", "Residual risks"):
            self.assertIn(field, plan)
        for field in ("Task ID", "Source finding", "Phase", "Status"):
            self.assertIn(field, tasks)
        for field in ("Commands executed", "Actual results", "Failed checks", "Skipped checks", "Remaining risks", "Gate result"):
            self.assertIn(field, evidence)

    def test_workflow_adapters_require_approval_and_are_thin(self):
        implement = (ROOT / "commands/security-implement.md").read_text(encoding="utf-8").lower()
        self.assertIn("explicit approval", implement)
        self.assertIn("plan is not approval", implement)
        for path in (ROOT / "commands").glob("*.md"):
            self.assertLess(len(path.read_text(encoding="utf-8")), 1200)

    def test_plugin_and_package_json_parse(self):
        json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    def test_readme_local_links_resolve(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            self.assertTrue((ROOT / target).exists(), target)

    def test_package_builder_is_readable_and_no_zip_slip_literals(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/build_agensi_package.py"), "--check"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_package_archive_has_one_skill_and_safe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "skill.zip"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_agensi_package.py"), "--output", str(archive)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()
                self.assertTrue(all(".." not in Path(name).parts for name in names))
                self.assertEqual(sum(Path(name).name == "SKILL.md" for name in names), 1)
                self.assertIsNone(zf.testzip())
                self.assertIn("security-coverage/SKILL.md", names)
                self.assertNotIn("install.sh", names)
                extracted = Path(tmp) / "extracted"
                zf.extractall(extracted)
                self.assertTrue((extracted / "security-coverage/SKILL.md").is_file())
                self.assertTrue((extracted / "security-coverage/references/layers.md").is_file())


if __name__ == "__main__":
    unittest.main()
