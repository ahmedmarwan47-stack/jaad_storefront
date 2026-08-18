"""Loyalty points — redesigned to mirror Exception's points page (Ahmed,
2026-08-04): an available-points card with a live progress bar to the next tier,
the membership-tier ladder, a "how to earn" grid, and a Redeem-Points modal that
converts points into wallet credit. All demo/client-side (no live endpoint,
DESIGN-NOTES §1); scripts.js initPoints/syncPointsUI keep the balance, the bar
and the wallet in step, persisted under jaad:pointsSpent."""
from _account import (
    CUSTOMER, POINT_TIERS, POINTS_PER_EGP, TIERS, account_page, account_title,
    card, tier_progress,
)

SLUG = "my-account-point.html"

# POINT_TIERS order → the shining metallic badge key (styles.css tier-badge--*).
_TIER_KEYS = ["silver", "gold", "platinum"]

# One earn rule per card. Emoji stand-ins for the 3D renders still to come
# (prompts handed to Ahmed) — the build validates asset refs, so these stay
# emoji until the files exist.
_EARN = [
    ("🛍️", "اكسب نقطة على كل جنيه", "على كل جنيه تشتريه من الموقع"),
    ("⭐", "قيّم مشترياتك", "نقاط إضافية عند تقييم المنتجات"),
    ("🎁", "مكافأة ترحيبية", "نقاط هدية عند إنشاء حساب جديد"),
    ("🎂", "عروض المناسبات", "نقاط مضاعفة في العروض الموسمية"),
]


def _tier_cards(current_idx):
    """The membership ladder. The current tier is inked and ringed; the others
    stay muted — a selected state that never reads like a hover (CLAUDE.md)."""
    cells = ""
    for i, (label, mn) in enumerate(POINT_TIERS):
        top = POINT_TIERS[i + 1][1] - 1 if i + 1 < len(POINT_TIERS) else None
        rng = f'<span class="latin">{mn:,}+</span>' if top is None else f'<span class="latin">{mn:,} – {top:,}</span>'
        cur = ' data-current' if i == current_idx else ''
        # The shining metallic membership badge (Ahmed, 2026-08-04) — same
        # gloss-swept badge as the sidebar, one per tier. No self-start here so
        # it centres in the card.
        blabel, bcls = TIERS[_TIER_KEYS[i]]
        badge = (f'<span class="tier-badge {bcls} inline-flex items-center px-3 py-1 '
                 f'rounded-full font-bold text-xs"><span class="relative z-10">{blabel}</span></span>')
        cells += f"""
                <div data-tier="{i}"{cur} class="tier-card flex flex-col items-center gap-2 p-4 border-2 rounded-2xl text-center">
                  {badge}
                  <span class="text-xs">{rng} نقطة</span>
                </div>"""
    return cells


def build():
    pts = CUSTOMER["points"]
    tp = tier_progress(pts)
    nxt_label = tp["next"][0] if tp["next"] else ""
    tonext = (f'<span class="latin">{tp["to_next"]:,}</span> نقطة للوصول لعضوية {nxt_label}'
              if tp["next"] else "وصلت لأعلى مستوى عضوية 🎉")
    earn = "".join(f"""
                <div class="flex flex-col gap-1 bg-white shadow-custom4 p-4 rounded-2xl">
                  <span class="place-items-center grid bg-interaction-base rounded-xl size-11 text-2xl" aria-hidden="true">{emoji}</span>
                  <span class="mt-1 font-bold text-[#003616] text-sm">{title}</span>
                  <span class="text-neutral-secondary text-xs leading-5">{sub}</span>
                </div>""" for emoji, title, sub in _EARN)

    content = f"""
            <div class="flex flex-wrap justify-between items-center gap-3">
              {account_title("my-account-point.html", "نقاطي")}
              <button type="button" data-open="pointsRedeem" class="btn-elevate flex items-center gap-2 bg-cta hover:bg-cta-hover px-6 py-3 rounded-full font-semibold text-white text-sm transition-colors">
                <span class="w-4 h-4">{_COIN}</span>استبدال النقاط
              </button>
            </div>

            <!-- Available points + live tier progress. data-points is the sync
                 root; data-points-base lets scripts.js recompute remaining after
                 a redeem without hard-coding the start. -->
            <div data-points data-points-base="{pts}" class="flex flex-col gap-5 bg-primary shadow-custom4 p-6 xl:p-7 rounded-[20px] text-white">
              <div class="flex items-center gap-4">
                <img src="images/jaad/icons/points-3d.png" alt="" class="w-16 h-16 object-contain shrink-0" />
                <div class="flex flex-col min-w-0">
                  <span class="text-white/70 text-sm">النقاط المتاحة</span>
                  <span class="font-bold text-4xl latin" data-points-balance>{pts:,}</span>
                </div>
              </div>
              <div>
                <div class="bg-white/20 rounded-full w-full h-2.5 overflow-hidden">
                  <div data-points-progress class="bg-accent-yellow rounded-full h-full transition-[width] duration-500" style="width:{tp['pct']}%"></div>
                </div>
                <p class="mt-2 text-white/80 text-xs text-end" data-points-tonext>{tonext}</p>
              </div>
            </div>

            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#003616] text-lg">مستويات العضوية</h2>
              <div class="gap-3 grid grid-cols-3" data-tier-cards>{_tier_cards(tp['idx'])}
              </div>
            </div>

            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#003616] text-lg">إزاي تكسب نقاط؟</h2>
              <div class="gap-3 grid grid-cols-2 lg:grid-cols-4">{earn}
              </div>
            </div>"""
    return account_page("نقاطي | جاد", "رصيد نقاطك وطرق استبدالها.",
                        content, "my-account-point", "/my-account/points",
                        "نقاطي", "my-account-point.html")


_COIN = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
         '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/>'
         '<path d="M12 7v10M9.5 9.5h3.2a1.8 1.8 0 0 1 0 3.6H10m0 0h3" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
