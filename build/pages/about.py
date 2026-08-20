"""About — 'From nature to you', a scroll-scrubbed journey.

Redesigned (Ahmed, 2026-08-20). The previous version was a token-reskin of the
shape inherited from the fork: hero image, a row of stat boxes, then three
headed paragraphs stacked down the page. Recolouring it did not change that it
was still the fork's page.

This is a different page. The three story beats are no longer paragraphs you
scroll past — they are CHAPTERS in one pinned, scroll-scrubbed sequence, each
paired with the product world it describes. A single circular window stays fixed
at centre while the product worlds travel THROUGH it (coffee -> nuts -> spices),
the chapter copy cross-fades beside it, a progress rail fills, and leaves drift
out on each hand-off.

Deliberately a different MECHANIC from the product page's white-mode story
(which flies a packshot to centre and holds): here the frame is the constant and
the contents move through it. Same motion language and the same leaf vocabulary,
so the two read as one site, without the About page being a copy of the product
page. All of it is scroll-scrubbed CSS/transform work driven by initAboutJourney
in scripts.js, and it degrades to a plain static stack under
prefers-reduced-motion.
"""
from catalog import e
from components import button, page, page_header

SLUG = "about.html"

# PLACEHOLDER (Ahmed, 2026-08-17): this whole page was the fork source's real
# about-us copy — real founding year, real 316-branch/25-governorate stats, and
# a product list (nut butters, dried fruit, "healthy foods") Jaad doesn't carry.
# Replaced with only what's actually true about Jaad: the real SKU/category
# count and the brand manual's real tagline. No founding year, no branch count —
# absence over invention, per CLAUDE.md's own rule.
STATS = [("26", "منتج"), ("3", "فئات منتجات"), ("100%", "طبيعي")]

# The journey. Each chapter: (image, kicker, heading, copy).
# The headings and copy are the page's original three story beats; the images
# are the homepage's Our Story photography, so both pages tell one story with
# one set of pictures.
CHAPTERS = [
    ("story-coffee.jpg", "قهوة", "قصتنا",
     "من الطبيعة إليك — جاد تقدم قهوة ومكسرات وبهارات طبيعية عالية الجودة، "
     "مصدرها الأصلي في قلب كل منتج."),
    ("story-nuts.jpg", "مكسرات", "جودة في كل خطوة",
     "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل "
     "خطوة في عملية الإنتاج في جاد تُدار بعناية لضمان إنتاج منتجات عالية "
     "الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم."),
    ("story-spices.jpg", "بهارات", "نغذي العقل والروح",
     "نعطي الأولوية لابتكار المنتجات ونأخذ في الاعتبار اتجاهات السوق ورغبات "
     "العملاء وتغيُّر الأذواق، كما نشجع دائمًا نمط الحياة الصحي؛ لأن هدفنا ليس "
     "فقط تغذية الجسم، بل تغذية العقل والروح أيضًا."),
]

# Leaves that drift out of the circular window on each chapter hand-off.
# (leaf file, angle in degrees from centre, distance multiplier, width class)
JOURNEY_LEAVES = [
    ("leaf-1.svg", -28, 1.00, "w-12"),
    ("leaf-3.svg", 18, 1.15, "w-16"),
    ("leaf-2.svg", -64, 0.85, "w-9"),
    ("leaf-5.svg", 52, 1.05, "w-10"),
    ("leaf-4.svg", -104, 1.20, "w-11"),
    ("leaf-1.svg", 104, 0.95, "w-8"),
]


