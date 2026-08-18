"""
Shared account-area shell — Figma 'Account > Overview' (312:13041).

All eight my-account pages are this sidebar plus a content column, so the
sidebar, membership badge and help links are defined once here.
"""
from catalog import e, in_category, money, title as _ptitle
from components import WALLET_BALANCE, page, page_header

# `wallet` comes from components.WALLET_BALANCE rather than a second literal:
# the cart/checkout wallet toggle offers to spend this exact balance, so if the
# two drifted the shopper would be offered money this page says they do not
# have. Same failure the old points banner shipped with — 100 on one page, 120
# on the other.
CUSTOMER = {"name": "محمد", "full": "محمد عادل",
            "email": "mosawabi15@gmail.com", "phone": "0109809839",
            # `tier` is a KEY now (Ahmed, 2026-08-04), so the label and the
            # metallic wash have one source in TIERS instead of a bare string.
            # `points` sits in the gold band (see POINT_TIERS) so the redesigned
            # points page has a meaningful progress bar toward platinum.
            "tier": "gold", "wallet": WALLET_BALANCE, "points": 3200}

# Loyalty tiers BY POINTS (demo thresholds; DESIGN-NOTES). The redesigned points
# page mirrors Exception: one "available points" figure drives BOTH the redeem
# and the tier progress, so spending points can move the tier. label → min pts.
POINT_TIERS = [("فضية", 0), ("ذهبية", 2000), ("بلاتينية", 4000)]
# 10 points → EGP 1, mirroring the existing "120 نقطة → EGP 12" the page shipped.
POINTS_PER_EGP = 10

# Available vouchers to claim (demo/placeholder — no live endpoint, DESIGN-NOTES,
# same footing as the wallet history). Each: (label, validity, EGP value).
VOUCHERS = [
    ("خصم 100 جنيه", "صالحة حتى 20 أكتوبر 2026", 100),
    ("خصم 150 جنيه", "صالحة حتى 5 نوفمبر 2026", 150),
    ("خصم 250 جنيه", "صالحة حتى 18 ديسمبر 2026", 250),
]


def tier_progress(points):
    """Current tier + progress toward the next, from a points balance. Shared by
    the build-time render and mirrored in scripts.js for live updates on redeem."""
    idx = 0
    for i, (_label, mn) in enumerate(POINT_TIERS):
        if points >= mn:
            idx = i
    cur = POINT_TIERS[idx]
    nxt = POINT_TIERS[idx + 1] if idx + 1 < len(POINT_TIERS) else None
    if nxt:
        span = nxt[1] - cur[1]
        pct = max(0, min(100, round((points - cur[1]) / span * 100)))
        to_next = max(0, nxt[1] - points)
    else:
        pct, to_next = 100, 0
    return {"idx": idx, "cur": cur, "next": nxt, "pct": pct, "to_next": to_next}

# Membership tiers — silver / gold / platinum. The badge actively shines
# (`.tier-badge` in styles.css sweeps a gloss across it on a loop); the label
# and the metallic gradient follow the tier. Text colour lives in the CSS tier
# class so each metal keeps a legible AA ink on its own wash.
TIERS = {
    "silver": ("عضوية فضية", "tier-badge--silver"),
    "gold": ("عضوية ذهبية", "tier-badge--gold"),
    "platinum": ("عضوية بلاتينية", "tier-badge--platinum"),
}


def tier_badge(tier_key, extra=""):
    """Shining membership badge. `self-start` keeps it from stretching to the
    column width (flex-col children stretch by default). The label sits in a
    `relative z-10` span so it stays crisp while the gloss sweeps over it."""
    label, cls = TIERS.get(tier_key, TIERS["gold"])
    return (f'<span class="tier-badge {cls} inline-flex items-center self-start px-3 py-1 '
            f'rounded-full font-bold text-xs {extra}">'
            f'<span class="relative z-10">{e(label)}</span></span>')

