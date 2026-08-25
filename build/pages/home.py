"""Home page — Figma node 9943:16397 (Jaad-Ecommerce file)."""
from _posts import POSTS
from catalog import PRODUCTS, e, home_categories, rail_products, category
from components import (
    ICON, article_card, button, carousel, category_tile, page,
    product_card, product_widget, review_card, section_heading,
)

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}

# Our Story three-column banner — Figma node 9971:16537. (image, title, copy).
STORY_COLUMNS = [
    ("story-coffee.jpg", "Premium Coffee",
     "Sourced directly from Anatolia, our Turkish coffee blends deliver rich, authentic flavor in every cup."),
    ("story-nuts.jpg", "Fresh Nuts",
     "Hand-selected Mediterranean nuts - walnuts, almonds, and cashews - naturally processed for peak freshness."),
    ("story-spices.jpg", "Aromatic Spices",
     "The finest spices from trusted growers, carefully curated to bring authentic flavor to your kitchen."),
]

# Scattered decorative leaves (Figma frames 2147227079-083) — (leaf, top%, left%,
# width class, rotate deg). Purely decorative; positions approximate the design.
STORY_LEAVES = [
    ("leaf-1.svg", "6%", "91%", "w-9", -50),
    ("leaf-2.svg", "14%", "46%", "w-14", 20),
    ("leaf-3.svg", "72%", "37%", "w-20", -140),
    ("leaf-4.svg", "30%", "75%", "w-9", -30),
    ("leaf-5.svg", "76%", "61%", "w-10", 80),
]

SLUG = "index.html"

# The Jaad Figma hero ("Natural Snacks / For Every Event", node 9943:16468)
# had its headline baked into the raster image as English text — wrong for
# an Arabic-first RTL site with a live language switch (Ahmed, 2026-08-17:
# "we want to setup the content to respect RTL and LTR, we already did that
# in Abu Auf"). Generated a version of the same photography via Higgsfield
# with the product cluster recomposed onto the LEFT third (packaging logos
# still render correctly, not mirrored) so real Arabic HTML text — not
# baked-in pixels — can sit in the open right two-thirds, translatable and
# under the site's own i18n system like every other heading.
# This is the ONE real hero, not Abu Auf's 4-banner rotation — no invented
# second/third slide.
HERO = [
    ("hero-jaad.webp", "hero-jaad-mob.webp", "جاد — سناكس طبيعية لكل مناسبة",
     "shop.html", "سناكس طبيعية", "لكل مناسبة", "تسوق الآن"),
]

# Explore JAAD's Categories — Figma node 9950:18205. Each card is a pair of
# product cutouts that "fly apart" on hover (Figma Default -> Variant2), sitting
# on a soft ground shadow, with a bold green title and a one-line description.
# (back cutout, front cutout) are exported straight from the Figma design assets.
CATEGORY_CARDS = [
    ("Nuts", "Premium hand-picked selections for every taste",
     "shop.html", "nuts-a.png", "nuts-b.png"),
    ("Spices", "Aromatic blends from the world's finest regions",
     "shop.html", "spices-a.png", "spices-b.png"),
    ("Coffee", "Rich, authentic flavors brewed to perfection",
     "shop.html", "coffee-a.png", "coffee-b.png"),
]

# Customer Reviews — Figma node 9950:17989. (quote, name, role). The design's
# own copy is bakery placeholder text; these are JAAD-appropriate (coffee /
# nuts / spices), in-house placeholder pending real testimonials.
REVIEWS = [
    ("The coffee and nuts are always fresh and consistently good, and every order arrives quickly.",
     "Mona Abdallah", "Loyal Customer"),
    ("Their Turkish coffee is one of the best I've tried, and the packaging keeps the aroma locked in.",
     "Ahmed Fouad", "Coffee Lover"),
    ("The spices have a strong, authentic aroma that genuinely changed my cooking — I'll order again.",
     "Sara Mahmoud", "Home Cook"),
    ("Excellent nut selection and fair prices for the quality you get. Highly recommended.",
     "Karim Samir", "Regular Customer"),
    ("From the very first cup I could taste the care — rich flavor, beautiful packaging, fast delivery.",
     "Omar Abdulrahman", "Celebrating Customer"),
]