def build():
    # --- the pinned journey -------------------------------------------------
    # Every chapter's media and copy ship in the DOM; the JS reveals exactly one
    # at a time from scroll progress. Chapter 0 is marked current so the section
    # is readable before any JS runs (and stays so if it never does).
    media = "".join(f"""
                <img src="images/jaad/site/{e(img)}" alt="{e(head)}"
                     class="about-journey__img{' is-current' if i == 0 else ''}"
                     data-journey-img data-index="{i}" loading="lazy" />"""
                    for i, (img, _k, head, _c) in enumerate(CHAPTERS))

    leaves = "".join(f"""
                <img src="images/jaad/decor/{e(leaf)}" alt="" aria-hidden="true"
                     class="about-journey__leaf {cls} h-auto" data-journey-leaf
                     style="--ang:{ang}deg;--dist:{dist}" />"""
                     for leaf, ang, dist, cls in JOURNEY_LEAVES)

    nodes = "".join(f"""
                  <li class="about-journey__node{' is-current' if i == 0 else ''}" data-journey-node data-index="{i}">
                    <span class="about-journey__node-dot" aria-hidden="true"></span>
                    <span class="about-journey__node-label">{e(kicker)}</span>
                  </li>""" for i, (_img, kicker, _h, _c) in enumerate(CHAPTERS))

    chapters = "".join(f"""
                <article class="about-journey__chapter{' is-current' if i == 0 else ''}" data-journey-chapter data-index="{i}">
                  <span class="about-journey__kicker">{e(kicker)}</span>
                  <h2 class="about-journey__heading">{e(head)}</h2>
                  <p class="about-journey__copy">{e(copy)}</p>
                </article>""" for i, (_img, kicker, head, copy) in enumerate(CHAPTERS))

    stats = "".join(f"""
              <div class="about-stat" data-stat>
                <span class="about-stat__value latin" data-stat-value="{e(v)}">{e(v)}</span>
                <span class="about-stat__label">{e(label)}</span>
              </div>""" for v, label in STATS)

    # Empty heading: the hero block below carries this page's h1, so page_header
    # would otherwise emit a second one above it.
    body = f"""{page_header("", [("الرئيسية", "index.html"), ("قصتنا", None)])}

      <!-- ============================== HERO ============================== -->
      <section class="about-hero">
        <div class="flex flex-col gap-6 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-col gap-3">
            <span class="self-start bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-greenDeep text-[13px] uppercase tracking-[1px]">عن جاد</span>
            <h1 class="font-medium text-heading text-[32px] md:text-[52px] leading-none tracking-[-1px]">من الطبيعة إليك</h1>
            <p class="max-w-[560px] text-bodyMuted text-base xl:text-lg leading-[1.6]">
              قهوة ومكسرات وبهارات طبيعية، مصدرها الأصلي في قلب كل منتج.
            </p>
          </div>
          <!-- Slow parallax on the hero art (data-about-parallax); a no-op
               under reduced motion, where it simply sits still. -->
          <div class="about-hero__frame">
            <img src="images/jaad/site/hero-jaad.webp" alt="جاد"
                 class="about-hero__img" data-about-parallax />
          </div>
        </div>
      </section>

      <!-- ============================ THE JOURNEY ============================ -->
      <!-- A tall spacer whose scroll drives the pinned stage inside it. The
           stage holds ONE circular window; the product worlds travel through
           it while the chapter copy cross-fades beside it. -->
      <section class="about-journey" data-about-journey aria-label="قصة جاد">
        <div class="about-journey__stage">
          <div class="about-journey__inner mx-auto px-4 xl:px-[60px] max-w-[1512px]">

            <div class="about-journey__media" data-journey-media>
              <span class="about-journey__ring" aria-hidden="true"></span>
              <span class="about-journey__progress" data-journey-progress aria-hidden="true"></span>
              <div class="about-journey__window">{media}
              </div>{leaves}
            </div>

            <div class="about-journey__side">
              <ol class="about-journey__rail" data-journey-rail>{nodes}
              </ol>
              <div class="about-journey__chapters">{chapters}
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- ============================== STATS ============================== -->
      <section class="about-stats">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="gap-6 grid grid-cols-1 sm:grid-cols-3">{stats}
          </div>
        </div>
      </section>

      <!-- =============================== CTA =============================== -->
      <section class="about-cta">
        <div class="flex flex-col items-center gap-5 mx-auto px-4 max-w-[720px] text-center">
          <h2 class="font-medium text-heading text-[28px] md:text-[36px] leading-[1.2]">جرب جاد بنفسك</h2>
          <p class="text-bodyMuted text-base leading-[1.6]">
            كل منتج بنقدمه بيعدي بنفس الرحلة — من مصدره لحد ما يوصلك.
          </p>
          <div class="flex flex-wrap justify-center gap-3">
            {button("تسوق الآن", "shop.html", "primary", "md")}
            {button("تواصل معنا", "contact-us.html", "secondary", "md")}
          </div>
        </div>
      </section>"""

    # The description carried "منذ 2010" and "أطعمة صحية" until 2026-08-20 —
    # the founding year and product range this page's own header comment says
    # were removed as the fork source's, not Jaad's.
    return page("قصتنا | جاد",
                "تعرف على قصة جاد — قهوة ومكسرات وبهارات طبيعية عالية الجودة.",
                body, "about", "/about")
