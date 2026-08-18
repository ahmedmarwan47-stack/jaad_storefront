"""Shop — all products. Figma 'Collection' (173:17211)."""
from _listing import listing
from catalog import PRODUCTS, nav_categories

SLUG = "shop.html"


def build():
    # Three-item chips are live filters. Every slug here is a real
    # `categorySlug` from catalog.json, so each one has products behind it —
    # previously these all linked to shop-category.html, which shows coffee
    # whatever you picked.
    chips = [("كل المنتجات", "#all", "all")] + [
        (c["ar"], "#" + c["slug"], c["slug"]) for c in nav_categories()
    ]
    return listing(
        title_text="كل المنتجات | جاد",
        description="تصفح كل منتجات جاد: قهوة، مكسرات وبهارات طبيعية.",
        heading="كل المنتجات",
        trail=[("الرئيسية", "index.html"), ("كل المنتجات", None)],
        chips=chips,
        products=PRODUCTS,
        page_id="shop",
        path="/shop",
        active_chip="كل المنتجات",
    )
