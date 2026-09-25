"""Best-effort external-link inventory; temporary third-party failures never fail CI."""

from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "articles").glob("*.html"))


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        if href.startswith(("https://", "http://")):
            self.urls.add(href)


def check(url):
    request = Request(url, method="HEAD", headers={"User-Agent": "PHB-production-audit/1.0"})
    try:
        with urlopen(request, timeout=10) as response:
            return {"url": url, "domain": urlparse(url).netloc, "status": response.status, "result": "ok"}
    except HTTPError as error:
        # Authentication, anti-bot and rate limiting prove that the host answered.
        result = "reachable" if error.code in {401, 403, 405, 429} else "broken" if error.code in {404, 410} else "warning"
        return {"url": url, "domain": urlparse(url).netloc, "status": error.code, "result": result}
    except (URLError, TimeoutError, OSError) as error:
        return {"url": url, "domain": urlparse(url).netloc, "status": None, "result": "unavailable", "detail": str(error)}


def main():
    urls = set()
    for path in FILES:
        parser = Links()
        parser.feed(path.read_text(encoding="utf-8"))
        urls.update(parser.urls)
    with ThreadPoolExecutor(max_workers=12) as executor:
        results = sorted(executor.map(check, urls), key=lambda item: item["url"])
    output = ROOT / "reports" / "external-links-audit.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {name: sum(item["result"] == name for item in results) for name in ("ok", "reachable", "warning", "broken", "unavailable")}
    print(f"Liens externes : {len(results)} URL, " + ", ".join(f"{value} {name}" for name, value in counts.items()))
    for item in results:
        if item["result"] in {"broken", "unavailable"}:
            print(item["result"].upper(), item["status"], item["url"])
    print("INFO : cet audit est indicatif ; une indisponibilité externe temporaire ne bloque jamais le build.")


if __name__ == "__main__":
    main()
