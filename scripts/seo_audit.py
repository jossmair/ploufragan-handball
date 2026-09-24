"""Validate SEO and local references in the generated static PHB website."""
from collections import Counter, defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ploufragan-handball.fr/"
FILES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "articles").glob("*.html"))
REQUIRED_OG = {"og:type", "og:site_name", "og:locale", "og:title",
               "og:description", "og:url", "og:image"}
REQUIRED_TWITTER = {"twitter:card", "twitter:title", "twitter:description", "twitter:image"}
COMPETITIVE = {
    "u11-mixte", "u13-filles", "u13-garcons", "u15-filles", "u15-garcons",
    "u18-garcons", "seniors-feminines", "seniors-masculins-1",
    "seniors-masculins-2",
}
ALLOWED_NOINDEX = {"404.html", "actualites.html", "permanences-seniors-masculins.html"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.reading_title = False
        self.reading_schema = False
        self.schema_text = ""
        self.schemas = []
        self.lang = ""
        self.h1 = 0
        self.main = 0
        self.meta = {}
        self.meta_counts = Counter()
        self.canonical = []
        self.references = []
        self.links = []
        self.anchors = []
        self.images = []
        self.ids = Counter()
        self.text_elements = []
        self.open_text_elements = []
        self.refresh = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids[attrs["id"]] += 1
        if tag in ("h2", "h3", "button"):
            item = {"tag": tag, "attrs": attrs, "text": ""}
            self.text_elements.append(item)
            self.open_text_elements.append(item)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "title":
            self.reading_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "main":
            self.main += 1
        elif tag == "meta":
            name = attrs.get("name") or attrs.get("property")
            if name:
                self.meta[name] = attrs.get("content", "")
                self.meta_counts[name] += 1
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        elif tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical.append(attrs.get("href", ""))
            elif attrs.get("href") and attrs.get("rel") != "sitemap":
                self.references.append(("resource", attrs["href"]))
        elif tag == "a":
            self.links.append(attrs.get("href", ""))
            self.anchors.append(attrs)
            self.references.append(("link", attrs.get("href", "")))
        elif tag in ("img", "script", "source", "video", "iframe"):
            if tag == "img":
                self.images.append(attrs)
            if attrs.get("src"):
                self.references.append(("resource", attrs["src"]))
            if tag == "script" and attrs.get("type") == "application/ld+json":
                self.reading_schema = True
                self.schema_text = ""

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "button"):
            for index in range(len(self.open_text_elements) - 1, -1, -1):
                if self.open_text_elements[index]["tag"] == tag:
                    self.open_text_elements.pop(index)
                    break
        if tag == "title":
            self.reading_title = False
        elif tag == "script" and self.reading_schema:
            self.schemas.append(self.schema_text)
            self.reading_schema = False

    def handle_data(self, data):
        for item in self.open_text_elements:
            item["text"] += data
        if self.reading_title:
            self.title += data
        if self.reading_schema:
            self.schema_text += data


def local_path(page_file, url):
    parsed = urlparse(url)
    if parsed.scheme in ("mailto", "tel", "javascript", "data") or url.startswith("//"):
        return None
    if parsed.scheme and parsed.scheme != "https":
        return None
    if parsed.netloc and parsed.netloc != "ploufragan-handball.fr":
        return None
    if parsed.scheme == "https":
        path = ROOT / unquote(parsed.path.lstrip("/"))
    elif parsed.path.startswith("/"):
        path = ROOT / unquote(parsed.path.lstrip("/"))
    else:
        path = page_file.parent / unquote(parsed.path)
    if not parsed.path:
        path = page_file
    if path == ROOT or path.is_dir():
        path /= "index.html"
    return path.resolve()


def schema_types(node):
    return {item.get("@type") for item in schema_nodes(node)}


def schema_nodes(node):
    if isinstance(node, list):
        return [item for item in node if isinstance(item, dict)]
    if isinstance(node, dict):
        return [item for item in node.get("@graph", [node]) if isinstance(item, dict)]
    return []


