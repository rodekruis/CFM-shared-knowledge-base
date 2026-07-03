# CFM Shared Knowledge Base

Publish Knowledge Base articles to [EspoCRM](https://www.espocrm.com/) from Markdown files.

Team members write articles as Markdown inside language subfolders of `articles/`,
and a script (locally or via GitHub Actions) converts them to HTML and
creates/updates the corresponding articles in EspoCRM. The subfolder name is used
as the Knowledge Base category. Articles are matched by category and title, so
re-running is idempotent.

## Repository layout

```
publish_kb.py         # Converts Markdown -> HTML and publishes to EspoCRM
markdown_utils.py     # Markdown-to-HTML helpers
espo_api_client.py    # Minimal EspoCRM API client
pyproject.toml        # Project metadata and dependencies (managed with uv)
uv.lock               # Locked dependency versions
articles/             # Markdown source, organised by category subfolder
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for dependency management.
- Access to an EspoCRM instance with an API key.

## Setup

Install dependencies into a managed virtual environment:

```powershell
uv sync
```

Create a `.env` file in the project root with your EspoCRM credentials:

```
ESPO_URL=https://your-espocrm-instance.example.com
ESPO_API_KEY=your-api-key
```

## Writing articles

1. Create (or pick) a category subfolder in `articles/`. The folder name is used
   as the Knowledge Base category **name** (exactly as shown in EspoCRM).
2. Add a Markdown file inside that subfolder.

```
articles/
  English/roles-and-permissions.md   -> category "English"
  Français/roles-and-permissions.md  -> category "Français"
  Español/roles-and-permissions.md   -> category "Español"
  Arabic/roles-and-permissions.md    -> category "Arabic"
```

The article title is taken from the first `# Heading` in the file, falling back to
the file name. All articles are published with status `Published`.

## Publishing

```powershell
uv run publish_kb.py                          # publish all articles
uv run publish_kb.py --dry-run                # show what would happen, no writes
```

## Continuous deployment

The [`Publish Knowledge Base`](.github/workflows/publish-kb.yml) GitHub Actions workflow:

- Runs a **dry-run** on pull requests targeting `main`/`master` to validate changes.
- **Publishes** to EspoCRM on push to `main`/`master`.
- Can be triggered manually via **Actions → Publish Knowledge Base → Run workflow**.

Configure the `ESPO_URL` and `ESPO_API_KEY` repository secrets for the workflow to run.
