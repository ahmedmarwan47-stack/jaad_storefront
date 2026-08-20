"""
Rewards — the nav links to /rewards; without this page the route would fall
through to index.html.

PLACEHOLDER (Ahmed, 2026-08-17): before the fork, this page's H1 and hero image
were scraped verbatim from the fork source's real live /rewards page — their
content, not Jaad's. Replaced with a generic heading, and everything it says is
still limited to what the site actually implements: it does NOT invent a rewards
programme Jaad hasn't described.

Rebuilt (Ahmed, 2026-08-20) in the homepage's design language. It was an image,
an h2, a paragraph and two buttons — no card, no panel, no shadow, the plainest
page on the site. The facts it shows are now pulled from _account (the real tier
thresholds and the real points-to-EGP rate the account pages use), so this page
and the points page can no longer disagree about how the programme works.
"""
from _account import POINT_TIERS, POINTS_PER_EGP
from catalog import e
from components import button, page, page_header

SLUG = "rewards.html"

HEADING = "اجمع نقاط مع كل عملية شراء من جاد"

# How it works, in three steps — describing only what the account area really
# does today (earn on orders, watch the balance, spend it at checkout).
STEPS = [
    ("images/jaad/icons/orders-3d.png", "اطلب",
     "اجمع نقاط مع كل طلب تعمله من جاد، من غير أي تسجيل إضافي."),
    ("images/jaad/icons/points-3d.png", "اتابع رصيدك",
     "رصيد نقاطك ومستوى عضويتك بيتحدثوا في صفحة النقاط في حسابك."),
    ("images/jaad/icons/wallet-3d.png", "اصرفها",
     f"كل {POINTS_PER_EGP} نقاط بتساوي جنيه واحد تقدر تستخدمه في طلبك الجاي."),
]


def build():
    steps = "".join(f"""
              <div class="flex flex-col gap-3 bg-white shadow-[0px_8px_8px_rgba(0,0,0,0.03)] p-6 rounded-3xl">
                <img src="{e(img)}" alt="" class="w-14 h-14 object-contain" loading="lazy" />
                <h3 class="font-bold text-[#29612F] text-lg">{e(title)}</h3>
                <p class="text-[#1e2219] text-sm leading-[1.6]">{e(copy)}</p>
              </div>""" for img, title, copy in STEPS)

    # The real tier ladder the account pages use, so the two agree.
    # The unit sits in its OWN span: interpolating it next to the number
    # ("{mn}+ نقطة") produced a unique string per tier that the dictionary
    # could never match, so it stayed Arabic on the English site.
    tiers = "".join(f"""
              <div class="flex justify-between items-center gap-4 px-5 py-4 border-neutral-divider border-b last:border-0">
                <span class="font-bold text-[#29612F] text-base">عضوية {e(label)}</span>
                <span class="flex items-center gap-1 text-[#636959] text-sm">
                  <span class="latin">{mn:,}+</span><span>نقطة</span>
                </span>
              </div>""" for label, mn in POINT_TIERS)

    # Empty heading: the eyebrow block below carries this page's h1.
    body = f"""{page_header("", [("الرئيسية", "index.html"), ("المكافآت", None)])}

      <section class="py-8 xl:py-10">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-col gap-3">
            <span class="self-start bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-[#006328] text-[13px] uppercase tracking-[1px]">المكافآت</span>
            <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-none tracking-[-1px]">{e(HEADING)}</h1>
            <p class="max-w-[630px] text-[#4b5563] text-base leading-[1.6]">
              اجمع نقاطك مع كل طلب من جاد، وتابع رصيدك ومستوى عضويتك من صفحة النقاط في حسابك.
            </p>
          </div>
          <div class="rounded-3xl overflow-hidden">
            <!-- Was images/jaad/rewards-hero.webp until 2026-08-20 — an inherited
                 path with no file behind it (and at the wrong level: every other
                 site asset lives under images/jaad/site/), so this rendered
                 broken. Uses Jaad's own hero art until rewards art is delivered. -->
            <img src="images/jaad/site/hero-jaad.webp" alt="{e(HEADING)}"
                 class="w-full h-[240px] xl:h-[400px] object-cover" />
          </div>
          <div class="flex flex-wrap gap-3">
            {button("نقاطي", "my-account-point.html", "primary", "md")}
            {button("محفظتي", "my-account-wallet.html", "secondary", "md")}
          </div>
        </div>
      </section>

      <section class="bg-[#FDF8F1] py-12 xl:py-14">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <h2 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">إزاي بتشتغل</h2>
          <div class="gap-6 grid grid-cols-1 md:grid-cols-3">{steps}
          </div>
          <div class="flex flex-col gap-6 max-w-[620px]">
            <h2 class="font-medium text-[#29612F] text-[28px] md:text-[32px] leading-[1.2]">مستويات العضوية</h2>
            <div class="flex flex-col bg-white shadow-[0px_8px_8px_rgba(0,0,0,0.03)] rounded-3xl">{tiers}
            </div>
          </div>
        </div>
      </section>"""

    return page("المكافآت | جاد",
                "اجمع نقاط مع كل طلب من جاد وتابع رصيدك ومستوى عضويتك.",
                body, "rewards", "/rewards")