I = {
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V10Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "orders": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6ZM3 6h18M16 10a4 4 0 0 1-8 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    "heart": '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.7"/>',
    "wallet": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" stroke="currentColor" stroke-width="1.7"/><path d="M16 12h3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "user": '<circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.7"/><path d="M4 21a8 8 0 0 1 16 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
    "voucher": '<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4V8Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M14 6v12" stroke="currentColor" stroke-width="1.7" stroke-dasharray="2 2.5"/>',
    "out": '<path d="M15 17l5-5-5-5M20 12H9M12 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    # Chevron points to the inline end (left in RTL), matching the Figma rows.
    "chev": '<path d="m15 6-6 6 6 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
}

NAV = [
    ("الرئيسية", "my-account.html", "home"),
    ("طلباتي", "my-account-orders.html", "orders"),
    ("المفضلة", "my-account-favorites.html", "heart"),
    ("عناويني", "my-account-addresses.html", "pin"),
    ("محفظتي", "my-account-wallet.html", "wallet"),
    ("القسائم", "my-account-vouchers.html", "voucher"),
    ("نقاطي", "my-account-point.html", "star"),
    ("بيانات الحساب", "my-account-profile.html", "user"),
]

# 3D icons the client has delivered, keyed by the tab they belong to (Ahmed,
# 2026-08-04). A tab with an entry here renders the rendered PNG in the sidebar
# and beside the page title; the rest keep the line-art glyph until their 3D
# renders land (prompts handed to Ahmed). The build validates these refs, so
# only real files may appear.
NAV_ICON_3D = {
    "my-account.html": "images/jaad/icons/home-3d.png",
    "my-account-orders.html": "images/jaad/icons/orders-3d.png",
    "my-account-favorites.html": "images/jaad/icons/favorites-3d.png",
    "my-account-addresses.html": "images/jaad/icons/addresses-3d.png",
    "my-account-wallet.html": "images/jaad/icons/wallet-3d.png",
    "my-account-vouchers.html": "images/jaad/icons/voucher-3d.png",
    "my-account-point.html": "images/jaad/icons/points-3d.png",
    "my-account-profile.html": "images/jaad/icons/profile-3d.png",
}


def _icon(key, cls="w-5 h-5"):
    return f'<svg viewBox="0 0 24 24" fill="none" class="{cls}">{I[key]}</svg>'


def nav_icon(href, key, cls="w-6 h-6", img_cls="w-7 h-7"):
    """A tab's mark: the 3D render when one exists for that tab, else the
    line-art glyph. Keeping one lookup means the sidebar, the mobile sheet and
    the page title all show the same icon for a tab."""
    src = NAV_ICON_3D.get(href)
    if src:
        return f'<img src="{src}" alt="" class="{img_cls} object-contain shrink-0" />'
    return f'<span class="text-cta shrink-0">{_icon(key, cls)}</span>'


def account_title(active_slug, title):
    """Page heading with its sidebar tab's ICON beside it (Ahmed, 2026-08-04),
    so a tab and the page it opens carry the same mark. The icon is looked up
    from NAV by slug; the title text is whatever the page passes, so no page
    title changes — only the glyph is added."""
    icon_key = next((ic for _l, href, ic in NAV if href == active_slug), None)
    inner = nav_icon(active_slug, icon_key, cls="w-5 h-5", img_cls="w-8 h-8") if icon_key else ""
    icon = (f'<span class="place-items-center grid bg-interaction-base rounded-xl size-11 shrink-0">{inner}</span>'
            if icon_key else "")
    return (f'<div class="flex items-center gap-3">{icon}'
            f'<h1 class="font-bold text-[#003616] text-2xl xl:text-3xl">{e(title)}</h1></div>')


