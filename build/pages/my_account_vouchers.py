"""Vouchers — new page mirroring Exception's vouchers screen (Ahmed,
2026-08-04): a wallet-balance banner, the list of available vouchers each with
an activate (+) control, and two sheets (add a code / confirm activation).

Adding a code (Ahmed, 2026-08-05) does NOT credit the wallet — it drops a new
voucher into the AVAILABLE list with its value and expiry, persisted under
jaad:vouchersAdded. Only ACTIVATING a voucher (the + → confirm) moves its
value into the wallet, under jaad:vouchersWallet, and syncWalletBalance then
plays the credit animation. Demo/placeholder (no live endpoint, DESIGN-NOTES §1)."""
from _account import (
    CUSTOMER, VOUCHERS, account_page, account_title,
)

SLUG = "my-account-vouchers.html"

_PLUS = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 5v14M5 12h14" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')

# Old vouchers (used / expired) — demo history placeholder, like the wallet
# history. (label, status line, pill text, is_used). Activated vouchers are
# PREPENDED to this list at runtime by scripts.js (renderVoucherHistory).
OLD_VOUCHERS = [
    ("خصم 100 جنيه", "تم الاستخدام 20 أكتوبر 2025", "مستخدمة", True),
    ("خصم 50 جنيه", "انتهت في 3 سبتمبر 2025", "منتهية", False),
]


def build():
    rows = "".join(f"""
                <div data-voucher data-voucher-id="{i}" class="flex items-center gap-3 bg-white shadow-custom4 p-4 rounded-2xl">
                  <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-11 h-11 object-contain shrink-0" />
                  <div class="flex flex-col flex-1 min-w-0">
                    <span class="font-bold text-cta text-sm">{label}</span>
                    <span class="text-muted text-xs">{validity}</span>
                  </div>
                  <button type="button" data-voucher-activate data-value="{value}" data-label="{label}"
                          aria-label="تفعيل {label}"
                          class="place-items-center grid bg-cream hover:bg-cta hover:text-white border border-divider rounded-full size-10 text-cta shrink-0 transition-colors">
                    <span class="w-4 h-4">{_PLUS}</span>
                  </button>
                </div>""" for i, (label, validity, value) in enumerate(VOUCHERS))

    old_rows = "".join(f"""
                <div class="flex items-center gap-3 bg-white/70 p-4 border border-divider rounded-2xl">
                  <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-11 h-11 object-contain shrink-0 opacity-60 grayscale" />
                  <div class="flex flex-col flex-1 min-w-0">
                    <span class="font-bold text-muted text-sm">{label}</span>
                    <span class="text-muted text-xs">{sub}</span>
                  </div>
                  <span class="inline-flex items-center shrink-0 px-2.5 py-1 rounded-full font-semibold text-xs {'bg-mint text-ink-800' if used else 'bg-blush text-error'}">{pill}</span>
                </div>""" for label, sub, pill, used in OLD_VOUCHERS)

    content = f"""
            <div class="flex flex-wrap justify-between items-center gap-3">
              {account_title("my-account-vouchers.html", "القسائم")}
              <button type="button" data-open="voucherAdd" class="btn-elevate flex items-center gap-2 bg-cta hover:bg-cta-hover px-6 py-3 rounded-full font-semibold text-white text-sm transition-colors">
                <span class="w-4 h-4">{_PLUS}</span>أضف قسيمة
              </button>
            </div>

            <!-- Wallet banner: activating any voucher lands its value here.
                 data-wallet-card is glowed by the credit animation (scripts.js). -->
            <div data-wallet-card class="flex flex-wrap items-center gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              <img src="images/jaad/icons/wallet-3d.png" alt="" class="w-14 h-14 object-contain shrink-0" />
              <div class="flex flex-col">
                <span class="text-muted text-sm">رصيد المحفظة</span>
                <span class="font-bold text-cta text-2xl latin" data-wallet-amount>EGP {CUSTOMER['wallet']}</span>
              </div>
              <p class="flex-1 min-w-[200px] text-muted text-sm leading-6 text-end">فعّل أي قسيمة وتُضاف قيمتها مباشرة إلى رصيد محفظتك.</p>
            </div>

            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-heading text-lg">القسائم المتاحة</h2>
              <div class="flex flex-col gap-3" data-vouchers-list>{rows}
              </div>
              <p data-vouchers-empty hidden class="bg-cream py-10 rounded-2xl text-muted text-sm text-center">فعّلت كل القسائم المتاحة — تابعنا للعروض الجاية.</p>
            </div>

            <!-- History: used + expired vouchers (Ahmed, 2026-08-04). Activated
                 vouchers are prepended into [data-vouchers-history-dynamic] by
                 scripts.js; the static rows below are demo placeholder. -->
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-heading text-lg">القسائم السابقة</h2>
              <div class="flex flex-col gap-3">
                <div data-vouchers-history-dynamic class="flex flex-col gap-3"></div>
{old_rows}
              </div>
            </div>"""
    return account_page("القسائم | جاد", "قسائم الخصم المتاحة في حسابك.",
                        content, "my-account-vouchers", "/my-account/vouchers",
                        "القسائم", "my-account-vouchers.html")
