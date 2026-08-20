"""Single order — Figma 'Account > Single Order' (312:20393)."""
from _account import account_page, card
from catalog import e, in_category, money

SLUG = "my-account-order.html"
DELIVERY_FEE = 30.0

STEPS = [("تم الطلب", True), ("جاري التحضير", True), ("في الطريق إليك", False), ("تم التسليم", False)]
CHECK = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="m5 13 4 4L19 7" '
         'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def build():
    items = in_category("Coffee", 2)
    subtotal = sum(p["price"] for p in items)
    total = subtotal + DELIVERY_FEE

    steps = "".join(f"""
                <li class="flex flex-col flex-1 items-center gap-2 text-center">
                  <span class="place-items-center grid rounded-full size-8 {'bg-primary text-white' if done else 'bg-interaction-base text-neutral-secondary'}">
                    {CHECK if done else f'<span class="font-semibold text-sm latin">{i + 1}</span>'}
                  </span>
                  <span class="font-semibold text-[#003616] text-xs">{e(label)}</span>
                </li>""" for i, (label, done) in enumerate(STEPS))

    lines = "".join(f"""
                <div class="flex items-center gap-3 py-3 border-neutral-divider border-b last:border-0">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-16 h-16 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#003616] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">250 جم · عدد <span class="latin">1</span></span>
                  </div>
                  <span class="font-bold text-[#003616] text-sm latin shrink-0">EGP {money(p['price'])}</span>
                </div>""" for p in items)

    content = f"""
            <div class="flex flex-wrap justify-between items-center gap-3">
              <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">طلب رقم <span class="latin">#30941</span></h1>
              <span class="bg-accent-yellow px-4 py-1.5 rounded-full font-semibold text-[#003616] text-xs">تحت التحضير</span>
            </div>
            {card("", f'<ol class="flex gap-2">{steps}</ol>')}
            {card("تفاصيل الطلب", f'''<div class="flex flex-col">{lines}</div>
              <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
                <div class="flex justify-between"><span class="text-neutral-secondary">مصاريف التوصيل</span><span class="font-semibold text-[#003616] latin">EGP {money(DELIVERY_FEE)}</span></div>
                <div class="flex justify-between"><span class="text-neutral-secondary">الإجمالي</span><span class="font-semibold text-[#003616] latin">EGP {money(subtotal)}</span></div>
              </div>
              <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
                <span class="font-bold text-[#003616]">الإجمالي</span>
                <span class="font-bold text-[#003616] text-2xl latin">EGP {money(total)}</span>
              </div>''')}
            {card("عنوان التوصيل", '''<div class="flex flex-col gap-1 text-neutral-secondary text-sm">
                <span>شقة 3 - 220 شارع الحرية - الدور الأول</span><span>مصر الجديدة، القاهرة</span></div>''')}"""

    return account_page("تفاصيل الطلب | جاد", "تفاصيل وحالة طلبك من جاد.",
                        content, "my-account-order", "/my-account/order",
                        "تفاصيل الطلب", "my-account-orders.html")
