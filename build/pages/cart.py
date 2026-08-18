"""Shopping cart — Figma 'Cart' (4231:22875)."""
from catalog import in_category, money, rail_products
from components import (
    ICON, cart_line, carousel, freeship_bar, order_notes, page, page_header,
    promo_field, wallet_toggle, product_card, section_heading,
)

SLUG = "cart.html"

DELIVERY_FEE = 30.0
# No MIN_ORDER here any more. The minimum is a runtime rule now that the
# below-minimum state is painted from the live basket rather than the
# build-time one, so scripts.js owns the single copy of it (MIN_ORDER = 150).
# Keeping a second constant here would only be a number to drift.


def build():
    items = [(p, 1) for p in in_category("Coffee", 3)]
    subtotal = sum(p["price"] * q for p, q in items)
    total = subtotal + DELIVERY_FEE

    lines = "".join(cart_line(p, q) for p, q in items)
    more = rail_products("Nuts", "Spices", limit=10)

    # The basket is client state, so whether this button is usable cannot be
    # decided here. It used to pick between a disabled <button> and a live <a>
    # from the build-time subtotal and then never change — which shipped a
    # fully live "أطلب الآن" that carried an EMPTY basket through to checkout,
    # while the drawer's own smaller CTA beside it was correctly greyed out.
    #
    # Always the anchor now, tagged data-cart-checkout, and renderCart gates
    # it on every cart:change exactly as it already gated the drawer's.
    order_btn = (
        '<a href="checkout.html" data-cart-checkout class="block bg-cta hover:bg-cta-hover '
        'py-4 rounded-full w-full font-semibold text-white text-base text-center '
        'transition-colors">إتمام الطلب</a>'
    )
    # Same reasoning: always rendered, hidden by default, and shown with the
    # live shortfall by renderCart via data-cart-warning/data-cart-shortfall.
    # Alert glyph (Ahmed's alert-01.svg) in an error-ink wrapper, replacing the
    # bare ⚠ emoji so the notice matches the rest of the UI's iconography.
    warning = (
        '<p data-cart-warning hidden class="flex items-start gap-2 text-accent-error '
        'text-xs leading-5"><span class="w-4 h-4 shrink-0 mt-px" aria-hidden="true">'
        f'{ICON["alert"]}</span>'
        '<span>متبقي <span class="latin" data-cart-shortfall></span> '
        'لاستكمال الحد الأدنى للطلب</span></p>'
    )

    body = f"""{page_header("سلة التسوق", [("الرئيسية", "index.html"), ("سلة التسوق", None)])}

      <!-- ============================== CART ============================== -->
      <section class="py-8 xl:py-10">
        <div class="items-start gap-6 lg:gap-8 grid grid-cols-1 lg:grid-cols-[1fr_380px] mx-auto px-4 max-w-[1536px]">

          <!-- Summary on the LEFT at lg, matching the checkout/payment layout
               (Ahmed, 2026-08-05): the 380px column is the grid's SECOND track,
               which in RTL is the inline-end (left) side. `lg:order-2` puts the
               summary there while the line items (lg:order-1) take the 1fr track
               on the right. `order-last` keeps the Figma mobile cart order below
               lg — line items first, summary beneath (804:32907). -->
          <aside class="flex flex-col gap-4 lg:sticky lg:top-4 order-last lg:order-2 min-w-0">
            <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              <h2 class="font-bold text-[#003616] text-xl">ملخص السلة</h2>
{freeship_bar()}
              <!-- Wallet, promo and the note editor grouped together (Ahmed,
                   2026-08-04), the same grouping the checkout summary uses, so
                   the "extras" sit as one block above the totals rather than
                   scattered around them. -->
{wallet_toggle()}
{promo_field()}
              <div class="pt-1">{order_notes()}
              </div>
              <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
                <div class="flex justify-between">
                  <span class="text-neutral-secondary">مصاريف التوصيل</span>
                  <span class="font-semibold text-[#003616] latin" data-cart-delivery>EGP {money(DELIVERY_FEE)}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-neutral-secondary">الإجمالي</span>
                  <span class="font-semibold text-[#003616] latin" data-cart-subtotal>EGP {money(subtotal)}</span>
                </div>
                <!-- Wallet and promo discounts, each its own row — hidden
                     until applied; renderCart owns both the visibility and
                     the figure for each, and a promo applied together with
                     the wallet must show both amounts rather than one
                     combined figure that hides what the code itself took
                     off. -->
                <div class="flex justify-between items-center" data-cart-discount-row hidden>
                  <span class="text-neutral-secondary">خصم المحفظة</span>
                  <!-- The green counterpart of the yellow price chip: a saving
                       is good news and should read as one at a glance. -->
                  <span class="inline-flex items-center -me-2 bg-[#E9F3E6] px-2 py-0.5 rounded-full font-bold text-[#00451C] text-sm latin" data-cart-discount></span>
                </div>
                <div class="flex justify-between items-center" data-cart-promo-row hidden>
                  <span class="text-neutral-secondary">خصم كود الخصم</span>
                  <span class="inline-flex items-center -me-2 bg-[#E9F3E6] px-2 py-0.5 rounded-full font-bold text-[#00451C] text-sm latin" data-cart-promo-discount></span>
                </div>
              </div>
              <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
                <span class="font-bold text-[#003616] text-base">الإجمالي</span>
                <span class="font-bold text-[#003616] text-2xl latin" data-cart-total>EGP {money(total)}</span>
              </div>
              {order_btn}
              {warning}
            </div>
          </aside>

          <!-- Line items — the 1fr track (inline-start / right in RTL). -->
          <div class="bg-white shadow-custom4 px-6 py-2 rounded-[20px] lg:order-1 min-w-0" data-cart-lines>{lines}
          </div>
        </div>
      </section>

      <!-- =========================== SHOP MORE =========================== -->
      <section class="py-12">
        <div class="mx-auto px-4 max-w-[1536px]">
          {section_heading("تسوق اكتر", "عرض المزيد", "shop.html")}
          {carousel("".join(product_card(x) for x in more))}
        </div>
      </section>"""

    return page("سلة التسوق | جاد",
                "راجع منتجاتك وأتمم طلبك من جاد.",
                body, "cart", "/cart")
