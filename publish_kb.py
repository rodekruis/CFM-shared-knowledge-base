"""
Publish Knowledge Base articles to EspoCRM from Markdown files.

Workflow for the team:
1. Write each article as a Markdown file in the ./articles folder.
2. Map each file to one or more Knowledge Base categories in config.yaml,
   using the category NAME (not internal id).
3. Run this script to convert Markdown -> HTML and create/update the articles
   in EspoCRM.

EspoCRM entities used:
- KnowledgeBaseArticle: `name` (title), `body` (HTML / wysiwyg),
  `categoriesIds` (link to categories), `status`.
- KnowledgeBaseCategory: `name`, `id`.

Articles are matched by title (name): if an article with the same title already
exists it is updated, otherwise a new one is created (idempotent).

Usage:
    python publish_kb.py                       # publish using config.yaml
    python publish_kb.py --dry-run             # show what would happen, no writes
    python publish_kb.py --create-missing-categories
"""

import argparse
import os
from pathlib import Path

import markdown
import yaml
from dotenv import load_dotenv
from espo_api_client import EspoAPI
from tqdm import tqdm

# Configuration
BASE_DIR = Path(__file__).parent
ARTICLES_DIR = BASE_DIR / "articles"
CONFIG_PATH = BASE_DIR / "config.yaml"

ARTICLE_ENTITY = "KnowledgeBaseArticle"
CATEGORY_ENTITY = "KnowledgeBaseCategory"

VALID_STATUSES = {"Draft", "In Review", "Published", "Archived"}
DEFAULT_STATUS = "Published"

MARKDOWN_EXTENSIONS = ["extra", "sane_lists", "smarty"]

load_dotenv(BASE_DIR / ".env")
ESPO_URL = os.environ["ESPO_URL"]
ESPO_API_KEY = os.environ["ESPO_API_KEY"]


def load_config(path: Path) -> dict:
    """Load and lightly validate the YAML config."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    articles = config.get("articles")
    if not articles:
        raise ValueError(f"No 'articles' defined in {path}")

    default_status = (config.get("defaults") or {}).get("status", DEFAULT_STATUS)
    if default_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid defaults.status '{default_status}'. "
            f"Must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )
    config.setdefault("defaults", {})["status"] = default_status
    return config


def get_existing_records(
    client: EspoAPI, entity_type: str, key_field: str = "name"
) -> dict[str, str]:
    """Fetch all records for an entity type. Returns {name: id} mapping."""
    existing: dict[str, str] = {}
    offset = 0
    limit = 200
    while True:
        params = {
            "select": f"id,{key_field}",
            "offset": offset,
            "maxSize": limit,
        }
        response = client.request("GET", entity_type, params)
        records = response.get("list", [])
        if not records:
            break
        for rec in records:
            key = rec.get(key_field)
            if key:
                existing[key] = rec["id"]
        if len(records) < limit:
            break
        offset += limit
    return existing


def extract_title_and_body(md_text: str) -> tuple[str | None, str]:
    """Return (h1_title, body_markdown).

    If the file starts with a top-level "# Heading", it is used as the title
    and removed from the body to avoid duplicating it inside the article.
    """
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# ") and not stripped.startswith("##"):
            title = stripped[2:].strip()
            remaining = lines[:i] + lines[i + 1 :]
            return title, "\n".join(remaining).strip()
        break  # first non-empty line is not an H1
    return None, md_text


def resolve_title(entry: dict, h1_title: str | None, file_name: str) -> str:
    """Resolve the article title: explicit config > first H1 > file name."""
    if entry.get("title"):
        return str(entry["title"]).strip()
    if h1_title:
        return h1_title
    return Path(file_name).stem.replace("-", " ").replace("_", " ").strip().title()


def md_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML for the EspoCRM wysiwyg body."""
    return markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)


def resolve_categories(
    client: EspoAPI,
    names: list[str],
    category_ids: dict[str, str],
    create_missing: bool,
    dry_run: bool,
) -> tuple[list[str], list[str]]:
    """Map category names to ids. Returns (resolved_ids, missing_names).

    When create_missing is True, missing categories are created (unless dry_run).
    """
    resolved: list[str] = []
    missing: list[str] = []
    for name in names:
        name = str(name).strip()
        if name in category_ids:
            resolved.append(category_ids[name])
        elif create_missing:
            if dry_run:
                print(f"    [dry-run] would create category '{name}'")
                category_ids[name] = f"<new:{name}>"
            else:
                result = client.request("POST", CATEGORY_ENTITY, {"name": name})
                category_ids[name] = result["id"]
                print(f"    Created category '{name}'")
            resolved.append(category_ids[name])
        else:
            missing.append(name)
    return resolved, missing


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish Knowledge Base articles to EspoCRM from Markdown files."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_PATH,
        help="Path to the YAML config (default: config.yaml).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing to EspoCRM.",
    )
    parser.add_argument(
        "--create-missing-categories",
        action="store_true",
        help="Create categories that don't exist yet instead of failing.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    default_status = config["defaults"]["status"]

    client = EspoAPI(ESPO_URL, ESPO_API_KEY)

    print("Fetching existing categories and articles from EspoCRM...")
    category_ids = get_existing_records(client, CATEGORY_ENTITY)
    existing_articles = get_existing_records(client, ARTICLE_ENTITY)
    print(f"  Categories: {len(category_ids)}, Articles: {len(existing_articles)}")

    created = 0
    updated = 0
    errors: list[str] = []

    for entry in tqdm(config["articles"], desc="Publishing"):
        file_name = entry.get("file")
        if not file_name:
            errors.append("An entry is missing the required 'file' field.")
            continue

        md_path = ARTICLES_DIR / file_name
        if not md_path.exists():
            errors.append(f"{file_name}: file not found in {ARTICLES_DIR}")
            continue

        category_names = entry.get("categories") or []
        if not category_names:
            errors.append(f"{file_name}: no 'categories' specified.")
            continue
        if isinstance(category_names, str):
            category_names = [category_names]

        status = entry.get("status", default_status)
        if status not in VALID_STATUSES:
            errors.append(
                f"{file_name}: invalid status '{status}'. "
                f"Must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
            continue

        md_text = md_path.read_text(encoding="utf-8")
        h1_title, body_md = extract_title_and_body(md_text)
        title = resolve_title(entry, h1_title, file_name)
        body_html = md_to_html(body_md if not entry.get("title") else md_text)

        resolved_ids, missing = resolve_categories(
            client,
            category_names,
            category_ids,
            args.create_missing_categories,
            args.dry_run,
        )
        if missing:
            available = ", ".join(sorted(category_ids)) or "(none)"
            errors.append(
                f"{file_name}: unknown categor{'y' if len(missing) == 1 else 'ies'} "
                f"{missing}. Available: {available}. "
                f"Use --create-missing-categories to create them."
            )
            continue

        payload = {
            "name": title,
            "body": body_html,
            "status": status,
            "categoriesIds": resolved_ids,
        }

        if title in existing_articles:
            record_id = existing_articles[title]
            if args.dry_run:
                print(f"    [dry-run] would UPDATE '{title}' ({status})")
            else:
                client.request("PUT", f"{ARTICLE_ENTITY}/{record_id}", payload)
            updated += 1
        else:
            if args.dry_run:
                print(f"    [dry-run] would CREATE '{title}' ({status})")
            else:
                result = client.request("POST", ARTICLE_ENTITY, payload)
                existing_articles[title] = result["id"]
            created += 1

    print(f"\nDone. Created: {created}, Updated: {updated}, Errors: {len(errors)}")
    if errors:
        print("\nProblems:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
