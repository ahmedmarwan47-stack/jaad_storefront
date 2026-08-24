"""
Shared data access for the Jaad static build.

Everything page builders know about products, categories and prices comes
through here, so a change to (say) price formatting or which products feed a
rail happens in one place and reaches every page on the next build.

Unlike Abu Auf (scraped from a live WooCommerce store, needing name-cleanup
repair and a 316-branch dataset), Jaad's catalog.json is hand-authored from
the client's own 26-SKU table — no scrape-damage repair, no branches.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = os.path.join(ROOT, "static-export")
CATALOG_PATH = os.path.join(EXPORT, "data", "catalog.json")

_data = json.load(open(CATALOG_PATH, encoding="utf-8"))

PRODUCTS = _data["products"]
CATEGORIES = _data["categories"]
BY_API_NAME = {c["name"]: c for c in CATEGORIES}
BY_SLUG = {c["slug"]: c for c in CATEGORIES if c.get("slug")}


def e(s):
    """Escape for HTML attribute/text context."""
    return html.escape(str(s or ""), quote=True)


def title(p):
    """Display name — Arabic where we have it, English as a fallback."""
    return p.get("nameAr") or p["name"]


def money(v):
    """450.0 -> '450'  |  45.99 -> '45.99'"""
    return f"{v:.2f}".rstrip("0").rstrip(".") if v % 1 else f"{int(v)}"


def weight(p):
    """Pack weight as the display string, e.g. "250 جم" — or "" when unknown.

    PLACEHOLDER DATA (Ahmed, 2026-08-24). The client's table carries name,
    category and price only; these figures were added to catalog.json as
    plausible retail sizes per category so the card, the cart line and the
    product page can all show a pack size. They are not the real pack weights
    and must be replaced from the client's own list before launch.

    Returned from ONE place so every surface says the same thing: the card, the
    drawer, the cart page, the checkout summary and the product page all call
    this rather than formatting the number themselves.
    """
    w = p.get("weight")
    return f"{w} جم" if w else ""


def in_category(api_name, limit=None):
    out = [p for p in PRODUCTS if p["category"] == api_name]
    return out[:limit] if limit else out


def rail_products(*api_names, limit=12):
    """Products for a carousel, de-duplicated across the given categories."""
    seen, out = set(), []
    for name in api_names:
        for p in in_category(name):
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            out.append(p)
            if len(out) >= limit:
                return out
    return out


def category(api_name):
    return BY_API_NAME.get(api_name)


def nav_categories():
    return [c for c in CATEGORIES if c.get("nav")]


def home_categories():
    return [c for c in CATEGORIES if c.get("home")]