def _nav_badge(href):
    """Count/value shown right BESIDE a dashboard tab's title (Ahmed,
    2026-08-04): the wishlist count, the wallet balance and the points balance.
    A light-green pill with NO border — the "good news" tint (#E9F3E6) reads on
    both the white sidebar and the interaction-base active row, and the dark
    green ink clears AA on it. The favourites count is live (scripts.js keeps
    every [data-favs-count] in step); wallet and points are the demo figures."""
    pill = ('inline-flex items-center justify-center shrink-0 bg-[#E9F3E6] '
            'rounded-full px-2 min-w-[26px] h-6 font-bold text-[#00451C] text-xs latin')
    if href == "my-account-favorites.html":
        return f'<span class="{pill}" data-favs-count>0</span>'
    if href == "my-account-wallet.html":
        return f'<span class="{pill}" data-wallet-amount>EGP {CUSTOMER["wallet"]}</span>'
    if href == "my-account-vouchers.html":
        return f'<span class="{pill}" data-vouchers-count>{len(VOUCHERS)}</span>'
    if href == "my-account-point.html":
        return f'<span class="{pill}" data-points-badge>{CUSTOMER["points"]}</span>'
    return ""


def sidebar(active_slug):
    # Icon, then the label with its count pill right beside it (the label group
    # is NOT flex-1, so the badge hugs the title instead of being pushed to the
    # row's far end).
    items = "".join(f"""
              <a href="{href}" class="flex items-center gap-3 px-4 py-3 rounded-xl font-semibold text-base transition-colors {'bg-interaction-base text-[#003616]' if href == active_slug else 'text-neutral-800 hover:bg-interaction-base'}">
                {nav_icon(href, icon)}
                <span class="flex items-center gap-2 min-w-0">
                  <span class="truncate">{e(label)}</span>{_nav_badge(href)}
                </span>
              </a>""" for label, href, icon in NAV)

    return f"""
          <aside class="hidden lg:flex flex-col gap-1 bg-white shadow-custom4 p-5 rounded-[20px] lg:sticky lg:top-4 min-w-0 h-max">
            {tier_badge(CUSTOMER['tier'])}
            <h2 class="mt-2 mb-3 font-bold text-[#003616] text-xl">مرحبا {e(CUSTOMER['name'])}</h2>
            {items}
            <div class="flex flex-col gap-2 mt-4 pt-4 border-neutral-divider border-t">
              <span class="font-semibold text-neutral-secondary text-sm">تحتاج مساعدة؟</span>
              <a href="faqs.html" class="link-sweep self-start font-semibold text-cta text-sm">الأسئلة المتداولة</a>
              <a href="contact-us.html" class="link-sweep self-start font-semibold text-cta text-sm">تواصل معنا</a>
            </div>
            <!-- One logout only (Ahmed, 2026-08-04): a real data-logout button.
                 The old red "تسجيل الخروج" text button AND this one shipped
                 together — and the second merely linked home without logging
                 out, so there were two controls, one of them lying. -->
            <button type="button" data-logout class="flex justify-center items-center gap-2 mt-4 py-3 border border-neutral-divider hover:border-cta rounded-full font-semibold text-[#003616] text-sm transition-colors">
              {_icon('out', 'w-4 h-4')} تسجيل الخروج
            </button>
          </aside>"""


def _active_label(active_slug):
    for label, href, _icon_key in NAV:
        if href == active_slug:
            return label
    return NAV[0][0]


