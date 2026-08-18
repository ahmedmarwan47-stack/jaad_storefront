"""Blog index — Figma 'Blog' (937:37091)."""
from _posts import POSTS
from components import blog_card, page, page_header

SLUG = "blogs.html"


def build():
    cards = "".join(blog_card(img, tag, heading, excerpt, "blog.html")
                    for _slug, img, tag, heading, excerpt, _read in POSTS)

    body = f"""{page_header("البلوج", [("الرئيسية", "index.html"), ("البلوج", None)])}

      <section class="py-8 xl:py-10">
        <div class="mx-auto px-4 max-w-[1536px]">
          <p class="mb-10 max-w-[720px] text-neutral-secondary text-base xl:text-lg leading-8">
            نصائح ووصفات ومعلومات عن القهوة والمكسرات والتمور والأكل الصحي — من فريق جاد.
          </p>
          <!-- Restores the level the post cards' h3 skipped; blog_card is
               shared with the home page, where it sits under a real h2. -->
          <h2 class="sr-only">أحدث المقالات</h2>
          <div class="gap-6 xl:gap-8 grid md:grid-cols-2 lg:grid-cols-3">{cards}
          </div>
        </div>
      </section>"""

    return page("البلوج | جاد",
                "نصائح ووصفات ومقالات عن القهوة والمكسرات والتمور والأكل الصحي من جاد.",
                body, "blogs", "/blogs")
