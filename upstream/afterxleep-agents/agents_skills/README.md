# Agents Skills Installer

This is a small terminal app for copying the skills in this repo into the
default skill folders used by local coding agents.

It installs skills from:

```text
./skills
```

Into:

```text
~/.codex/skills
~/.claude/skills
~/.pi/skills
~/.gemini/skills
```

## Install Skills

Run:

```bash
bin/agents-skills install
```

The installer will:

1. Show every skill found in `./skills`.
2. Let you select one or more skills with checkboxes.
3. Ask for confirmation.
4. Copy the selected skills into Codex, Claude, Pi, and Gemini.

In the checkbox list:

- Press `space` to select or unselect a skill.
- Press `a` to select or unselect all skills.
- Press `enter` to continue.
- Press `q` to cancel.

## Update Installed Skills

Run:

```bash
bin/agents-skills update
```

Update checks each agent skill folder and only reinstalls skills that are
already installed there.

For example, if `swift-standards` is already installed in `~/.codex/skills`,
`update` replaces that copy with the current version from `./skills`.

Update does not install new skills that are missing from an agent. Use
`install` when you want to add a new skill.

## Useful Commands

List available skills:

```bash
bin/agents-skills list
```

Install every skill without prompts:

```bash
bin/agents-skills install --all --yes
```

Install specific skills without prompts:

```bash
bin/agents-skills install swift-standards engineering-standards --yes
```

Run through Python instead of the script:

```bash
python3 -m agents_skills install
python3 -m agents_skills update
```

## What Gets Replaced

Installing or updating a skill replaces the whole destination skill directory.
This keeps the installed copy clean and removes stale files from older versions.

The installer skips common local metadata such as `.DS_Store` and Python cache
files.

