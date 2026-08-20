"""Shared legal-document layout — Figma 'Privacy Policy/ TCs/ Refund Policy' (399:26319)."""
from catalog import e
from components import page, page_header


def legal_page(title_text, description, heading, sections, page_id, path):
    """sections: [(heading, [paragraph, ...])]"""
    toc = "".join(
        f'<a href="#s{i}" class="text-neutral-secondary hover:text-cta text-sm transition-colors">{e(h)}</a>'
        for i, (h, _) in enumerate(sections))

    blocks = "".join(f"""
            <section id="s{i}" class="flex flex-col gap-3 scroll-mt-24">
              <h2 class="font-bold text-[#29612F] text-xl">{e(h)}</h2>
              {"".join(f'<p class="text-neutral-800 text-base leading-9">{e(p)}</p>' for p in paras)}
            </section>""" for i, (h, paras) in enumerate(sections))

    body = f"""{page_header(heading, [("الرئيسية", "index.html"), (heading, None)])}

      <section class="py-8 xl:py-10">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-[240px_1fr] mx-auto px-4 xl:px-[190px] max-w-[1400px]">
          <nav class="lg:top-4 lg:sticky lg:flex flex-col gap-2 hidden bg-white shadow-custom4 p-5 rounded-2xl">
            <span class="mb-1 font-bold text-[#003616] text-sm">المحتويات</span>
            {toc}
          </nav>
          <div class="flex flex-col gap-8">{blocks}
          </div>
        </div>
      </section>"""

    return page(title_text, description, body, page_id, path)
