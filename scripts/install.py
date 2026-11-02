#!/usr/bin/env python3
"""Ownership-aware installer shared by install.sh and install.ps1 (Python 3.8+)."""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

PLUGIN = "security-coverage"
COMMANDS = ("security-assess.md", "security-plan.md", "security-implement.md")
MANIFEST = ".security-coverage-install.json"


class InstallError(Exception):
    pass


def print_safe(message: str, stream=None) -> None:
    """Write paths safely even when the active Windows console encoding is legacy."""
    target = stream if stream is not None else sys.stdout
    encoding = getattr(target, "encoding", None) or "utf-8"
    rendered = str(message).encode(encoding, errors="backslashreplace").decode(encoding)
    print(rendered, file=target)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_relative(value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or any(part in ("..", "") for part in rel.parts):
        raise InstallError("Unsafe manifest path rejected: " + value)
    if rel.parts[0] not in ("skills", "commands", "plugins"):
        raise InstallError("Manifest path outside installer scope: " + value)
    if rel.parts[0] == "skills" and (len(rel.parts) < 2 or rel.parts[1] != PLUGIN):
        raise InstallError("Manifest path outside skill scope: " + value)
    if rel.parts[0] == "plugins" and (len(rel.parts) < 2 or rel.parts[1] != PLUGIN):
        raise InstallError("Manifest path outside plugin scope: " + value)
    if rel.parts[0] == "commands" and (len(rel.parts) != 2 or rel.name not in COMMANDS):
        raise InstallError("Manifest path outside command scope: " + value)
    return rel


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except (ValueError, OSError):
        return False


def read_manifest(path: Path) -> Dict[str, str]:
    if path.is_symlink():
        raise InstallError("Install manifest is a symlink; refusing to follow it: {}".format(path))
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        files = raw["files"]
        if not isinstance(files, dict):
            raise ValueError("files must be an object")
        result = {}
        for name, digest in files.items():
            safe_relative(name)
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("invalid digest")
            result[name] = digest
        return result
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise InstallError("Install manifest is invalid; preserve files and inspect {}: {}".format(path, exc))


def copy_sources(root: Path, agent: str) -> Dict[str, Path]:
    items: Dict[str, Path] = {}
    skill = root / "skills" / PLUGIN
    if not (skill / "SKILL.md").is_file():
        raise InstallError("Canonical skill missing: {}".format(skill / "SKILL.md"))
    for src in sorted(skill.rglob("*")):
        if src.is_file() and not src.is_symlink() and "__pycache__" not in src.parts:
            items[(Path("skills") / PLUGIN / src.relative_to(skill)).as_posix()] = src
    for name in COMMANDS:
        src = root / "commands" / name
        if not src.is_file():
            raise InstallError("Command file missing: {}".format(src))
        items[(Path("commands") / name).as_posix()] = src
    if agent == "codex":
        manifest = root / ".codex-plugin" / "plugin.json"
        if not manifest.is_file():
            raise InstallError("Codex plugin manifest missing: {}".format(manifest))
        items[(Path("plugins") / PLUGIN / ".codex-plugin" / "plugin.json").as_posix()] = manifest
        # Plugin commands and skill are kept in the same source form as the global install.
        for name in COMMANDS:
            items[(Path("plugins") / PLUGIN / "commands" / name).as_posix()] = root / "commands" / name
        for src in sorted(skill.rglob("*")):
            if src.is_file() and not src.is_symlink() and "__pycache__" not in src.parts:
                items[(Path("plugins") / PLUGIN / "skills" / PLUGIN / src.relative_to(skill)).as_posix()] = src
    return items


def atomic_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=".sc-stage-", dir=str(dst.parent), delete=False) as tmp:
        stage = Path(tmp.name)
        try:
            with src.open("rb") as source:
                shutil.copyfileobj(source, tmp)
            tmp.flush()
            os.fsync(tmp.fileno())
        except Exception:
            stage.unlink(missing_ok=True)
            raise
    try:
        os.replace(str(stage), str(dst))
    except Exception:
        stage.unlink(missing_ok=True)
        raise


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", prefix=".sc-manifest-", dir=str(path.parent), delete=False) as tmp:
        stage = Path(tmp.name)
        try:
            json.dump(value, tmp, indent=2, sort_keys=True)
            tmp.write("\n")
            tmp.flush()
            os.fsync(tmp.fileno())
        except Exception:
            stage.unlink(missing_ok=True)
            raise
    try:
        os.replace(str(stage), str(path))
    except Exception:
        stage.unlink(missing_ok=True)
        raise


