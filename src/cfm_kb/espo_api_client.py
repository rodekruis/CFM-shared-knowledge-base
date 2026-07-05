import time
import urllib

import requests


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ""
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs

    return urllib.parse.urlencode(r_urlencode(data))


class EspoAPI:

    url_path = "/api/v1/"

    # Retry transient failures (network errors and 5xx / 429 responses) with
    # exponential backoff. Non-transient errors (e.g. 4xx) are not retried.
    max_retries = 3
    retry_backoff = 1.0  # seconds; doubled after each attempt
    retry_statuses = frozenset({429, 500, 502, 503, 504})

    def __init__(self, url, api_key):
        if url.endswith("/"):
            url = url[:-1]
        self.url = url
        self.api_key = api_key
        self.status_code = None

    def request(self, method, action, params=None):
        if params is None:
            params = {}

        headers = {"X-Api-Key": self.api_key}

        kwargs = {
            "url": self.normalize_url(action),
            "headers": headers,
        }

        if method in ["POST", "PATCH", "PUT"]:
            kwargs["json"] = params
        else:
            kwargs["url"] = kwargs["url"] + "?" + http_build_query(params)

        backoff = self.retry_backoff
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.request(method, **kwargs)
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
                raise ValueError(f"Content response is empty")

            return response.json()

        # Loop exhausted on repeated retryable status codes.
        reason = self.parse_reason(response.headers)
        raise ValueError(
            f"{reason}, status code: {self.status_code} "
            f"(after {self.max_retries} attempts)"
        )

    def normalize_url(self, action):
        return self.url + self.url_path + action

    @staticmethod
    def parse_reason(headers):
        if "X-Status-Reason" not in headers:
            return "Unknown Error"

        return headers["X-Status-Reason"]
