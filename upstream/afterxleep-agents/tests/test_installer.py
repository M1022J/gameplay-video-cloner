from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agents_skills.installer import (
    AgentTarget,
    SkillInstallError,
    install_skills,
    list_skills,
    update_installed_skills,
)


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "skills"
        self.source.mkdir()
        self.targets = (
            AgentTarget("Codex", self.root / "codex" / "skills"),
            AgentTarget("Claude", self.root / "claude" / "skills"),
            AgentTarget("Pi", self.root / "pi" / "skills"),
            AgentTarget("Gemini", self.root / "gemini" / "skills"),
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_listSkills_returnsDirectoriesWithSkillFile(self) -> None:
        self.write_skill("swift-standards")
        self.write_skill("engineering-standards")
        (self.source / "notes").mkdir()
        (self.source / ".hidden").mkdir()

        self.assertEqual(
            list_skills(self.source),
            ["engineering-standards", "swift-standards"],
        )

    def test_installSkills_copiesSelectedSkillsToAllAgentTargets(self) -> None:
        self.write_skill("swift-standards", references={"concurrency.md": "updated"})
        self.write_skill("lemonsqueezy")
        (self.source / "swift-standards" / ".DS_Store").write_text("metadata")

        results = install_skills(["swift-standards"], self.source, self.targets)

        self.assertEqual(len(results), 4)
        for target in self.targets:
            installed = target.skills_dir / "swift-standards"
            self.assertEqual((installed / "SKILL.md").read_text(), "# swift-standards\n")
            self.assertEqual((installed / "references" / "concurrency.md").read_text(), "updated")
            self.assertFalse((installed / ".DS_Store").exists())
            self.assertFalse((target.skills_dir / "lemonsqueezy").exists())

    def test_installSkills_replacesExistingSkillDirectory(self) -> None:
        self.write_skill("engineering-standards")
        stale_dir = self.targets[0].skills_dir / "engineering-standards"
        stale_dir.mkdir(parents=True)
        (stale_dir / "old.txt").write_text("stale")

        install_skills(["engineering-standards"], self.source, self.targets)

        self.assertFalse((stale_dir / "old.txt").exists())
        self.assertEqual((stale_dir / "SKILL.md").read_text(), "# engineering-standards\n")

    def test_installSkills_raisesForUnknownSkill(self) -> None:
        self.write_skill("swift-standards")

        with self.assertRaises(SkillInstallError):
            install_skills(["missing"], self.source, self.targets)

    def test_updateInstalledSkills_reinstallsOnlySkillsAlreadyPresentInAgents(self) -> None:
        self.write_skill("swift-standards", body="# swift-standards\nnew")
        self.write_skill("lemonsqueezy", body="# lemonsqueezy\nnew")
        codex_swift = self.targets[0].skills_dir / "swift-standards"
        codex_swift.mkdir(parents=True)
        (codex_swift / "SKILL.md").write_text("old")
        claude_lemon = self.targets[1].skills_dir / "lemonsqueezy"
        claude_lemon.mkdir(parents=True)
        (claude_lemon / "SKILL.md").write_text("old")

        results = update_installed_skills(self.source, self.targets)

        self.assertEqual(
            sorted((result.agent_name, result.skill_name) for result in results),
            [("Claude", "lemonsqueezy"), ("Codex", "swift-standards")],
        )
        self.assertEqual((codex_swift / "SKILL.md").read_text(), "# swift-standards\nnew")
        self.assertEqual((claude_lemon / "SKILL.md").read_text(), "# lemonsqueezy\nnew")
        self.assertFalse((self.targets[2].skills_dir).exists())
        self.assertFalse((self.targets[0].skills_dir / "lemonsqueezy").exists())

    def write_skill(
        self,
        name: str,
        body: str | None = None,
        references: dict[str, str] | None = None,
    ) -> None:
        skill_dir = self.source / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(body if body is not None else f"# {name}\n")

        if references:
            references_dir = skill_dir / "references"
            references_dir.mkdir()
            for filename, content in references.items():
                (references_dir / filename).write_text(content)


if __name__ == "__main__":
    unittest.main()

