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

Card is the DEFAULT method and the card form is open beneath it (Ahmed,
2026-08-23) — number, name, expiry and CVV, revealed and hidden with the
"بطاقة ائتمان" row.

⚠️ These fields are a PROTOTYPE of the gateway screen, not the gateway. This is
a static export with no backend: nothing is validated, nothing is transmitted
and nothing is stored, and the previous build deliberately shipped no card
fields at all for exactly that reason — a page that asks for a card number
teaches shoppers to type one into a page that cannot protect it. They exist now
so the checkout can be reviewed end to end. Before this goes anywhere near real
shoppers the block must be replaced by the payment provider's own hosted fields
or iframe, so the number never touches a Jaad-served page. `autocomplete="off"`
and `data-demo-card` are on the inputs so a browser or password manager is not
invited to remember anything, and the block is easy to find and rip out.
Flagged in DESIGN-NOTES alongside the demo sign-in.
"""
from catalog import e, in_category, money
from components import (
    checkout_steps, checkout_summary, field, page, price_sticker, radio_card,
    scene_image,
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


# --------------------------------------------------------------------------
# Card form (PROTOTYPE — see the module docstring before wiring this up)
# --------------------------------------------------------------------------
# Hand-rolled rather than field(), because each of these needs an input mode,
# a length cap and a formatting hook that the generic field has no business
# knowing about. Every one carries `autocomplete="off"` and `data-demo-card`:
# off so no browser or password manager is invited to remember a number this
# page cannot protect, and the data attribute so both the JS that formats them
# and the person who eventually deletes this block can find them in one grep.
_CARD_INPUT = ('bg-white border border-divider rounded-2xl px-4 h-12 w-full '
               'text-ink text-base placeholder:text-muted outline-none '
               'focus:border-cta '
               'transition-colors latin')


def _card_field(label, name, placeholder, inputmode, maxlength, extra=""):
    return f"""
                    <div class="flex flex-col gap-1.5">
                      <label for="{name}" class="font-medium text-muted text-sm">{label}</label>
                      <input type="text" id="{name}" name="{name}" data-demo-card
                             inputmode="{inputmode}" maxlength="{maxlength}" autocomplete="off"
                             dir="ltr" placeholder="{placeholder}"{extra}
                             class="{_CARD_INPUT}" />
                    </div>"""


def _card_number():
    # The Visa/Mastercard marks sit INSIDE the field rather than repeating the
    # ones already on the option row above — here they say "this is the number
    # those marks accept", which the row cannot say about a field that does not
    # exist yet. `data-card-number` is the grouping hook (1234 5678 …).
    return f"""
                    <div class="flex flex-col gap-1.5">
                      <label for="card-number" class="font-medium text-muted text-sm">رقم البطاقة</label>
                      <div class="relative">
                        <input type="text" id="card-number" name="card-number" data-demo-card data-card-number
                               inputmode="numeric" maxlength="19" autocomplete="off"
                               dir="ltr" placeholder="1234 5678 9012 3456"
                               class="{_CARD_INPUT} pe-20" />
                        <span class="top-1/2 end-3 absolute flex items-center gap-1.5 -translate-y-1/2 pointer-events-none">
                          <img src="images/jaad/payments/pay-visa.svg" alt="" class="w-auto h-5 object-contain" />
                          <img src="images/jaad/payments/pay-mastercard.svg" alt="" class="w-auto h-5 object-contain" />
                        </span>
                      </div>
                    </div>"""


def _card_expiry():
    # maxlength 5 for MM/YY; the slash is inserted by the formatter in
    # scripts.js as the shopper types, so it is never something to type.
    return _card_field("تاريخ الانتهاء", "card-expiry", "MM/YY", "numeric", 5,
                       extra=' data-card-expiry')


def _card_cvv():
    return _card_field("رمز التحقق CVV", "card-cvv", "123", "numeric", 4)


def build():
    items = in_category("Coffee", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE

    summary_lines = "".join(f"""
                <div data-cart-static class="flex items-center gap-3">
                  <img src="{e(scene_image(p))}" alt="" class="cart-thumb bg-cream rounded-lg w-16 h-16 shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-ink text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                  </div>
                  {price_sticker(p['price'], "sm")}
                </div>""" for p in items)

    body = f"""
      <section class="py-8">
        <div class="items-start gap-10 grid grid-cols-1 lg:grid-cols-[1fr_380px] mx-auto px-4 max-w-[1100px]">

          <div class="flex flex-col gap-3 order-1 lg:order-none lg:col-span-2 min-w-0">
            <h1 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">طريقة الدفع</h1>
            <nav aria-label="خطوات الشراء" class="flex flex-wrap items-center gap-2">{checkout_steps(1)}</nav>
          </div>

          <!-- RTL start: form -->
          <div class="flex flex-col gap-8 order-3 lg:order-none min-w-0">
            <form class="flex flex-col gap-8">
              <fieldset class="flex flex-col gap-4">
                <legend class="mb-3 font-bold text-ink text-lg">اختر طريقة الدفع</legend>
                <div class="flex flex-col gap-4">

                  <!-- Card leads the list AND is the default (Ahmed,
                       2026-08-23). It used to lead visually while COD kept the
                       `checked`, so the row the eye landed on first was not the
                       row that was selected — and the card form below it stayed
                       shut on arrival. Card is now genuinely the pre-selected
                       method and its fields are open underneath. COD remains
                       one tap away, and its gift-order block (below) is
                       unaffected: that rule only ever fires when COD is the
                       chosen row. -->
                  <div class="flex">
{radio_card("payment-method", "card", "بطاقة ائتمان", "فيزا أو ماستركارد",
            _marks("pay-visa.svg", "pay-mastercard.svg"), checked=True)}
                  </div>

                  <!-- The card form. `data-card-fields` is revealed/hidden by
                       scripts.js off the payment-method radios, so it is open on
                       arrival (card is the default) and folds away the moment
                       another method is chosen — no orphan card form under a
                       cash order. READ THE MODULE DOCSTRING before wiring this
                       to anything: it is a prototype of a gateway screen, not a
                       gateway. -->
                  <div data-card-fields class="flex flex-col gap-4 bg-cream mx-1 p-5 rounded-2xl">
{_card_number()}
{field("الاسم على البطاقة", "card-name", autocomplete="off")}
                    <div class="gap-4 grid grid-cols-2">
{_card_expiry()}
{_card_cvv()}
                    </div>
                  </div>

                  <!-- Cash on delivery is blocked for gift orders, which is not
                       a new rule invented here: the gift card on the previous
                       screen already states it ("الدفع عند الاستلام غير متاح
                       لطلبات الهدايا"). Until now that was a promise with
                       nothing enforcing it, because there was no payment step
                       for it to apply to. scripts.js reads the gift flag saved
                       on checkout and blocks this row on load. -->
                  <div class="flex" data-cod-option>
{radio_card("payment-method", "cod", "الدفع عند الاستلام", "ادفع نقداً عند وصول طلبك", ICON_COD,
            blocked_note="غير متاح لطلبات الهدايا")}
                  </div>

                  <div class="flex">
{radio_card("payment-method", "etisalat", "اتصالات كاش", "ادفع من محفظتك على الموبايل",
            _marks("pay-etisalat-cash.png"))}
                  </div>
                </div>
              </fieldset>

              <p class="flex items-start gap-2 bg-cream p-4 rounded-xl text-muted text-xs leading-5">
                <span aria-hidden="true">🔒</span>
                <span>بيانات الدفع تتم بشكل آمن عند تأكيد الطلب. لن نحفظ بيانات بطاقتك.</span>
              </p>

              <!-- Same gate as the other CTA: renderCart disables this on an
                   EMPTY basket, so payment cannot be the one door left open on
                   an empty order. -->
              <a href="thank-you.html" data-cart-checkout class="bg-cta hover:bg-cta-hover py-4 rounded-full w-full font-semibold text-white text-base text-center transition-colors">
                تأكيد الطلب
              </a>
              <!-- The "العودة لبيانات التوصيل" link under the CTA is gone
                   (Ahmed, 2026-08-23): the breadcrumb at the top of the page
                   already links "بيانات شخصية" back to exactly this destination,
                   and a second way back sitting directly beneath the confirm
                   button competed with it for the last press of the flow. -->
            </form>
          </div>

{checkout_summary(summary_lines, subtotal, total, DELIVERY_FEE, interactive=False)}
        </div>
      </section>"""

    return page("طريقة الدفع | جاد",
                "اختر طريقة الدفع وأكد طلبك من جاد.",
                body, "checkout", "/payment")
