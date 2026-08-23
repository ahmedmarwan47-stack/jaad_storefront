"""Product detail — Figma 'Product' (383:33745).

One layout, NINETY-NINE pages. `build()` still writes product.html (the worked
example below), and `build_many()` writes product-<id>.html for every product
in the catalogue — before that, every card on the site linked to the same
single page, so clicking any product opened the coffee. The card links in
components.py carry the id; the build fails loudly if a page goes missing.

What differs per page is only what we genuinely have per product:

  * name, prices, gallery, sizes, badge, social proof — catalog.json fields,
    all fetched
  * description — the client's own Arabic `short_description`
    (`descAr`, fetched by build/fetch_descriptions.py); omitted when absent
  * the "الفوائد" accordion — the client's own Arabic `description` HTML
    (`descHtmlAr`, same scraper), sanitised down to lists and emphasis

The hero keeps its hand-curated copy (translated from the client's English,
flagged in DESIGN-NOTES); nothing else gets invented prose. A product the
client never wrote copy for renders without a description rather than with
ours — same rule as the branch phone numbers.
"""
import re
from html import unescape

from catalog import PRODUCTS, e, in_category, money, rail_products, title
from components import (
    ICON, accordion, best_seller_badge, button, carousel, page, page_header,
    points_callout, product_card, product_gallery, price_sticker, qty_stepper,
    rating, size_chips, sold_proof, specs_block, bundle_item, section_heading,
)

SLUG = "product.html"

# Uniform product "specs" copy (Ahmed, 2026-08-02) — the SAME tagline,
# description and three leaf-marked sentences on ALL 99 product pages, drawn by
# specs_block(). It replaces the old per-product icon/label tiles, which varied
# with whatever benefit lines each product carried (some were single words like
# "مخبوزة"), so the strip now reads identically for the handoff. Brand-level
# reassurance only — no auditable product claim — and still OUR unsigned Arabic
# pending client sign-off, flagged in DESIGN-NOTES like every in-house string.
SPECS_TAGLINE = "جودة جاد في كل قضمة"
SPECS_DESC = "منتجات نختارها بعناية ونقدّمها لك بالطزاجة والجودة اللي تستاهلها."
SPECS_POINTS = [
    "مكوّنات مختارة بعناية من مصادر موثوقة لضمان أفضل مذاق.",
    "معايير جودة ثابتة من التحضير حتى التغليف للحفاظ على الطزاجة.",
    "مثالي للتسالي اليومية أو للمشاركة مع العائلة والأصحاب.",
]


def product_slug(p):
    """The output filename for a product's own page — used by components.py
    for card links, so the two can never drift apart."""
    return f"product-{p.get('id', 0)}.html"


# Worked example — the first Coffee SKU. Unlike Abu Auf's 99-product catalog
# (10 of which had real multi-size pricing to demo via size chips), none of
# Jaad's 26 SKUs are sold in more than one size, so there's no multi-size
# product to specifically pick for that reason. Simple, honest fallback.
def _hero():
    return in_category("Coffee")[0]


# All the descriptive copy below belongs to the hero product above. It used to
# describe chocolate-stuffed dates, which stopped being true the moment the
# hero became coffee — a page whose body copy contradicts its own title is
# worse than one with thin copy.
#
# The wording is a translation of the client's OWN English `shortDesc` for this
# SKU ("Enjoy the delicate, bright flavors of Jaad's light-roasted Brazilian
# coffee... smooth, refreshing brew, perfect for those who appreciate a lighter
# roast") plus what the product's real name states — light roast, Brazilian
# beans. So it restates client copy rather than inventing claims.
#
# It is still OUR Arabic, and unsigned-off, exactly like every other
# translated string in this build. Flagged in DESIGN-NOTES. Note what is
# deliberately absent: no health or nutrition claim, and nothing like the
# reference design's "third-party tested" / "100% vegan", which are auditable
# statements about a supply chain that nobody at Jaad has made.
DESCRIPTION = (
    "استمتع بالنكهات الخفيفة والمشرقة من بن جاد البرازيلي فاتح التحميص. "
    "مذاق ناعم ومنعش، مثالي لمن يفضلون التحميص الفاتح في فنجانهم اليومي."
)

