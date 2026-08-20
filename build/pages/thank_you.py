"""Order confirmation — Figma 'Thanks' (268:11025)."""
from _account import order_tracker_ride
from catalog import e, in_category, money, rail_products
from components import carousel, page, product_card, section_heading

SLUG = "thank-you.html"

DELIVERY_FEE = 30.0
ORDER_NO = "304585"

# The shared courier "ride" tracker — IDENTICAL to the dashboard current-order
# card (Ahmed, 2026-08-19): same order_tracker_ride component, no per-step
# subtitles, so the thank-you and the dashboard read as one thing. Right after
# placing an order the current step is index 1 (order placed, now being prepared).
TRACKER_STEP = 1

# A trailing True on a pair spans it across BOTH columns of the 2-up grid
# below — used for the email, whose long latin address would otherwise wrap
# every few characters inside a half-width cell on a phone.
# Demo customer. The email/phone here were a REAL personal address and number
# carried over from the fork (Ahmed, 2026-08-20) — replaced with the same
# demo@jad.com identity scripts.js already uses for its signed-in demo state,
# so no live third party is printed on a shipped page.
CUSTOMER = [
    ("الاسم الأول", "محمد"), ("اسم العائلة", "عادل"),
    ("البريد الالكتروني", "DEMO@JAD.COM", True),
    ("رقم الهاتف", "01200000000"),
]

DELIVERY = [
    ("الميعاد المتوقع للتوصيل", "23 مارس 2026"),
    ("المدينة", "القاهرة"), ("الحي", "القاهرة الجديدة"), ("المنطقة", "التجمع"),
    ("رقم العقار و الشارع", "شارع 5 عقار رقم 4"),
    ("الطابق", "5"), ("الشقة", "2"),
]

CHECK = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4">'
         '<path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _rows(pairs):
    out = []
    for pair in pairs:
        k, v = pair[0], pair[1]
        span = " col-span-2" if len(pair) > 2 and pair[2] else ""
        out.append(
            f'<div class="flex flex-col gap-0.5{span}">'
            f'<span class="text-neutral-secondary text-xs">{e(k)}</span>'
            f'<span class="font-semibold text-[#003616] text-sm break-words">{e(v)}</span></div>'
        )
    return "".join(out)


def build():
    items = in_category("Coffee", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE
    more = rail_products("Nuts", "Spices", limit=10)

    lines = "".join(f"""
                <div class="flex items-center gap-3 py-3 border-neutral-divider border-b last:border-0">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#003616] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">250 جم</span>
                    <span class="text-neutral-secondary text-xs">عدد <span class="latin">1</span></span>
                  </div>
                  <span class="font-bold text-[#003616] text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    body = f"""
      <section class="pt-10 pb-6">
        <div class="flex flex-col gap-3 mx-auto px-4 max-w-[1200px]">
          <div class="flex items-center gap-3">
            <span class="place-items-center grid bg-primary rounded-full text-white size-8">{CHECK}</span>
            <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">شكراً لك</h1>
          </div>
          <p class="font-semibold text-[#003616] text-base">تم تقديم طلبك بنجاح</p>
          <p class="text-neutral-secondary text-sm leading-7">
            إذا كانت لديك أسئلة حول طلبك، يمكنك مراسلتنا عبر البريد الإلكتروني على
            <a href="mailto:info@jad.com" class="font-semibold text-cta hover:text-primary underline transition-colors latin">INFO@JAD.COM</a>
            أو الاتصال بنا على <a href="tel:01200000000" class="font-semibold text-cta hover:text-primary underline transition-colors latin">01200000000</a>
          </p>
        </div>
      </section>

      <!-- ========================== ORDER TRACKER ========================== -->
      <!-- The SAME animated tracker as the dashboard and order drawer (Ahmed,
           2026-08-04), so the progress is one unified thing across the site. -->
      <section class="pb-8">
        <div class="mx-auto px-4 max-w-[1200px]">
          <div class="bg-white shadow-custom4 p-6 xl:px-10 rounded-[20px]">
            {order_tracker_ride(TRACKER_STEP)}
          </div>
        </div>
      </section>

      <!-- ============================ ORDER DETAIL ============================ -->
      <section class="pb-12">
        <!-- The order-detail block sits in a narrower 1200px column (Ahmed,
             2026-08-02): a full 1536 made the order box huge for its few items
             and the customer column a long narrow strip. Order stays the wider
             box, the customer info is 2-up so it is no longer a tall ribbon,
             and the two now read as a balanced pair. -->
        <div class="items-stretch gap-6 xl:gap-8 grid grid-cols-1 lg:grid-cols-[1fr_400px] mx-auto px-4 max-w-[1200px]">
          <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px] min-w-0">
            <h2 class="font-bold text-[#29612F] text-xl">طلب رقم <span class="latin">#{ORDER_NO}</span></h2>
            <div class="flex flex-col">{lines}
            </div>
            <!-- mt-auto sinks the totals to the bottom so the (shorter) order box
                 fills the height the taller customer box sets — the two columns
                 are items-stretch, so they end level (Ahmed, 2026-08-02). -->
            <div class="flex flex-col gap-2 mt-auto pt-3 border-neutral-divider border-t text-sm">
              <div class="flex justify-between">
                <span class="text-neutral-secondary">مصاريف التوصيل</span>
                <span class="font-semibold text-[#003616] latin">EGP {money(DELIVERY_FEE)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-neutral-secondary">الإجمالي</span>
                <span class="font-semibold text-[#003616] latin">EGP {money(subtotal)}</span>
              </div>
            </div>
            <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
              <span class="font-bold text-[#003616] text-base">الإجمالي</span>
              <span class="font-bold text-[#003616] text-2xl latin">EGP {money(total)}</span>
            </div>
          </div>

          <div class="flex flex-col gap-5 bg-interaction-base p-6 rounded-[20px]">
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#29612F] text-base">بيانات العميل</h2>
              <!-- Two columns at EVERY width (Ahmed, 2026-08-05): stacked in a
                   single column on a phone, this info left half the card empty
                   down its side. The values are short (the long email spans both
                   columns), so 2-up fills the width from 320 up. -->
              <div class="gap-x-4 gap-y-4 grid grid-cols-2">{_rows(CUSTOMER)}
              </div>
            </div>
            <div class="flex flex-col gap-3 pt-5 border-neutral-divider border-t">
              <h2 class="font-bold text-[#29612F] text-base">بيانات التوصيل</h2>
              <div class="gap-x-4 gap-y-4 grid grid-cols-2">{_rows(DELIVERY)}
              </div>
            </div>
            <!-- "Continue shopping", secondary (Ahmed, 2026-08-05): after an
                 order is placed the natural next step is back to the store, not
                 a second solid-green CTA competing with the confirmation. Full
                 width on mobile, content-width aligned to the end from sm up. -->
            <a href="shop.html" class="bg-white hover:bg-interaction-base px-8 py-3 border border-cta rounded-full w-full sm:w-auto sm:self-end font-semibold text-cta text-sm text-center transition-colors">متابعة التسوق</a>
          </div>
        </div>
      </section>

      <!-- ============================= SHOP MORE ============================= -->
      <section class="pb-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page("تم استلام طلبك | جاد",
                "شكراً لك — تم تقديم طلبك بنجاح في جاد.",
                body, "thank-you", "/thank-you")
