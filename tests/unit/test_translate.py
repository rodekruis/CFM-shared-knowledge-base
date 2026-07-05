"""Unit tests for ``translate_all`` source-file selection.

The real model call (``translate_markdown``) is monkeypatched, so these tests
run without Azure OpenAI credentials or network access. They verify that
passing explicit ``source_files`` restricts translation to just those files —
the behaviour the CI workflow relies on to translate only changed articles.
"""

from pathlib import Path

import pytest

from cfm_kb import translate as translate_mod
from cfm_kb.glossary import TerminologyError
from cfm_kb.translate import translate_all


@pytest.fixture(autouse=True)
def _fake_azure_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide dummy Azure OpenAI env so ``translate_all`` can build a client.

    ``translate_all`` resolves the deployment and OpenAI client (fail-fast,
    reused across files) before delegating to the monkeypatched
    ``translate_markdown``. The client is never actually called, so dummy values
    are enough — this keeps the tests hermetic and free of real credentials,
    which the CI test step does not (and should not) provide.
    """
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://dummy.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "dummy-key")
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "dummy-deployment")


def _make_articles(tmp_path: Path) -> Path:
    """Create an ``articles`` dir with two English sources and one target lang."""
    articles = tmp_path / "articles"
    (articles / "English").mkdir(parents=True)
    (articles / "Français").mkdir(parents=True)
    (articles / "English" / "a.md").write_text("# A\n\nAlpha.\n", encoding="utf-8")
    (articles / "English" / "b.md").write_text("# B\n\nBeta.\n", encoding="utf-8")
    return articles


@pytest.fixture
def recorded_targets(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Replace ``translate_markdown`` with a fake recording target paths."""
    calls: list[Path] = []

    def fake_translate_markdown(source_path, target_path, **kwargs) -> Path:  # noqa: ANN001
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("TRANSLATED", encoding="utf-8")
        calls.append(target_path)
        return target_path

    monkeypatch.setattr(translate_mod, "translate_markdown", fake_translate_markdown)
    return calls


class TestSourceFileSelection:
    def test_none_translates_all_files(
        self, tmp_path: Path, recorded_targets: list[Path]
    ) -> None:
        articles = _make_articles(tmp_path)

        count = translate_all(articles_dir=articles, target_langs=["Français"])

        assert count == 2
        assert len(recorded_targets) == 2

    def test_restricts_to_given_files(
        self, tmp_path: Path, recorded_targets: list[Path]
    ) -> None:
        articles = _make_articles(tmp_path)

        count = translate_all(
            articles_dir=articles,
            target_langs=["Français"],
            source_files=[articles / "English" / "a.md"],
        )

        assert count == 1
        assert recorded_targets == [articles / "Français" / "a.md"]

    def test_unrelated_paths_translate_nothing(
        self, tmp_path: Path, recorded_targets: list[Path]
    ) -> None:
        articles = _make_articles(tmp_path)

        count = translate_all(
            articles_dir=articles,
            target_langs=["Français"],
            source_files=[articles / "English" / "does-not-exist.md"],
        )

        assert count == 0
        assert recorded_targets == []

    def test_empty_list_translates_all(
        self, tmp_path: Path, recorded_targets: list[Path]
    ) -> None:
        # An empty list is falsy in the CLI, which passes None; ensure passing
        # None (the default) still translates everything.
        articles = _make_articles(tmp_path)

        count = translate_all(
            articles_dir=articles, target_langs=["Français"], source_files=None
        )

        assert count == 2


class TestTerminologyGate:
    def test_missing_glossary_term_raises(
        self, tmp_path: Path, recorded_targets: list[Path]
    ) -> None:
        # Source contains the glossary term "feedback"; the fake translation
        # ("TRANSLATED") omits the agreed French rendering, so the run fails.
        articles = tmp_path / "articles"
        (articles / "English").mkdir(parents=True)
        (articles / "Français").mkdir(parents=True)
        (articles / "English" / "a.md").write_text(
            "# A\n\nSubmit feedback here.\n", encoding="utf-8"
        )

        with pytest.raises(TerminologyError) as excinfo:
            translate_all(articles_dir=articles, target_langs=["Français"])

        assert any("feedback" in issue for issue in excinfo.value.issues)

    def test_valid_translation_passes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        articles = tmp_path / "articles"
        (articles / "English").mkdir(parents=True)
        (articles / "Français").mkdir(parents=True)
        (articles / "English" / "a.md").write_text(
            "# A\n\nSubmit feedback here.\n", encoding="utf-8"
        )

        def fake_translate_markdown(source_path, target_path, **kwargs) -> Path:  # noqa: ANN001
            target_path = Path(target_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(
                "Soumettez votre retour d'information ici.", encoding="utf-8"
            )
            return target_path

        monkeypatch.setattr(
            translate_mod, "translate_markdown", fake_translate_markdown
        )

        count = translate_all(articles_dir=articles, target_langs=["Français"])

        assert count == 1
