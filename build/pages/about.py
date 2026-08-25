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
from components import button, hero_wave, page, page_header

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

# --------------------------------------------------------------------------
# The timeline — the road to Jaad.
#
# THE COPY BELOW IS INVENTED PLACEHOLDER (Ahmed, 2026-08-23) and has to be
# replaced with the company's real milestones before this page goes anywhere
# near a client. It is written to READ finished — real-looking years, a real
# arc — because Ahmed asked for a placeholder that shows the section working
# rather than a row of gaps. That is exactly what makes it dangerous to leave:
# nothing on the rendered page says these dates are made up.
#
# What it is NOT is the fork source's history. The Abu Auf about page shipped a
# real founding year and a real branch count, and this file's header records
# them being deleted rather than reskinned; putting them back under Jaad's name
# would be worse than inventing, because they are true of somebody else. So the
# arc here is generic — sourcing, roasting, range, brand, launch — and the only
# entry that is actually true of Jaad is the last one: the brand launched this
# year.
#
# Replacing it: swap the years and lines, and nothing else has to change. The
# path, the node spacing and the scroll scrub are all generated from the length
# of this list, so adding or removing a milestone just works.
#
# Each milestone: (year, heading, copy, photo).
#
# The photos are the site's own existing art, not new shoots: the orchard and
# the brewing tray from the blog set, and the branded pack shots from the
# homepage story. Chosen so no two rows repeat a subject, and so the finished
# brand only appears on the last row — the launch is what it illustrates.
MILESTONES = [
    ("2016", "من المزرعة",
     "بدأت الحكاية من علاقة مباشرة مع المزارعين — اختيار المحصول من مصدره، "
     "وموسم بعد موسم نتعلم إن الجودة بتبدأ قبل ما المنتج يوصل المصنع بكتير.",
     "article-2.jpg"),
    ("2019", "أول محمصة",
     "افتتحنا أول محمصة خاصة بينا، وبقى التحميص بإيدينا من أول ما نستلم الحبة "
     "لحد ما توصل درجة التحميص اللي إحنا عايزينها بالظبط.",
     "article-1.jpg"),
    ("2022", "المكسرات والبهارات",
     "وسّعنا من القهوة للمكسرات والبهارات، بنفس المبدأ — مصدر معروف، وتشغيل "
     "بنشرف عليه خطوة بخطوة، من غير أي إضافات.",
     "article-3.jpg"),
    ("2024", "فكرة العلامة",
     "بدأنا نشتغل على هوية تجمع ده كله تحت اسم واحد: منتجات طبيعية، واضحة في "
     "مصدرها، وسهل إن أي حد يعرف بالظبط بيشتري إيه.",
     "story-nuts.jpg"),
    ("2026", "إطلاق جاد",
     "من الطبيعة إليك — قهوة ومكسرات وبهارات طبيعية، مصدرها الأصلي في قلب كل "
     "منتج، بتوصلك من غير وسطاء.",
     "story-spices.jpg"),
]

# The meandering vector the milestones hang off, drawn on scroll.
#
# Generated rather than hand-authored so it can never fall out of step with the
# list above: the viewBox is 100 units wide and ROW units tall PER MILESTONE, and
# every node sits at x=50, y=ROW*i + ROW/2 - exactly the centre of its grid row,
# because the row track and the viewBox row are the same 1/N of the same box.
# The SVG stretches with `preserveAspectRatio="none"`, so the two stay locked
# together at any height, and `vector-effect="non-scaling-stroke"` keeps the
# stroke an even 2px while that happens.
#
# Between two nodes the line bows out to alternating sides, which is what makes
# it read as a wandering path rather than a rule. The bow is a cubic whose two
# control points share the offset x, so the curve leaves and rejoins the centre
# line vertically and the joins never kink.
ROW = 100
SWING = 34


