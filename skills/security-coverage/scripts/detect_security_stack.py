#!/usr/bin/env python3
"""Report heuristic stack and attack-surface signals; never report vulnerabilities.

Standard-library only. Symlink targets are not followed. Text samples are bounded.
JSON schema v2 adds explicit signal states and scan warnings while retaining the
v1 summary keys (`languages`, `frameworks`, `signals`, and `layer_hints`).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

MAX_DEPTH = 32
MAX_FILES = 50000
MAX_FILE_BYTES = 2_000_000
SAMPLE_BYTES = 200_000
IGNORE_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", "__pycache__", ".next", "dist", "build", "coverage", ".cache", ".pytest_cache", ".venv", "venv"}
TEXT_EXTS = {".js", ".jsx", ".ts", ".tsx", ".php", ".py", ".rb", ".go", ".rs", ".java", ".kt", ".cs", ".swift", ".dart", ".html", ".css", ".json", ".yml", ".yaml", ".toml", ".env", ".md", ".sql", ".sh", ".conf", ".ini", ".xml", ".gradle", ".kts"}
LANG_BY_EXT = {".js":"JavaScript", ".jsx":"JavaScript", ".ts":"TypeScript", ".tsx":"TypeScript", ".php":"PHP", ".py":"Python", ".rb":"Ruby", ".go":"Go", ".rs":"Rust", ".java":"Java", ".kt":"Kotlin", ".cs":"C#", ".swift":"Swift", ".dart":"Dart"}
PACKAGE_FILES = {"package.json":"JavaScript package metadata", "pnpm-lock.yaml":"pnpm", "yarn.lock":"Yarn", "package-lock.json":"npm", "composer.json":"Composer/PHP", "requirements.txt":"pip", "pyproject.toml":"Python", "Pipfile":"Pipenv", "poetry.lock":"Poetry", "Gemfile":"Bundler/Ruby", "go.mod":"Go modules", "Cargo.toml":"Cargo/Rust", "pom.xml":"Maven", "build.gradle":"Gradle", "build.gradle.kts":"Gradle"}
# Strong markers use full-ish tokens; broad heuristic surfaces stay POSSIBLE.
FRAMEWORKS = {
    "Next.js": [r"next\.config\.(?:js|mjs|ts)", r"['\"]next['\"]\s*:"] ,
    "React": [r"['\"]react['\"]\s*:", r"from\s+['\"]react['\"]"],
    "Vue": [r"['\"]vue['\"]\s*:", r"from\s+['\"]vue['\"]"],
    "Express": [r"['\"]express['\"]\s*:", r"require\(['\"]express['\"]\)"],
    "Django": [r"from\s+django\.", r"import\s+django", r"manage\.py", r"['\"]django['\"]\s*:"],
    "Flask": [r"from\s+flask\s+import", r"import\s+flask", r"['\"]flask['\"]\s*:"],
    "FastAPI": [r"from\s+fastapi\s+import", r"FastAPI\s*\(", r"['\"]fastapi['\"]\s*:"],
    "Laravel": [r"laravel/framework", r"Illuminate\\"], "Symfony": [r"symfony/"],
    "Rails": [r"config/routes\.rb", r"gem\s+['\"]rails['\"]"],
    "Supabase": [r"['\"]@supabase/[^'\"]+['\"]\s*:", r"from\s+['\"]@supabase/", r"supabase/migrations/"],
}
SIGNAL_PATTERNS = {
    "auth_session": [r"session_start", r"setcookie", r"password_hash", r"passport", r"nextauth", r"auth0", r"jwt", r"oauth", r"csrf"],
    "admin_surface": [r"/admin(?:/|\b)", r"is_admin", r"admin_"],
    "api_surface": [r"/api/", r"fetch\s*\(", r"axios", r"router\.", r"\$_POST", r"\$_GET"],
    "database": [r"\bselect\s+", r"\binsert\s+into\b", r"\bupdate\s+\w+\s+set\b", r"\bdelete\s+from\b", r"mysqli", r"\bPDO\b", r"postgres", r"mysql", r"sqlite", r"mongodb", r"supabase"],
    "payments": [r"stripe", r"paymob", r"paypal", r"paddle", r"webhook", r"payment_status", r"paid_amount"],
    "secrets_config": [r"secret", r"private_key", r"service_key", r"api_key", r"\.env"],
    "browser_security": [r"innerHTML", r"dangerouslySetInnerHTML", r"target\s*=\s*['\"]_blank", r"Content-Security-Policy", r"htmlspecialchars", r"sanitize"],
    "infrastructure": [r"Dockerfile", r"docker-compose", r"nginx", r"apache", r"\.htaccess", r"github/workflows", r"vercel", r"netlify"],
}
COMPILED = {group: {name: [re.compile(p, re.I) for p in pats] for name, pats in values.items()} for group, values in (("frameworks", FRAMEWORKS), ("signals", SIGNAL_PATTERNS))}


def inside(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def iter_files(root: Path, warnings: List[str]) -> Iterable[Path]:
    count = 0
    def on_error(exc: OSError) -> None:
        location = getattr(exc, "filename", None) or str(root)
        try:
            location = Path(location).relative_to(root).as_posix()
        except ValueError:
            location = "outside selected root"
        warnings.append("Directory scan failed ({}): {}".format(type(exc).__name__, location))

    for current, dirs, files in os.walk(str(root), topdown=True, onerror=on_error, followlinks=False):
        base = Path(current)
        try:
            depth = len(base.relative_to(root).parts)
        except ValueError:
            warnings.append("Traversal escaped selected root; remaining paths skipped")
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not (base / d).is_symlink()]
        if depth >= MAX_DEPTH and dirs:
            warnings.append("Maximum traversal depth reached; deeper paths not scanned")
            dirs[:] = []
        for name in files:
            count += 1
            if count > MAX_FILES:
                warnings.append("Maximum file count reached; remaining paths not scanned")
                return
            yield base / name


def read_text(path: Path, root: Path, warnings: List[str]) -> Optional[str]:
    if path.is_symlink():
        try:
            target = path.resolve(strict=True)
            if not inside(root, target):
                warnings.append("Symlink outside selected root skipped: " + path.relative_to(root).as_posix())
                return None
        except OSError:
            warnings.append("Broken or inaccessible symlink skipped: " + path.relative_to(root).as_posix())
            return None
    try:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            warnings.append("File exceeds 2 MB and was not scanned: " + path.relative_to(root).as_posix())
            return None
        with path.open("rb") as handle:
            raw = handle.read(SAMPLE_BYTES + 1)
        if b"\x00" in raw:
            return None
        if len(raw) > SAMPLE_BYTES:
            warnings.append("Text sample truncated at 200 KB: " + path.relative_to(root).as_posix())
        return raw[:SAMPLE_BYTES].decode("utf-8", errors="replace")
    except OSError as exc:
        warnings.append("Unreadable file skipped (" + type(exc).__name__ + "): " + path.relative_to(root).as_posix())
        return None


def detect(root: Path) -> dict:
    warnings: List[str] = []
    root = root.resolve()
    files = list(iter_files(root, warnings))
    by_ext: Dict[str, int] = defaultdict(int)
    languages: Dict[str, int] = defaultdict(int)
    package_managers: Dict[str, List[str]] = defaultdict(list)
    frameworks: Dict[str, List[str]] = defaultdict(list)
    signals: Dict[str, List[str]] = defaultdict(list)
    risk_flags: List[str] = []
    scanned = 0
    for path in files:
        rel = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        if suffix:
            by_ext[suffix] += 1
        if suffix in LANG_BY_EXT:
            languages[LANG_BY_EXT[suffix]] += 1
        if path.name in PACKAGE_FILES:
            package_managers[PACKAGE_FILES[path.name]].append(rel)
        if path.name.startswith(".env") and path.name != ".env.example":
            risk_flags.append("Environment file present: " + rel)
        if suffix in {".pem", ".key", ".p12", ".pfx"}:
            risk_flags.append("Key/certificate-like file present: " + rel)
        if any(part.lower() in {"backup", "backups"} for part in path.parts):
            risk_flags.append("Backup path present: " + rel)
        if suffix not in TEXT_EXTS and not path.name.startswith(".env") and path.name not in PACKAGE_FILES:
            continue
        content = read_text(path, root, warnings)
        if content is None:
            continue
        scanned += 1
        haystack = (rel + "\n" + content).lower()
        for name, patterns in COMPILED["frameworks"].items():
            if any(p.search(haystack) for p in patterns):
                frameworks[name].append(rel)
        for name, patterns in COMPILED["signals"].items():
            if any(p.search(haystack) for p in patterns):
                signals[name].append(rel)
    def paths_map(values: Dict[str, List[str]]) -> dict:
        return {k: sorted(set(v))[:20] for k, v in sorted(values.items())}
    detected_frameworks = paths_map(frameworks)
    possible_signals = paths_map(signals)
    all_framework_names = sorted(FRAMEWORKS)
    all_signal_names = sorted(SIGNAL_PATTERNS)
    layer_sources = {"auth_session":"S2", "admin_surface":"S3", "api_surface":"S4", "database":"S5", "payments":"S6", "browser_security":"S7", "infrastructure":"S8", "secrets_config":"S1"}
    layer_hints = [layer + " review likely applies (heuristic)" for signal, layer in layer_sources.items() if possible_signals.get(signal)]
    states = {
        "frameworks": {name: {"status":"DETECTED" if name in detected_frameworks else "NOT DETECTED", "evidence":detected_frameworks.get(name, [])} for name in all_framework_names},
        "surfaces": {name: {"status":"POSSIBLE" if name in possible_signals else ("NOT SCANNED" if scanned == 0 else "NOT DETECTED"), "evidence":possible_signals.get(name, [])} for name in all_signal_names},
    }
    status = "INCOMPLETE SCAN" if warnings else ("NOT SCANNED" if not files or not scanned else "COMPLETE")
    return {"schema_version":2, "scan_status":status, "root":str(root), "file_count":len(files), "text_files_scanned":scanned, "languages":dict(sorted(languages.items())), "extensions":dict(sorted(by_ext.items())), "package_managers":paths_map(package_managers), "frameworks":detected_frameworks, "signals":possible_signals, "states":states, "risk_flags":sorted(set(risk_flags))[:50], "layer_hints":layer_hints, "warnings":warnings, "note":"Heuristic planning signals only. DETECTED means a stack marker was found, not that a vulnerability exists. Read representative code before deciding."}


def print_text(report: dict) -> None:
    print("Security stack signals for: " + report["root"])
    print("Scan status: " + report["scan_status"])
    print("Files visited: {}; text files scanned: {}".format(report["file_count"], report["text_files_scanned"]))
    for section in ("languages", "package_managers", "frameworks", "signals"):
        print("\n" + section.replace("_", " ").title())
        data = report[section]
        print("  none detected" if not data else "  " + json.dumps(data, ensure_ascii=False))
    print("\nWarnings")
    print("  none" if not report["warnings"] else "\n".join("  - " + item for item in report["warnings"]))
    print("\n" + report["note"])


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Detect heuristic stack signals. This is not a vulnerability scanner.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path")
    parser.add_argument("--json", action="store_true", help="Print structured JSON")
    args = parser.parse_args(argv)
    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        parser.error("not a directory: {}".format(root))
    try:
        report = detect(root)
    except OSError as exc:
        print("scan failed: {}".format(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 1 if report["scan_status"] == "INCOMPLETE SCAN" else 0


if __name__ == "__main__":
    raise SystemExit(main())
