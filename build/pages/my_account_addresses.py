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
    # "العنوان الافتراضي" as a real SWITCH, not a read-only badge (Ahmed,
    # 2026-08-23) — see addressCardHTML in scripts.js, which this shadows. The
    # default's own switch is checked and disabled: switching a default OFF would
    # leave no default at all, so you promote another card instead.
    cards = "".join(card(
        label,
        f'''<div class="flex flex-col gap-1 text-muted text-sm">
              <span>{line1}</span><span>{line2}</span>
            </div>
            <!-- mt-auto pins this row and the actions under it to the card
                 bottom, so the switch and تعديل/حذف line up across cards of
                 different heights. Grid rows already stretch to equal height, so
                 the shorter card just distributes the slack above. -->
            <label class="flex justify-between items-center gap-3 mt-auto pt-4 border-divider border-t{'' if default else ' cursor-pointer'}">
              <span class="font-semibold {'text-ink' if default else 'text-muted'} text-sm">العنوان الافتراضي</span>
              <input type="checkbox" data-switch data-address-default class="sr-only"{' checked disabled' if default else ''} />
              <span class="switch shrink-0" aria-hidden="true"><span class="switch__knob"></span></span>
            </label>
            <div class="flex gap-2">
              <button type="button" class="hover:bg-cream px-4 py-1.5 border border-divider rounded-full font-semibold text-ink text-xs transition-colors">تعديل</button>
              <button type="button" class="px-4 py-1.5 font-semibold text-error text-xs">حذف</button>
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
