"""
Publish Knowledge Base articles to EspoCRM from Markdown files.

Workflow for the team:
1. Write each article as a Markdown file inside a language subfolder of the
   ./articles folder, e.g. ./articles/English/roles-and-permissions.md.
2. The subfolder name is used as the Knowledge Base category NAME (e.g.
   English, Français, Español, العربية). Categories that don't exist yet are
   created automatically.
3. Run this script to convert Markdown -> HTML and create/update the articles
   in EspoCRM.

EspoCRM entities used:
- KnowledgeBaseArticle: `name` (title), `body` (HTML / wysiwyg),
  `categoriesIds` (link to categories), `status`.
- KnowledgeBaseCategory: `name`, `id`.

Articles are matched by category and title: if an article with the same title
already exists in that category it is updated, otherwise a new one is created
(idempotent). All articles are published with status "Published".

Usage:
    python publish_kb.py                            # publish all articles
    python publish_kb.py --dry-run                  # show what would happen, no writes
"""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from espo_api_client import EspoAPI
from markdown_utils import extract_title_and_body, md_to_html, resolve_title
from tqdm import tqdm

# Configuration
BASE_DIR = Path(__file__).parent
ARTICLES_DIR = BASE_DIR / "articles"

ARTICLE_ENTITY = "KnowledgeBaseArticle"
CATEGORY_ENTITY = "KnowledgeBaseCategory"

DEFAULT_STATUS = "Published"

load_dotenv(BASE_DIR / ".env")
ESPO_URL = os.environ["ESPO_URL"]
ESPO_API_KEY = os.environ["ESPO_API_KEY"]


def discover_articles(articles_dir: Path) -> list[tuple[Path, str]]:
    """Find Markdown files and infer their category from the folder structure.

    Each Markdown file must live inside a subfolder of ``articles_dir``; the
    name of that immediate subfolder is used as the category name. Returns a
    sorted list of ``(md_path, category_name)`` tuples.
    """
    found: list[tuple[Path, str]] = []
    for md_path in sorted(articles_dir.rglob("*.md")):
        rel = md_path.relative_to(articles_dir)
        if len(rel.parts) < 2:
            continue  # file sits directly in articles_dir with no category folder
        category = rel.parts[0]
        found.append((md_path, category))
    return found


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


def get_existing_articles_by_category(
    client: EspoAPI, category_ids: dict[str, str]
) -> dict[tuple[str, str], str]:
    """Fetch existing articles keyed by (category_name, title) -> id.

    The same title may exist in several language categories, so the category is
    part of the key to keep per-language articles distinct.
    """
    id_to_category = {cat_id: name for name, cat_id in category_ids.items()}
    existing: dict[tuple[str, str], str] = {}
    offset = 0
    limit = 200
    while True:
        params = {
            "select": "id,name,categoriesIds",
            "offset": offset,
            "maxSize": limit,
        }
        response = client.request("GET", ARTICLE_ENTITY, params)
        records = response.get("list", [])
        if not records:
            break
        for rec in records:
            title = rec.get("name")
            if not title:
                continue
            for cat_id in rec.get("categoriesIds") or []:
                category = id_to_category.get(cat_id)
                if category:
                    existing[(category, title)] = rec["id"]
        if len(records) < limit:
            break
        offset += limit
    return existing


def resolve_categories(
    client: EspoAPI,
    names: list[str],
    category_ids: dict[str, str],
    dry_run: bool,
) -> list[str]:
    """Map category names to ids, creating any that don't exist yet.

    Returns the list of resolved category ids.
    """
    resolved: list[str] = []
    for name in names:
        name = str(name).strip()
        if name in category_ids:
            resolved.append(category_ids[name])
        else:
            if dry_run:
                print(f"    [dry-run] would create category '{name}'")
                category_ids[name] = f"<new:{name}>"
            else:
                result = client.request("POST", CATEGORY_ENTITY, {"name": name})
                category_ids[name] = result["id"]
                print(f"    Created category '{name}'")
            resolved.append(category_ids[name])
    return resolved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish Knowledge Base articles to EspoCRM from Markdown files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing to EspoCRM.",
    )
    args = parser.parse_args()

    client = EspoAPI(ESPO_URL, ESPO_API_KEY)

    print("Fetching existing categories and articles from EspoCRM...")
    category_ids = get_existing_records(client, CATEGORY_ENTITY)
    existing_articles = get_existing_articles_by_category(client, category_ids)
    print(f"  Categories: {len(category_ids)}, Articles: {len(existing_articles)}")

    articles = discover_articles(ARTICLES_DIR)
    if not articles:
        print(f"No Markdown files found under {ARTICLES_DIR}")
        return

    created = 0
    updated = 0

    for md_path, category in tqdm(articles, desc="Publishing"):
        md_text = md_path.read_text(encoding="utf-8")
        h1_title, body_md = extract_title_and_body(md_text)
        title = resolve_title(h1_title, md_path.name)
        body_html = md_to_html(body_md)

        resolved_ids = resolve_categories(
            client,
            [category],
            category_ids,
            args.dry_run,
        )

        payload = {
            "name": title,
            "body": body_html,
            "status": DEFAULT_STATUS,
            "categoriesIds": resolved_ids,
        }

        article_key = (category, title)
        if article_key in existing_articles:
            record_id = existing_articles[article_key]
            if args.dry_run:
                print(
                    f"    [dry-run] would UPDATE '{title}' [{category}] ({DEFAULT_STATUS})"
                )
            else:
                client.request("PUT", f"{ARTICLE_ENTITY}/{record_id}", payload)
            updated += 1
        else:
            if args.dry_run:
                print(
                    f"    [dry-run] would CREATE '{title}' [{category}] ({DEFAULT_STATUS})"
                )
            else:
                result = client.request("POST", ARTICLE_ENTITY, payload)
                existing_articles[article_key] = result["id"]
            created += 1

    print(f"\nDone. Created: {created}, Updated: {updated}")


if __name__ == "__main__":
    main()
