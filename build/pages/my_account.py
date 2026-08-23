"""Account overview — Figma 'Account > Overview' (312:13041)."""
from _account import (
    CUSTOMER, ORDERS, _icon, account_page, account_title, card, order_drawer,
    order_tracking_card, reorder_card,
)
from catalog import e

SLUG = "my-account.html"


def _stat(icon, label, value_html, href):
    """One dashboard stat card, linking to the matching account page (Ahmed,
    2026-08-04). It is an <a>, so it earns its own hover state: `tile-lift`
    lifts the shadow and `hover:-translate-y-0.5` nudges it up, and the chevron
    inks to cta on hover — the same navigable-tile language as the order rows.
    `icon` is the client's rendered 3D icon (points/wallet/orders), drawn inside
    the interaction-base tile."""
    return f"""
              <a href="{href}" class="tile-lift group flex items-center gap-3 bg-white shadow-custom4 p-4 xl:p-5 rounded-[20px] hover:-translate-y-0.5">
                <span class="place-items-center grid bg-cream rounded-2xl size-12 shrink-0" aria-hidden="true"><img src="{icon}" alt="" class="w-9 h-9 object-contain" /></span>
                <div class="flex flex-col flex-1 min-w-0">
                  <span class="text-muted text-xs">{label}</span>
                  <span class="font-bold text-ink text-xl">{value_html}</span>
                </div>
                <span class="ltr:scale-flip text-muted group-hover:text-cta shrink-0 transition-colors">{_icon('chev', 'w-4 h-4')}</span>
              </a>"""


