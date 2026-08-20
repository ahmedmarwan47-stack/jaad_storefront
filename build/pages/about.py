"""About — Figma 'About' (394:24746).

Rebuilt (Ahmed, 2026-08-20) in the homepage's design language. It was three
bare stacked <section>s — a hero image, a row of tinted stat boxes and a column
of headed paragraphs — with no cards, no panels and an `xl:px-[190px]` padding
hack found nowhere else on the site. It predated the redesign, so it read as
the plainest page here despite being the brand's own story.

Now: the Media Center-style eyebrow + heading block, a full-bleed hero, stats as
white cards on cream, and the story sections as a picture-led three-up (reusing
the homepage's Our Story column treatment) followed by the prose in a readable
measure. Same copy, same facts — only the presentation changed.
"""
from catalog import e
from components import page, page_header

SLUG = "about.html"

# PLACEHOLDER (Ahmed, 2026-08-17): this whole page was the fork source's real
# about-us copy — real founding year, real 316-branch/25-governorate stats, and
# a product list (nut butters, dried fruit, "healthy foods") Jaad doesn't carry.
# Replaced with only what's actually true about Jaad: the real SKU/category
# count and the brand manual's real tagline. No founding year, no branch count —
# absence over invention, per CLAUDE.md's own rule.
STATS = [("26", "منتج"), ("3", "فئات منتجات"), ("100%", "طبيعي")]

# The three product worlds, reusing the homepage's Our Story photography so the
# two pages tell the same story with the same pictures.
PILLARS = [
    ("story-coffee.jpg", "قهوة", "قهوة تركية محمصة على دفعات صغيرة، بدرجات محسوبة تحافظ على النكهة."),
    ("story-nuts.jpg", "مكسرات", "مكسرات من مصادرها الأصلية، محمصة بعناية وبأقل تدخل ممكن."),
    ("story-spices.jpg", "بهارات", "بهارات طازة تُطحن وتُعبأ بكميات صغيرة عشان تفضل محتفظة بزيوتها."),
]

BODY = [
    ("قصتنا", "من الطبيعة إليك — جاد تقدم قهوة ومكسرات وبهارات طبيعية عالية الجودة، "
              "مصدرها الأصلي في قلب كل منتج."),
    ("جودة في كل خطوة", "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل "
                        "خطوة في عملية الإنتاج في جاد تُدار بعناية لضمان إنتاج منتجات عالية "
                        "الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم."),
    ("نغذي العقل والروح", "نعطي الأولوية لابتكار المنتجات ونأخذ في الاعتبار اتجاهات السوق ورغبات "
                          "العملاء وتغيُّر الأذواق، كما نشجع دائمًا نمط الحياة الصحي؛ لأن هدفنا ليس "
                          "فقط تغذية الجسم، بل تغذية العقل والروح أيضًا."),
]


def build():
    stats = "".join(f"""
              <div class="flex flex-col items-center gap-1 bg-white shadow-[0px_8px_8px_rgba(0,0,0,0.03)] px-4 py-8 rounded-3xl text-center">
                <span class="font-medium text-[#29612F] text-[40px] leading-none latin">{e(v)}</span>
                <span class="text-[#636959] text-sm">{e(label)}</span>
              </div>""" for v, label in STATS)

    # Same picture-led column as the homepage's Our Story band.
    pillars = "".join(f"""
              <div class="relative rounded-3xl min-h-[300px] overflow-hidden">
                <img src="images/jaad/site/{e(img)}" alt="{e(title)}" class="absolute inset-0 w-full h-full object-cover" loading="lazy" />
                <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/55"></div>
                <div class="absolute inset-x-6 bottom-7 flex flex-col gap-2 text-white">
                  <h3 class="font-bold text-2xl leading-tight">{e(title)}</h3>
                  <p class="text-white/90 text-sm leading-[1.5]">{e(copy)}</p>
                </div>
              </div>""" for img, title, copy in PILLARS)

    sections = "".join(f"""
              <div class="flex flex-col gap-3">
                <h2 class="font-medium text-[#29612F] text-[28px] md:text-[32px] leading-[1.2]">{e(h)}</h2>
                <p class="text-[#1e2219] text-base xl:text-lg leading-[1.9]">{e(p)}</p>
              </div>""" for h, p in BODY)

    # Empty heading: the eyebrow block below carries this page's h1, so
    # page_header would otherwise emit a second one above it.
    body = f"""{page_header("", [("الرئيسية", "index.html"), ("قصتنا", None)])}

      <section class="py-8 xl:py-10">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-col gap-3">
            <span class="self-start bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-[#006328] text-[13px] uppercase tracking-[1px]">عن جاد</span>
            <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-none tracking-[-1px]">قصتنا</h1>
            <p class="max-w-[630px] text-[#4b5563] text-base leading-[1.6]">
              من الطبيعة إليك — قهوة ومكسرات وبهارات طبيعية، مصدرها الأصلي في قلب كل منتج.
            </p>
          </div>
          <div class="rounded-3xl overflow-hidden">
            <!-- Was about-hero.webp until 2026-08-20 — a WordPress-media
                 filename inherited from the fork whose file never existed in
                 this repo, so this hero rendered broken. Points at Jaad's own
                 hero photography until dedicated about-page art is delivered. -->
            <img src="images/jaad/site/hero-jaad.webp" alt="جاد" class="w-full h-[280px] xl:h-[460px] object-cover" />
          </div>
        </div>
      </section>

      <section class="bg-[#FDF8F1] py-12 xl:py-14">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="gap-6 grid grid-cols-1 sm:grid-cols-3">{stats}
          </div>
          <div class="gap-6 grid grid-cols-1 md:grid-cols-3">{pillars}
          </div>
        </div>
      </section>

      <section class="py-12 xl:py-14">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[860px]">{sections}
        </div>
      </section>"""

    # The description carried "منذ 2010" and "أطعمة صحية" until 2026-08-20 —
    # the founding year and product range this page's own header comment says
    # were removed as the fork source's, not Jaad's. The body was cleaned then;
    # the meta description was missed, so it kept shipping both to search
    # results and link previews. Now it matches the page: real categories only.
    return page("قصتنا | جاد",
                "تعرف على قصة جاد — قهوة ومكسرات وبهارات طبيعية عالية الجودة.",
                body, "about", "/about")