def _timeline_path(n):
    """The `d` for the server-rendered timeline vector.

    This is the NO-JS fallback only: scripts.js re-authors the path in pixel
    space from where the node dots actually land, which it has to, because the
    dots move between breakpoints and the dash maths needs a 1:1 viewBox. What
    ships here just has to be the same shape, in a 100-wide viewBox with one ROW
    per milestone.

    It is a Catmull-Rom spline through the same point list the script builds -
    an entry point, then each node with a swung midpoint between consecutive
    ones, then an exit. Splined rather than drawn segment by segment for the
    same reason as the script: every join takes its tangent from its neighbours,
    so no join can come out as a corner - not even the first, which is where a
    straight vertical lead-in used to meet a sideways departure and put a right
    angle on the most visible node on the page (Ahmed, 2026-08-23).
    """
    mid = ROW / 2
    h = ROW * n
    nodes = [(50.0, ROW * i + mid) for i in range(n)]

    pts = [(50 + SWING * 0.5, -h * 0.04)]
    for i, (x, y) in enumerate(nodes):
        pts.append((x, y))
        if i < n - 1:
            bx, by = nodes[i + 1]
            lobe = SWING if i % 2 == 0 else -SWING
            pts.append(((x + bx) / 2 + lobe, (y + by) / 2))
    pts.append((50 - SWING * 0.5, h + h * 0.04))

    # Duplicate the ends so the first and last segments have a neighbour to take
    # their tangent from; /6 is the standard Catmull-Rom to bezier conversion.
    p = [pts[0]] + pts + [pts[-1]]
    d = ["M%g %g" % pts[0]]
    for i in range(1, len(p) - 2):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
        d.append("C%g %g, %g %g, %g %g" % (
            x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6,
            x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6,
            x2, y2))
    return " ".join(d)


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

    # --- the timeline -------------------------------------------------------
    # One <li> per milestone. The node dot is a child of the row rather than of
    # the SVG on purpose: `preserveAspectRatio="none"` scales x and y by
    # different factors, so a <circle> in there would paint as an ellipse. The
    # dot is a CSS circle centred on the same line the path runs down, so it
    # stays round at every width.
    #
    # Rows alternate sides from md up (`is-start` / `is-end`); below that they
    # all sit after the line, which hugs the inline start.
    n_ms = len(MILESTONES)
    milestones = "".join(f"""
                <li class="about-time__row {'is-start' if i % 2 == 0 else 'is-end'}"
                    data-time-row data-index="{i}">
                  <span class="about-time__dot" aria-hidden="true"></span>
                  <div class="about-time__card">
                    <div class="about-time__shot">
                      <img src="images/jaad/site/{e(photo)}" alt="{e(head)}" loading="lazy" />
                    </div>
                    <div class="about-time__text">
                      <span class="about-time__year latin">{e(year)}</span>
                      <h3 class="about-time__heading">{e(head)}</h3>
                      <p class="about-time__copy">{e(copy)}</p>
                    </div>
                  </div>
                </li>""" for i, (year, head, copy, photo) in enumerate(MILESTONES))

    stats = "".join(f"""
              <div class="about-stat" data-stat>
                <span class="about-stat__value latin" data-stat-value="{e(v)}">{e(v)}</span>
                <span class="about-stat__label">{e(label)}</span>
              </div>""" for v, label in STATS)

    # Empty heading: the hero block below carries this page's h1, so page_header
    # would otherwise emit a second one above it.
    body = f"""{page_header("", [("الرئيسية", "index.html"), ("قصتنا", None)])}

      <!-- ============================== HERO ============================== -->
      <!-- FULL BLEED, with the title ON the picture and the homepage's scalloped
           edge handing over to the journey below (Ahmed, 2026-08-23).

           The previous version was a title block with a rounded, inset picture
           under it — a picture ABOUT the page rather than the page itself, and
           it made the one section that should open the story read like a card
           in a list. Full bleed gives the photography the whole width, which is
           what the homepage hero already does, and the scallop is the same
           hand-off shape used there, so the two pages open the same way.

           The scrim is what makes white type legible on a bright cream-and-
           orange packshot: a deep-green wash weighted to the inline start, so it
           is dense under the words and clears by the middle of the frame rather
           than greying the whole picture. -->
      <section class="about-hero">
        <!-- Slow parallax on the hero art (data-about-parallax); a no-op under
             reduced motion, where it simply sits still. -->
        <!-- Its OWN picture, not the homepage banner (Ahmed, 2026-08-23).
             hero-jaad.webp is a packshot line-up: nine bags fanned across the
             frame, which is the right image for a shop front and the wrong one
             here. Under the scrim it turned to clutter, and a page called "from
             nature to you" opening on a product photograph argues against its
             own headline. This is the origin instead - a plantation at golden
             hour, with the sky carrying the title. -->
        <img src="images/jaad/site/hero-about.webp" alt="مزارع جاد"
             class="about-hero__img" data-about-parallax />
        <span class="about-hero__scrim" aria-hidden="true"></span>

        <div class="about-hero__inner mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <span class="self-start bg-[rgba(253,248,241,0.16)] backdrop-blur-sm px-3 py-1 rounded-md font-bold text-white text-[13px] uppercase tracking-[1px]">عن جاد</span>
          <h1 class="font-medium text-white text-[38px] md:text-[64px] xl:text-[76px] leading-[1.02] tracking-[-1.5px]">من الطبيعة إليك</h1>
          <p class="max-w-[520px] text-white/85 text-base xl:text-lg leading-[1.6]">
            قهوة ومكسرات وبهارات طبيعية، مصدرها الأصلي في قلب كل منتج.
          </p>
        </div>

        {hero_wave()}
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

      <!-- ============================= TIMELINE ============================= -->
      <!-- The road to Jaad. The journey above is about WHAT the products are;
           this is about WHEN, so it is a separate section with its own
           mechanic rather than another chapter of the pinned sequence.

           The vector is drawn on scroll: the path ships with its dash array set
           to its own length and its offset at full, i.e. completely undrawn,
           and initAboutTimeline walks the offset to zero as the section passes
           the viewport. A head dot rides the drawn end, and each milestone
           wakes as the line reaches its node. Under reduced motion the CSS
           hands over a fully drawn line and all rows visible. -->
      <section class="about-time" data-about-timeline aria-label="مسيرة جاد">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <!-- CENTRED, and no longer "The Road To JAAD" (Ahmed, 2026-08-25).
               The timeline is the PARENT company's history — the years that run
               up to Jaad rather than Jaad's own — so naming it after Jaad
               described the wrong subject. -->
          <div class="flex flex-col items-center gap-3 text-center">
            <span class="bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-greenDeep text-[13px] uppercase tracking-[1px]">مسيرتنا</span>
            <h2 class="font-medium text-heading text-[28px] md:text-[40px] leading-[1.15] tracking-[-0.5px]">إرث الشركة الأم</h2>
          </div>

          <div class="about-time__body">
            <!-- aria-hidden: the line carries no information the rows do not
                 already carry in text, so it is decoration to a screen reader. -->
            <svg class="about-time__vector" viewBox="0 0 100 {ROW * n_ms}"
                 preserveAspectRatio="none" fill="none" aria-hidden="true" focusable="false">
              <path class="about-time__track" d="{_timeline_path(n_ms)}"
                    stroke="#E3EBD8" stroke-width="1.5" stroke-linecap="round"
                    vector-effect="non-scaling-stroke" />
              <path class="about-time__draw" data-time-path d="{_timeline_path(n_ms)}"
                    stroke="#98CA55" stroke-width="1.5" stroke-linecap="round"
                    vector-effect="non-scaling-stroke" />
            </svg>
            <span class="about-time__head" data-time-head aria-hidden="true"></span>

            <ol class="about-time__rows">{milestones}
            </ol>
            <!-- The run-out. Empty on purpose: it exists to give the body extra
                 height below the last milestone, which the vector's viewBox
                 picks up automatically, so the line has somewhere to travel
                 after the last node instead of stopping dead at it. The head
                 rides it down to the stats (Ahmed, 2026-08-25). -->
            <div class="about-time__tail" aria-hidden="true"></div>
          </div>
        </div>
      </section>

      <!-- ============================== STATS ============================== -->
      <section class="about-stats">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div data-about-stats class="gap-6 grid grid-cols-1 sm:grid-cols-3">{stats}
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
