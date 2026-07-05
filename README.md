# CFM Shared Knowledge Base

Maintain a multilingual Knowledge Base in [EspoCRM](https://www.espocrm.com/) from
Markdown files, with **English as the single source of truth**.

You write (or edit) articles in English only. From there, everything is automated:
the articles are machine-translated into every other language, then converted to
HTML and published to EspoCRM.

## The intended workflow

1. **Edit English.** Add or change a Markdown file under `articles/English/`.
2. **Push to `main`** (or open a PR to preview).
3. **Watch the magic.** The GitHub Actions pipeline:
   - translates the English articles **that changed** into every other language
     folder (`Français`, `Español`, `العربية`, …), reusing existing translations
     so established terminology and manual corrections stay consistent;
   - commits the generated translations back to the repo;
   - publishes **all** languages to EspoCRM.

English is the source of truth, so most of the time you only edit English. But
if a machine translation isn't accurate enough you **can** fix it by hand; the
correction is preserved on future runs (see
[Fixing a machine translation](#fixing-a-machine-translation)).

## Writing articles

Only touch the `English` folder:

1. Add a Markdown file to `articles/English/`, e.g. `roles-and-permissions.md`.
2. The article title is taken from the first `# Heading` in the file, falling
   back to a title-cased version of the file name.

The matching translated files (`articles/Français/roles-and-permissions.md`,
etc.) are produced automatically, don't create them yourself.

## Fixing a machine translation

Sometimes a machine translation isn't accurate enough. You can edit the
translated file directly and your fix will be preserved:

1. Edit the translated file (e.g. `articles/Français/roles-and-permissions.md`)
   and commit it.
2. The CI pipeline only retranslates a language file when its **English source**
   changed. Editing a translation doesn't touch the English source, so on the
   next run your file is left exactly as you saved it.

In other words, a translation is only regenerated when you change the
corresponding English article. Until then, manual corrections stay put.

If you *do* change the English for an article, all of its translations are
regenerated (your previous translation is still passed to the model as reference
to keep terminology consistent), so re-check any manual wording afterwards.

You can reproduce the same behaviour locally:

```powershell
# Translate only specific changed files (what CI does):
uv run cfm-kb translate articles/English/roles-and-permissions.md

# Skip files that already have a translation:
uv run cfm-kb translate --only-missing
```

Because English is the source of truth, prefer fixing the English article when
the issue is in the content itself; reserve hand-editing a translation for cases
where only the target-language wording is wrong.

## Keeping terminology consistent (glossary)

Domain terms must be translated the same way everywhere (e.g. *feedback*,
*National Society*, *EspoCRM*). A curated **glossary** enforces this in two
deterministic ways:

- **Prompt guidance.** When an article is translated, the glossary terms that
  appear in it are injected into the prompt with their agreed translations, so
  the model uses the established wording.
- **A hard check (fail + flag).** After each file is translated, every glossary
  term present in the English source must have one of its accepted target forms
  in the machine translation. If any is missing, the run **fails** and lists the
  offending `language/file: term` so a human can review it; nothing is
  committed or published until it's fixed. The check only runs on the
  translations the pipeline generates; hand-edited translations are never gated.

The term base lives in [glossary.json](glossary.json) at the repo root (it's
pipeline config, not code). Each entry lists the English source form(s) and the
accepted translation(s) per language (list every inflected form, e.g.
singular/plural, so the check doesn't raise false positives). Do-not-translate
terms simply repeat the same value across languages. Extend it as new domain
terms appear.

Changing the glossary **retranslates every article** on the next CI run, since a
term change can affect any of them (see
[Continuous deployment](#continuous-deployment)).

## Repository layout

```
src/cfm_kb/
  cli.py              # Command-line entry point (translate / publish commands)
  publish_kb.py       # Converts Markdown -> HTML and publishes to EspoCRM
  translate.py        # Translates English articles into the other languages
  glossary.py         # Term-base loading + terminology check (fail + flag)
  markdown_utils.py   # Markdown-to-HTML helpers (title extraction, nested lists)
  data_types.py       # Typed containers (Article, Category, GlossaryTerm, ...)
  espo_api_client.py  # Minimal EspoCRM API client
  utils.py            # Logging setup + shared helpers
glossary.json         # Curated domain glossary (config; edit to add terms)
pyproject.toml        # Project metadata and dependencies (managed with uv)
uv.lock               # Locked dependency versions
articles/             # Markdown source, one subfolder per language
  English/            #   <- the source of truth; edit these
  Français/           #   <- generated by the translate command
  Español/            #   <- generated by the translate command
  العربية/           #   <- generated by the translate command
.github/workflows/
  publish-kb.yml      # Translate -> commit -> publish pipeline
```

Each language subfolder maps to a Knowledge Base **category** of the same name.
Categories that don't exist yet are created automatically on publish.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for dependency management.
- An EspoCRM instance with an API key.
- An Azure OpenAI resource with a chat model deployment.

## Setup

Install dependencies into a managed virtual environment:

```powershell
uv sync
```

Create a `.env` file in the project root:

```
# EspoCRM (publishing)
ESPO_URL=https://your-espocrm-instance.example.com
ESPO_API_KEY=your-api-key

# Azure OpenAI (translation)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

## Running locally

Translate English into the other languages, then publish everything:

```powershell
uv run cfm-kb translate                        # regenerate all translations
uv run cfm-kb publish                          # translate missing, then publish to EspoCRM
```

Add `-v` / `--verbose` before the sub-command for debug logging, e.g.
`uv run cfm-kb -v translate`.

Preview without making changes:

```powershell
uv run cfm-kb translate --dry-run              # show translation plan, no API calls
uv run cfm-kb publish --dry-run               # show publish plan, no writes
uv run cfm-kb translate --target-langs Français  # limit to specific languages
```

## Development

Lint, format-check, type-check, and test locally the same way CI does:

```powershell
uv run ruff check .           # lint
uv run ruff format .          # auto-format (use --check to only verify)
uv run ty check               # type check
uv run python -m pytest       # run the unit tests
```

## Continuous deployment

The [`Translate and Publish Knowledge Base`](.github/workflows/publish-kb.yml)
GitHub Actions workflow runs the full pipeline:

- **On push to `main`**: translates the English articles that changed in the
  push into the other languages, commits the results, then publishes to EspoCRM.
  Translation is skipped entirely when nothing under `articles/English/` (or the
  glossary) changed. If `glossary.json` changed, **all** articles are
  retranslated, since a term change can affect any of them.
- **Via Actions → Run workflow** (`workflow_dispatch`): retranslates **all**
  articles (no diff to compare against), then publishes.
- **On pull requests to `main`**: runs a publish **dry-run** only (no translation,
  no writes) so changes can be validated before merging.

Whenever the code changes (`src/`, `tests/`, or project config), the workflow
first runs `ruff` (lint + format check), `ty` (type check), and the test suite,
and stops if any of them fail.

Configure these repository secrets for the workflow to run: `ESPO_URL`,
`ESPO_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`,
`AZURE_OPENAI_DEPLOYMENT`.