# Scattered leaves for the reviews band (Figma frames under 9967) — (leaf, top%,
# left%, width class, rotate deg).
REVIEW_LEAVES = [
    ("leaf-1.svg", "4%", "1%", "w-12", 15),
    ("leaf-2.svg", "0%", "23%", "w-9", -35),
    ("leaf-3.svg", "2%", "72%", "w-8", 25),
    ("leaf-4.svg", "0%", "91%", "w-11", -65),
    ("leaf-5.svg", "40%", "1%", "w-9", -95),
    ("leaf-2.svg", "46%", "95%", "w-9", 120),
    ("leaf-3.svg", "80%", "2%", "w-16", -145),
    ("leaf-1.svg", "86%", "87%", "w-14", 50),
    ("leaf-4.svg", "90%", "38%", "w-10", -160),
    ("leaf-5.svg", "92%", "61%", "w-8", 70),
]

# Latest From JAAD — Figma node 9974:21059. The posts themselves live in
# _posts.POSTS (Ahmed, 2026-08-20), shared with the blog index and post pages,
# so the homepage teaser always shows the three most recent real articles
# instead of its own hardcoded copy of them.

# Frequently Asked Questions — Figma node 9967:21115. (question, answer). First
# is open by default. Answers are in-house, consistent with the site's policies.
FAQS = [
    ("What makes JAAD products different?",
     "At JAAD, we source our products directly from their origins — premium Turkish coffee from Anatolia, fresh nuts from Mediterranean farms, and aromatic spices from the finest growers. Every product is carefully selected and naturally processed to preserve its authentic flavor."),
    ("How should I store my coffee after opening?",
     "Keep your coffee in an airtight container away from heat, light and moisture. For the freshest cup, grind the beans just before brewing."),
    ("Do you offer international shipping?",
     "We currently deliver across Egypt — two-hour delivery in Greater Cairo and one to three working days for other governorates. International shipping is on the way."),
    ("Are your products organic?",
     "Our products are 100% natural and carefully sourced. We roast and pack in small batches to preserve flavor, aroma and nutritional value, with no additives."),
    ("What is your return policy?",
     "You can request a return within 14 days of delivery as long as the product is unopened and in its original condition. Opened food products cannot be returned, for food-safety reasons."),
    ("How can I track my order?",
     "Once your order ships you'll get a confirmation by email and SMS, and you can follow its status any time from the My Orders page in your account."),
]

# Kept from the about.py fix: real tagline, no invented founding year, no
# product categories Jaad doesn't carry (nut butters, dried fruit, snacks).
ABOUT_COPY = (
    "من الطبيعة إليك — جاد تقدم قهوة ومكسرات وبهارات طبيعية عالية الجودة، "
    "مصدرها الأصلي في قلب كل منتج. فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا "
    "المستمر بالتفاصيل، فإن كل خطوة في عملية الإنتاج في جاد تُدار بعناية "
    "لضمان إنتاج منتجات عالية الجودة يتم توصيلها بحب وملئها بالمكونات "
    "المغذية من الطبيعة الأم."
)

RAILS = [
    ("best", "الأكثر مبيعاً", ("Coffee", "Nuts", "Spices")),
    ("new", "وصل حديثاً", ("Coffee", "Nuts", "Spices")),
]

