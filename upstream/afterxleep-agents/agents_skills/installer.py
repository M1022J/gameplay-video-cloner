from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IGNORED_COPY_PATTERNS = (
    ".DS_Store",
    "__pycache__",
    "*.pyc",
    ".git",
    ".hg",
    ".svn",
)


@dataclass(frozen=True)
class AgentTarget:
    name: str
    skills_dir: Path

    @property
    def expanded_skills_dir(self) -> Path:
        return self.skills_dir.expanduser()


@dataclass(frozen=True)
class InstallResult:
    agent_name: str
    skill_name: str
    destination: Path


DEFAULT_AGENT_TARGETS = (
    AgentTarget("Codex", Path("~/.codex/skills")),
    AgentTarget("Claude", Path("~/.claude/skills")),
    AgentTarget("Pi", Path("~/.pi/skills")),
    AgentTarget("Gemini", Path("~/.gemini/skills")),
)


class SkillInstallError(RuntimeError):
    pass


def repo_root_from(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "skills").is_dir():
            return candidate

    raise SkillInstallError(f"Could not find a skills directory above {start}")


def list_skills(source_dir: Path) -> list[str]:
    source_dir = source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        raise SkillInstallError(f"Skills source does not exist: {source_dir}")

    skills = [
        path.name
        for path in source_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and (path / "SKILL.md").is_file()
    ]
    return sorted(skills)


def install_skills(
    skill_names: Iterable[str],
    source_dir: Path,
    agent_targets: Iterable[AgentTarget] = DEFAULT_AGENT_TARGETS,
) -> list[InstallResult]:
    source_dir = source_dir.expanduser().resolve()
    selected = _validate_skill_names(skill_names, source_dir)
    results: list[InstallResult] = []

    for target in agent_targets:
        target_dir = target.expanded_skills_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        for skill_name in selected:
            destination = _replace_skill_directory(
                source_dir / skill_name,
                target_dir / skill_name,
            )
            results.append(InstallResult(target.name, skill_name, destination))

    return results


def update_installed_skills(
    source_dir: Path,
    agent_targets: Iterable[AgentTarget] = DEFAULT_AGENT_TARGETS,
) -> list[InstallResult]:
    source_dir = source_dir.expanduser().resolve()
    repo_skills = list_skills(source_dir)
    results: list[InstallResult] = []

    for target in agent_targets:
        target_dir = target.expanded_skills_dir
        if not target_dir.is_dir():
            continue

        for skill_name in repo_skills:
            destination = target_dir / skill_name
            if destination.exists():
                installed_destination = _replace_skill_directory(
                    source_dir / skill_name,
                    destination,
                )
                results.append(
                    InstallResult(target.name, skill_name, installed_destination)
                )

    return results


def default_source_dir() -> Path:
    return repo_root_from(Path(__file__)) / "skills"


def _validate_skill_names(skill_names: Iterable[str], source_dir: Path) -> list[str]:
    available = set(list_skills(source_dir))
    selected = list(dict.fromkeys(skill_names))
    missing = sorted(name for name in selected if name not in available)

    if missing:
        missing_text = ", ".join(missing)
        raise SkillInstallError(f"Unknown skill: {missing_text}")
    if not selected:
        raise SkillInstallError("No skills selected")

    return selected


def _replace_skill_directory(source: Path, destination: Path) -> Path:
    if not source.is_dir():
        raise SkillInstallError(f"Skill source does not exist: {source}")
    if not (source / "SKILL.md").is_file():
        raise SkillInstallError(f"Skill source is missing SKILL.md: {source}")
    if destination.exists() and not destination.is_dir() and not destination.is_symlink():
        raise SkillInstallError(f"Destination exists and is not a directory: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_parent = destination.parent
    temp_dir = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.", suffix=".tmp", dir=temp_parent)
    )

    try:
        temp_dir.rmdir()
        shutil.copytree(
            source,
            temp_dir,
            ignore=shutil.ignore_patterns(*IGNORED_COPY_PATTERNS),
        )
        _remove_existing_path(destination)
        os.replace(temp_dir, destination)
    except Exception:
        _remove_existing_path(temp_dir)
        raise

    return destination


def _remove_existing_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)