# The SINGLE uniform "الفوائد" list, shown on EVERY product (Ahmed,
# 2026-08-02). The client's own benefit copy varies in count and layout
# product-to-product (some labelled, some plain bullets, some absent), so the
# only way to give the section the same density and layout everywhere is one
# fixed list. Brand-level reassurance, no auditable SKU claim; in-house Arabic
# pending sign-off (flagged in DESIGN-NOTES).
# Each benefit now leads with its own short heading (text-sm, below the
# accordion's text-base title) and a supporting line beneath it, so the section
# reads as four labelled points rather than a flat bullet list. Same in-house
# Arabic, still pending sign-off (DESIGN-NOTES).
_BENEFIT_ITEMS = [
    ("مكوّنات مختارة بعناية", "من مصادر موثوقة ودون أي إضافات غير ضرورية."),
    ("نكهة غنية ومتوازنة", "مثالية للتسالي في أي وقت من اليوم."),
    ("الأنسب للضيافة", "خيار رائع للمشاركة مع العائلة والأصحاب."),
    ("طازج حتى آخر قضمة", "يصلك بتغليف يحافظ على جودته وطزاجته."),
]
BENEFITS_UNIFORM = '<ul class="flex flex-col gap-4">' + "".join(f"""
                        <li class="flex gap-2.5">
                          <span class="mt-1.5 bg-cta rounded-full size-1.5 shrink-0"></span>
                          <div class="min-w-0">
                            <p class="font-semibold text-ink text-sm">{t}</p>
                            <p class="text-muted text-xs leading-6">{d}</p>
                          </div>
                        </li>""" for t, d in _BENEFIT_ITEMS) + """
                      </ul>"""