def mobile_nav(active_slug):
    """Figma 'Account > menu bottom sheet' (973:47270).

    A 300px sidebar has nowhere to go on a 375px screen, so below `lg` it
    collapses to a selector row that opens a sheet. Both the sidebar and this
    sheet render from NAV, so a new account page appears in both or neither.
    """
    rows = "".join(f"""
              <a href="{href}" class="flex items-center gap-3 px-1 py-4 border-neutral-divider border-b font-semibold text-base {'text-cta' if href == active_slug else 'text-[#003616]'}">
                {nav_icon(href, icon)}
                <span class="flex flex-1 items-center gap-2 min-w-0">
                  <span class="truncate">{e(label)}</span>{_nav_badge(href)}
                </span>
                <span class="text-neutral-secondary shrink-0">{_icon('chev', 'w-4 h-4')}</span>
              </a>""" for label, href, icon in NAV)

    return f"""
          <div class="lg:hidden flex flex-col gap-3 min-w-0">
            {tier_badge(CUSTOMER['tier'])}
            <h2 class="font-bold text-[#003616] text-xl">مرحبا {e(CUSTOMER['name'])}</h2>
            <button type="button" data-open="accountMenu" class="flex justify-between items-center gap-3 bg-white px-5 py-3.5 border border-neutral-divider rounded-full w-full font-semibold text-[#003616] text-base">
              <span class="flex items-center gap-3 min-w-0">
                <span class="text-cta shrink-0">{_icon('menu')}</span>
                <span class="truncate">{e(_active_label(active_slug))}</span>
              </span>
              <span class="-rotate-90 text-neutral-secondary shrink-0">{_icon('chev', 'w-4 h-4')}</span>
            </button>
          </div>

          <div data-sheet="account-menu" class="lg:hidden bottom-sheet">
            <div class="bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
            <div class="flex justify-between items-center mb-2">
              <h2 class="font-bold text-[#003616] text-lg">القائمة</h2>
              <button type="button" data-close class="place-items-center grid hover:bg-interaction-base border border-neutral-divider rounded-full w-8 h-8 text-[#003616]" aria-label="إغلاق">{_icon('close', 'w-4 h-4')}</button>
            </div>
            <nav class="flex flex-col">{rows}
            </nav>
            <button type="button" data-close class="bg-cta hover:bg-cta-hover mt-4 py-3 rounded-full w-full font-semibold text-white transition-colors">تأكيد</button>
          </div>"""


def account_page(title_text, description, content, page_id, path,
                 crumb, active_slug):
    # Breadcrumb: الرئيسية / حسابي / <page>. On the overview page itself the
    # page's crumb IS "حسابي", so the middle link and the current crumb would
    # duplicate (الرئيسية / حسابي / حسابي) — collapse to a single "حسابي"
    # (Ahmed, 2026-08-04).
    if active_slug == "my-account.html":
        trail = [("الرئيسية", "index.html"), ("حسابي", None)]
    else:
        trail = [("الرئيسية", "index.html"), ("حسابي", "my-account.html"), (crumb, None)]
    body = f"""{page_header("", trail)}

      <section class="py-6 xl:py-8">
        <div class="items-start gap-6 xl:gap-8 grid grid-cols-1 lg:grid-cols-[300px_1fr] mx-auto px-4 max-w-[1536px]">
{mobile_nav(active_slug)}
{sidebar(active_slug)}
          <div class="flex flex-col gap-6 min-w-0">{content}
          </div>
        </div>
      </section>"""
    return page(title_text, description, body, page_id, path)


def card(heading, inner, cta=None, cta_href="#"):
    action = (f'<a href="{cta_href}" class="hover:bg-interaction-base px-5 py-2 border '
              f'border-neutral-divider rounded-full font-semibold text-[#003616] text-xs '
              f'transition-colors">{e(cta)}</a>') if cta else ""
    # h2, not h3: these cards are the account page's top-level sections and
    # the only heading above them is the page h1, so h3 skipped a level and
    # broke heading-by-heading navigation on all seven account pages.
    head = (f'<div class="flex justify-between items-center gap-3">'
            f'<h2 class="font-bold text-[#003616] text-base">{e(heading)}</h2>{action}</div>'
            ) if heading else ""
    return (f'<div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">'
            f'{head}{inner}</div>')


DELIVERY_FEE = 30.0


def _oitems(cat, qtys):
    prods = in_category(cat, len(qtys))
    return [(p, q) for p, q in zip(prods, qtys)]


# Orders carry their own line items now (Ahmed, 2026-08-02) so the detail drawer
# can list them and the dashboard can offer a real re-order. Still placeholder —
# there is no orders endpoint (DESIGN-NOTES) — but each order's total is derived
# from its items + delivery, so the list row and the drawer agree instead of the
# decoupled 490 the old tuple carried. `step` is how far the tracker has advanced
# (0..3); a cancelled order shows no tracker.
ORDERS = [
    {"no": "#30941", "date": "28 مارس 2026", "status": "تحت التحضير",
     "tone": "amber", "step": 1, "items": _oitems("Coffee", [1, 2])},
    {"no": "#30942", "date": "21 مارس 2026", "status": "ملغي",
     "tone": "red", "step": 0, "items": _oitems("Nuts", [2, 1])},
    {"no": "#30943", "date": "14 مارس 2026", "status": "مكتمل",
     "tone": "green", "step": 3, "items": _oitems("Spices", [1, 1, 1])},
]

