#!/usr/bin/env python3
"""Check whether baidu.com and google.com are reachable."""

from __future__ import annotations

import socket
import urllib.error
import urllib.request


DEFAULT_URLS = (
	"https://www.baidu.com",
	"https://www.google.com",
)
TIMEOUT_SECONDS = 2.0


def check_url(url: str, timeout: float) -> tuple[bool, str]:
	"""Return whether a URL can be reached and a short result message."""
	request = urllib.request.Request(
		url,
		headers={"User-Agent": "network-accessibility-check/1.0"},
	)

	try:
		with urllib.request.urlopen(request, timeout=timeout) as response:
			response.read(1)
			return True, f"HTTP {response.status}"
	except urllib.error.HTTPError as error:
		# An HTTP response, including 4xx/5xx, proves that the host is reachable.
		return True, f"HTTP {error.code}"
	except (urllib.error.URLError, socket.timeout, TimeoutError, OSError) as error:
		reason = getattr(error, "reason", error)
		return False, str(reason)


def main() -> int:
	all_reachable = True
	for url in DEFAULT_URLS:
		reachable, detail = check_url(url, TIMEOUT_SECONDS)
		status = "reachable" if reachable else "unreachable"
		print(f"{url}: {status} ({detail})")
		all_reachable = all_reachable and reachable

	return 0 if all_reachable else 1


if __name__ == "__main__":
	raise SystemExit(main())
