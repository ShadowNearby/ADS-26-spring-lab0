"""Load all SKILL.md files from skills subdirectories."""

from pathlib import Path


def load_all_skills(skills_dir: Path = Path("skills")) -> str:
    """Scan skills/*/SKILL.md and skills/*/skill.md, load and merge their content.

    Strips YAML frontmatter from each file. Skips empty files.
    Returns concatenated body content separated by "\\n\\n---\\n\\n".
    """
    skill_contents: list[str] = []

    for path in sorted(skills_dir.iterdir()):
        if not path.is_dir():
            continue
        # Try SKILL.md first, then skill.md
        for name in ("SKILL.md", "skill.md"):
            skill_file = path / name
            if skill_file.exists():
                text = skill_file.read_text(encoding="utf-8").strip()
                if not text:
                    break

                body = text
                if body.startswith("---"):
                    end_index = body.find("\n---", 3)
                    if end_index != -1:
                        body = body[end_index + len("\n---") :].strip()

                if body:
                    skill_contents.append(body)
                break

    return "\n\n---\n\n".join(skill_contents)