STATUS_STYLE = {
    "amber": "bg-accent-yellow text-[#003616]",
    "red": "bg-accent-error text-white",
    "green": "bg-primary text-white",
}


def status_badge(o):
    """Order status pill. An in-progress order (amber) carries a live pulsing
    dot (`.status-live-dot`, styles.css) so the status reads as active at a
    glance; completed and cancelled orders are settled and stay static (Ahmed,
    2026-08-04 — "make sure the order status is animated")."""
    live = o["tone"] == "amber"
    dot = '<span class="status-live-dot" aria-hidden="true"></span>' if live else ""
    return (f'<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full '
            f'font-semibold text-xs {STATUS_STYLE[o["tone"]]}">{dot}{e(o["status"])}</span>')


_ORDER_STEPS = ["تم الطلب", "جاري التحضير", "في الطريق إليك", "تم التسليم"]
_OCHECK = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m5 13 4 4L19 7" '
           'stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# One 3D visual per step (Ahmed, 2026-08-04): the client's rendered icons,
# replacing the earlier 🧾📦🛵🎉 emoji placeholders — order placed (receipt),
# preparing (packed box), in transit (delivery scooter), delivered (gift box).
# Rendered as <img> by order_tracker below; the build validates these refs.
_STEP_ART = [
    "images/jaad/icons/track-placed-3d.png",
    "images/jaad/icons/track-preparing-3d.png",
    "images/jaad/icons/track-transit-3d.png",
    "images/jaad/icons/track-delivered-3d.png",
]


def order_total(o):
    return sum(p["price"] * q for p, q in o["items"]) + DELIVERY_FEE


def order_tracker(step, subs=None):
    """Animated order tracker (Ahmed, 2026-08-04), shared across the dashboard,
    the order drawer AND the thank-you page so the progress reads as one thing
    everywhere. Each step carries its own visual inside a bubble; the connector
    up to the reached step is filled, the one entering the CURRENT step flows (a
    travelling shimmer), and the current bubble pulses so the status reads as
    live. All motion is CSS (`.order-track` in styles.css) and is disabled under
    prefers-reduced-motion — worst case is a plain, correct stepper.

    `subs` is an optional per-step subtitle list (the thank-you page passes it);
    the compact account trackers pass none, and the subtitles hide on mobile
    (styles.css) so the horizontal row stays uncramped."""
    # A DELIVERED order (the tracker has reached its final step) is terminal, so
    # that last node is DONE — a checkmark, not the in-progress spinner (Ahmed,
    # 2026-08-04). Only a genuinely in-progress step (placed/preparing/transit)
    # gets the spinner + travelling shimmer + arrows.
    last = len(_ORDER_STEPS) - 1
    delivered = step >= last
    cells = ""
    for i, label in enumerate(_ORDER_STEPS):
        done = i < step or (delivered and i == last)
        now = (i == step) and not delivered
        state = "is-done" if done else "is-now" if now else "is-todo"
        # Connector INTO this node (from the previous one): filled once the node
        # is reached, and animated ONLY on the segment entering an in-progress
        # step (never once delivered).
        conn = ""
        if i > 0:
            filled = "is-filled" if i <= step else ""
            active = "is-active" if now else ""
            # The connector ENTERING the current step carries flowing chevrons
            # that head toward it (styles.css .track-conn__arrows).
            arrows = ('<span class="track-conn__arrows"><b></b><b></b><b></b></span>'
                      if now else "")
            conn = f'<span class="track-step__conn {filled} {active}" aria-hidden="true">{arrows}</span>'
        # A small check badge marks a completed step's bubble.
        check = f'<span class="track-step__check">{_OCHECK}</span>' if done else ""
        sub = (f'<span class="track-step__sub">{e(subs[i])}</span>'
               if subs and i < len(subs) else "")
        art = f'<img src="{_STEP_ART[i]}" alt="" class="w-12 h-12 object-contain" />'
        cells += f"""
                <li class="track-step {state}">{conn}
                  <span class="track-step__art" aria-hidden="true">{art}{check}</span>
                  <span class="track-step__label">{e(label)}</span>{sub}
                </li>"""
    return f'<ol class="order-track" data-order-tracker>{cells}\n              </ol>'


