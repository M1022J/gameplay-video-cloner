from __future__ import annotations

import argparse
import curses
import sys
from collections import defaultdict
from pathlib import Path

from .installer import (
    DEFAULT_AGENT_TARGETS,
    AgentTarget,
    InstallResult,
    SkillInstallError,
    default_source_dir,
    install_skills,
    list_skills,
    update_installed_skills,
)


def main(argv: list[str] | None = None) -> int:
    parser = _make_parser()
    args = parser.parse_args(argv)

    try:
        source_dir = args.source.expanduser().resolve()
        targets = _resolve_targets(args)

        if args.command == "list":
            for skill_name in list_skills(source_dir):
                print(skill_name)
            return 0

        if args.command == "install":
            selected = _selected_skills(args, source_dir)
            if not _confirm_install(selected, targets, args.yes):
                print("Install cancelled.")
                return 1
            results = install_skills(selected, source_dir, targets)
            _print_results("Installed", results)
            return 0

        if args.command == "update":
            results = update_installed_skills(source_dir, targets)
            _print_results("Updated", results)
            return 0

        parser.print_help()
        return 0
    except (KeyboardInterrupt, SkillInstallError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agents-skills",
        description="Install skills from this repository into local agent skill folders.",
    )
    parser.set_defaults(command=None, source=default_source_dir(), home=None)
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="Show installable skills.")
    _add_common_options(list_parser)

    install_parser = subparsers.add_parser(
        "install",
        help="Choose skills and install them into all default agent folders.",
    )
    _add_common_options(install_parser)
    install_parser.add_argument("skills", nargs="*", help="Skill names to install.")
    install_parser.add_argument("--all", action="store_true", help="Install every skill.")
    install_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt.",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Reinstall repo skills that are already present in agent folders.",
    )
    _add_common_options(update_parser)

    return parser


def _add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source_dir(),
        help="Skill source directory. Defaults to this repository's skills folder.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        help=argparse.SUPPRESS,
    )


def _resolve_targets(args: argparse.Namespace) -> tuple[AgentTarget, ...]:
    if args.home is None:
        return DEFAULT_AGENT_TARGETS

    home = args.home.expanduser()
    return tuple(
        AgentTarget(target.name, home / target.skills_dir.expanduser().relative_to(Path.home()))
        for target in DEFAULT_AGENT_TARGETS
    )


def _selected_skills(args: argparse.Namespace, source_dir: Path) -> list[str]:
    if args.all:
        return list_skills(source_dir)
    if args.skills:
        return args.skills
    return select_skills(list_skills(source_dir))


def _confirm_install(
    selected: list[str],
    targets: tuple[AgentTarget, ...],
    skip_prompt: bool,
) -> bool:
    if skip_prompt:
        return True

    print()
    print("Install these skills:")
    for skill_name in selected:
        print(f"  - {skill_name}")

    print()
    print("Into these agent skill folders:")
    for target in targets:
        print(f"  - {target.name}: {target.expanded_skills_dir}")

    answer = input("\nContinue? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def select_skills(skill_names: list[str]) -> list[str]:
    if not skill_names:
        raise SkillInstallError("No skills found")
    if sys.stdin.isatty() and sys.stdout.isatty():
        return _select_skills_curses(skill_names)
    return _select_skills_prompt(skill_names)


def _select_skills_prompt(skill_names: list[str]) -> list[str]:
    print("Select skills to install:")
    for index, skill_name in enumerate(skill_names, start=1):
        print(f"  [{index}] {skill_name}")

    raw_selection = input("\nEnter numbers separated by spaces or commas: ").strip()
    if not raw_selection:
        raise SkillInstallError("No skills selected")

    selected: list[str] = []
    tokens = raw_selection.replace(",", " ").split()
    for token in tokens:
        try:
            index = int(token)
        except ValueError as error:
            raise SkillInstallError(f"Invalid selection: {token}") from error

        if index < 1 or index > len(skill_names):
            raise SkillInstallError(f"Selection out of range: {index}")
        selected.append(skill_names[index - 1])

    return list(dict.fromkeys(selected))


def _select_skills_curses(skill_names: list[str]) -> list[str]:
    return curses.wrapper(_run_checkbox_list, skill_names)


def _run_checkbox_list(stdscr: curses.window, skill_names: list[str]) -> list[str]:
    curses.curs_set(0)
    selected = [False] * len(skill_names)
    cursor = 0

    while True:
        _draw_checkbox_list(stdscr, skill_names, selected, cursor)
        key = stdscr.getch()

        if key in (ord("q"), 27):
            raise SkillInstallError("Install cancelled")
        if key in (curses.KEY_UP, ord("k")):
            cursor = max(0, cursor - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            cursor = min(len(skill_names) - 1, cursor + 1)
        elif key == ord(" "):
            selected[cursor] = not selected[cursor]
        elif key in (ord("a"), ord("A")):
            all_selected = all(selected)
            selected = [not all_selected] * len(skill_names)
        elif key in (10, 13, curses.KEY_ENTER):
            chosen = [name for name, is_selected in zip(skill_names, selected) if is_selected]
            if chosen:
                return chosen


def _draw_checkbox_list(
    stdscr: curses.window,
    skill_names: list[str],
    selected: list[bool],
    cursor: int,
) -> None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = "Select skills: space toggles, enter confirms, a selects all, q cancels"
    stdscr.addnstr(0, 0, title, width - 1, curses.A_BOLD)

    visible_rows = max(1, height - 2)
    start = max(0, min(cursor - visible_rows + 1, len(skill_names) - visible_rows))

    for row, index in enumerate(range(start, min(len(skill_names), start + visible_rows)), start=1):
        marker = "x" if selected[index] else " "
        line = f"[{marker}] {skill_names[index]}"
        mode = curses.A_REVERSE if index == cursor else curses.A_NORMAL
        stdscr.addnstr(row, 0, line, width - 1, mode)

    stdscr.refresh()


def _print_results(action: str, results: list[InstallResult]) -> None:
    if not results:
        print("No matching installed skills found.")
        return

    grouped: dict[str, list[InstallResult]] = defaultdict(list)
    for result in results:
        grouped[result.agent_name].append(result)

    for agent_name in sorted(grouped):
        print(f"{action} for {agent_name}:")
        for result in sorted(grouped[agent_name], key=lambda item: item.skill_name):
            print(f"  - {result.skill_name} -> {result.destination}")