def schema_asset_urls(value):
    """Yield only image/logo URLs, not external identity or social URLs."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ("image", "logo") and isinstance(item, str):
                yield item
            else:
                yield from schema_asset_urls(item)
    elif isinstance(value, list):
        for item in value:
            yield from schema_asset_urls(item)


def audit():
    errors = []
    warnings = []
    pages = {}
    indexable = {}
    inbound = defaultdict(set)
    titles = Counter()
    descriptions = Counter()
    canonicals = Counter()
    for file in FILES:
        relative = file.relative_to(ROOT).as_posix()
        page = Page()
        try:
            page.feed(file.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{relative}: HTML illisible ({exc})")
            continue
        pages[file.resolve()] = page
        noindex = "noindex" in page.meta.get("robots", "").lower()
        if relative not in ALLOWED_NOINDEX and noindex:
            errors.append(f"{relative}: noindex inattendu")
        if not noindex:
            indexable[file.resolve()] = relative
        if page.lang != "fr":
            errors.append(f"{relative}: html lang=fr absent")
        if not page.title.strip():
            errors.append(f"{relative}: title absent")
        if not noindex:
            titles[page.title.strip()] += 1
            description = page.meta.get("description", "").strip()
            descriptions[description] += 1
            if not description:
                errors.append(f"{relative}: description absente")
            if page.h1 != 1 or page.main != 1:
                errors.append(f"{relative}: {page.h1} H1 et {page.main} main (attendu : 1 de chaque)")
            expected = SITE if relative == "index.html" else SITE + relative
            canonicals[expected] += 1
            if page.canonical != [expected]:
                errors.append(f"{relative}: canonical {page.canonical} au lieu de {expected}")
            if len(page.title.strip()) < 24 or len(page.title.strip()) > 78:
                warnings.append(f"{relative}: longueur du title à examiner ({len(page.title.strip())} caractères)")
            if description and (len(description) < 65 or len(description) > 190):
                warnings.append(f"{relative}: longueur de description à examiner ({len(description)} caractères)")
            for name in ("description", "og:title", "og:description", "og:url", "og:image"):
                if page.meta_counts[name] != 1:
                    errors.append(f"{relative}: {name} présent {page.meta_counts[name]} fois")
            if page.meta.get("og:url") != expected:
                errors.append(f"{relative}: og:url incohérent")
            if page.meta.get("og:site_name") != "Ploufragan Handball" or page.meta.get("og:locale") != "fr_FR":
                errors.append(f"{relative}: identité Open Graph incohérente")
            for item in REQUIRED_OG | REQUIRED_TWITTER:
                if not page.meta.get(item):
                    errors.append(f"{relative}: balise {item} absente")
            for item in ("og:image", "twitter:image"):
                image = page.meta.get(item, "")
                if not image.startswith(SITE):
                    errors.append(f"{relative}: {item} doit utiliser le domaine HTTPS officiel")
                elif not (ROOT / image.removeprefix(SITE)).is_file():
                    errors.append(f"{relative}: image sociale absente : {image}")
            for name in ("og:image:width", "og:image:height"):
                if not page.meta.get(name, "").isdigit() or int(page.meta[name]) <= 0:
                    errors.append(f"{relative}: dimension Open Graph {name} invalide")
            nodes = []
            for raw in page.schemas:
                try:
                    parsed = json.loads(raw)
                    nodes.extend(schema_nodes(parsed))
                    for image in schema_asset_urls(parsed):
                        if image.startswith(SITE) and not (ROOT / image.removeprefix(SITE)).is_file():
                            errors.append(f"{relative}: image JSON-LD absente : {image}")
                except (ValueError, TypeError) as exc:
                    errors.append(f"{relative}: JSON-LD invalide ({exc})")
            schema = [node.get("@type") for node in nodes]
            ids = [node.get("@id") for node in nodes if node.get("@id")]
            if len(ids) != len(set(ids)) or any(not item.startswith(SITE) for item in ids):
                errors.append(f"{relative}: @id JSON-LD dupliqué ou non canonique")
            webpage = next((node for node in nodes if node.get("@type") == "WebPage"), None)
            if not webpage or webpage.get("@id") != expected + "#webpage" or webpage.get("url") != expected:
                errors.append(f"{relative}: WebPage canonique absent ou incohérent")
            elif webpage.get("isPartOf") != {"@id": SITE + "#website"} or webpage.get("publisher") != {"@id": SITE + "#organization"}:
                errors.append(f"{relative}: WebPage non reliée au site et au club")
            if relative == "index.html" and not {"SportsOrganization", "WebSite"} <= set(schema):
                errors.append(f"{relative}: identité SportsOrganization/WebSite absente")
            if relative == "index.html":
                organization = next((node for node in nodes if node.get("@type") == "SportsOrganization"), {})
                website = next((node for node in nodes if node.get("@type") == "WebSite"), {})
                if organization.get("@id") != SITE + "#organization" or website.get("@id") != SITE + "#website" or website.get("publisher") != {"@id": SITE + "#organization"}:
                    errors.append(f"{relative}: identifiants Organisation/WebSite incohérents")
            if relative.startswith("articles/") and "BlogPosting" not in schema:
                errors.append(f"{relative}: BlogPosting absent")
            if relative.startswith("articles/"):
                article = next((node for node in nodes if node.get("@type") == "BlogPosting"), {})
                if article.get("@id") != expected + "#article" or article.get("mainEntityOfPage") != {"@id": expected + "#webpage"} or article.get("publisher") != {"@id": SITE + "#organization"}:
                    errors.append(f"{relative}: BlogPosting non relié à sa page ou au club")
            if relative.removesuffix(".html") in COMPETITIVE and "SportsTeam" not in schema:
                errors.append(f"{relative}: SportsTeam absent")
            if relative.removesuffix(".html") in COMPETITIVE:
                team = next((node for node in nodes if node.get("@type") == "SportsTeam"), {})
                if team.get("@id") != expected + "#team" or team.get("parentOrganization") != {"@id": SITE + "#organization"}:
                    errors.append(f"{relative}: SportsTeam non relié au club")
            if relative != "index.html" and "BreadcrumbList" not in schema:
                errors.append(f"{relative}: BreadcrumbList absent")
            if relative != "index.html":
                crumb = next((node for node in nodes if node.get("@type") == "BreadcrumbList"), {})
                trail = crumb.get("itemListElement", [])
                if not trail or trail[-1].get("item") != expected or [part.get("position") for part in trail] != list(range(1, len(trail) + 1)):
                    errors.append(f"{relative}: BreadcrumbList incohérent")
            if "keywords" in page.meta:
                errors.append(f"{relative}: meta keywords interdite")
        if relative == "404.html" and not noindex:
            errors.append("404.html: noindex absent")
        if relative == "actualites.html" and not (noindex and page.refresh):
            errors.append("actualites.html: ancienne URL doit rester une redirection non indexable")
        duplicates = sorted(item for item, count in page.ids.items() if count > 1)
        if duplicates:
            errors.append(f"{relative}: id dupliqué : {', '.join(duplicates)}")
        for item in page.text_elements:
            if item["text"].strip():
                continue
            attrs = item["attrs"]
            if item["tag"] == "button" and (attrs.get("aria-label", "").strip() or attrs.get("title", "").strip()):
                continue
            errors.append(f"{relative}: {item['tag']} vide ou sans nom accessible")
        for image in page.images:
            if "alt" not in image:
                errors.append(f"{relative}: image sans alt ({image.get('src', '')})")
            if "width" not in image or "height" not in image:
                warnings.append(f"{relative}: dimensions absentes ({image.get('src', '')})")
        for kind, url in page.references:
            if not url or url == "#":
                errors.append(f"{relative}: lien vide ou #")
                continue
            if url.startswith("http://"):
                errors.append(f"{relative}: ressource HTTP non sécurisée {url}")
            target = local_path(file, url)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f"{relative}: {kind} local cassé : {url}")
            elif kind == "link":
                inbound[target].add(file.resolve())
                if target.name == "actualites.html":
                    errors.append(f"{relative}: lien interne vers l’ancienne URL {url}")
                if urlparse(url).path.endswith("/index.html") or urlparse(url).path == "index.html":
                    errors.append(f"{relative}: lien interne non canonique vers index.html : {url}")
        for anchor in page.anchors:
            if anchor.get("target") == "_blank" and "noopener" not in anchor.get("rel", ""):
                errors.append(f"{relative}: lien target=_blank sans noopener : {anchor.get('href', '')}")
    for value, count in titles.items():
        if count > 1:
            errors.append(f"title dupliqué ({count}) : {value}")
    for value, count in descriptions.items():
        if count > 1 and value:
            errors.append(f"description dupliquée ({count}) : {value}")
    for value, count in canonicals.items():
        if count > 1:
            errors.append(f"canonical dupliquée ({count}) : {value}")
    for file, page in pages.items():
        relative = file.relative_to(ROOT).as_posix()
        for url in page.links:
            fragment = urlparse(url).fragment
            if not fragment:
                continue
            target = local_path(file, url)
            if target in pages and fragment not in pages[target].ids:
                errors.append(f"{relative}: ancre interne introuvable : {url}")
    sitemap = ROOT / "sitemap.xml"
    try:
        entries = ElementTree.parse(sitemap).findall("{*}url")
        urls = [entry.findtext("{*}loc") for entry in entries]
    except (ElementTree.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml invalide : {exc}")
        urls = []
    if len(urls) != len(set(urls)):
        errors.append("sitemap.xml contient des URL dupliquées")
    expected_urls = {SITE if name == "index.html" else SITE + name for name in indexable.values()}
    for url in sorted(expected_urls - set(urls)):
        errors.append(f"URL indexable absente du sitemap : {url}")
    for url in sorted(set(urls) - expected_urls):
        errors.append(f"URL non canonique ou non indexable dans le sitemap : {url}")
    for file, relative in indexable.items():
        if relative != "index.html" and not inbound[file]:
            errors.append(f"page orpheline : {relative}")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: " + SITE + "sitemap.xml" not in robots or "Disallow:" in robots:
        errors.append("robots.txt bloque potentiellement le crawl ou omet le sitemap")
    for css in (ROOT / "assets").rglob("*.css"):
        source = css.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", source):
            url = match.group(1)
            target = local_path(css, url)
            if target is not None and not target.is_file():
                errors.append(f"{css.relative_to(ROOT)}: ressource CSS absente : {url}")
    print(f"SEO : {len(indexable)} pages indexables, {len(urls)} URL sitemap, {len(errors)} erreurs, {len(warnings)} avertissements")
    for message in errors:
        print("ERROR", message)
    for message in warnings:
        print("WARNING", message)
    if not errors:
        print("PASS : aucune erreur SEO critique")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(audit())