# Kept for internal callers that used the private name.
_order_tracker = order_tracker


def _order_lines(o):
    return "".join(f"""
                <div class="flex items-center gap-3 py-3 border-neutral-divider border-b last:border-0">
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base p-1.5 rounded-lg w-14 h-14 object-contain shrink-0" loading="lazy" />
                  <div class="flex flex-col flex-1 min-w-0">
                    <span class="font-semibold text-[#003616] text-sm line-clamp-2">{e(p.get('nameAr') or p['name'])}</span>
                    <span class="text-neutral-secondary text-xs">عدد <span class="latin">{q}</span></span>
                  </div>
                  <span class="font-bold text-[#003616] text-sm latin shrink-0">EGP {money(p['price'] * q)}</span>
                </div>""" for p, q in o["items"])


def order_panel(o):
    """One order's full detail, rendered hidden inside the shared drawer and
    revealed by its id when a row is clicked (the favourites 'ship-all, reveal
    one' pattern) — so a shopper can open several orders in turn without leaving
    the list."""
    subtotal = order_total(o) - DELIVERY_FEE
    tracker = "" if o["tone"] == "red" else f'<div class="pb-1">{_order_tracker(o["step"])}</div>'
    return f"""
              <div data-order-panel data-order-id="{e(o['no'])}" hidden class="flex flex-col gap-4">
                <div class="flex flex-wrap justify-between items-center gap-2">
                  <h3 class="font-bold text-[#003616] text-base">طلب رقم <span class="latin">{e(o['no'])}</span></h3>
                  {status_badge(o)}
                </div>
                {tracker}
                <div class="flex flex-col">{_order_lines(o)}
                </div>
                <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
                  <div class="flex justify-between"><span class="text-neutral-secondary">الإجمالي الفرعي</span><span class="font-semibold text-[#003616] latin">EGP {money(subtotal)}</span></div>
                  <div class="flex justify-between"><span class="text-neutral-secondary">مصاريف التوصيل</span><span class="font-semibold text-[#003616] latin">EGP {money(DELIVERY_FEE)}</span></div>
                  <div class="flex justify-between items-center pt-2 border-neutral-divider border-t"><span class="font-bold text-[#003616]">الإجمالي</span><span class="font-bold text-[#003616] text-lg latin">EGP {money(order_total(o))}</span></div>
                </div>
                <div class="flex flex-col gap-1 bg-interaction-base p-3 rounded-xl text-neutral-secondary text-sm">
                  <span class="font-semibold text-[#003616]">عنوان التوصيل</span>
                  <span>شقة 3 - 220 شارع الحرية - الدور الأول</span>
                  <span>مصر الجديدة، القاهرة</span>
                </div>
              </div>"""


def order_drawer(orders):
    """Shared side-drawer holding every order's panel, opened by initOrders in
    scripts.js. Appended to the orders list and the dashboard."""
    panels = "".join(order_panel(o) for o in orders)
    # --left so it opens from the RIGHT in RTL — the OPPOSITE side to the cart
    # drawer (which is --right / left in RTL), at Ahmed's request. Its width is
    # widened past the 340px --left default in styles.css.
    return f"""
    <aside data-drawer="order" class="side-drawer side-drawer--left" aria-label="تفاصيل الطلب">
      <button type="button" data-close aria-label="إغلاق" class="drawer-close place-items-center grid bg-white shadow-custom3 rounded-full size-8 text-[#003616]">{_icon('close', 'w-3.5 h-3.5')}</button>
      <div class="flex justify-between items-center px-5 py-4 border-neutral-divider border-b">
        <h2 class="font-bold text-[#003616] text-lg">تفاصيل الطلب</h2>
      </div>
      <div class="flex-1 px-5 py-4 overflow-y-auto" data-order-panels>{panels}
      </div>
    </aside>"""


