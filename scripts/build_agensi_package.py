#!/usr/bin/env python3
"""Build and validate the one-skill Agensi ZIP. Python 3.8+, standard library."""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "security-coverage"
OUTPUT = ROOT / "dist" / "security-coverage-agensi.zip"
SECRET_PATTERNS = [re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), re.compile(r"\bAKIA[0-9A-Z]{16}\b")]


def validate_sources():
    skill_md = SKILL / "SKILL.md"
    raw = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", raw, re.S)
    if not match:
        raise ValueError("SKILL.md is missing YAML frontmatter")
    front = yaml.safe_load(match.group(1))
    if not isinstance(front, dict) or not front.get("name") or not front.get("description"):
        raise ValueError("SKILL.md requires name and description")
    if front["name"] != SKILL.name or len(front["description"]) > 1024:
        raise ValueError("SKILL.md name must match its directory and description must be <=1024 chars")
    files = [p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts and "node_modules" not in p.parts]
    for path in files:
        try:
            path.resolve().relative_to(SKILL.resolve())
            contained = True
        except ValueError:
            contained = False
        if path.is_symlink() or not contained:
            raise ValueError("Unsafe path in skill source: {}".format(path))
        if path.suffix.lower() in {".exe", ".dll", ".so", ".dylib", ".bin", ".wasm", ".pyc"}:
            raise ValueError("Executable/binary file is not allowed: {}".format(path))
        if "__pycache__" in path.parts or "node_modules" in path.parts or ".git" in path.parts:
            raise ValueError("Generated/dependency directory is not allowed: {}".format(path))
        if path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".sh", ".ps1"}:
            text = path.read_text(encoding="utf-8", errors="strict")
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                raise ValueError("Possible credential/private-key material in package source: {}".format(path))
    if not (ROOT / "LICENSE").is_file():
        raise ValueError("LICENSE file missing")
    return front, sorted(files)


def create_zip(output=OUTPUT):
    front, files = validate_sources()
    entries = [(ROOT / "LICENSE", PurePosixPath("security-coverage/LICENSE"))]
    entries += [(path, PurePosixPath("security-coverage") / PurePosixPath(path.relative_to(SKILL).as_posix())) for path in files]
    skill_count = sum(1 for _, rel in entries if rel.name == "SKILL.md")
    if skill_count != 1:
        raise ValueError("Package must contain exactly one SKILL.md; found {}".format(skill_count))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(output), "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, rel in entries:
            archive.write(str(source), rel.as_posix())
    with zipfile.ZipFile(str(output), "r") as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError("ZIP integrity failure at " + bad)
        names = archive.namelist()
        if any(PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts for name in names):
            raise ValueError("Unsafe archive path found")
        if sum(1 for name in names if PurePosixPath(name).name == "SKILL.md") != 1:
            raise ValueError("Archive must contain exactly one SKILL.md")
    data = output.read_bytes()
    return {"path": str(output), "name": front["name"], "version": front.get("metadata", {}).get("version", "unversioned"), "files": len(entries), "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate sources without creating an archive")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args(argv)
    try:
        front, files = validate_sources()
        if args.check:
            print(json.dumps({"status":"PASS", "skill_count":1, "files":len(files)+1, "name":front["name"]}, indent=2))
        else:
            print(json.dumps(create_zip(args.output), indent=2))
        return 0
    except (OSError, ValueError, yaml.YAMLError, zipfile.BadZipFile) as exc:
        print("package validation failed: {}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
