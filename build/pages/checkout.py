"""
Checkout — Figma 'Checkout > Info' (173:17235).

Header and footer collapse to the minimal checkout variants automatically:
scripts.js keys off data-page="checkout" via isCheckout().
"""
from _geo import CAIRO_AREAS, GOVERNORATES

from catalog import e, in_category, money
from components import (
    ICON, checkout_steps, checkout_summary, field, gift_toggle, page,
    radio_card, select_field,
)

SLUG = "checkout.html"

DELIVERY_FEE = 30.0

ICON_CAL = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
            '<rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.7"/>'
            '<path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>')
ICON_TRUCK = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
              '<path d="M1 3h13v13H1zM14 8h4l3 3v5h-7V8ZM7.5 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM19.5 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" '
              'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def build():
    items = in_category("Coffee", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE

    steps_html = checkout_steps(1)

    # data-cart-static: server-rendered so the summary is never blank before
    # scripts.js boots, and dropped by renderCart on the first paint — the
    # same contract the cart page's line list uses. Before this, the summary
    # was baked at build time and never read the store at all, so a basket
    # worth EGP 60 was checked out against a printed EGP 322.50 and two
    # products the shopper had never added.
    summary_lines = "".join(f"""
                <div data-cart-static class="flex items-center gap-3">
                  <img src="{e(p['image'])}" alt="" class="bg-cream p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-ink text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                  </div>
                  <span class="font-bold text-ink text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    body = f"""
      <section class="py-8">
        <!-- 1100px, NOT the site's 1536px container (Ahmed, 2026-07-26: the
             form is far too wide). Checkout is the one page that is a form
             rather than a shop window, and it inherited a container built for
             product grids: at 1536 the summary takes its fixed 380 and the
             form column is left with 1116px, so a two-up name row put each
             field at ~540px. A 540px text input is not generous, it is hard to
             use — the eye has to travel the whole width to find a 5-character
             answer, and typography guidance puts a comfortable input at
             roughly 45-75 characters.

             1100 leaves the form ~680px and the same 380px summary beside it,
             and `mx-auto` then centres the pair on the page rather than
             stretching them across it. The header above spans both columns and
             is inside this container, so it narrows and centres with them —
             which is what makes the page read as one centred block. -->
        <div class="items-start gap-10 grid grid-cols-1 lg:grid-cols-[1fr_380px] mx-auto px-4 max-w-[1100px]">

          <!-- Header is its own grid item spanning both columns, because the
               Figma mobile checkout (753:36339) puts the order summary directly
               beneath it, ahead of the form body — which is impossible while
               the header lives inside the form column. At lg every order resets
               and this spans row 1, leaving the desktop columns as they were. -->
          <div class="flex flex-col gap-3 order-1 lg:order-none lg:col-span-2 min-w-0">
            <h1 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">إتمام عملية الشراء بأمان</h1>
            <nav aria-label="خطوات الشراء" class="flex flex-wrap items-center gap-2">{steps_html}</nav>
          </div>

          <!-- RTL start: form -->
          <div class="flex flex-col gap-8 order-3 lg:order-none min-w-0">
            <form class="flex flex-col gap-8">
              <fieldset class="flex flex-col gap-4">
                <div class="flex flex-wrap justify-between items-center gap-2 mb-1">
                  <legend class="font-bold text-ink text-lg">بيانات العميل</legend>
                  <p class="text-muted text-sm">
                    هل لديك حساب بالفعل؟
                    <!-- ?next=checkout.html so a shopper who signs in mid-flow
                         lands back HERE after the OTP, not on the dashboard
                         (Ahmed, 2026-08-04). -->
                    <a href="login.html?next=checkout.html" class="font-semibold text-cta underline">تسجيل الدخول</a>
                  </p>
                </div>
                <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", required=True)}
{field("الاسم الاخير", "last-name", required=True)}
                </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
              </fieldset>

              <!-- Gifting sits AFTER the customer's own details: it asks who is
                   receiving the order, which only makes sense once who is
                   ordering has been answered. It replaced a normal/gift radio
                   pair at the top of the form — see gift_toggle(). -->
{gift_toggle()}

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-ink text-lg">وقت التوصيل</legend>
                <div class="flex sm:flex-row flex-col gap-4">
{radio_card("delivery-time", "now", "اليوم", "في غضون 60 دقيقة", ICON_CAL, checked=True)}
{radio_card("delivery-time", "later", "أختار تاريخ", "", ICON_CAL,
            meta_key="later", meta_prompt="حدد اليوم والوقت", opens="schedule")}
                </div>
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-ink text-lg">طريقة التوصيل</legend>
                <!-- Delivery only — Jaad has no physical branches, so the
                     in-store pickup option this build forked from (and its
                     branch picker modal) was dropped, not carried over disabled. -->
                <div class="flex sm:flex-row flex-col gap-4">
{radio_card("delivery-method", "delivery", "توصيل", "بإضافة مصاريف اضافية", ICON_TRUCK, checked=True)}
                </div>
              </fieldset>

              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-ink text-lg">عنوان التوصيل</legend>
{select_field("المدينة", "city", GOVERNORATES, required=True)}
                <div class="gap-4 grid sm:grid-cols-2">
{select_field("الحي", "district", CAIRO_AREAS, required=True)}
{select_field("المنطقة", "area", CAIRO_AREAS, required=True)}
                </div>
{field("رقم العقار و الشارع", "street", required=True)}
                <div class="flex flex-col gap-2">
                  <span class="font-medium text-muted text-sm">نوع العقار<span class="text-error">*</span></span>
                  <div class="flex items-center gap-6">
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="property-type" value="apartment" checked class="accent-ink-800 w-4 h-4" />
                      <span class="text-ink text-sm">شقة</span>
                    </label>
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="property-type" value="villa" class="accent-ink-800 w-4 h-4" />
                      <span class="text-ink text-sm">فيلا</span>
                    </label>
                  </div>
                </div>
                <div class="gap-4 grid grid-cols-2 max-w-[320px]">
{field("الطابق", "floor")}
{field("رقم الشقة", "apartment", required=True)}
                </div>
              </fieldset>

              <!-- data-cart-checkout: renderCart blocks this on an empty or
                   below-minimum basket, exactly as it already blocked the cart
                   page's own CTA. Without it checkout was the one place you
                   could carry an empty basket through to the thank-you page. -->
              <a href="payment.html" data-cart-checkout class="bg-cta hover:bg-cta-hover py-4 rounded-full w-full font-semibold text-white text-base text-center transition-colors">
                أكمل إلى الدفع
              </a>
            </form>
          </div>

{checkout_summary(summary_lines, subtotal, total, DELIVERY_FEE)}
        </div>
      </section>"""

    return page("إتمام عملية الشراء | جاد",
                "أكمل بيانات التوصيل وأتمم طلبك من جاد بأمان.",
                body, "checkout", "/checkout")
