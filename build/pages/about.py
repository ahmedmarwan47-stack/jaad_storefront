"""About — Figma 'About' (394:24746)."""
from components import page, page_header

SLUG = "about.html"

# PLACEHOLDER (Ahmed, 2026-08-17): this whole page was Abu Auf's real about-us
# copy before the fork — real founding year, real 316-branch/25-governorate
# stats, and a product list (nut butters, dried fruit, "healthy foods") Jaad
# doesn't carry. Replaced with only what's actually true about Jaad: the real
# SKU/category count and the brand manual's real tagline. No founding year,
# no branch count — absence over invention, per CLAUDE.md's own rule.
STATS = [("26", "منتج"), ("3", "فئات منتجات"), ("100%", "طبيعي")]

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
              <div class="flex flex-col items-center gap-1 bg-interaction-base px-4 py-6 rounded-2xl text-center">
                <span class="font-bold text-primary text-3xl latin">{v}</span>
                <span class="text-neutral-secondary text-sm">{label}</span>
              </div>""" for v, label in STATS)

    sections = "".join(f"""
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#003616] text-xl xl:text-2xl">{h}</h2>
              <p class="text-neutral-800 text-base xl:text-lg leading-9">{p}</p>
            </div>""" for h, p in BODY)

    body = f"""{page_header("قصتنا", [("الرئيسية", "index.html"), ("قصتنا", None)])}

      <section class="py-8">
        <div class="mx-auto px-4 max-w-[1536px]">
          <div class="rounded-[20px] overflow-hidden">
            <!-- Was about-hero.webp until 2026-08-20 — a WordPress-media
                 filename inherited from the fork whose file never existed in
                 this repo, so this hero rendered broken. Points at Jaad's own
                 hero photography until dedicated about-page art is delivered. -->
            <img src="images/jaad/site/hero-jaad.webp" alt="جاد" class="w-full h-[280px] xl:h-[460px] object-cover" />
          </div>
        </div>
      </section>

      <section class="pb-10">
        <div class="gap-4 grid grid-cols-2 lg:grid-cols-4 mx-auto px-4 max-w-[1536px]">{stats}
        </div>
      </section>

      <section class="pb-16">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[190px] max-w-[1000px]">{sections}
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
