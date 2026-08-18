"""Single post — Figma 'Blog Single' (973:38801)."""
from _posts import POSTS
from catalog import e
from components import blog_card, page, page_header, section_heading

SLUG = "blog.html"

PARAGRAPHS = [
    "المكسرات من أقدم الأطعمة اللي عرفها الإنسان، ولحد النهارده فضلت واحدة من أغنى "
    "المصادر الطبيعية للدهون الصحية والبروتين والألياف. الدراسات بتشير إن تناول حفنة "
    "صغيرة يومياً بيرتبط بتحسن في صحة القلب ومستويات الكوليسترول.",
    "الفرق بين المكسرات النيئة والمحمصة مش بس في الطعم. التحميص على درجات حرارة عالية "
    "ممكن يقلل نسبة بعض الفيتامينات الحساسة للحرارة، وعشان كده بنحمص على دفعات صغيرة "
    "وبدرجات محسوبة تحافظ على القيمة الغذائية والنكهة في نفس الوقت.",
    "أحسن طريقة تدخل بيها المكسرات في يومك إنك تخليها في متناول إيدك — علبة صغيرة على "
    "المكتب أو في شنطة الشغل. جربها كمان فوق الزبادي أو السلطة، أو اطحنها وحطها في "
    "العجين للمخبوزات.",
]

TIPS = ["ابدأ بكمية صغيرة — حفنة يومياً كفاية",
        "نوّع بين اللوز والكاجو وعين الجمل عشان تنوع العناصر",
        "احفظها في برطمان محكم بعيد عن الحرارة والضوء"]


def build():
    slug, img, tag, heading, excerpt, read = POSTS[0]
    related = "".join(blog_card(i, t, h, x, "blog.html")
                      for _s, i, t, h, x, _r in POSTS[1:4])

    paras = "".join(f'<p class="text-neutral-800 text-base xl:text-lg leading-9">{e(p)}</p>'
                    for p in PARAGRAPHS)
    tips = "".join(f'<li>{e(t)}</li>' for t in TIPS)

    body = f"""{page_header("", [("الرئيسية", "index.html"), ("البلوج", "blogs.html"), (heading, None)])}

      <article class="py-6">
        <div class="flex flex-col gap-6 mx-auto px-4 xl:px-10 max-w-[880px]">
          <div class="flex flex-wrap items-center gap-3">
            <span class="bg-interaction-base px-3 py-1 rounded-full font-semibold text-primary text-xs">{e(tag)}</span>
            <span class="text-neutral-secondary text-xs">قراءة {e(read)}</span>
          </div>
          <h1 class="font-bold text-[#003616] text-3xl xl:text-4xl leading-tight">{e(heading)}</h1>
          <p class="text-neutral-secondary text-base xl:text-lg leading-8">{e(excerpt)}</p>
          <div class="rounded-[20px] overflow-hidden">
            <img src="{e(img)}" alt="{e(heading)}" class="w-full h-[260px] xl:h-[420px] object-cover" />
          </div>
          {paras}
          <div class="flex flex-col gap-3 bg-interaction-base p-6 rounded-2xl">
            <h2 class="font-bold text-[#003616] text-lg">نصائح سريعة</h2>
            <ul class="flex flex-col gap-2 ps-5 text-neutral-800 text-base leading-8 list-disc">{tips}</ul>
          </div>
        </div>
      </article>

      <section class="py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("مقالات ذات صلة", "كل المقالات", "blogs.html")}
          <div class="gap-6 xl:gap-8 grid md:grid-cols-2 lg:grid-cols-3">{related}
          </div>
        </div>
      </section>"""

    return page(f"{heading} | جاد", excerpt, body, "blog", "/blog")
