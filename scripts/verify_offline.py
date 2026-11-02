#!/usr/bin/env python3
"""Verify detector and package build work inside a networkless container."""
import hashlib
import json
import socket
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path("/workspace")
FIXTURE = ROOT / "tests" / "fixtures" / "vulnerable_app"
DETECTOR = ROOT / "skills" / "security-coverage" / "scripts" / "detect_security_stack.py"
BUILDER = ROOT / "scripts" / "build_agensi_package.py"
OUTPUT = Path("/tmp/security-coverage-agensi-offline.zip")


def run(command):
    return subprocess.run(command, cwd=str(ROOT), check=True, capture_output=True, text=True)


def main():
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=2):
            raise RuntimeError("network boundary failed: external TCP connection succeeded")
    except OSError as exc:
        network_probe = "BLOCKED ({})".format(type(exc).__name__)

    scan_result = run([sys.executable, str(DETECTOR), str(FIXTURE), "--json"])
    scan = json.loads(scan_result.stdout)
    if scan.get("scan_status") != "COMPLETE":
        raise RuntimeError("offline detector did not complete: {}".format(scan.get("scan_status")))

    check = run([sys.executable, str(BUILDER), "--check"])
    check_result = json.loads(check.stdout)
    if check_result.get("status") != "PASS":
        raise RuntimeError("offline package source check did not pass")

    build = run([sys.executable, str(BUILDER), "--output", str(OUTPUT)])
    build_result = json.loads(build.stdout)
    with zipfile.ZipFile(str(OUTPUT), "r") as archive:
        bad = archive.testzip()
        names = archive.namelist()
        if bad:
            raise RuntimeError("offline package archive failed integrity check: {}".format(bad))
        if sum(PurePosixPath(name).name == "SKILL.md" for name in names) != 1:
            raise RuntimeError("offline package must contain exactly one SKILL.md")
        if any(PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts for name in names):
            raise RuntimeError("offline package contains an unsafe archive path")

    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    if digest != build_result.get("sha256"):
        raise RuntimeError("offline package digest does not match package-builder output")

    print(json.dumps({
        "status": "PASS",
        "network_probe": network_probe,
        "detector_scan_status": scan["scan_status"],
        "detector_file_count": scan["file_count"],
        "package_source_validation": check_result["status"],
        "package_file_count": len(names),
        "package_size_bytes": build_result["size_bytes"],
        "package_sha256": digest,
        "package_integrity": "PASS",
        "exactly_one_skill_md": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print("offline verification failed: {}".format(exc), file=sys.stderr)
        raise SystemExit(1)
