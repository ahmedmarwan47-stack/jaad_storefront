"""Single post — JAAD Media Center article.

Rebuilt (Ahmed, 2026-08-20) alongside the blog index: English-first, JAAD type
and color, and a related rail built from the SAME shared `article_card` the
homepage uses. The previous version rendered Arabic Abu-Auf copy against image
paths that do not exist in this repo.

Still ONE static page for every post (the fork ships no per-post routing). The
index links each card with `?post=<slug>`; scripts.js swaps the copy client-side
so a shopper who clicks the third card reads the third post rather than always
the first.
"""
from _posts import POSTS
from catalog import e
from components import article_card, page, page_header

SLUG = "blog.html"


def _post_json(p):
    """Every post's copy, inlined for the client-side `?post=` swap."""
    import json
    return json.dumps({
        p["slug"]: {
            "image": p["image"], "tags": p["tags"], "meta": p["meta"],
            "title": p["title"], "excerpt": p["excerpt"],
            "body": p["body"], "tips": p["tips"],
        } for p in POSTS
    }, ensure_ascii=False)


def build():
    first = POSTS[0]
    related = "".join(
        article_card(p["image"], p["tags"], p["meta"], p["title"], p["excerpt"],
                     href=f"blog.html?post={p['slug']}", rail=True)
        for p in POSTS[1:4]
    )

    tag_html = "".join(
        f'<span class="inline-flex items-center px-3 py-1 border border-heading '
        f'rounded-full font-medium text-heading text-xs">{e(t)}</span>'
        for t in first["tags"]
    )
    paras = "".join(
        f'<p class="text-bodyInk text-base xl:text-lg leading-[1.9]">{e(par)}</p>'
        for par in first["body"]
    )
    tips = "".join(f'<li>{e(t)}</li>' for t in first["tips"])

    body = f"""{page_header("", [("Home", "index.html"), ("Blog", "blogs.html"), (first["title"], None)])}

      <article class="py-6" data-post-article>
        <div class="flex flex-col gap-6 mx-auto px-4 xl:px-10 max-w-[880px]">
          <div class="flex flex-wrap items-center gap-3" data-post-tags>{tag_html}</div>
          <h1 class="font-medium text-heading text-[32px] xl:text-[44px] leading-[1.15] tracking-[-1px]" data-post-title>{e(first["title"])}</h1>
          <span class="font-medium text-metaGray text-sm" data-post-meta>{e(first["meta"])}</span>
          <p class="text-bodyMuted text-base xl:text-lg leading-[1.6]" data-post-excerpt>{e(first["excerpt"])}</p>
          <div class="rounded-3xl overflow-hidden">
            <img src="{e(first["image"])}" alt="{e(first["title"])}" class="w-full h-[260px] xl:h-[420px] object-cover" data-post-image />
          </div>
          <div class="flex flex-col gap-6" data-post-body>{paras}
          </div>
          <div class="flex flex-col gap-3 bg-cream p-6 xl:p-8 rounded-3xl">
            <h2 class="font-bold text-greenDeep text-lg">Quick tips</h2>
            <ul class="flex flex-col gap-2 ps-5 text-bodyInk text-base leading-[1.8] list-disc" data-post-tips>{tips}</ul>
          </div>
        </div>
      </article>

      <section class="bg-cream py-12 xl:py-14">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[1512px]">
          <div class="flex flex-wrap justify-between items-end gap-4">
            <h2 class="font-medium text-heading text-[28px] md:text-[36px] leading-none tracking-[-1px]">Related Articles</h2>
            <a href="blogs.html" class="group/link inline-flex items-center gap-2 font-bold text-heading text-base">
              Explore All Articles
              <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4 transition-transform group-hover/link:translate-x-1"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
          <!-- Same phone treatment as the homepage rail: one horizontal
               scroller below md, a grid from md up. -->
          <div class="flex md:grid md:grid-cols-3 gap-6 -mx-4 md:mx-0 px-4 md:px-0 overflow-x-auto md:overflow-visible no-scrollbar snap-x scroll-pl-4">{related}
          </div>
        </div>
      </section>

      <script id="post-data" type="application/json">{_post_json(POSTS)}</script>"""

    return page(f"{first['title']} | JAAD", first["excerpt"], body, "blog", "/blog")
