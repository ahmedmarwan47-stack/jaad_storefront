"""Wallet — redesigned to mirror Exception's wallet page (Ahmed, 2026-08-04): a
balance banner with an "Explore Vouchers" link, and a transaction history with a
running-balance column. The live balance ([data-wallet-amount]) reflects
redeemed points AND activated vouchers (scripts.js syncWalletBalance). The
history rows are demo/placeholder — no live endpoint (DESIGN-NOTES §1)."""
from _account import CUSTOMER, account_page, account_title, card

SLUG = "my-account-wallet.html"

# (amount, reason, date, running balance) — demo history, most recent first.
TXNS = [
    ("+500", "شحن المحفظة", "02 يوليو 2026", 1200),
    ("-320", "دفع طلب #30941", "28 يونيو 2026", 700),
    ("+150", "استبدال نقاط", "21 يونيو 2026", 1020),
    ("-260", "دفع طلب #30942", "14 يونيو 2026", 870),
    ("+80", "استرداد طلب #30918", "05 يونيو 2026", 1130),
]

_UP = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 19V5M6 11l6-6 6 6" '
       'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
_DOWN = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 5v14M6 13l6 6 6-6" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def build():
    rows = ""
    for amount, reason, date, bal in TXNS:
        credit = amount.startswith("+")
        rows += f"""
                  <tr class="border-divider border-b last:border-0">
                    <td class="py-4 pe-3">
                      <span class="inline-flex items-center gap-2 font-bold text-sm latin {'text-primary' if credit else 'text-error'}">
                        <span class="place-items-center grid rounded-full size-6 shrink-0 {'bg-mint' if credit else 'bg-blush'}"><span class="w-3 h-3">{_UP if credit else _DOWN}</span></span>
                        {amount} EGP
                      </span>
                    </td>
                    <td class="py-4 px-3 text-muted text-sm whitespace-nowrap">{date}</td>
                    <td class="py-4 px-3 text-ink text-sm">{reason}</td>
                    <td class="py-4 ps-3 font-semibold text-ink text-sm text-end latin whitespace-nowrap">{bal:,} EGP</td>
                  </tr>"""

    content = f"""
            {account_title("my-account-wallet.html", "محفظتي")}

            <!-- Balance banner + Explore Vouchers (Exception parity).
                 data-wallet-card is the hook the credit animation glows when a
                 voucher or points top up the balance (scripts.js). -->
            <div data-wallet-card class="flex flex-wrap justify-between items-center gap-4 bg-white shadow-custom4 p-6 xl:p-7 rounded-[20px]">
              <div class="flex items-center gap-4 min-w-0">
                <img src="images/jaad/icons/wallet-3d.png" alt="" class="w-16 h-16 object-contain shrink-0" />
                <div class="flex flex-col min-w-0">
                  <span class="text-muted text-sm">رصيد محفظتي</span>
                  <span class="font-bold text-cta text-4xl latin" data-wallet-amount>EGP {CUSTOMER['wallet']}</span>
                </div>
              </div>
              <a href="my-account-vouchers.html" class="btn-elevate bg-cta hover:bg-cta-hover px-6 py-3 rounded-full font-semibold text-white text-sm text-center transition-colors">استكشف القسائم</a>
            </div>

            {card("سجل المعاملات", f'''<div class="overflow-x-auto"><table class="w-full min-w-[460px] text-start">
              <thead>
                <tr class="border-divider border-b text-muted text-xs">
                  <th class="py-2 pe-3 font-semibold text-start">المبلغ</th>
                  <th class="py-2 px-3 font-semibold text-start">التاريخ</th>
                  <th class="py-2 px-3 font-semibold text-start">السبب</th>
                  <th class="py-2 ps-3 font-semibold text-end">الرصيد</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody></table></div>''')}"""

    return account_page("محفظتي | جاد", "رصيد محفظتك وسجل المعاملات.",
                        content, "my-account-wallet", "/my-account/wallet",
                        "محفظتي", "my-account-wallet.html")
