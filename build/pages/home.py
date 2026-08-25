"""Home page — Figma node 9943:16397 (Jaad-Ecommerce file)."""
from _posts import POSTS
from pathlib import Path

from catalog import PRODUCTS, e, home_categories, rail_products, category
from components import (
    # `carousel` and `review_card` went with the reviews rebuild (2026-08-25) —
    # that section no longer uses the generic carousel, and the card is authored
    # here. NOTE for whoever is next: category_tile, product_card and
    # section_heading were already unused before that change and are left alone
    # rather than swept up in an unrelated edit.
    ICON, article_card, button, category_tile, page,
    product_card, product_widget, section_heading,
)

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}

# Our Story — four steps of one journey, shown as a progressive carousel:
# a single large photograph with a glass control bar of four steps across its
# foot (Ahmed, 2026-08-25). (image, title, copy).
#
# The photography is NEW and generated (Higgsfield / Recraft V4.1, 2026-08-25),
# because this section changed shape: it used to be three tiles reusing the
# product-scene shots, and one wide frame per step needs pictures composed for
# a wide frame. Deliberately INGREDIENT and PROCESS photography with no
# packaging in it — a generated shot of a JAAD bag would be inventing product
# photography, while a basket of coffee cherries is illustrating a claim the
# site already makes in words.
#
# The copy says nothing new either: sourcing, no additives and no middlemen are
# all claims the hero, the about page and the specs strip already carry. Same
# standing as the rest of the section's English — in-house, pending client
# sign-off (DESIGN-NOTES).
STORY_COLUMNS = [
    ("story-source.jpg", "From The Source",
     "Picked at the farm, in the part of the season the crop is actually ready."),
    ("story-roast.jpg", "Roasted With Care",
     "Small batches, watched from first crack to the exact colour we want."),
    ("story-pantry.jpg", "Nuts And Spices",
     "Whole nuts and ground spices, cleaned and packed with nothing added."),
    ("story-table.jpg", "To Your Table",
     "Sealed fresh and sent straight to you, with no middlemen in between."),
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


def _seal_face():
    """The seal's FACE half, inlined rather than an <img> (Ahmed, 2026-08-25:
    "in the moss version change the color of this badge").

    The disc's #98CA55 is baked into the exported SVG, and an external <img>'s
    fills are beyond CSS's reach — so as long as the face was a file, every
    palette got the same lime disc, and in Moss that is now the BUTTON colour,
    which the badge system says a badge must not share. Inlining at build time
    turns the disc into a normal styleable element: the path keeps its exported
    fill as the value every palette but Moss uses, and gains .seal-disc for the
    variant sheet to repaint (see html[data-btn="v3"] .seal-disc in styles.css).

    Read at build time so the artwork stays one source file — an edited export
    dropped into images/jaad/brand/ flows into the page on the next build."""
    svg_path = Path(__file__).resolve().parents[2] / "static-export/images/jaad/brand/badge-jaad.svg"
    svg = svg_path.read_text(encoding="utf-8")
    assert 'fill="#98CA55"' in svg, "badge-jaad.svg lost its disc fill - re-check the export"
    svg = svg.replace('fill="#98CA55"', 'class="seal-disc" fill="#98CA55"', 1)
    return svg.replace("<svg ", '<svg class="hero-badge__face" ', 1).strip()


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
        # 2xl, not xl (Ahmed's audit, 2026-08-25): the rail stops scrolling and lays
        # its five cards out side by side — but five 258px cards plus the page's
        # 60px gutters need 1410px, and xl is 1280. Between 1280 and 1410 the
        # fifth card was clipped by <main>'s overflow-x-clip with NO scrollbar to
        # reach it — invisible, unreachable stock. 2xl (1536) is the first stop
        # in the scale where the row genuinely fits (1536-120=1416 >= 1410).
        f'<div class="flex 2xl:justify-between gap-4 2xl:gap-0 -mx-4 2xl:mx-0 px-4 2xl:px-0 scroll-pl-4 2xl:scroll-pl-0 '
        f'overflow-x-auto 2xl:overflow-visible no-scrollbar snap-x">{pp_widgets(ids, disc)}'
        f'</div></div>'
        for i, (key, _label, ids, disc) in enumerate(PERFECT_PICKS)
    )

    # Three photographic tiles. Two things were wrong with them (Ahmed,
    # 2026-08-25) and they share a cause: the scrim.
    #
    # 1. "the small text is weak and hard to read". The copy was white/90 over a
    #    `from-transparent to-black/50` wash — a gradient that reaches its
    #    darkest at the very bottom edge and is still only half black when it
    #    gets there. The text sits 32px UP from that edge, so it was reading
    #    against roughly 45% black over photography that is bright in two of the
    #    three tiles (the spice bowls, the wheat field). Now the ramp runs from
    #    the BOTTOM up and lands at 88% black under the words, which is a real
    #    surface rather than a tint, and the copy is full white on it.
    # 2. "I want a mouse hover animation here". The tiles were the only
    #    photographic block on the page that did nothing on hover, while the
    #    category cards right above them fan apart. So: a slow push-in on the
    #    photograph (1.07, 900ms — a drift, not a pop), the scrim deepening with
    #    it, and the copy block rising 4px to meet it. The push-in is why the
    #    tile keeps `overflow-hidden`; the image is `inset-0` on a clipped box,
    #    so it can never leave its frame.
    # A PROGRESSIVE CAROUSEL (Ahmed, 2026-08-25), replacing the expanding panel
    # set: "replace the current our story section with [21st.dev
    # uilayout/progressive-carousel]".
    #
    # Same situation as the testimonials: that component is a React/shadcn
    # registry item behind an authenticated endpoint, and this project is
    # generated static HTML with no React to add it to — so this is its layout
    # and behaviour rebuilt here. One large photograph, and a glassmorphic bar
    # of four steps across its foot; picking a step brings its photograph
    # forward. The bar is two columns on phones and four from md, which is the
    # component's own responsive shape.
    #
    # <button>, because choosing a step is an action and has to be reachable
    # from the keyboard; aria-pressed is what says which one is showing.
    story_shots = "".join(
        f"""
                <img src="images/jaad/site/{img}" alt="{e(title)}"
                     class="pcar__shot{' is-on' if i == 0 else ''}" data-pcar-shot data-index="{i}"
                     {'fetchpriority="high"' if i == 0 else 'loading="lazy"'} />"""
        for i, (img, title, _copy) in enumerate(STORY_COLUMNS)
    )
    story_steps = "".join(
        f"""
                <button type="button" class="pcar__btn{' is-on' if i == 0 else ''}"
                        data-pcar-btn data-index="{i}" aria-pressed="{'true' if i == 0 else 'false'}">
                  <span class="pcar__num latin" aria-hidden="true">0{i + 1}</span>
                  <span class="pcar__btnTitle">{e(title)}</span>
                  <span class="pcar__btnDesc">{e(copy)}</span>
                  <span class="pcar__bar" aria-hidden="true"></span>
                </button>"""
        for i, (_img, title, copy) in enumerate(STORY_COLUMNS)
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
                  <span class="faq-toggle place-items-center grid size-6 shrink-0">
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

    # A STAGGERED FAN (Ahmed, 2026-08-25), replacing the deck this section
    # carried for about an hour: "replace the current testimonial section with
    # [21st.dev stagger-testimonials] ... light mode ... and change the corner
    # radius to be suitable for us".
    #
    # WHAT THIS IS AND IS NOT. That component is a React/shadcn registry item and
    # its source is behind an authenticated endpoint, so `npx shadcn add` could
    # not fetch it here — and this project has no React to add it to; it is
    # Python-generated static HTML with one hand-written stylesheet. So this is
    # its LAYOUT AND BEHAVIOUR rebuilt in the stack that exists: the cards fan
    # out either side of a centred, lifted, highlighted one, each neighbour
    # stepped further out and tilted the opposite way, and moving the fan slides
    # every card one place along. Light ground, and the corners are the site's
    # own 12px rather than the component's.
    #
    # The avatar stays the reviewer's INITIALS. The original shows a photograph
    # per testimonial; we have no photographs of these people, and generating
    # faces for named customers is inventing evidence, not styling.
    def _initials(nm):
        parts = [w for w in nm.split() if w]
        return (parts[0][:1] + (parts[-1][:1] if len(parts) > 1 else "")).upper()

    review_cards = "".join(
        f"""
                <article data-rv-card data-index="{i}" class="rv__card">
                  <span class="rv__quote" aria-hidden="true">&ldquo;</span>
                  <p class="rv__text">{e(text)}</p>
                  <div class="rv__who">
                    <span class="rv__avatar latin" aria-hidden="true">{e(_initials(name))}</span>
                    <span class="rv__whoText">
                      <span class="rv__name">{e(name)}</span>
                      <span class="rv__role">{e(role)}</span>
                    </span>
                  </div>
                </article>"""
        for i, (text, name, role) in enumerate(REVIEWS)
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
              <span data-hero-kicker class="z-[2] -mb-2 -rotate-2 inline-flex items-center bg-limeFigma px-2.5 pb-1 sm:pb-0 rounded-tl-[20px] rounded-br-[20px] font-normal text-heading text-[28px] md:text-[36px] xl:text-[42px] leading-none tracking-[-0.21px]">Natural Snacks</span>
              <span data-hero-title class="z-[1] inline-flex items-center whitespace-nowrap bg-white px-2.5 pt-1.5 sm:pt-0 pb-1 rounded-[12px] font-bold text-[#333] text-[34px] md:text-[50px] xl:text-[62px] leading-[1.15] sm:leading-[1.2]">For Every Event</span>
            </div>
            <!-- Roughly twice the button it was (Ahmed, 2026-08-25: "2x
                 larger"). 24/40px padding against 12/24, 22px type against 16,
                 and a 24px chevron against 16 — about double the footprint, and
                 the corner goes 8 -> 12 so the radius keeps its proportion to
                 the box rather than tightening as the box grows. It stays a
                 step smaller on phones, where the hero copy is already at
                 max-w-[80%] and a 74px-tall button would own the frame. -->
            <a href="shop.html" class="inline-flex items-center gap-3 bg-cta hover:bg-cta-hover px-7 sm:px-10 py-4 sm:py-5 rounded-[12px] font-medium text-white text-[18px] sm:text-[22px] transition-colors">
              Shop Now
              <svg viewBox="0 0 24 24" fill="none" class="w-5 sm:w-6 h-5 sm:h-6"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
          <!-- Trust seal (Ahmed, 2026-08-25). The supplied BADGE.svg — a lime
               disc reading 100% NATURAL, ringed by a repeating NATURAL PRODUCTS
               legend — replacing the cream disc + 3D teapot this carried before.

               It ships as TWO files split out of that one export: badge-jaad.svg
               is the disc and the centre lockup, badge-jaad-ring.svg is the ring
               legend on a transparent ground. They share the same 588 viewBox,
               so stacking them reassembles the artwork exactly, and splitting is
               what lets the ring turn on scroll (initHeroBadge, unchanged) while
               the centre stays upright — a seal with a moving legend rather than
               a spinning sticker, which is the behaviour this badge already had.

               NOTE: the old ring was LIVE TEXT with data-i18n, so it read in
               Arabic on the Arabic site. This artwork has the legend as outlined
               paths in English only, so it no longer switches with the language.
               That is a property of the asset, not of this markup — an Arabic
               cut of the ring file would drop straight in beside it.

               aria-hidden: the legend repeats a claim the page already makes in
               real text, and a screen reader would otherwise read the phrase
               once per repetition around the circle. -->
          <div class="hero-badge" data-hero-badge aria-hidden="true">
            {_seal_face()}
            <img src="images/jaad/brand/badge-jaad-ring.svg" alt="" class="hero-badge__ring" />
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
      <!-- LIGHT now, and a staggered fan — see review_cards above for what this
           is a rebuild of and why it is not an npx install. The band was a dark
           green slab; on cream the cards themselves carry the section and the
           centred one is the only saturated thing in it. -->
      <section id="reviews" class="rv relative bg-cream overflow-hidden" data-reviews>
        <div class="relative flex flex-col items-center gap-8 mx-auto px-4 xl:px-[60px] py-16 xl:py-20 max-w-[1512px]">
          {render_leaves(REVIEW_LEAVES)}

          <div class="z-10 relative flex flex-col items-center gap-3 text-center">
            <span class="rv__kicker">Customer Reviews</span>
            <h2 class="font-medium text-heading text-[32px] md:text-[40px] tracking-[-0.2px]">What People Say About JAAD</h2>
          </div>

          <!-- The fan. Cards are absolutely positioned and placed by --pos,
               --rise and --tilt (initReviewFan writes them; styles.css does the
               arithmetic), so the whole arrangement is one transform per card. -->
          <div class="rv__fan z-10 relative" data-rv-fan tabindex="0" role="group"
               aria-roledescription="carousel" aria-label="Customer reviews">{review_cards}
          </div>

          <div class="rv__controls z-10 relative">
            <button type="button" class="rv__nav" data-rv-prev aria-label="Previous review">
              <svg viewBox="0 0 24 24" fill="none" class="w-[18px] h-[18px]"><path d="M14 6l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <button type="button" class="rv__nav" data-rv-next aria-label="Next review">
              <svg viewBox="0 0 24 24" fill="none" class="w-[18px] h-[18px]"><path d="M10 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
          </div>
        </div>
      </section>

      <!-- ============================== OUR STORY ============================== -->
      <!-- Figma node 9943:16606. Cap (logo, heading, copy, link) + a rounded
           three-column image banner with gradient captions; scattered leaves. -->
      <section id="our-story" class="relative bg-cream py-14 xl:py-[60px] overflow-hidden">
        <div class="relative flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="relative">{story_leaves}
            <!-- data-reveal is the site's own scroll-reveal contract (initReveal
                 + the .js-reveal gate in styles.css), not a new mechanism; the
                 only thing this section adds is the stagger, in .story__cap. -->
            <div class="story__cap relative z-10 flex flex-col gap-6 max-w-[502px]">
              <div class="flex flex-col gap-2" data-reveal>
                <img src="images/jaad/brand/logo-jaad-mark.svg" alt="JAAD" class="w-[84px] xl:w-[112px] h-auto" />
                <h2 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">Our Story</h2>
              </div>
              <p class="text-black text-base leading-[1.4]" data-reveal>At JAAD, we carefully select the finest natural products from their original sources to deliver a pure and authentic experience.</p>
              <a href="about.html" data-reveal class="group/link inline-flex items-center gap-2 w-fit font-normal text-greenDeep text-base">
                Read More
                <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4 transition-transform group-hover/link:translate-x-1"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </a>
            </div>
          </div>
          <!-- data-pcar is the hook initStoryCarousel binds to; one `is-on`
               class drives both the photograph and its step. -->
          <div class="pcar relative z-10" data-pcar>
            <div class="pcar__stage">{story_shots}
            </div>
            <div class="pcar__panel">{story_steps}
            </div>
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
          <!-- 2xl mirrors the Perfect Picks rail above: five 258px cards need 1410px
               and only fit past 1536; below that the strip stays a scroller. -->
          <div data-recent-track class="flex 2xl:justify-between gap-4 2xl:gap-0 -mx-4 2xl:mx-0 px-4 2xl:px-0 scroll-pl-4 2xl:scroll-pl-0 overflow-x-auto 2xl:overflow-visible no-scrollbar snap-x"></div>
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