def prune_empty_dirs(path: Path, stop: Path) -> None:
    current = path
    while current != stop and inside(stop, current):
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def install(root: Path, base: Path, agent: str) -> List[str]:
    base.mkdir(parents=True, exist_ok=True)
    manifest_path = base / MANIFEST
    old = read_manifest(manifest_path)
    sources = copy_sources(root, agent)
    new_hashes = {name: sha(src) for name, src in sources.items()}
    # Preflight every destination before writing anything. Unowned content is never overwritten.
    for name, src in sources.items():
        rel = safe_relative(name)
        dst = base / rel
        if not inside(base, dst):
            raise InstallError("Destination path escapes install root: {}".format(dst))
        if dst.is_symlink():
            raise InstallError("Destination is a symlink; refusing to follow it: {}".format(dst))
        if dst.exists() and name not in old:
            raise InstallError("Destination collision (not owned by this installer): {}".format(dst))
        if dst.exists() and name in old and dst.is_file() and sha(dst) != old[name] and sha(dst) != new_hashes[name]:
            raise InstallError("Installed file was locally modified; refusing to overwrite: {}".format(dst))
        parent = dst.parent
        while parent != base and inside(base, parent):
            if parent.exists() and parent.is_symlink():
                raise InstallError("Destination parent is a symlink; refusing: {}".format(parent))
            parent = parent.parent
    for name in old:
        if name not in new_hashes:
            dst = base / safe_relative(name)
            if dst.is_file() and not dst.is_symlink() and sha(dst) != old[name]:
                raise InstallError("Stale owned file was locally modified; refusing to remove: {}".format(dst))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = base / ".security-coverage-backups" / timestamp
    written: List[Tuple[Path, Path]] = []
    created: List[Path] = []
    try:
        for name, src in sources.items():
            rel = safe_relative(name)
            dst = base / rel
            if dst.exists() and sha(dst) == new_hashes[name]:
                continue
            if dst.exists():
                backup = backup_root / rel
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(dst), str(backup))
                written.append((dst, backup))
            else:
                created.append(dst)
            atomic_copy(src, dst)
        # Prune obsolete files only when their recorded installed hash still matches.
        for name, digest in old.items():
            if name not in new_hashes:
                dst = base / safe_relative(name)
                if dst.is_file() and not dst.is_symlink() and sha(dst) == digest:
                    dst.unlink()
                    prune_empty_dirs(dst.parent, base)
        atomic_json(manifest_path, {"schema_version": 1, "product": PLUGIN, "agent": agent, "files": new_hashes})
    except Exception:
        for dst in reversed(created):
            try:
                # Do not remove a file changed concurrently after our write.
                matching = next((digest for name, digest in new_hashes.items() if (base / safe_relative(name)) == dst), None)
                if dst.is_file() and not dst.is_symlink() and matching is not None and sha(dst) == matching:
                    dst.unlink()
                    prune_empty_dirs(dst.parent, base)
            except OSError:
                pass
        for dst, backup in reversed(written):
            try:
                shutil.copy2(str(backup), str(dst))
            except OSError:
                pass
        raise
    result = ["Installed {} files for {} to {}".format(len(sources), agent, base)]
    if written:
        result.append("Updated {} owned file(s); recover prior copies from {}".format(len(written), backup_root))
    return result


def uninstall(base: Path) -> List[str]:
    manifest_path = base / MANIFEST
    owned = read_manifest(manifest_path)
    removed, preserved = [], []
    for name, digest in owned.items():
        dst = base / safe_relative(name)
        if not inside(base, dst) or dst.is_symlink():
            preserved.append(name + " (unsafe path or symlink)")
        elif dst.is_file() and sha(dst) == digest:
            dst.unlink()
            removed.append(name)
            prune_empty_dirs(dst.parent, base)
        elif dst.exists():
            preserved.append(name + " (modified since installation)")
    manifest_path.unlink(missing_ok=True)
    lines = ["Removed {} unchanged owned files from {}".format(len(removed), base)]
    if preserved:
        lines.append("Preserved modified or unsafe files: " + "; ".join(preserved))
    return lines


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Safely install Security Coverage skills and command adapters.")
    agents = parser.add_mutually_exclusive_group()
    agents.add_argument("--claude", action="store_true", help="Install Claude files only")
    agents.add_argument("--codex", action="store_true", help="Install Codex files only")
    parser.add_argument("--local", action="store_true", help="Install under the current directory")
    parser.add_argument("--uninstall", action="store_true", help="Remove only unchanged files owned by this installer")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    names = ["claude"] if args.claude else (["codex"] if args.codex else ["claude", "codex"])
    try:
        for agent in names:
            if args.local:
                base = Path.cwd() / (".claude" if agent == "claude" else ".codex")
            elif agent == "claude":
                base = Path.home() / ".claude"
            else:
                base = Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
            lines = uninstall(base) if args.uninstall else install(root, base, agent)
            for line in lines:
                print_safe(line)
    except (InstallError, OSError) as exc:
        print_safe("Installation failed safely: {}".format(exc), stream=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
