"""Store closed / out-of-hours notice."""
from components import page

SLUG = "store-closed.html"


def build():
    body = """
      <section class="py-20">
        <div class="flex flex-col items-center gap-5 mx-auto px-4 max-w-[560px] text-center">
          <span class="place-items-center grid bg-interaction-base rounded-full size-24">
            <svg viewBox="0 0 24 24" fill="none" class="w-12 h-12 text-cta">
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
              <path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
          </span>
          <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">المتجر مغلق حالياً</h1>
          <p class="text-neutral-secondary text-base xl:text-lg leading-8">
            مواعيد العمل من <span class="latin">9</span> صباحاً حتى <span class="latin">11</span> مساءً يومياً.
            تقدر تتصفح المنتجات دلوقتي وتكمل طلبك في المواعيد.
          </p>
          <div class="flex flex-wrap justify-center gap-3 mt-2">
            <a href="shop.html" class="bg-cta hover:bg-cta-hover px-8 py-3 rounded-full font-semibold text-white text-base transition-colors">تصفح المنتجات</a>
          </div>
        </div>
      </section>"""
    return page("المتجر مغلق | جاد", "مواعيد عمل متجر جاد الإلكتروني.",
                body, "store-closed", "/store-closed")
