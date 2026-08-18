"""
Shared product-listing layout — Figma 'Collection' (173:17211).

Both shop.html (everything) and shop-category.html (one category) are the same
view with different data, so they share this builder. Change the listing here
and both pages follow.
"""
from catalog import e
from components import chip, page, page_header, product_grid, sort_select

SORT_OPTIONS = [
    ("popular", "الأكثر مبيعاً"),
    ("newest", "وصل حديثاً"),
    ("price-asc", "السعر: من الأقل"),
    ("price-desc", "السعر: من الأعلى"),
]


def listing(title_text, description, heading, trail, chips, products,
            page_id, path, intro=None, active_chip=None, cat_of=None):
    # A chip may be (label, href) or (label, href, filter_slug). Only the
    # three-item form becomes a live filter; the two-item form stays a link,
    # which is what the sub-category chips are until the client's taxonomy
    # exists (see DESIGN-NOTES).
    chip_html = "".join(
        chip(c[0], c[1], active=(c[0] == active_chip),
             filter_slug=(c[2] if len(c) > 2 else None))
        for c in chips
    )
    filterable = any(len(c) > 2 for c in chips)
    intro_html = (
        f'<p class="max-w-[720px] text-neutral-secondary text-base xl:text-lg leading-8">{e(intro)}</p>'
        if intro else ""
    )

    body = f"""{page_header(heading, trail)}

      <!-- ============================== FILTERS ============================== -->
      <section class="pt-6">
        <div class="flex flex-col gap-6 mx-auto px-4 max-w-[1536px]">
          {intro_html}
          <!-- Chips and sort share ONE row again on desktop (Ahmed,
               2026-08-04). They are a flex ROW at xl: the chips wrap inside a
               flex-1 area and the sort pill is pinned to the inline end with a
               gap between them, so the two can never overlap — a flex row lays
               its children out side by side, it does not stack them — and the
               chips are a touch smaller at xl (see chip()) so the whole set
               fits. Below xl the column stacks: the chips scroll on one line
               and the sort drops beneath them, aligned to the inline start. -->
          <div class="flex flex-col items-start gap-4 xl:flex-row xl:items-start xl:justify-between xl:gap-6"{' data-listing' if filterable else ''}>
            <!-- Mobile: one scrolling row (swipe). Desktop: WRAP instead — a
                 no-scrollbar horizontal scroll clipped the last chip mid-word,
                 which read as a collision. Wrapping shows every category. -->
            <!-- Full-bleed to the viewport edge on mobile: the width is the
                 parent content PLUS the 2rem the negative margins pull out, so
                 the row reaches both screen edges and the last chip crops at the
                 edge (signalling more) rather than 32px short of it. At xl it
                 becomes flex-1 so it shares the row with the sort pill. -->
            <div data-drag-scroll class="flex gap-2 -mx-4 px-4 xl:mx-0 xl:px-0 w-[calc(100%_+_2rem)] xl:w-auto xl:flex-1 min-w-0 overflow-x-auto no-scrollbar xl:flex-wrap xl:overflow-visible">{chip_html}
            </div>
{sort_select(SORT_OPTIONS)}
          </div>
        </div>
      </section>

      <!-- ============================== PRODUCTS ============================== -->
      <section class="py-8 xl:py-10">
        <div class="mx-auto px-4 max-w-[1536px]">
          <!-- Names the grid for heading navigation and restores the level
               the cards' h3 was skipping — the page h1 sat directly above
               them. Not painted: the visible label is the result count. -->
          <h2 class="sr-only">قائمة المنتجات</h2>
          <p class="mb-6 text-neutral-secondary text-sm">
            <span class="latin" data-result-count>{len(products)}</span> منتج
          </p>
          <p data-empty-state hidden class="py-10 text-neutral-secondary text-base text-center">
            لا توجد منتجات في هذا القسم حالياً.
          </p>
          {product_grid(products, cat_of=cat_of)}
          <div class="flex justify-center mt-12">
            <button type="button" class="hover:bg-interaction-base px-10 py-3 border border-cta rounded-full font-semibold text-cta text-base transition-colors">
              عرض المزيد
            </button>
          </div>
        </div>
      </section>"""

    return page(title_text, description, body, page_id, path)
