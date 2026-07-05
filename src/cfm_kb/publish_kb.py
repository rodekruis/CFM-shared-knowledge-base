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

The command-line entry point lives in ``cli.py``; call ``run_publish`` to run
the pipeline programmatically.
"""

import base64
import logging
import mimetypes
from pathlib import Path

from dotenv import load_dotenv

from .data_types import Article, Category, LocalImageRef
from .espo_api_client import EspoAPI
from .markdown_utils import (
    extract_local_images,
    extract_title_and_body,
    md_to_html,
    resolve_title,
    rewrite_image_sources,
)
from tqdm import tqdm
from .translate import DEFAULT_SOURCE_LANG, translate_all
from .utils import require_env

logger = logging.getLogger(__name__)

# Configuration
ARTICLES_DIR = Path("articles")

ARTICLE_ENTITY = "KnowledgeBaseArticle"
CATEGORY_ENTITY = "KnowledgeBaseCategory"

DEFAULT_STATUS = "Published"

load_dotenv()


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
            category = Category.from_api(rec)
            if category.id:
                existing[category.name] = category.id
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
                logger.info("[dry-run] would create category '%s'", name)
                category_ids[name] = f"<new:{name}>"
            else:
                result = client.request("POST", CATEGORY_ENTITY, {"name": name})
                category_ids[name] = result["id"]
                logger.info("Created category '%s'", name)
            resolved.append(category_ids[name])
    return resolved


def upload_images(
    client: EspoAPI,
    refs: list[LocalImageRef],
    dry_run: bool,
) -> dict[str, str]:
    """Upload local images to EspoCRM; return an ``{original_src: new_src}`` map.

    This is the load-side counterpart to the pure ``extract_local_images`` /
    ``rewrite_image_sources`` helpers: each referenced image is uploaded once as
    an inline attachment on the article ``body`` field, and its new EspoCRM
    entry-point URL is recorded in the returned map. Images whose file is
    missing are skipped with a warning and left out of the map, so their src
    stays unchanged.
    """
    src_map: dict[str, str] = {}
    for ref in refs:
        if not ref.path.is_file():
            logger.warning("image not found, leaving src unchanged: %s", ref.src)
            continue

        if dry_run:
            logger.info("[dry-run] would upload image '%s'", ref.path.name)
            src_map[ref.src] = f"?entryPoint=attachment&id=<new:{ref.path.name}>"
            continue

        mime_type = mimetypes.guess_type(ref.path.name)[0] or "application/octet-stream"
        encoded = base64.b64encode(ref.path.read_bytes()).decode("ascii")
        payload = {
            "name": ref.path.name,
            "type": mime_type,
            "role": "Inline Attachment",
            "relatedType": ARTICLE_ENTITY,
            "field": "body",
            "file": f"data:{mime_type};base64,{encoded}",
        }
        result = client.request("POST", "Attachment", payload)
        src_map[ref.src] = f"?entryPoint=attachment&id={result['id']}"
        logger.info("Uploaded image '%s'", ref.path.name)
    return src_map


def run_publish(dry_run: bool = False) -> None:
    """Translate missing articles, then publish every language to EspoCRM.

    Args:
        dry_run: When True, no writes are made to EspoCRM; the planned actions
            are logged instead.
    """
    espo_url = require_env("ESPO_URL")
    espo_api_key = require_env("ESPO_API_KEY")
    client = EspoAPI(espo_url, espo_api_key)

    logger.info("Creating missing translations...")
    translate_all(
        articles_dir=ARTICLES_DIR,
        source_lang=DEFAULT_SOURCE_LANG,
        dry_run=dry_run,
        only_missing=True,
    )

    logger.info("Fetching existing categories and articles from EspoCRM...")
    category_ids = get_existing_records(client, CATEGORY_ENTITY)
    existing_articles = get_existing_articles_by_category(client, category_ids)
    logger.info(
        "Found %d categories, %d articles",
        len(category_ids),
        len(existing_articles),
    )

    articles = discover_articles(ARTICLES_DIR)
    if not articles:
        logger.warning("No Markdown files found under %s", ARTICLES_DIR)
        return

    created = 0
    updated = 0

    for md_path, category in tqdm(articles, desc="Publishing"):
        md_text = md_path.read_text(encoding="utf-8")
        h1_title, body_md = extract_title_and_body(md_text)
        title = resolve_title(h1_title, md_path.name)

        # Transform (pure): Markdown -> HTML and locate any local images.
        body_html = md_to_html(body_md)
        image_refs = extract_local_images(body_html, md_path.parent)

        # Load (I/O): upload the images, then rewrite their sources in the HTML.
        src_map = upload_images(client, image_refs, dry_run)
        body_html = rewrite_image_sources(body_html, src_map)

        resolved_ids = resolve_categories(
            client,
            [category],
            category_ids,
            dry_run,
        )

        article = Article(
            title=title,
            body_html=body_html,
            category=category,
            category_ids=tuple(resolved_ids),
            status=DEFAULT_STATUS,
        )
        payload = article.to_dict()

        article_key = (category, title)
        if article_key in existing_articles:
            record_id = existing_articles[article_key]
            if dry_run:
                logger.info(
                    "[dry-run] would UPDATE '%s' [%s] (%s)",
                    title,
                    category,
                    DEFAULT_STATUS,
                )
            else:
                client.request("PUT", f"{ARTICLE_ENTITY}/{record_id}", payload)
            updated += 1
        else:
            if dry_run:
                logger.info(
                    "[dry-run] would CREATE '%s' [%s] (%s)",
                    title,
                    category,
                    DEFAULT_STATUS,
                )
            else:
                result = client.request("POST", ARTICLE_ENTITY, payload)
                existing_articles[article_key] = result["id"]
            created += 1

    logger.info("Done. Created: %d, Updated: %d", created, updated)


if __name__ == "__main__":
    # Dev smoke test only; the production entry point is the `cfm-kb` CLI.
    # Run with `python -m cfm_kb.publish_kb` so relative imports resolve.
    from .utils import configure_utf8_output, setup_logging

    configure_utf8_output()
    setup_logging()
    run_publish(dry_run=True)
