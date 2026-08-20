"""
Rewards — the nav links to /rewards; without this page the route would fall
through to index.html.

PLACEHOLDER (Ahmed, 2026-08-17): before the fork, this page's H1 and hero
image were scraped verbatim from Abu Auf's real live /rewards page — real
Abu Auf content, not Jaad's. Replaced with a generic heading. Everything
else stays deliberately minimal — the page routes honestly and links to the
account points area that already exists, rather than inventing a rewards
programme Jaad hasn't described.
"""
from components import button, page, page_header

SLUG = "rewards.html"

HEADING = "اجمع نقاط مع كل عملية شراء من جاد"


def build():
    body = f"""{page_header("المكافآت", [("الرئيسية", "index.html"), ("المكافآت", None)])}

      <section class="py-8">
        <div class="flex flex-col gap-8 mx-auto px-4 max-w-[1536px]">
          <!-- Was images/jaad/rewards-hero.webp until 2026-08-20 — an inherited
               path with no file behind it (and at the wrong level: every other
               site asset lives under images/jaad/site/), so this rendered
               broken. Uses Jaad's own hero art until rewards art is delivered. -->
          <img src="images/jaad/site/hero-jaad.webp" alt="{HEADING}"
               class="rounded-[20px] w-full max-h-[420px] object-cover" />

          <div class="flex flex-col gap-4 max-w-[820px]">
            <h2 class="font-bold text-[#003616] text-2xl xl:text-3xl leading-tight">{HEADING}</h2>
            <p class="text-neutral-800 text-base xl:text-lg leading-9">
              اجمع نقاطك مع كل طلب من جاد، وتابع رصيدك ومستوى عضويتك من صفحة النقاط
              في حسابك.
            </p>
          </div>

          <div class="flex flex-wrap gap-3">
            {button("نقاطي", "my-account-point.html", "primary", "md")}
            {button("محفظتي", "my-account-wallet.html", "secondary", "md")}
          </div>
        </div>
      </section>"""

    return page("المكافآت | جاد",
                "اجمع نقاط مع كل طلب من جاد وتابع رصيدك ومستوى عضويتك.",
                body, "rewards", "/rewards")
