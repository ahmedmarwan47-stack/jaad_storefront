"""Blog index — JAAD Media Center, matching the homepage's 'Latest from JAAD'
section (Figma node 9974:21059).

Rebuilt (Ahmed, 2026-08-20): the page previously rendered the inherited Abu-Auf
blog card — an Arabic horizontal image-beside-text strip — under an Arabic
heading, so following "Explore All Articles" from the homepage landed the
shopper on what looked like a different site. It now uses the SAME shared
`article_card` the homepage rail uses, under the homepage's Media Center badge +
heading treatment.
"""
from _posts import POSTS
from components import article_card, page, page_header

SLUG = "blogs.html"


def build():
    cards = "".join(
        article_card(p["image"], p["tags"], p["meta"], p["title"], p["excerpt"],
                     href=f"blog.html?post={p['slug']}")
        for p in POSTS
    )

    # Empty heading: the Media Center block below carries this page's h1, and
    # page_header would otherwise emit a second one above it.
    body = f"""{page_header("", [("Home", "index.html"), ("Blog", None)])}

      <section class="bg-cream py-10 xl:py-14">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-col gap-3">
            <span class="self-start bg-[rgba(138,204,62,0.13)] px-3 py-1 rounded-md font-bold text-greenDeep text-[13px] uppercase tracking-[1px]">Media Center</span>
            <h1 class="font-medium text-heading text-[32px] md:text-[40px] leading-none tracking-[-1px]">Latest from JAAD</h1>
            <p class="max-w-[630px] text-bodyMuted text-base leading-[1.5]">
              Guides, recipes and notes on coffee, nuts, dates and spices — written by the JAAD team.
            </p>
          </div>
          <div class="gap-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">{cards}
          </div>
        </div>
      </section>"""

    return page("Blog | JAAD",
                "Guides, recipes and articles on coffee, nuts, dates and healthy eating from JAAD.",
                body, "blogs", "/blogs")