# Perfect Picks — Figma node 9946:16770. Three segmented tabs, five product
# widgets each. Curated from the real 26-SKU catalog by id. `discount` (Offers
# tab) applies a demo markdown so the tab has content — the catalog carries no
# real sale data (Ahmed: exact-match with demo data).
PERFECT_PICKS = [
    # Best Selling curated to the five products that have styled Figma
    # photography, so the default tab is fully styled.
    ("best", "Best Selling", [1, 2, 3, 12, 11], None),
    ("new", "New", [4, 8, 10, 21, 5], None),
    ("offers", "Offers", [9, 23, 20, 6, 22], 0.8),
]


# Mobile widths for the decorative leaves. The leaves now render on phones too
# (the leaves-on-scroll effect needs them present), but the hero/bands are much
# narrower there, so each leaf drops to a smaller width below `md` and the exact
# Figma width is restored at `md`+ — the desktop layout is left untouched. Any
# width not listed falls back to itself (i.e. no shrink), which is safe.
_LEAF_MOBILE_W = {
    "w-8": "w-5", "w-9": "w-5", "w-10": "w-6", "w-11": "w-6",
    "w-12": "w-7", "w-14": "w-8", "w-16": "w-9", "w-20": "w-11",
}


def render_leaves(items, dark=False):
    """Scattered decorative leaf layer (Figma). Absolute inside the nearest
    positioned ancestor. items: (leaf, top%, left%, width class, deg).

    Shown on every breakpoint (previously hidden below md): the mobile
    leaves-on-scroll effect needs the leaves in the DOM. On phones each leaf
    renders at a reduced width (`_LEAF_MOBILE_W`) so nothing crowds the smaller
    bands, and the parent bands are already `overflow-hidden` so a leaf near an
    edge is clipped rather than spilling the page. At `md`+ the original width
    is restored, so the desktop layout is identical to before.

    `data-leaf` + the `.leaf-wind` class let initLeafWind() scatter each leaf with
    the cursor. Base rotation is kept in `--lr` so the JS can layer a translate +
    rotation on top. `dark=True` brightens the leaves so they read on the dark
    green bands (the #015A2A leaf art is near-invisible there otherwise)."""
    tone = "opacity-90 brightness-150" if dark else "opacity-80"
    return "".join(
        f'<img src="images/jaad/decor/{leaf}" alt="" aria-hidden="true" data-leaf '
        f'class="leaf-wind block absolute {_LEAF_MOBILE_W.get(cls, cls)} md:{cls} h-auto {tone} pointer-events-none z-0" '
        f'style="top:{top};left:{left};--lr:{rot}deg" />'
        for leaf, top, left, cls, rot in items
    )