def order_rows(orders):
    """The orders table body — the WHOLE row is the target now (Ahmed,
    2026-08-02), opening the detail drawer, not a bordered 'view' button. A
    chevron is the affordance; role/tabindex + the keydown handler in scripts.js
    keep it keyboard-operable."""
    return "".join(f"""
                  <tr data-order-open="{e(o['no'])}" tabindex="0" role="button" aria-label="عرض تفاصيل الطلب {e(o['no'])}" class="group border-neutral-divider border-b last:border-0 cursor-pointer hover:bg-interaction-base focus-visible:bg-interaction-base transition-colors">
                    <td class="py-4 ps-2 font-semibold text-[#003616] text-sm latin">{e(o['no'])}</td>
                    <td class="py-4 text-neutral-secondary text-sm">{e(o['date'])}</td>
                    <td class="py-4">{status_badge(o)}</td>
                    <td class="py-4 font-semibold text-[#003616] text-sm latin">EGP {money(order_total(o))}</td>
                    <td class="py-4 pe-2 text-end"><span class="inline-flex justify-center items-center text-neutral-secondary group-hover:text-cta transition-colors size-8">{_icon('chev', 'w-4 h-4')}</span></td>
                  </tr>""" for o in orders)


def order_tracking_card(o):
    """Dashboard 'current order' widget — live tracker + a details button.

    The status pill is GONE (Ahmed, 2026-08-04): the animated tracker already
    shows the order is in preparation, so a "تحت التحضير" badge repeated it.
    Its slot in the header now holds the details button (moved up from the
    card's foot), so the header carries the one action worth taking."""
    return f"""
            <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              <div class="flex flex-wrap justify-between items-center gap-3">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-[#003616] text-base">تتبع طلبك الحالي</span>
                  <span class="font-semibold text-neutral-secondary text-sm latin">{e(o['no'])}</span>
                </div>
                <button type="button" data-order-open="{e(o['no'])}" class="bg-cta hover:bg-cta-hover px-6 py-2.5 rounded-full font-semibold text-white text-sm transition-colors">تفاصيل الطلب</button>
              </div>
              {_order_tracker(o['step'])}
            </div>"""


def reorder_card(o):
    """Dashboard 'last order' widget with a real re-order button — the hidden
    [data-reorder-item] payloads let scripts.js add the whole order back to the
    cart in one press."""
    items_data = "".join(
        f'<span data-reorder-item data-id="{e(p.get("id", 0))}" data-name="{e(_ptitle(p))}" '
        f'data-price="{p["price"]}" data-image="{e(p["image"])}" data-qty="{q}" hidden></span>'
        for p, q in o["items"]
    )
    thumbs = "".join(
        f'<img src="{e(p["image"])}" alt="" class="bg-interaction-base p-1 rounded-lg w-12 h-12 object-contain shrink-0" loading="lazy" />'
        for p, q in o["items"][:4]
    )
    return f"""
            <div data-reorder-card class="flex flex-wrap justify-between items-center gap-4 bg-white shadow-custom4 p-6 rounded-[20px]">
              {items_data}
              <div class="flex items-center gap-3 min-w-0">
                <div class="flex gap-1 shrink-0">{thumbs}
                </div>
                <div class="flex flex-col min-w-0">
                  <span class="font-bold text-[#003616] text-sm">آخر طلب <span class="latin">{e(o['no'])}</span></span>
                  <span class="text-neutral-secondary text-xs">{e(o['date'])} · <span class="latin">EGP {money(order_total(o))}</span></span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button type="button" data-order-open="{e(o['no'])}" class="hover:bg-interaction-base px-4 py-2 border border-neutral-divider rounded-full font-semibold text-[#003616] text-xs transition-colors">التفاصيل</button>
                <button type="button" data-reorder class="bg-cta hover:bg-cta-hover px-5 py-2 rounded-full font-semibold text-white text-xs transition-colors">إعادة الطلب</button>
              </div>
            </div>"""
