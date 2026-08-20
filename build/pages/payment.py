"""
Payment — step 3 of the checkout breadcrumb.

This page did not exist. The checkout CTA read "أكمل إلى الدفع" ("continue to
payment") and went straight to thank-you.html, so the step the button named was
the one step the flow skipped, and an order was "placed" without ever choosing
how to pay for it (Ahmed, 2026-07-26).

**The method list is not invented.** Every option here is a payment mark the
site already ships and displays in its own footer — `images/jaad/payments/`
carries exactly COD, Etisalat Cash, Visa and Mastercard. Nothing was added
beyond what the client already tells customers they accept; Visa and Mastercard
are folded into one "card" option because they are one flow, not two.

Card fields are deliberately NOT collected. This is a static export with no
backend, and a form that asks for a card number teaches shoppers to type one
into a page that cannot protect it — see the demo sign-in note in
DESIGN-NOTES for the same reasoning. Choosing the method is the real decision;
the number belongs to whatever gateway the client wires in later.
"""
from catalog import e, in_category, money
from components import (
    checkout_steps, checkout_summary, page, radio_card,
)

SLUG = "payment.html"

DELIVERY_FEE = 30.0

ICON_COD = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
            '<rect x="2" y="6" width="20" height="12" rx="2" stroke="currentColor" stroke-width="1.7"/>'
            '<circle cx="12" cy="12" r="2.6" stroke="currentColor" stroke-width="1.7"/>'
            '<path d="M5 9.5v5M19 9.5v5" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round"/></svg>')
ICON_PHONE_PAY = ('<svg viewBox="0 0 24 24" fill="none" class="w-6 h-6">'
                  '<rect x="6" y="2" width="12" height="20" rx="2.5" stroke="currentColor" stroke-width="1.7"/>'
                  '<path d="M10 18h4M9.5 8.5h5M9.5 12h5" stroke="currentColor" stroke-width="1.7" '
                  'stroke-linecap="round"/></svg>')


def _marks(*files):
    """
    The client's own payment marks, used AS the option's icon rather than as a
    strip underneath it (Ahmed, 2026-07-26). A generic outline-of-a-card glyph
    beside a row that then repeats the real Visa and Mastercard logos below was
    saying the same thing twice, and the weaker version first.

    ⚠️ These SVGs came out of Figma carrying `preserveAspectRatio="none"`,
    `width/height="100%"` AND `overflow="visible"` — the same export defect
    CLAUDE.md records for the logo. That combination stretches the artwork to
    whatever box it lands in and then paints outside it, which is why the
    Mastercard circles rendered as two enormous blobs across the row. Fixed in
    the assets themselves, so the viewBox is now the only source of intrinsic
    size and every future use gets the right shape for free.

    Explicit `h-6 w-auto` and a `shrink-0` wrapper: `w-auto` on an SVG only
    resolves correctly once the intrinsic ratio exists, which is exactly what
    the repair restored (verified — the file now reports 219x150, i.e. 35/24).

    NOT `loading="lazy"`, unlike the product thumbnails. These are three ~1KB
    marks inside the page's primary control, visible without scrolling, so
    deferring them saves nothing and costs a layout shift: until a lazy image
    loads it has no intrinsic size, so `w-auto` resolves to 0 and the row
    reflows when it arrives. Lazy is right for a 99-product grid and wrong
    here.
    """
    return (
        '<span class="flex items-center gap-1.5 shrink-0">'
        + "".join(
            f'<img src="images/jaad/payments/{f}" alt="" '
            f'class="h-6 w-auto object-contain" />'
            for f in files
        )
        + "</span>"
    )


def build():
    items = in_category("Coffee", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE

    summary_lines = "".join(f"""
                <div data-cart-static class="flex items-center gap-3">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#003616] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                  </div>
                  <span class="font-bold text-[#003616] text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    body = f"""
      <section class="py-8">
        <div class="items-start gap-10 grid grid-cols-1 lg:grid-cols-[1fr_380px] mx-auto px-4 max-w-[1100px]">

          <div class="flex flex-col gap-3 order-1 lg:order-none lg:col-span-2 min-w-0">
            <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">طريقة الدفع</h1>
            <nav aria-label="خطوات الشراء" class="flex flex-wrap items-center gap-2">{checkout_steps(2)}</nav>
          </div>

          <!-- RTL start: form -->
          <div class="flex flex-col gap-8 order-3 lg:order-none min-w-0">
            <form class="flex flex-col gap-8">
              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-[#003616] text-lg">اختر طريقة الدفع</legend>
                <div class="flex flex-col gap-4">

                  <!-- Credit card first at Ahmed's request (2026-08-02). COD
                       keeps the default selection (checked) — it is the
                       prevailing method in this market and the gift-order rule
                       below depends on it — but card now leads the list. -->
                  <div class="flex">
{radio_card("payment-method", "card", "بطاقة ائتمان", "فيزا أو ماستركارد",
            _marks("pay-visa.svg", "pay-mastercard.svg"))}
                  </div>

                  <!-- Cash on delivery is blocked for gift orders, which is not
                       a new rule invented here: the gift card on the previous
                       screen already states it ("الدفع عند الاستلام غير متاح
                       لطلبات الهدايا"). Until now that was a promise with
                       nothing enforcing it, because there was no payment step
                       for it to apply to. scripts.js reads the gift flag saved
                       on checkout and blocks this row on load. -->
                  <div class="flex" data-cod-option>
{radio_card("payment-method", "cod", "الدفع عند الاستلام", "ادفع نقداً عند وصول طلبك", ICON_COD, checked=True,
            blocked_note="غير متاح لطلبات الهدايا")}
                  </div>

                  <div class="flex">
{radio_card("payment-method", "etisalat", "اتصالات كاش", "ادفع من محفظتك على الموبايل",
            _marks("pay-etisalat-cash.png"))}
                  </div>
                </div>
              </fieldset>

              <!-- No card-number fields: see the module docstring. -->
              <p class="flex items-start gap-2 bg-interaction-base p-4 rounded-xl text-neutral-secondary text-xs leading-5">
                <span aria-hidden="true">🔒</span>
                <span>بيانات الدفع تتم بشكل آمن عند تأكيد الطلب. لن نحفظ بيانات بطاقتك.</span>
              </p>

              <!-- Same gate as the other two CTAs: renderCart disables this on
                   an empty or below-minimum basket, so payment cannot be the
                   one door left open on an empty order. -->
              <a href="thank-you.html" data-cart-checkout class="bg-cta hover:bg-cta-hover py-4 rounded-full w-full font-semibold text-white text-base text-center transition-colors">
                تأكيد الطلب
              </a>
              <a href="checkout.html" class="font-semibold text-cta text-sm text-center underline">العودة لبيانات التوصيل</a>
            </form>
          </div>

{checkout_summary(summary_lines, subtotal, total, DELIVERY_FEE, interactive=False)}
        </div>
      </section>"""

    return page("طريقة الدفع | جاد",
                "اختر طريقة الدفع وأكد طلبك من جاد.",
                body, "checkout", "/payment")