def category_card(title, desc, href, back, front):
    """Figma 9950:18205 — a pair of product cutouts on a soft shadow that fan
    apart on hover (Default -> Variant2): both bags lift, scale ~1.13x and tilt
    away from each other. Physical left/right on purpose — this is a product
    arrangement, not reading-order content."""
    return f"""
          <a href="{href}" data-cat-card class="group flex flex-col items-center gap-3 sm:gap-[18px] w-full max-w-[240px] sm:max-w-[356px]">
            <div class="relative w-full aspect-[356/260]">
              <!-- A soft blob behind each pair (Ahmed, 2026-08-25). FIRST child
                   and absolutely positioned, so it sits under the shadow and
                   both bags — the siblings below carry no z-index and simply
                   stack in DOM order, which is all the layering this needs.
                   Its own hover motion is deliberately slower and smaller than
                   the bags': it should feel like the ground shifting under
                   them, not a fourth thing fanning out. The bags are untouched. -->
              <span class="cat-blob" aria-hidden="true"></span>
              <!-- The fan-apart is a group-hover on desktop; on touch (no hover)
                   initCategoryReveal adds .in-view when the card scrolls to the
                   viewport centre, so the group-[.in-view] variants fire the same
                   motion (Ahmed, 2026-08-19). -->
              <img src="images/jaad/categories/cat-shadow.svg" alt="" aria-hidden="true"
                   class="bottom-[2%] left-1/2 absolute w-[72%] -translate-x-1/2 transition-all duration-500 ease-out group-hover:w-[82%] group-[.in-view]:w-[82%]" />
              <img src="images/jaad/categories/{back}" alt="" aria-hidden="true"
                   class="top-[4%] left-0 absolute w-[67.5%] aspect-square object-contain -rotate-[1.66deg] transition-transform duration-500 ease-out will-change-transform group-hover:-translate-x-[10%] group-hover:-translate-y-[7%] group-hover:-rotate-[7deg] group-hover:scale-[1.05] group-[.in-view]:-translate-x-[10%] group-[.in-view]:-translate-y-[7%] group-[.in-view]:-rotate-[7deg] group-[.in-view]:scale-[1.05]" />
              <img src="images/jaad/categories/{front}" alt="{e(title)}"
                   class="top-0 left-[27%] absolute w-[73%] aspect-square object-contain rotate-[1.56deg] transition-transform duration-500 ease-out will-change-transform group-hover:-translate-y-[6%] group-hover:rotate-[7deg] group-hover:scale-[1.05] group-[.in-view]:-translate-y-[6%] group-[.in-view]:rotate-[7deg] group-[.in-view]:scale-[1.05]" />
            </div>
            <div class="flex flex-col items-center gap-1.5 sm:gap-3 text-center">
              <h3 class="font-bold text-heading text-lg sm:text-2xl leading-[1.4]">{e(title)}</h3>
              <p class="max-w-[341px] text-[#4a4a4a] text-sm sm:text-base leading-[1.4]">{e(desc)}</p>
            </div>
          </a>"""


