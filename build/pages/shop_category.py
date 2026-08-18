"""
Category listing — Figma 'Collection' (173:17211).

Coffee is the worked example for the /shop/<category> route pattern.

Simplified from the Abu Auf build this was forked from: that version had a
real coffee sub-category taxonomy (Turkish/Brazilian/instant/French/green,
read off Abu Auf's live filter bar) with a `subCats` field per product,
scraped from a Store API. Jaad has no live API and a much simpler coffee
line (light/medium/dark, plain or with cardamom, plus espresso — 7 SKUs,
not Abu Auf's ~30-variant coffee catalog), so there is no real sub-category
data to filter by. No sub-category chips were invented to fill that gap —
absence over invention.
"""
from _listing import listing
from catalog import in_category

SLUG = "shop-category.html"

CATEGORY_AR = "القهوة"
INTRO = ("قهوة تركية أصيلة بثلاث درجات تحميص — فاتح، وسط وغامق — سادة أو "
         "محوجة بالحبهان، بالإضافة للإسبريسو. محمصة ومطحونة تحافظ على "
         "الريحة لآخر فنجان.")


def build():
    products = in_category("Coffee")

    return listing(
        title_text=f"{CATEGORY_AR} | جاد",
        description="تسوق قهوة جاد: فاتح، وسط وغامق — سادة أو محوجة بالحبهان — "
                    "بأفضل الأسعار وتوصيل لكل مصر.",
        heading=CATEGORY_AR,
        trail=[("الرئيسية", "index.html"), ("المنتجات", "shop.html"), (CATEGORY_AR, None)],
        chips=[("القهوة", "shop-category.html", "all")],
        products=products,
        page_id="shop-category",
        path="/shop/coffee",
        intro=INTRO,
        active_chip=CATEGORY_AR,
    )
