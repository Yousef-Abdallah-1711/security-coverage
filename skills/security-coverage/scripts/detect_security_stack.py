#!/usr/bin/env python3
"""Detect security-relevant stack and attack surface signals.

Standard library only. This is a heuristic scanner for assessment planning, not
a vulnerability scanner and not a replacement for reading the code.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "__pycache__",
    ".next",
    "dist",
    "build",
    "coverage",
    ".cache",
    ".pytest_cache",
}

TEXT_EXTS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".php",
    ".py",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".cs",
    ".html",
    ".css",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".env",
    ".md",
    ".sql",
    ".sh",
    ".conf",
    ".ini",
}

LANG_BY_EXT = {
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".cs": "C#",
    ".swift": "Swift",
    ".dart": "Dart",
}

PACKAGE_FILES = {
    "package.json": "npm/yarn/pnpm",
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "Yarn",
    "package-lock.json": "npm",
    "composer.json": "Composer/PHP",
    "requirements.txt": "pip",
    "pyproject.toml": "Python",
    "Pipfile": "Pipenv",
    "poetry.lock": "Poetry",
    "Gemfile": "Bundler/Ruby",
    "go.mod": "Go modules",
    "Cargo.toml": "Cargo/Rust",
    "pom.xml": "Maven",
    "build.gradle": "Gradle",
    "build.gradle.kts": "Gradle",
}

FRAMEWORK_PATTERNS = {
    "React": [r"react", r"vite", r"next"],
    "Next.js": [r"next\.config", r"next"],
    "Vue": [r"vue"],
    "Laravel": [r"laravel", r"artisan"],
    "Symfony": [r"symfony"],
    "Django": [r"django", r"manage\.py"],
    "Flask": [r"flask"],
    "FastAPI": [r"fastapi"],
    "Rails": [r"rails", r"config/routes\.rb"],
    "Express": [r"express"],
    "Supabase": [r"supabase"],
}

SIGNAL_PATTERNS = {
    "auth_session": [
        r"session_start",
        r"setcookie",
        r"password_hash",
        r"password_verify",
        r"passport",
        r"nextauth",
        r"auth0",
        r"jwt",
        r"oauth",
        r"login",
        r"logout",
        r"csrf",
    ],
    "admin_surface": [
        r"/admin",
        r"admin/",
        r"dashboard",
        r"ADMIN_",
        r"is_admin",
    ],
    "api_surface": [
        r"/api/",
        r"fetch\(",
        r"axios",
        r"route",
        r"router\.",
        r"\$_POST",
        r"\$_GET",
        r"Request",
    ],
    "database": [
        r"SELECT ",
        r"INSERT ",
        r"UPDATE ",
        r"DELETE ",
        r"mysqli",
        r"PDO",
        r"postgres",
        r"mysql",
        r"sqlite",
        r"mongodb",
        r"supabase",
    ],
    "payments": [
        r"stripe",
        r"paymob",
        r"paypal",
        r"paddle",
        r"webhook",
        r"payment",
        r"paid_amount",
        r"payment_status",
    ],
    "secrets_config": [
        r"SECRET",
        r"PRIVATE_KEY",
        r"SERVICE_KEY",
        r"API_KEY",
        r"TOKEN",
        r"PASSWORD",
        r"\.env",
    ],
    "browser_security": [
        r"innerHTML",
        r"dangerouslySetInnerHTML",
        r"target=\"_blank\"",
        r"Content-Security-Policy",
        r"htmlspecialchars",
        r"sanitize",
    ],
    "infrastructure": [
        r"Dockerfile",
        r"docker-compose",
        r"nginx",
        r"apache",
        r"\.htaccess",
        r"github/workflows",
        r"vercel",
        r"netlify",
    ],
}


def iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in files:
            yield Path(current) / name


def is_text_candidate(path: Path) -> bool:
    if path.name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_EXTS or path.name in PACKAGE_FILES


def read_sample(path: Path, limit: int = 200_000) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return handle.read(limit)
    except OSError:
        return ""


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def detect(root: Path) -> dict:
    files = list(iter_files(root))
    by_ext: dict[str, int] = defaultdict(int)
    languages: dict[str, int] = defaultdict(int)
    package_managers: dict[str, list[str]] = defaultdict(list)
    frameworks: dict[str, list[str]] = defaultdict(list)
    signals: dict[str, list[str]] = defaultdict(list)
    risk_flags: list[str] = []

    for path in files:
        suffix = path.suffix.lower()
        if suffix:
            by_ext[suffix] += 1
        if suffix in LANG_BY_EXT:
            languages[LANG_BY_EXT[suffix]] += 1
        if path.name in PACKAGE_FILES:
            package_managers[PACKAGE_FILES[path.name]].append(rel(root, path))

        path_text = rel(root, path).lower()
        content = read_sample(path) if is_text_candidate(path) else ""
        haystack = f"{path_text}\n{content}".lower()

        for framework, patterns in FRAMEWORK_PATTERNS.items():
            if any(re.search(pattern.lower(), haystack) for pattern in patterns):
                frameworks[framework].append(rel(root, path))

        for signal, patterns in SIGNAL_PATTERNS.items():
            if any(re.search(pattern.lower(), haystack) for pattern in patterns):
                signals[signal].append(rel(root, path))

        if path.name.startswith(".env") and path.name != ".env.example":
            risk_flags.append(f"Environment file present: {rel(root, path)}")
        if path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            risk_flags.append(f"Key/certificate-like file present: {rel(root, path)}")
        if any(part in {"backup", "backups"} for part in path.parts):
            risk_flags.append(f"Backup path present: {rel(root, path)}")
        if ".git" in path.parts:
            risk_flags.append(f"Git internals visible in scan path: {rel(root, path)}")

    def top_paths(items: dict[str, list[str]], max_paths: int = 12) -> dict[str, list[str]]:
        return {key: sorted(set(value))[:max_paths] for key, value in sorted(items.items())}

    adopted_hints = []
    if signals.get("auth_session"):
        adopted_hints.append("S2 Authentication/session review likely applies")
    if signals.get("admin_surface"):
        adopted_hints.append("S3 Authorization/admin review likely applies")
    if signals.get("api_surface"):
        adopted_hints.append("S4 API validation likely applies")
    if signals.get("database"):
        adopted_hints.append("S5 Data access review likely applies")
    if signals.get("payments"):
        adopted_hints.append("S6 Payment/admin money flow review likely applies")
    if signals.get("browser_security"):
        adopted_hints.append("S7 Browser security review likely applies")
    if signals.get("infrastructure"):
        adopted_hints.append("S8 Infrastructure review likely applies")
    if signals.get("secrets_config"):
        adopted_hints.append("S1 Secrets/config review likely applies")

    return {
        "root": str(root),
        "file_count": len(files),
        "languages": dict(sorted(languages.items())),
        "extensions": dict(sorted(by_ext.items())),
        "package_managers": top_paths(package_managers),
        "frameworks": top_paths(frameworks),
        "signals": top_paths(signals),
        "risk_flags": sorted(set(risk_flags))[:50],
        "layer_hints": adopted_hints,
        "note": "Heuristic output for planning. Read representative code before deciding security verdicts.",
    }


def print_text(report: dict) -> None:
    print(f"Security stack detection for: {report['root']}")
    print(f"Files scanned: {report['file_count']}")
    print()

    for section in ["languages", "package_managers", "frameworks", "signals"]:
        print(section.replace("_", " ").title())
        data = report[section]
        if not data:
            print("  none detected")
        elif section == "languages":
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            for key, paths in data.items():
                print(f"  {key}:")
                for path in paths[:8]:
                    print(f"    - {path}")
        print()

    print("Layer Hints")
    if report["layer_hints"]:
        for item in report["layer_hints"]:
            print(f"  - {item}")
    else:
        print("  none detected")
    print()

    print("Risk Flags")
    if report["risk_flags"]:
        for item in report["risk_flags"]:
            print(f"  - {item}")
    else:
        print("  none detected")
    print()
    print(report["note"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect security-relevant stack signals.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"not a directory: {root}")

    report = detect(root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