def build():
    cards = "".join(category_card(*c) for c in CATEGORY_CARDS)

    def pp_widgets(ids, discount):
        out = []
        for pid in ids:
            p = PRODUCTS_BY_ID.get(pid)
            if not p:
                continue
            sale = round(p["price"] * discount) if discount else None
            out.append(product_widget(p, sale=sale, slide=True))
        return "".join(out)

    pp_chips = "".join(
        f'<button type="button" class="tab-btn{" is-active" if i == 0 else ""}" '
        f'data-tab="{key}">{label}</button>'
        for i, (key, label, _ids, _d) in enumerate(PERFECT_PICKS)
    )
    pp_panels = "".join(
        f'<div class="tab-panel" data-panel="{key}"{"" if i == 0 else " hidden"}>'
        f'<div class="flex xl:justify-between gap-4 xl:gap-0 -mx-4 xl:mx-0 px-4 xl:px-0 scroll-pl-4 xl:scroll-pl-0 '
        f'overflow-x-auto xl:overflow-visible no-scrollbar snap-x">{pp_widgets(ids, disc)}'
        f'</div></div>'
        for i, (key, _label, ids, disc) in enumerate(PERFECT_PICKS)
    )

    story_cols = "".join(
        f"""
              <div class="relative h-full min-h-[300px] overflow-hidden">
                <img src="images/jaad/site/{img}" alt="{e(title)}" class="absolute inset-0 w-full h-full object-cover" loading="lazy" />
                <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/50"></div>
                <div class="absolute inset-x-6 bottom-8 flex flex-col gap-2 text-white">
                  <h3 class="font-bold text-2xl leading-tight">{e(title)}</h3>
                  <p class="text-white/90 text-sm leading-[1.4]">{e(copy)}</p>
                </div>
              </div>"""
        for img, title, copy in STORY_COLUMNS
    )
    story_leaves = render_leaves(STORY_LEAVES)

    # The card itself now lives in components.article_card (Ahmed, 2026-08-20)
    # so the blog index and the related rail render the identical card; the
    # posts come from _posts.POSTS, which is also what those pages read — the
    # homepage teaser and the blog can no longer drift apart.
    articles_html = "".join(
        article_card(p["image"], p["tags"], p["meta"], p["title"], p["excerpt"],
                     href=f"blog.html?post={p['slug']}", rail=True)
        for p in POSTS[:3]
    )

    faq_rows = "".join(
        f"""
              <div class="faq-card accordion-item rounded-2xl overflow-hidden{' is-open' if i == 0 else ''}">
                <button type="button" class="accordion-trigger flex justify-between items-center gap-4 p-6 w-full text-start">
                  <span class="faq-q text-lg leading-snug">{e(q)}</span>
                  <span class="place-items-center grid size-6 text-greenDeep shrink-0">
                    <span class="faq-plus w-5 h-5">{ICON['plus']}</span>
                    <span class="faq-minus w-5 h-5">{ICON['minus']}</span>
                  </span>
                </button>
                <div class="accordion-panel">
                  <div class="px-6 pb-6 text-bodyMuted text-[15px] leading-[1.6]">{e(a)}</div>
                </div>
              </div>"""
        for i, (q, a) in enumerate(FAQS)
    )

    review_cards = "".join(
        f"""
              <!-- bg-greenDeep, NOT the one-off #008536 it used to carry
                   (Ahmed, 2026-08-25). Two things were wrong with the arbitrary
                   hex. It failed contrast: the role line was 3.56:1 and the
                   quote glyph 2.27:1, and the body text "passed" at 4.51:1,
                   which is not passing, it is sitting exactly on the 4.5 line.
                   And being an arbitrary Tailwind value it matched none of the
                   variant overrides, so the card stayed the same bright green
                   in Moss while everything around it changed. The token fixes
                   both at once — 7.06:1 body, 5.58:1 role, 3.44:1 glyph on
                   #006328, and it follows the switcher. -->
              <article data-review-card class="flex flex-col gap-6 bg-greenDeep shrink-0 snap-start p-8 rounded-2xl w-[86%] sm:w-[47%] lg:w-[calc((100%-40px)/3)] h-[320px] carousel-slide">
                <span class="font-bold text-limeFigma text-[72px] leading-none opacity-90" aria-hidden="true">&ldquo;</span>
                <p class="flex-1 text-cream text-base leading-[1.5] overflow-hidden">{e(text)}</p>
                <div class="flex flex-col gap-1">
                  <p class="font-bold text-cream text-base">- {e(name)}</p>
                  <p class="text-[#BDEAC1] text-sm">{e(role)}</p>
                </div>
              </article>"""
        for text, name, role in REVIEWS
    )

    body = f"""
      <!-- ============================== HERO ============================== -->
      <!-- Figma node 9943:16468. Full-bleed banner: photographic background
           (products right), text block left, scalloped white bottom edge
           (the 'Union' shape). One static hero, no carousel. -->
      <section id="hero" class="relative bg-white w-full">
        <h1 class="sr-only">JAAD — Natural Coffee, Nuts &amp; Spices</h1>
        <div class="relative w-full">
          <!-- Language + device aware hero (Ahmed, 2026-08-19). Four sources:
               the product cluster sits on the side OPPOSITE the (side-aligned)
               headline, so EN (text left) uses products-right and AR (text right,
               RTL) uses products-left; desktop is wide, phone is a TALL portrait
               so the banner never squishes on mobile. styles.css (.hero-pic) shows
               exactly ONE via html[dir] + the sm breakpoint — no JS, no flash. -->
          <img src="images/jaad/site/hero-figma.jpg" fetchpriority="high"
               alt="Jaad natural snacks — nuts, coffee and spices"
               class="hero-pic hero-pic--en-desktop w-full aspect-[1512/728] max-h-[82vh] object-cover" />
          <img src="images/jaad/site/hero-ar-desktop.jpg" alt="" aria-hidden="true"
               class="hero-pic hero-pic--ar-desktop w-full aspect-[1512/728] max-h-[82vh] object-cover" />
          <img src="images/jaad/site/hero-en-mob.jpg" alt="" aria-hidden="true" loading="lazy"
               class="hero-pic hero-pic--en-mobile w-full aspect-[3/4] object-cover" />
          <img src="images/jaad/site/hero-ar-mob.jpg" alt="" aria-hidden="true" loading="lazy"
               class="hero-pic hero-pic--ar-mobile w-full aspect-[3/4] object-cover" />
          <div class="absolute inset-x-0 top-0 sm:inset-y-0 flex flex-col justify-start sm:justify-center items-start gap-3 sm:gap-4 md:gap-5 pt-[16%] sm:pt-0 ps-6 md:ps-10 xl:ps-[60px] pe-4 max-w-[80%] sm:max-w-[62%]">
            <div class="flex flex-col items-start isolate">
              <span class="z-[2] -mb-2 -rotate-2 inline-flex items-center bg-limeFigma px-2.5 pb-1 sm:pb-0 rounded-tl-[20px] rounded-br-[20px] font-normal text-heading text-[28px] md:text-[36px] xl:text-[42px] leading-none tracking-[-0.21px]">Natural Snacks</span>
              <span class="z-[1] inline-flex items-center whitespace-nowrap bg-white px-2.5 pt-1.5 sm:pt-0 pb-1 rounded-[12px] font-bold text-[#333] text-[34px] md:text-[50px] xl:text-[62px] leading-[1.15] sm:leading-[1.2]">For Every Event</span>
            </div>
            <a href="shop.html" class="inline-flex items-center gap-2.5 bg-cta hover:bg-cta-hover px-6 py-3 rounded-[8px] font-medium text-white text-base transition-colors">
              Shop Now
              <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
          <!-- Trust badge (Ahmed, 2026-08-25). A ring of type turning around a
               3D mark, parked on the side OPPOSITE the headline and low in the
               frame. inset-inline-end rather than right, so it swaps sides on
               its own in RTL and stays clear of the Arabic headline.

               The centre is spec-shield.png — the existing clay shield-with-a-
               check from the product specs. It is already a 320x320 cut-out in
               the brand greens, it reads as a guarantee, and it is not a leaf.
               No new asset needed.

               aria-hidden: the ring repeats a claim the page makes in real text
               elsewhere, and a screen reader would otherwise read the phrase
               twice around the circle. -->
          <div class="hero-badge" data-hero-badge aria-hidden="true">
            <span class="hero-badge__disc"></span>
            <svg class="hero-badge__ring" data-i18n viewBox="0 0 200 200" focusable="false">
              <defs>
                <!-- Two arcs, not one circle: a single `a` arc of 360 degrees
                     is degenerate and several engines refuse to lay text on it. -->
                <path id="hero-badge-arc" fill="none"
                      d="M100,100 m-72,0 a72,72 0 1,1 144,0 a72,72 0 1,1 -144,0" />
              </defs>
              <!-- textLength pins the run to the arc's own length (452 user
                   units) so the ring CLOSES in both languages instead of
                   leaving a gap or overrunning itself. Arabic measures 402 and
                   English 520 at the same size, so no single font-size fits
                   both. lengthAdjust="spacing" rather than spacingAndGlyphs:
                   it moves the letters apart or together without scaling the
                   glyphs, which matters for the Arabic, whose joining would
                   distort visibly if the shapes were stretched. -->
              <text><textPath href="#hero-badge-arc" startOffset="0" textLength="446" lengthAdjust="spacing">منتجات طبيعية • بدون إضافات • منتجات طبيعية • بدون إضافات • </textPath></text>
            </svg>
            <img src="images/jaad/icons/spec-shield.png" alt="" class="hero-badge__icon" />
          </div>

          <!-- Scalloped white bottom edge (Figma 'Union', fill #fff). Made wider
               than the hero and centred so the flat end-caps sit off-screen —
               only the seamless scallops show, with no cut at either edge. -->
          <img src="images/jaad/site/hero-wave.svg" alt="" aria-hidden="true"
               class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[112%] max-w-none h-[28px] md:h-[45px]" />
        </div>
      </section>

      <!-- ==================== EXPLORE JAAD'S CATEGORIES ==================== -->
      <!-- Figma node 9950:18205. Three category cards; each is a pair of
           product cutouts that fan apart on hover. -->
      <section id="categories" class="bg-white py-14 xl:py-[60px]">
        <div class="flex flex-col items-center gap-10 xl:gap-[54px] mx-auto px-4 max-w-[1512px]">
          <h2 class="font-medium text-black text-[28px] md:text-[40px] text-center leading-[1.2]">
            Explore <span class="font-bold text-heading">JAAD&rsquo;s</span> Categories
          </h2>
          <div class="justify-items-center gap-12 xl:gap-[58px] grid grid-cols-1 sm:grid-cols-3 w-full max-w-[1392px]">{cards}
          </div>
        </div>
      </section>

      <!-- ============================ PERFECT PICKS ============================ -->
      <!-- Figma node 9946:16770. Heading + segmented pill tabs on the same row,
           then a row of five product widgets per tab. -->
      <section id="perfect-picks" class="bg-cream py-14 xl:py-[60px]">
        <div data-tabs class="flex flex-col gap-8 xl:gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-wrap justify-between items-end gap-4">
            <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">Perfect Picks</h2>
            <div class="pp-tabs relative inline-flex items-center gap-1 bg-greenTintSoft p-1 rounded-full"><span data-tab-indicator aria-hidden="true"></span>{pp_chips}</div>
          </div>
{pp_panels}
        </div>
      </section>

      <!-- ============================== REVIEWS ============================== -->
      <!-- Figma node 9950:17989. Dark-green band, medium-green cards with a lime
           quote mark, slider with bottom-right arrows, scattered leaves. -->
      <section id="reviews" class="relative bg-greenDeepest overflow-hidden">
        <div class="relative flex flex-col items-center gap-10 mx-auto px-4 xl:px-[60px] py-16 xl:py-20 max-w-[1512px]">
          {render_leaves(REVIEW_LEAVES, dark=True)}
          <h2 class="z-10 relative font-medium text-greenTint text-[32px] md:text-[40px] text-center tracking-[-0.2px]">Customer Reviews</h2>
          <div class="z-10 relative w-full carousel" style="--carousel-gap:20px">
            <div class="carousel-track">{review_cards}
            </div>
            <div class="flex justify-end gap-4 mt-8">
              <button type="button" class="place-items-center grid bg-white hover:bg-white/90 shadow-custom4 rounded-full size-[42px] text-greenDeepest transition carousel-prev" aria-label="Previous">
                <svg viewBox="0 0 24 24" fill="none" class="w-[18px] h-[18px]"><path d="M14 6l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
              <button type="button" class="place-items-center grid bg-white hover:bg-white/90 shadow-custom4 rounded-full size-[42px] text-greenDeepest transition carousel-next" aria-label="Next">
                <svg viewBox="0 0 24 24" fill="none" class="w-[18px] h-[18px]"><path d="M10 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================== OUR STORY ============================== -->
      <!-- Figma node 9943:16606. Cap (logo, heading, copy, link) + a rounded
           three-column image banner with gradient captions; scattered leaves. -->
      <section id="our-story" class="relative bg-cream py-14 xl:py-[60px] overflow-hidden">
        <div class="relative flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="relative">{story_leaves}
            <div class="relative z-10 flex flex-col gap-6 max-w-[502px]">
              <div class="flex flex-col gap-2">
                <img src="images/jaad/brand/logo-jaad-mark.svg" alt="JAAD" class="w-[84px] xl:w-[112px] h-auto" />
                <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">Our Story</h2>
              </div>
              <p class="text-black text-base leading-[1.4]">At JAAD, we carefully select the finest natural products from their original sources to deliver a pure and authentic experience.</p>
              <a href="about.html" class="group/link inline-flex items-center gap-2 w-fit font-normal text-greenDeep text-base">
                Read More
                <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4 transition-transform group-hover/link:translate-x-1"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </a>
            </div>
          </div>
          <div class="relative z-10 grid grid-cols-1 md:grid-cols-3 rounded-[20px] overflow-hidden md:h-[540px]">{story_cols}
          </div>
        </div>
      </section>

      <!-- =========================== RECENTLY VIEWED =========================== -->
      <!-- Figma node 9946:16842. Filled client-side from localStorage
           (scripts.js initRecentlyViewed), padded from real products to five so
           it is never sparse. -->
      <section id="recently-viewed" class="bg-white py-14 xl:py-[60px]" data-recently-viewed data-recent-min="5">
        <div class="flex flex-col gap-8 xl:gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">Recently Viewed</h2>
          <div data-recent-track class="flex xl:justify-between gap-4 xl:gap-0 -mx-4 xl:mx-0 px-4 xl:px-0 scroll-pl-4 xl:scroll-pl-0 overflow-x-auto xl:overflow-visible no-scrollbar snap-x"></div>
        </div>
      </section>

      <!-- ========================= LATEST FROM JAAD ========================= -->
      <!-- Figma node 9974:21059. Media Center badge, heading + explore link,
           three article cards with tag pills and read-time meta. -->
      <section id="latest" class="bg-cream py-14 xl:py-[60px]">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-col gap-3">
            <span class="self-start bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-greenDeep text-[13px] uppercase tracking-[1px]">Media Center</span>
            <div class="flex flex-wrap justify-between items-end gap-4">
              <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-none tracking-[-1px]">Latest From JAAD</h2>
              <a href="blogs.html" class="group/link inline-flex items-center gap-2 font-bold text-heading text-base">
                Explore All Articles
                <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4 transition-transform group-hover/link:translate-x-1"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </a>
            </div>
          </div>
          <!-- Phone: ONE horizontal scroller (Ahmed, 2026-08-20) — three
               full-width stacked cards pushed the FAQ far down the page and
               read as a dead end. From md up it is the Figma 3-up grid. The
               negative margin + padding let the slides bleed to the screen
               edge while the first one still lines up with the section. -->
          <div class="flex md:grid md:grid-cols-3 gap-6 -mx-4 md:mx-0 px-4 md:px-0 overflow-x-auto md:overflow-visible no-scrollbar snap-x scroll-pl-4">{articles_html}
          </div>
        </div>
      </section>

      <!-- =============================== FAQ =============================== -->
      <!-- Figma node 9967:21115. Centered header + accordion; first row open. -->
      <!-- White band, not cream (Ahmed, 2026-08-23): the FAQ cards themselves
           are cream now — the same surface as the product page's specs strip —
           so a cream section behind them would leave the rows invisible until
           you hovered one. The band above and below is already white, so this
           simply lets the cards be the only shape on it. -->
      <section id="faq" class="py-14 xl:py-[60px]">
        <div class="flex flex-col items-center gap-10 mx-auto px-4 max-w-[1512px]">
          <div class="flex flex-col items-center gap-4 max-w-[800px] text-center">
            <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">Frequently Asked Questions</h2>
            <p class="max-w-[630px] text-bodyMuted text-base leading-[1.5]">Have questions about our premium coffee, fresh Mediterranean nuts, or natural spices? Find quick answers below.</p>
          </div>
          <div data-accordion class="flex flex-col gap-4 w-full max-w-[800px]">{faq_rows}
          </div>
        </div>
      </section>"""

    return page(
        "جاد — قهوة ومكسرات وبهارات طبيعية",
        "تسوق أونلاين من جاد: قهوة طازة، مكسرات وبهارات طبيعية — بأفضل الأسعار وتوصيل لكل مصر.",
        body, "home", "/",
    )