def build():
    # The dashboard is interactive now, not a data dump (Ahmed, 2026-08-02):
    # a current-order tracker and a last-order re-order, with a link out to the
    # full orders list rather than the whole table inline.
    current = next((o for o in ORDERS if o["tone"] == "amber"), ORDERS[0])
    last = next((o for o in ORDERS if o["tone"] == "green"), ORDERS[-1])

    content = f"""
            <!-- Email-verify prompt ABOVE the welcome banner (Ahmed,
                 2026-08-04): after passwordless registration the mobile is
                 verified but the email is not, and verifying it is not required
                 to order — so it is a deferred reminder, and the more actionable
                 of the two banners, so it leads. Hidden until scripts.js sees a
                 signed-in user whose email is explicitly unverified. -->
            <div data-email-unverified hidden class="flex flex-wrap items-center gap-3 bg-[#FFF7E6] px-5 py-4 border border-[#EAD9A0] rounded-xl">
              <span class="place-items-center grid bg-white rounded-full text-[#8a6d1a] size-9 shrink-0">
                <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="m2 7 10 6 10-6" stroke="currentColor" stroke-width="1.7"/></svg>
              </span>
              <span class="flex-1 min-w-0 text-sm leading-6">
                <span class="font-semibold text-ink">أكّد بريدك الإلكتروني</span>
                <span class="text-[#5f5035]"> — بعتنالك رسالة تأكيد على بريدك، أكّده عشان يوصلك كل جديد عن طلباتك.</span>
              </span>
              <button type="button" data-verify-email class="shrink-0 bg-cta hover:bg-cta-hover px-5 py-2.5 rounded-full font-semibold text-white text-sm transition-colors">تأكيد البريد</button>
            </div>

            <div class="flex items-center gap-3 bg-cream px-5 py-4 rounded-xl">
              <span class="place-items-center grid bg-primary rounded-full text-white size-7 text-sm">✓</span>
              <span class="font-semibold text-ink text-sm">شكرا لتسجيلك حساب معنا !</span>
            </div>

            <div class="flex flex-col gap-1">
              <!-- "نظرة عامة", matching the sidebar tab (Ahmed, 2026-08-23).
                   "صفحة حسابي الرئيسية" was a third name for the same screen —
                   the tab said one thing, the breadcrumb another and the heading
                   a third. -->
              {account_title("my-account.html", "نظرة عامة")}
              <p class="text-muted text-sm">يمكنك إدارة الطلبات والمحفظة ومعلومات الحساب الخاصة بك هنا.</p>
            </div>

            <!-- Order tracking leads the dashboard (Ahmed, 2026-08-04): the live
                 tracker sits ABOVE the stat cards, so the first thing a returning
                 shopper sees is where their current order is. -->
            <div class="flex flex-col gap-4">
              <div class="flex flex-wrap justify-between items-center gap-3">
                <h2 class="font-bold text-heading text-lg">طلباتي</h2>
                <a href="my-account-orders.html" class="hover:bg-cream px-5 py-2 border border-divider rounded-full font-semibold text-ink text-xs transition-colors">كل الطلبات</a>
              </div>
              {order_tracking_card(current)}
              {reorder_card(last)}
            </div>

            <!-- Dashboard stats (Ahmed, 2026-08-04): points, wallet AND orders —
                 not the wallet alone. The wallet value keeps data-wallet-amount
                 so syncWalletBalance updates it with redeemed points. -->
            <div class="gap-4 grid grid-cols-1 sm:grid-cols-3">
              {_stat("images/jaad/icons/points-3d.png", "نقاط الولاء", f'<span class="latin" data-points-balance>{CUSTOMER["points"]:,}</span> <span class="font-medium text-muted text-xs">نقطة</span>', "my-account-point.html")}
              {_stat("images/jaad/icons/wallet-3d.png", "رصيد المحفظة", f'<span class="latin" data-wallet-amount>EGP {CUSTOMER["wallet"]}</span>', "my-account-wallet.html")}
              {_stat("images/jaad/icons/orders-3d.png", "إجمالي الطلبات", f'<span class="latin">{len(ORDERS)}</span> <span class="font-medium text-muted text-xs">طلب</span>', "my-account-orders.html")}
            </div>

            <!-- Referral card, laid out SIDE BY SIDE (Ahmed, 2026-08-23).

                 Stacked — heading, then subtitle, then the link row full width —
                 it took four rows and about 190px of the dashboard to hold one
                 link and one button, and the link row spanned the whole column
                 for a string that is 27 characters long. Title + subtitle take
                 the inline-start half now and the link + copy button sit beside
                 them at the end, which is roughly half the height for the same
                 content. It stacks again below `md`, where two columns would
                 squeeze the URL to nothing.

                 Written out rather than going through card(), because card()
                 puts its heading in a row of its own — which is precisely the
                 stacking being removed here. -->
            <div class="flex md:flex-row flex-col md:items-center gap-4 md:gap-6 bg-white shadow-custom4 p-6 rounded-[20px]">
              <div class="flex flex-col gap-1 min-w-0 md:basis-1/2">
                <h2 class="font-bold text-heading text-base">شارك الموقع مع الأصحاب والعائلة</h2>
                <p class="text-muted text-sm">أنسخ الرابط أدناه وشاركه مع عائلتك وأصدقائك واحصل على خصومات حصرية</p>
              </div>
              <div class="flex flex-1 items-center gap-2 bg-cream px-4 py-2 rounded-xl min-w-0">
                <span data-ref-link class="flex-1 min-w-0 text-muted text-xs truncate latin">WWW.JAD.COM/REF/1-0200,20409</span>
                <button type="button" data-copy-ref class="bg-cta hover:bg-cta-hover px-4 py-1.5 rounded-full font-semibold text-white text-xs whitespace-nowrap transition-colors">نسخ</button>
              </div>
            </div>

            <h2 class="font-bold text-heading text-lg">بياناتي</h2>
            <div class="gap-6 grid md:grid-cols-2">
              {card("بيانات الحساب", f'''
                <div class="flex flex-col gap-1 text-sm">
                  <span class="text-ink">{e(CUSTOMER['full'])}</span>
                  <span class="text-muted latin">{e(CUSTOMER['email'])}</span>
                  <span class="text-muted latin">{e(CUSTOMER['phone'])}</span>
                </div>''', "تعديل", "my-account-profile.html")}
              {card("عنواني الافتراضي", '''
                <div class="flex flex-col gap-1 text-muted text-sm">
                  <span>شقة 3 - 220 شارع الحرية - الدور الأول</span>
                  <span>مصر الجديدة</span>
                  <span>القاهرة، مصر</span>
                </div>''', "تعديل", "my-account-addresses.html")}
            </div>
            {order_drawer(ORDERS)}"""

    return account_page("حسابي | جاد",
                        "إدارة طلباتك وعناوينك ومحفظتك في جاد.",
                        content, "my-account", "/my-account",
                        "حسابي", "my-account.html")
