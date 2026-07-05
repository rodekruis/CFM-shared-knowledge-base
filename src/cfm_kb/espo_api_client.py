"""Minimal EspoCRM REST API client.

Adapted from the official EspoCRM Python client
(https://github.com/espocrm/api-client-python), with added retry/backoff for
transient failures. Authenticates with an API key via the ``X-Api-Key`` header
and talks to the ``/api/v1/`` endpoint.
"""

import time
import urllib.parse
from collections.abc import Mapping
from typing import Any

import requests


def http_build_query(data: Any) -> str:
    """Serialize a nested dict/list into a PHP-style query string.

    Mirrors PHP's ``http_build_query`` so array/object parameters are encoded the
    way EspoCRM's API expects (e.g. ``where[0][type]=...``).
    """
    pairs: dict[str, str] = {}

    def render_key(parents: list[str | int]) -> str:
        key = ""
        for depth, part in enumerate(parents):
            bracketed = depth > 0 or isinstance(part, int)
            key += f"[{part}]" if bracketed else str(part)
        return key

    def encode(value: Any, parents: list[str | int]) -> None:
        if isinstance(value, (list, tuple)):
            for i, item in enumerate(value):
                encode(item, [*parents, i])
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                encode(sub_value, [*parents, sub_key])
        else:
            pairs[render_key(parents)] = str(value)

    encode(data, [])
    return urllib.parse.urlencode(pairs)


class EspoAPI:
    """Thin wrapper over the EspoCRM REST API with retry/backoff."""

    url_path = "/api/v1/"

    # Retry transient failures (network errors and 5xx / 429 responses) with
    # exponential backoff. Non-transient errors (e.g. 4xx) are not retried.
    max_retries = 3
    retry_backoff = 1.0  # seconds; doubled after each attempt
    retry_statuses = frozenset({429, 500, 502, 503, 504})

    def __init__(self, url: str, api_key: str) -> None:
        if url.endswith("/"):
            url = url[:-1]
        self.url = url
        self.api_key = api_key
        self.status_code: int | None = None

    def request(
        self, method: str, action: str, params: dict[str, Any] | None = None
    ) -> Any:
        """Send a request to ``action`` and return the parsed JSON response.

        For write methods (POST/PATCH/PUT) ``params`` is sent as the JSON body;
        otherwise it is encoded into the query string. Transient failures
        (network errors and the statuses in ``retry_statuses``) are retried with
        exponential backoff; any other non-200 response raises ``ValueError``.
        """
        if params is None:
            params = {}

        headers = {"X-Api-Key": self.api_key}

        url = self.normalize_url(action)
        json_body = None
        if method in ("POST", "PATCH", "PUT"):
            json_body = params
        else:
            url = url + "?" + http_build_query(params)

        backoff = self.retry_backoff
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.request(
                    method, url, headers=headers, json=json_body
                )
            except requests.exceptions.RequestException as exc:
                # Connection errors / timeouts: retry unless this was the last
                # attempt.
                if attempt >= self.max_retries:
                    raise ValueError(
                        f"Request to {action} failed after {attempt} attempts: {exc}"
                    ) from exc
                time.sleep(backoff)
                backoff *= 2
                continue

            self.status_code = response.status_code

            if self.status_code in self.retry_statuses and attempt < self.max_retries:
                time.sleep(backoff)
                backoff *= 2
                continue

            if self.status_code != 200:
                reason = self.parse_reason(response.headers)
                raise ValueError(f"{reason}, status code: {self.status_code}")

            data = response.content
            if not data:
                raise ValueError("Content response is empty")

            return response.json()

        # Loop exhausted on repeated retryable status codes.
        reason = self.parse_reason(response.headers)
        raise ValueError(
            f"{reason}, status code: {self.status_code} "
            f"(after {self.max_retries} attempts)"
        )

    def normalize_url(self, action: str) -> str:
        return self.url + self.url_path + action

    @staticmethod
    def parse_reason(headers: Mapping[str, str]) -> str:
        if "X-Status-Reason" not in headers:
            return "Unknown Error"

        return headers["X-Status-Reason"]