BENEFITS = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>نكهات خفيفة ومشرقة من التحميص الفاتح</li>
                        <li>حبوب برازيلية مختارة بعناية</li>
                        <li>مذاق ناعم ومنعش مناسب للتحضير اليومي</li>
                      </ul>"""

STORAGE = """
                      <ul class="flex flex-col gap-2 ps-5 list-disc">
                        <li>يحفظ في عبوة محكمة الغلق بعيداً عن الرطوبة</li>
                        <li>بعيداً عن أشعة الشمس المباشرة ومصادر الحرارة</li>
                        <li>يفضل استهلاكه خلال فترة قصيرة بعد الفتح للحفاظ على الطزاجة</li>
                      </ul>"""

# Generic product FAQ — IDENTICAL on all 99 pages by design (Ahmed, 2026-07-29).
# There is no per-product FAQ data in the catalogue, and this project does not
# invent product content, so every answer here restates something the site
# already commits to elsewhere: the two-hour delivery row on this same page, the
# 14-day window on return-policy.html, and the size chips above. Storage and
# freshness are generic handling advice, not a claim about this SKU. Making it
# uniform is the point — the developer handoff gets one FAQ component that is the
# same on every page rather than a section that appears only where data exists.
_P = 'class="text-neutral-800 leading-7"'
FAQ_ITEMS = [
    ("كم يستغرق توصيل الطلب؟",
     f'<p {_P}>التوصيل خلال ساعتين داخل القاهرة الكبرى، ويصل إلى باقي المحافظات حسب المنطقة. يمكنك تغيير منطقة التوصيل من أعلى الصفحة.</p>'),
    ("هل يمكنني استرجاع المنتج؟",
     f'<p {_P}>نعم، يمكنك الاسترجاع خلال 14 يوماً من تاريخ الاستلام وفق سياسة الاسترجاع المتبعة.</p>'),
    ("كيف أحافظ على المنتج طازجاً؟",
     f'<p {_P}>يُحفظ المنتج في مكان جاف بعيداً عن الرطوبة وأشعة الشمس المباشرة ومصادر الحرارة للحفاظ على نكهته وطزاجته.</p>'),
    ("هل تتوفر أحجام أو عبوات أخرى؟",
     f'<p {_P}>تختلف الأحجام المتاحة حسب المنتج، وتظهر خيارات الحجم أعلى الصفحة عند توفر أكثر من عبوة.</p>'),
]


# The client's `description` HTML is WordPress output — strong/ul/li plus
# whatever a content editor once pasted in. Keep only the structural tags the
# accordion can style and drop every attribute; anything else is stripped to
# its text. `.desc-rich` in styles.css restores the list treatment the hero's
# hand-written markup carries inline.
_ALLOWED_TAGS = {"strong", "b", "em", "ul", "ol", "li", "p", "br"}


def _clean_client_html(html):
    def keep(m):
        tag = m.group(2).lower()
        return f"<{m.group(1)}{tag}>" if tag in _ALLOWED_TAGS else ""
    cleaned = re.sub(r"<(/?)([a-zA-Z0-9]+)[^>]*/?>", keep, html)
    return f'<div class="desc-rich">{cleaned}</div>'


def _plain(text):
    """Strip markup out of a field that is supposed to be plain prose.

    `descAr` is the client's `short_description` and goes through e() into a
    <p>, so anything tag-shaped inside it escapes and renders as LITERAL
    VISIBLE MARKUP. It does contain such things: 20 of the 99 products carry
    pasted editor debris in that field — `<span data-sheets-root="1">` from a
    Google Sheets paste, `x_MsoListParagraph` from Word, and on product-8543 a
    whole `<div class="... AIPRM__conversation__response">` wrapper, which is
    what a ChatGPT web export leaves behind. Those pages were printing raw
    angle brackets at the shopper in body copy.

    Fixed here rather than in the scraped JSON on purpose: catalog.json is
    fetched data and is meant to stay a faithful copy of what the client's
    endpoints return (CLAUDE.md, "real data over invented data"). Laundering
    it in place would mean the next re-scrape silently reintroduces this. The
    presentation layer is the right place to be defensive about it, and the
    underlying data problem is the client's to fix — flagged in DESIGN-NOTES.
    """
    if not text:
        return ""
    stripped = re.sub(r"<[^>]*>", " ", text)
    return re.sub(r"\s+", " ", unescape(stripped)).strip()


# Two concept sets for the four benefit icons, swapped by the runtime
# Green/Orange toggle (Ahmed, 2026-08-19). Same benefit order in both, but a
# DIFFERENT metaphor per slot — not a restyle of the same object. V2 keeps the
# same green/lime/orange 3D house style so only the idea changes, not the look.
#   slot 0  selected ingredients   leaf        -> magnifier + bean
#   slot 1  rich balanced flavor   bolt        -> steaming cup
#   slot 2  best for hosting       shield      -> tray with two cups
#   slot 3  fresh arrival          motorbike   -> parcel with a leaf seal
_STORY_ICONS = [
    "images/jaad/icons/spec-leaf.png",
    "images/jaad/icons/spec-bolt.png",
    "images/jaad/icons/spec-shield.png",
    "images/jaad/icons/spec-delivery.png",
]
_STORY_ICONS_ALT = [
    "images/jaad/icons/spec-select.png",
    "images/jaad/icons/spec-cup.png",
    "images/jaad/icons/spec-serve.png",
    "images/jaad/icons/spec-parcel.png",
]


def _story_html(p):
    """White-image-mode scroll story (Ahmed, 2026-08-18) — prototype on the hero
    product only. A pinned, scroll-scrubbed stage: the white-bg packshot locks to
    screen-centre and drifts subtly (X/Y + a 2D-appropriate tilt, no 3D tumble)
    while each of the four benefits reveals in turn — alternating sides, each
    with its 3D icon, overlapping the image; the FAQ accordions close the story.
    Driven by initProductStory in scripts.js. Shown only under html[data-img=
    "plain"]; scene mode hides it and the normal in-panel benefits/FAQ take over
    (see the [data-buy-extras] wrapper)."""
    # White-bg packshot -> transparent cutout for the story, so the flying image
    # reads as an isolated product over the page (no white box over the copy).
    cutout = p["image"][:-4] + "-cutout.png"
    # Four fixed slots around the centred image — alternating sides, descending
    # so the panels ACCUMULATE (each stays once revealed) without colliding. The
    # first starts below 15% so it never sits under the top sticky buy bar.
    positions = [("is-right", "18%"), ("is-left", "38%"), ("is-right", "56%"), ("is-left", "72%")]
    panels = ""
    for i, (title_, desc_) in enumerate(_BENEFIT_ITEMS):
        side, top = positions[i % len(positions)]
        icon = _STORY_ICONS[i % len(_STORY_ICONS)]
        # Single icon; the site-wide concept swap (scripts.js initIconConcepts)
        # switches its src to the alt concept when the toggle is on Orange, the
        # same mechanism every other 3D icon on the site now uses.
        panels += f"""
            <div data-story-panel data-step="{i}" style="top:{top}" class="product-story__panel {side}">
              <img src="{e(icon)}" alt="" class="product-story__ico" loading="lazy" />
              <div class="min-w-0">
                <p class="font-bold text-ink text-sm sm:text-lg xl:text-xl leading-tight">{e(title_)}</p>
                <p class="mt-0.5 sm:mt-1 text-muted text-xs sm:text-sm leading-snug sm:leading-6">{e(desc_)}</p>
              </div>
            </div>"""
    return f"""
      <!-- ==================== WHITE-MODE SCROLL STORY ====================
           Pinned + scroll-scrubbed. Only rendered on the hero product, only
           shown in white-image mode (styles.css gates on html[data-img]).
           initProductStory drives the image transform + the panel reveals. -->
      <section data-story data-cutout="{e(cutout)}" class="product-story" aria-hidden="true">
        <div data-story-stage class="product-story__stage">
          <img data-story-img src="{e(cutout)}" alt="{e(title(p))}" class="product-story__img" />
          {panels}
        </div>
      </section>
      <section data-story-faq class="product-story-faq">
        <div class="mx-auto px-4 max-w-[760px]">
          <h2 class="mb-6 font-medium text-heading text-[32px] md:text-[40px] leading-[1.2] text-center">الأسئلة الشائعة</h2>
          {accordion(FAQ_ITEMS)}
        </div>
      </section>"""


def _render(p):
    hero = p["id"] == _hero()["id"]
    story_on = True  # rolled out to every product (each SKU has its own cutout)
    story_host_cls = " story-host" if story_on else ""
    story_html = _story_html(p) if story_on else ""
    on_sale = p.get("sale") and p["sale"] < p["regular"]
    old_price = (
        f'<span class="text-muted text-xl line-through latin">EGP {money(p["regular"])}</span>'
        if on_sale else ""
    )

    similar = [x for x in in_category(p["category"]) if x["id"] != p["id"]][:10]
    more = rail_products("Nuts", "Coffee", limit=10)

    # Description: the hero's curated paragraph, or the client's own Arabic
    # short_description. No fallback prose — absence is honest, filler is not.
    desc = DESCRIPTION if hero else _plain(p.get("descAr"))
    desc_html = (
        f'<p class="text-neutral-800 text-base leading-8">{e(desc)}</p>' if desc else ""
    )

    # Accordion: IDENTICAL on every product now (Ahmed, 2026-08-02) — the same
    # الفوائد list and the same طريقة الحفظ, so the section's density and layout
    # never change from one product to the next. The client's per-product
    # benefit HTML varied in count and shape (2/1/0 sections, labelled vs plain),
    # which is exactly the inconsistency being removed; it is set aside in favour
    # of one uniform list. The uniform FAQ follows below.
    acc_items = [("الفوائد", BENEFITS_UNIFORM), ("طريقة الحفظ", STORAGE)]
    acc_html = accordion(acc_items)

    # The spec strip is uniform on all 99 pages now (Ahmed, 2026-08-02): one
    # tagline, one description and three leaf-marked sentences, drawn by
    # specs_block from the SPECS_* copy above. It replaced the per-product
    # icon/label tiles, whose text came from the client's benefit lines and so
    # ranged from full sentences to single words like "مخبوزة".
    trust_html = specs_block(SPECS_TAGLINE, SPECS_DESC, SPECS_POINTS)

    # Related products — an INTERACTIVE "you may also like" widget in the sticky
    # media column (Ahmed, 2026-07-29): each row a checkbox, a running total and
    # an "add all" button, reusing the bundle machinery in scripts.js. It is a
    # [data-bundle] box with NO data-product and no data-bundle-base, so both the
    # total and the add cover the RELATED items only — the current product is not
    # folded in the way "frequently bought together" folds it (productFrom walks
    # up and finds no [data-product] host on this side, so the base is empty).
    # Capped to four so the media side stays shorter than the scrollable info
    # side; dropped entirely when the category has no companions.
    # The related list now lives in the content column beneath the details card
    # (Ahmed, 2026-08-19), so it simply fills that column — no gallery-alignment
    # inset any more (it used to be inset 96px to line up under the main photo
    # back when it sat in the gallery column).
    related_list = ""
    if similar:
        picks = similar[:4]
        related_total = sum(x["price"] for x in picks)
        rows = "".join(bundle_item(x) for x in picks)
        related_list = f"""
          <div data-bundle class="flex flex-col bg-white shadow-custom4 p-4 xl:p-5 rounded-[20px]">
            <h2 class="mb-1 px-2 font-bold text-heading text-base xl:text-lg">قد يعجبك أيضاً</h2>
            <div class="flex flex-col">{rows}
            </div>
            <div class="flex flex-wrap justify-between items-center gap-3 mt-3 px-2 pt-3 border-divider border-t">
              <div class="flex flex-col">
                <span class="text-muted text-xs">الإجمالي</span>
                <span class="font-bold text-ink text-lg latin" data-bundle-total>EGP {money(related_total)}</span>
              </div>
              <button type="button" data-bundle-add class="bg-cta hover:bg-cta-hover px-5 py-2.5 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors">أضف الكل للسلة</button>
            </div>
          </div>"""

    # Generic FAQ, same on every page — sits in the scrollable info column
    # beneath the client's benefits accordion. See FAQ_ITEMS for why it is
    # uniform rather than per-product.
    faq_html = f"""
            <div class="flex flex-col gap-2">
              <h2 class="mt-1 font-bold text-heading text-lg xl:text-xl">الأسئلة الشائعة</h2>
              {accordion(FAQ_ITEMS)}
            </div>"""

    # Breadcrumb category read off the product, not typed in — it said
    # "التمور والفواكه المجففة" on a coffee page until this was made dynamic.
    body = f"""{page_header("", [("الرئيسية", "index.html"),
                                 (p.get("categoryAr") or "المنتجات", "shop-category.html"),
                                 (title(p), None)])}

      <!-- ============================ PRODUCT ============================ -->
      <section class="pt-6 pb-12">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-2 mx-auto px-4 max-w-[1536px]">

          <!-- Media column FIRST in the DOM, so it leads the reading order in
               both directions: in RTL (the default) first means the RIGHT
               column, in LTR the left one. It holds ONLY the gallery now
               (Ahmed, 2026-08-19) — the related list moved to the content
               column beside it, so this column stays short and the WHOLE of it
               is the sticky one that RIDES down as the taller content column
               scrolls (and, in white-image mode, is the packshot that then
               detaches to centre). `items-start` on the grid is load-bearing —
               it is what lets a grid child be shorter than its row so sticky
               has room to move. Sticky scoped to lg; below it the columns stack
               and there is nothing to scroll past. Works only because <main> is
               overflow-x-clip (see page()). -->
          <div class="flex flex-col gap-6 min-w-0 lg:self-start lg:sticky lg:top-[132px]">
          {product_gallery(p.get("images") or [p["image"]], title(p), p)}
          <!-- SCENE version: frequently-bought UNDER the gallery. Hidden in the
               white/story version, which shows its own copy in the right column
               instead (CSS gates on html[data-img="plain"]). -->
          <div class="story-fb-scene">{related_list}</div>
          </div>

          <!-- Content column second: the RTL-left / LTR-right column, holding
               the product-details card. The "قد يعجبك أيضاً" (frequently-bought)
               list sits UNDER THE GALLERY in the media column instead (Ahmed,
               2026-08-19). This column is the tall one the sticky gallery
               scrolls against. -->
          <div class="flex flex-col gap-6 min-w-0">
          <!-- data-product lets the cart store read this product straight off
               the DOM, same as a product card. The white card is desktop-only
               (Ahmed, 2026-08-02): on mobile the info column drops its container
               so the content sits inline with the page grid, like the gallery
               beside it. lg+ keeps the card. -->
          <div class="flex flex-col gap-5 lg:bg-white lg:shadow-custom4 lg:p-6 xl:p-8 lg:rounded-[20px]{story_host_cls}"
               data-product data-record-view data-id="{p.get('id', 0)}" data-name="{e(title(p))}"
               data-price="{p.get('sale') or p.get('price') or 0}" data-image="{e(p['image'])}">
            <div class="flex flex-col gap-3">
              {best_seller_badge(p)}
              <h1 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">{e(title(p))}</h1>
              <!-- Points callout sits with the rating + social-proof line, right
                   beside the red "best seller" proof text (Ahmed, 2026-08-04) —
                   not up by the yellow best-seller badge. Wraps on a narrow
                   column instead of colliding. -->
              <div class="flex flex-wrap items-center gap-x-3 gap-y-2">
                {rating("4.8", 126)}
                {sold_proof(p)}
                {points_callout(p)}
              </div>
            </div>
            {desc_html}

            {size_chips(p)}

            <!-- The yellow is a marker BAND shorter than the digits, not a tall
                 pill around them (Ahmed, 2026-08-02): the inline line-height
                 pulls the highlight in from the glyph tops/bottoms, so the price
                 size is untouched and only the rectangle shrinks. The size chips
                 repoint data-unit-price at the chosen SKU's real price; quantity
                 no longer multiplies this — it is the UNIT price, and the running
                 order total lives in the cart drawer and summary. -->
            <div class="flex flex-wrap items-center gap-3">
              {old_price}
              <span data-price-display data-unit-price="{p.get('sale') or p.get('price') or 0}"
                    class="inline-flex items-center bg-greenDeep shadow-[3px_5px_0px_#98CA55] px-3 py-1 rounded-tl-[20px] rounded-br-[20px] font-bold text-white text-2xl latin">EGP {money(p['price'])}</span>
            </div>

            <!-- The stepper IS the add control (Ahmed, 2026-07-26). There is
                 no "add to cart" press any more: + puts the product in the
                 basket, +/- move that line live, and - at 1 removes it. The
                 counter therefore shows the CART's quantity and reads 0 when
                 the product is not in it — a counter that "syncs directly"
                 cannot sit at 1 while the basket holds none.

                 The button beside it is اشتري الان: it opens the summary
                 drawer to carry on, and adds one first if the basket is empty
                 of this product, so pressing "buy now" always buys something.

                 This is the second pass on this block. The first kept an
                 "اضف الى السلة" button that committed the stepper's number;
                 Ahmed's point is that if the counter is bound to the cart, the
                 commit step has nothing left to do. -->
            <!-- data-buy-block: the sticky re-CTA watches this row and appears
                 once it has scrolled above the viewport. -->
            <div data-buy-block class="flex items-center gap-3">
{qty_stepper(cart_bound=True)}
              <button type="button" data-buy-cta class="flex-1 bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">
                اشتري الان
              </button>
            </div>

            <!-- Divider between the CTA and the product specs below it. It is a
                 plain flex child, so it sits inside the card's own p-6/xl:p-8
                 padding and lines up with every other row rather than bleeding
                 to the card edges (Ahmed, 2026-07-29). -->
            <div class="border-divider border-t" role="separator"></div>

            {trust_html}

            <div class="flex flex-wrap justify-between items-center gap-3 bg-cream px-4 py-3 rounded-xl">
              <span class="flex items-center gap-2 font-semibold text-primary text-sm">
                <span class="place-items-center grid bg-primary rounded-full text-white size-5 text-xs">✓</span>
                التوصيل خلال ساعتين في القاهرة الكبرى
              </span>
              <button type="button" data-open="location" class="font-semibold text-cta text-sm underline">تغيير المنطقة</button>
            </div>

            <!-- In white-image mode on the story product these give way to the
                 scroll story below; scene mode keeps them here. -->
            <div data-buy-extras class="flex flex-col gap-5">
              {acc_html}
              {faq_html}
            </div>
          </div>

          <!-- WHITE/story version: frequently-bought in the RIGHT column, so it
               reads as part of the content the packshot detaches after. Shown
               only in white mode; the scene copy under the gallery is hidden
               there (CSS gates on html[data-img="plain"]). -->
          <div class="story-fb-plain">{related_list}</div>
          </div>
        </div>
      </section>

      {story_html}

      <!-- =========================== MORE FROM US =========================== -->
      <section data-reveal class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر من جاد", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more), loop=True)}
        </div>
      </section>

      <!-- ===================== PREVIOUSLY SEEN PRODUCTS =====================
           Per-shopper history, not catalogue data — there is nothing to render
           at build time, so this ships `hidden` and empty. scripts.js
           (initRecentlyViewed) fills [data-recent-track] from the
           `jaad:recent` localStorage store and un-hides the section only
           when it finds at least one entry that is not THIS product; a
           first-time visitor or one who has only ever viewed this page never
           sees it appear. No-JS/JS-broken degrades to "section absent",
           never to a broken empty rail. -->
      <section data-recently-viewed data-exclude-id="{p.get('id', 0)}" hidden class="py-12 xl:py-16">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("شاهدت هذا مؤخراً")}
          {carousel("", track_attr=" data-recent-track", loop=True)}
        </div>
      </section>

      <!-- ========================= STICKY BUY BAR =========================
           A re-CTA that appears once the real buy block scrolls above the
           viewport: fixed to the BOTTOM on mobile, and under the sticky nav at
           the TOP on desktop (lg). It owns no state — its −/＋ and CTA forward
           to the real cart-bound stepper and buy button, and its title/price/
           quantity mirror them, so there is one writer of the cart. Enter/exit
           and the hidden rest state live in styles.css (.sticky-buybar); JS
           only toggles .is-visible. -->
      <div data-sticky-buybar aria-hidden="true"
           class="sticky-buybar fixed inset-x-0 bottom-0 lg:bottom-auto lg:top-12 z-30
                  bg-white border-divider border-t lg:border-t-0 lg:border-b">
        <div class="flex items-center gap-3 lg:gap-6 mx-auto px-4 max-w-[1536px] py-3">
          <img src="{e(p['image'])}" alt=""
               class="hidden sm:block bg-cream p-1 rounded-xl w-12 xl:w-14 h-12 xl:h-14 object-contain shrink-0" />
          <div class="flex items-center flex-1 gap-3 min-w-0">
            <p class="font-bold text-ink text-sm xl:text-base truncate">{e(title(p))}</p>
            <!-- The green price sticker (not plain text) so the bar carries the
                 same price badge the cards and the buy block use (Ahmed,
                 2026-08-19). Static: the JS price mirror is dropped with the
                 data-sticky-price hook since this SKU's price does not vary. -->
            <span class="shrink-0">{price_sticker(p['price'], "sm")}</span>
          </div>
          <!-- Quantity mirror — buttons forward to the real cart-bound stepper.
               dir="ltr" so the + always sits on the RIGHT (Ahmed, 2026-07-29):
               in the page's RTL flow the − would otherwise take the right slot.
               The digit is latin already, so forcing LTR here changes nothing
               but the button order. -->
          <div dir="ltr" class="inline-flex items-center gap-1 bg-white p-1 border border-divider rounded-full shrink-0">
            <button type="button" data-sticky-step="-1" aria-label="إنقاص"
                    class="place-items-center grid border border-divider hover:bg-cream rounded-full size-9 text-ink transition-colors"><span class="w-4 h-4">{ICON['minus']}</span></button>
            <span data-sticky-qty class="min-w-[2ch] font-bold text-ink text-sm text-center latin">1</span>
            <button type="button" data-sticky-step="1" aria-label="زيادة"
                    class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-9 text-white transition-colors"><span class="w-4 h-4">{ICON['plus']}</span></button>
          </div>
          <!-- Buy now — forwards to the real buy CTA, which opens the side cart
               after the quantity is set (Ahmed, 2026-07-29). This mirrors the
               main block's own button; it is deliberately NOT a plain add. -->
          <button type="button" data-sticky-buy
                  class="bg-cta hover:bg-cta-hover px-5 xl:px-8 py-2.5 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors shrink-0">اشتري الان</button>
        </div>
      </div>"""

    return page(
        f"{title(p)} | جاد",
        f"اشتري {title(p)} من جاد أونلاين — جودة عالية وتوصيل سريع لكل مصر.",
        body, "product",
        f"/products/{p['slug']}" if p.get("slug") else "/product",
    )


def build():
    return _render(_hero())


def build_many():
    """One page per catalogue product, product-<id>.html."""
    return [(product_slug(p), _render(p)) for p in PRODUCTS]
