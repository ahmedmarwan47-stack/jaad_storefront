"""Addresses — Figma 'Account > Addresses' (312:16654)."""
from _account import account_page, account_title, card

SLUG = "my-account-addresses.html"

ADDRESSES = [
    ("المنزل", "شقة 3 - 220 شارع الحرية - الدور الأول", "مصر الجديدة، القاهرة", True),
    ("العمل", "مبنى 12 - شارع التسعين الشمالي", "التجمع الخامس، القاهرة", False),
]


def build():
    # These cards are the no-JS fallback ONLY. At runtime scripts.js owns the
    # grid (data-addresses-grid): it seeds a persistent store from these same
    # two addresses, re-renders the cards, and wires اضف عنوان / تعديل / حذف
    # for real — they were dead buttons until Ahmed pressed them (2026-07-22).
    # Change the seed in scripts.js (ADDR_SEED) if these two ever change.
    cards = "".join(card(
        label,
        f'''<div class="flex flex-col gap-1 text-neutral-secondary text-sm">
              <span>{line1}</span><span>{line2}</span>
            </div>
            {'<span class="bg-interaction-base px-3 py-1 rounded-full font-semibold text-primary text-xs self-start">العنوان الرئيسي</span>' if default else ''}
            <!-- mt-auto pins the actions to the card bottom so تعديل/حذف line up
                 across cards: without it, a card that lacks the main-address
                 badge floats its actions up under the address while the badged
                 card's sit a row lower. Grid rows already stretch to equal
                 height, so the shorter card just distributes the slack above. -->
            <div class="flex gap-2 mt-auto">
              <button type="button" class="hover:bg-interaction-base px-4 py-1.5 border border-neutral-divider rounded-full font-semibold text-[#003616] text-xs transition-colors">تعديل</button>
              <button type="button" class="px-4 py-1.5 font-semibold text-accent-error text-xs">حذف</button>
            </div>''')
        for label, line1, line2, default in ADDRESSES)

    content = f"""
            <div class="flex flex-wrap justify-between items-center gap-3">
              {account_title("my-account-addresses.html", "عناويني")}
              <button type="button" data-address-add class="bg-cta hover:bg-cta-hover px-6 py-2.5 rounded-full font-semibold text-white text-sm transition-colors">اضف عنوان</button>
            </div>
            <div class="gap-6 grid md:grid-cols-2" data-addresses-grid>{cards}</div>"""

    return account_page("عناويني | جاد", "إدارة عناوين التوصيل الخاصة بك.",
                        content, "my-account-addresses", "/my-account/addresses",
                        "عناويني", "my-account-addresses.html")
