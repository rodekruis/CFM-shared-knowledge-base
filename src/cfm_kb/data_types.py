"""Typed containers for the Knowledge Base pipeline.

EspoCRM API responses and outgoing payloads are parsed to / from these
dataclasses at the boundary so the rest of the pipeline never passes raw dicts
around. Serialization to the API payload lives in ``to_dict`` (camelCase field
names, matching the EspoCRM DTOs). Configuration types (e.g. the translation
glossary) also live here as frozen dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Category:
    """A KnowledgeBaseCategory record (a language folder maps to one)."""

    name: str
    id: str | None = None

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> Category:
        """Parse a raw EspoCRM category record into a ``Category``."""
        name = raw.get("name")
        if not name:
            raise ValueError(f"Category record missing 'name': {raw!r}")
        return cls(name=str(name), id=raw.get("id"))


@dataclass(frozen=True)
class Article:
    """A KnowledgeBaseArticle to be created or updated in EspoCRM."""

    title: str
    body_html: str
    category: str
    category_ids: tuple[str, ...] = ()
    status: str = "Published"
    id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to the EspoCRM API payload (camelCase field names)."""
        return {
            "name": self.title,
            "body": self.body_html,
            "status": self.status,
            "categoriesIds": list(self.category_ids),
        }


@dataclass(frozen=True)
class LocalImageRef:
    """A local image referenced by an ``<img>`` tag in article HTML.

    ``src`` is the original attribute value exactly as written in the HTML;
    ``path`` is the resolved filesystem path it points to.
    """

    src: str
    path: Path


@dataclass(frozen=True)
class GlossaryTerm:
    """A single domain-glossary entry used to keep terminology consistent.

    Attributes:
        id: Stable identifier for the term (used in messages).
        source_forms: English forms whose presence in a source article triggers
            the rule (e.g. singular and plural).
        translations: Mapping of target language name to the accepted target
            forms; the first form is the preferred one used in prompts.
    """

    id: str
    source_forms: tuple[str, ...]
    translations: dict[str, tuple[str, ...]]
