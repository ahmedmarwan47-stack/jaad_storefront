"""
Shared UI components for the Jaad static build.

THIS IS THE SINGLE SOURCE OF TRUTH for any markup that appears on more than
one page — product cards, category tiles, section headings, buttons, badges.
Edit a component here, run `python3 build/build.py`, and the change lands on
every page that uses it.

Split of responsibilities:
  * Chrome that is injected at runtime — header, footer, cart drawer, search,
    mobile menu — lives in static-export/scripts.js and updates with no
    rebuild at all.
  * Design tokens — colour, type scale, radii, shadows — live in
    static-export/tw-config.js and likewise need no rebuild.
  * Everything else (page content) is composed from the functions below and
    baked into static HTML so pages stay standalone and work from file://.
"""
import hashlib
import html as html_mod
import os
import re

from catalog import e, money, title

# Styled product photography (bag on a soft fabric ground with the product
# scattered around) — the Figma look. Exported from the design where available;
# keyed by product id. product_widget() prefers these over the plain white-bg
# catalog cutouts. IDs without a styled shot fall back to the catalog image.
_STYLED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static-export", "images", "jaad", "products-styled",
)
STYLED_IDS = (
    {os.path.splitext(f)[0] for f in os.listdir(_STYLED_DIR) if f.endswith(".jpg")}
    if os.path.isdir(_STYLED_DIR) else set()
)

# --------------------------------------------------------------------------
# Icons — generic UI glyphs. Brand marks and Figma-authored icons are real
# asset files under images/jaad/, never hand-drawn here.
# --------------------------------------------------------------------------
ICON = {
    "heart": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z" '
             'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
    "heart_full": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">'
                  '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z"/></svg>',
    # Note glyph — the order-note field's applied state. A clean lined card
    # (rounded rect + three text lines) reads better at 16px than a
    # folded-corner document. Wrapper-driven (w-full h-full + currentColor).
    "note": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<rect x="4" y="3.5" width="16" height="17" rx="3" stroke="currentColor" stroke-width="1.7"/>'
            '<path d="M8 8.5h8M8 12h8M8 15.5h5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    # X — removes an applied note / promo. Wrapper-driven.
    "close": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>',
    # Rounded warning triangle (Ahmed's alert-01.svg, 2026-08-04) — the
    # below-minimum-order notice. Recoloured to currentColor so it inherits the
    # error ink from its wrapper instead of the export's hard-coded #141B34.
    "alert": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M5.32171 9.68293C7.73539 5.41199 8.94222 3.27651 10.5983 2.72681C11.5093 2.4244 12.4907 2.4244 13.4017 2.72681C15.0578 3.27651 16.2646 5.41199 18.6783 9.68293C21.092 13.9539 22.2988 16.0893 21.9368 17.8293C21.7376 18.7866 21.2469 19.6549 20.535 20.3097C19.241 21.5 16.8274 21.5 12 21.5C7.17265 21.5 4.75897 21.5 3.46496 20.3097C2.75308 19.6549 2.26239 18.7866 2.06322 17.8293C1.70119 16.0893 2.90803 13.9539 5.32171 9.68293Z" stroke="currentColor" stroke-width="1.5"/>'
             '<path d="M12.2422 17V13C12.2422 12.5286 12.2422 12.2929 12.0957 12.1464C11.9493 12 11.7136 12 11.2422 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M11.992 9H12.001" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # Opening double-quote — testimonial cards. Two filled "66" blobs; the
    # caller sizes and colours it (accent yellow on the dark card).
    "quote": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">'
             '<path d="M10 6c-3.3 0-6 2.7-6 6v6h6v-6H7c0-1.7 1.3-3 3-3V6Z"/>'
             '<path d="M20 6c-3.3 0-6 2.7-6 6v6h6v-6h-3c0-1.7 1.3-3 3-3V6Z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/>'
             '<path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    # Horizontal chevron — carousel arrows, "read more" links. Mirrored in RTL
    # by the caller with rtl:scale-flip / ltr:scale-flip.
    "arrow": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<path d="M15 6 9 12l6 6" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # Vertical chevron — accordions and dropdowns, where direction is not
    # affected by writing direction.
    "chevron": '<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
               '<path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # --- Product-page trust row and social proof -------------------------
    # Wrapper-driven like everything else in here: no size class on the svg,
    # `currentColor` throughout, so the caller owns colour and scale.
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">'
            '<path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.58 1.11 6.47L12 17.44 '
            '6.19 20.5 7.3 14.03 2.6 9.45l6.5-.95L12 2.6Z"/></svg>',
    "flame": '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">'
             '<path d="M12.9 2.3c.26 2.2-.53 3.63-1.86 4.9-1.3 1.24-2.9 2.4-3.7 4.6a6.9 6.9 0 0 0 '
             '2.03 7.7c-.5-1.5-.3-3.1.86-4.2.9-.86 1.5-1.7 1.8-2.8.9 1 1.5 2 1.7 3.2.2 1.2 0 2.4-.5 3.6a6.9 '
             '6.9 0 0 0 3.6-6.2c-.05-3.6-2.3-5.9-3.94-10.8Z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h8A1.5 1.5 0 0 1 14 7.5V16H3V7.5Z" '
             'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M14 10h3.2c.4 0 .8.18 1.1.5l2.2 2.4c.3.3.5.7.5 1.1V16h-7v-6Z" '
             'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<circle cx="7" cy="17.5" r="1.9" stroke="currentColor" stroke-width="1.6"/>'
             '<circle cx="17" cy="17.5" r="1.9" stroke="currentColor" stroke-width="1.6"/></svg>',
    "return": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
              '<path d="M4 5v5h5" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M4.6 10a8 8 0 1 1-.4 5" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M20 4c0 9-5.2 13-11 13a5.6 5.6 0 0 1-5-2.6C6.5 7.6 12.3 4.6 20 4Z" '
            'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M4 20c1.6-4.6 4.6-7.7 9-9.6" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M13.2 2.5 5 13.4h5.6L9.8 21.5 18 10.6h-5.6l.8-8.1Z" stroke="currentColor" '
            'stroke-width="1.6" stroke-linejoin="round"/></svg>',
    # Stepper glyphs. SVG, not the ASCII −/+ they replace: a text glyph sits
    # on a baseline inside a line box, so grid-centring the box still leaves
    # the mark itself optically off-centre (Ahmed flagged it on the product
    # stepper). A viewBox-centred path has no baseline to drift on.
    "plus": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round"/></svg>',
    "minus": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M5 12h14" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
              '<path d="M12 3.2 5 5.8v5.4c0 4.2 2.9 7.6 7 9.6 4.1-2 7-5.4 7-9.6V5.8L12 3.2Z" '
              'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
              '<path d="m9.2 11.8 2 2 3.6-3.8" stroke="currentColor" stroke-width="1.6" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "store": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M4 9.5V19a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9.5" stroke="currentColor" '
             'stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M3.2 6.2 4.6 4h14.8l1.4 2.2a3 3 0 0 1-5.4 2.6 3 3 0 0 1-5.4 0 3 3 0 0 1-5.4 0 '
             '3 3 0 0 1-1.4-2.6Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
             '<path d="M10 20v-4.5h4V20" stroke="currentColor" stroke-width="1.6" '
             'stroke-linejoin="round"/></svg>',
    # Wrapper-driven like every other glyph here: w-full h-full + currentColor,
    # so the caller's span sets the size. The copy that used to live as
    # ICON_GIFT in pages/checkout.py carried its own `w-6 h-6` and fought its
    # wrapper — see the icons trap in CLAUDE.md.
    "gift": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
            '<path d="M20 12v9H4v-9M22 7H2v5h20V7ZM12 21V7M12 7H7.5a2.5 2.5 0 1 1 0-5C11 2 12 7 12 7Z'
            'M12 7h4.5a2.5 2.5 0 1 0 0-5C13 2 12 7 12 7Z" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="m5 12.5 4.5 4.5L19 7.5" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>',
    # Must stay identical to ICON.trash in scripts.js — the product page draws
    # this one at build time and the cart rows draw that one at runtime, and
    # they are the same control in the shopper's eyes.
    "trash": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
             '<path d="M4 7h16M10 4h4M9 7v11m6-11v11M6 7l.8 12.1A2 2 0 0 0 8.8 21h6.4a2 2 0 0 0 2-1.9L18 7" '
             'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
             'stroke-linejoin="round"/></svg>',
    # Same artwork as the account sidebar's wallet glyph in pages/_account.py,
    # so the toggle on the cart and the page it refers to draw the same mark.
    "wallet": '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full">'
              '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" '
              'stroke="currentColor" stroke-width="1.7"/>'
              '<path d="M16 12h3" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round"/></svg>',
    # Shopping-cart glyph — exact path from the Figma product widget's add
    # button (node 4994:7438). Wrapper-driven, currentColor.
    "cart": '<svg viewBox="0 0 20 19" fill="none" class="w-full h-full">'
            '<path d="M3.75 3.75V9.43333C3.75 10.9735 3.75 11.7436 4.04973 12.3318C4.31338 12.8493 4.73408 13.27 5.25153 13.5336C5.83978 13.8333 6.60986 13.8333 8.15 13.8333H12.7308C13.745 13.8333 14.2521 13.8333 14.697 13.676C15.0903 13.5369 15.4468 13.3102 15.7396 13.0129C16.0707 12.6767 16.2857 12.2175 16.7157 11.299L17.3165 10.0157C18.2915 7.93326 18.7789 6.89207 18.6388 6.04904C18.5164 5.31257 18.0998 4.65752 17.4847 4.23437C16.7806 3.75 15.631 3.75 13.3316 3.75H3.75ZM3.75 3.75V3.6757C3.75 2.89117 3.75 2.4989 3.63192 2.18601C3.44591 1.69313 3.05687 1.30409 2.56399 1.11809C2.2511 1 1.85883 1 1.0743 1H1M5.58333 17.5H6.5M12 17.5H12.9167" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


# The one source for the demo wallet balance. pages/_account.py reads this for
# CUSTOMER["wallet"], and the cart/checkout toggle renders it into its own
# data attribute, which scripts.js reads at click time. Defined here because
# components is imported BY the pages, never the other way round, so this is
# the lowest point both can see.
#
# It exists as a constant at all because the figure it replaced did NOT have
# one: the old points banner defaulted to 100 in one place and was called with
# 120 in another, and the cart and checkout spent months quoting different
# balances. Demo state either way — there is no wallet endpoint, see
# DESIGN-NOTES §1.
WALLET_BALANCE = 1200


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------
def button(label, href="#", variant="primary", size="md", extra="", full_mobile=True):
    """The one pill-button component. variant: primary | secondary | accent | outline

    Emits the shared `.btn` component classes (styles.css) ALONGSIDE the Tailwind
    utilities that actually paint the button. The utilities are kept on purpose:
    they keep the rendered result byte-identical AND they are what the runtime
    `data-btn="v2"` A/B toggle matches on (`a.bg-cta` / `a.border-cta` /
    `.rounded-full`), so the green/orange switch keeps working. Every `.btn--*`
    rule is defined to the SAME value as the utility it sits beside, so nothing
    repaints — the classes are just a semantic hook and a no-Tailwind fallback.

    Variants:
      primary   — bg-cta green pill, white label             (.btn--primary)
      secondary — cta-green outline, green label; the legacy pattern the section
                  headings and the rewards page use. Kept exactly as-is: it
                  carries the `.btn` base only, its outline stays on the
                  utilities, so the grey `.btn--secondary` rule never lands on it.
      accent    — lime fill, dark-green label                (.btn--accent)
      outline   — neutral-divider hairline, dark-green label (.btn--secondary)

    `href=None` is accepted and treated as "#", for a button wired up in JS
    rather than being a real link.

    `full_mobile` (default True): the button fills its container's width below
    `sm` and returns to content-width from 640px up (Ahmed, 2026-08-05) — the
    mobile pattern where a standalone CTA spans the column rather than sitting as
    a small pill against an empty gutter. Pass `full_mobile=False` for a button
    that must stay inline on a phone (the section-heading "view more" link, which
    rides on the heading's own row).
    """
    if href is None:
        href = "#"
    sizes = {
        "sm": "px-6 py-2.5 text-sm",
        "md": "px-8 py-3 text-base",
        "lg": "px-8 py-4 text-base xl:text-lg",
    }
    variants = {
        "primary": "bg-cta hover:bg-cta-hover text-white",
        "secondary": "border border-cta text-cta hover:bg-interaction-base",
        "accent": "bg-accent-yellow hover:bg-accent-500 text-[#003616]",
        "outline": "border border-neutral-divider hover:border-primary text-[#003616]",
    }
    # `.btn` component hook. The legacy green `secondary` keeps the base only, so
    # the grey `.btn--secondary` rule (the `outline` look) never repaints it.
    btn_hook = {
        "primary": "btn btn--primary",
        "secondary": "btn",
        "accent": "btn btn--accent",
        "outline": "btn btn--secondary",
    }
    width = "w-full sm:w-auto " if full_mobile else ""
    return (f'<a href="{href}" class="{btn_hook[variant]} inline-flex justify-center items-center rounded-full '
            f'font-semibold transition-colors {width}{sizes[size]} {variants[variant]} {extra}">{e(label)}</a>')


def section_heading(heading, cta_label=None, cta_href="#", centered=False):
    """Section title with an optional trailing link — Figma 'Section Header'.

    Type treatment matches the homepage's section headings (Ahmed, 2026-08-20):
    Figma's Primary/Dark Green #29612F at `font-medium` 32/40px, not the old
    `font-bold text-[#003616] text-3xl xl:text-4xl`. That older pairing came
    from the brand-manual-derived config, before the real Figma variables were
    pulled; it left every inner page's section titles heavier and a different
    green from the homepage that links to them.
    """
    if centered:
        return (f'<h2 class="mb-10 xl:mb-12 font-medium text-[#29612F] text-[32px] md:text-[40px] '
                f'leading-[1.2] text-center">{e(heading)}</h2>')
    cta = button(cta_label, cta_href, "secondary", "sm", full_mobile=False) if cta_label else ""
    return (f'<div class="flex flex-wrap justify-between items-center gap-4 mb-10">'
            f'<h2 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">'
            f'{e(heading)}</h2>{cta}</div>')


def carousel(slides_html, gap=24, arrows_top="130px", autoplay=False, dots=False, extra="", track_attr=""):
    """
    Direction-agnostic carousel shell. The JS in scripts.js drives it on a
    logical scroll axis so it behaves identically in RTL and LTR.

    `track_attr` tags the `.carousel-track` itself (e.g. a `data-*` marker),
    for the rare caller that needs to find ITS track specifically when a page
    holds more than one carousel — plain string, not `extra`, because `extra`
    lands on the outer `.carousel` wrapper instead.
    """
    return f"""
          <div class="relative carousel {extra}"{' data-autoplay' if autoplay else ''} style="--carousel-gap:{gap}px">
            <div class="carousel-track"{track_attr}>{slides_html}
            </div>
            <!-- The side offset is set in styles.css on .carousel-prev/.next
                 (centre ON the track border, -22px = half the 44px circle):
                 a -start/-end utility here ties with that rule and loses on
                 source order, same as the hero arrows. -->
            <button type="button" class="hidden xl:grid top-[{arrows_top}] absolute place-items-center bg-white shadow-custom3 rounded-full text-cta transition size-11 carousel-prev" aria-label="السابق">
              <span class="rtl:scale-flip">{ICON['arrow']}</span>
            </button>
            <button type="button" class="hidden xl:grid top-[{arrows_top}] absolute place-items-center bg-white shadow-custom3 rounded-full text-cta transition size-11 carousel-next" aria-label="التالي">
              <span class="ltr:scale-flip">{ICON['arrow']}</span>
            </button>
            {'<div class="flex justify-center mt-4 carousel-dots"></div>' if dots else ''}
          </div>"""


def breadcrumb(trail):
    """trail: [(label, href|None)] — the last item is the current page."""
    parts = []
    for i, (label, href) in enumerate(trail):
        last = i == len(trail) - 1
        if last or not href:
            parts.append(f'<span class="font-semibold text-[#003616]">{e(label)}</span>')
        else:
            parts.append(
                # link-sweep: on hover the crumb darkens to primary AND an
                # underline sweeps in (RTL-aware ::after in styles.css), the same
                # affordance the footer/account links already use — extend the
                # shared interaction system rather than paint a one-off border
                # (CLAUDE.md). self-start keeps the sweep tight to the text.
                f'<a href="{href}" class="link-sweep text-neutral-secondary hover:text-primary transition-colors">{e(label)}</a>'
                # Decorative separator: hidden from assistive tech, and
                # toned up from #C6C6C6 (1.71:1) so it is still visible.
                f'<span aria-hidden="true" class="text-neutral-outline">/</span>')
    return (f'<nav aria-label="مسار التنقل" class="flex flex-wrap items-center gap-2 text-sm">'
            f'{"".join(parts)}</nav>')


def chip(label, href="#", active=False, filter_slug=None):
    """Filter pill — Figma 'Chip Button'.

    The mobile Collection frame (350:17805) fills inactive chips with
    interaction-base and drops the outline; the desktop Web frame keeps the
    white-on-outline treatment. Carry both rather than pick one.
    """
    style = ("bg-cta text-white border-cta" if active
             else "chip-filter bg-white text-[#003616] border-neutral-divider hover:border-cta")
    # `filter_slug` turns the chip into a live client-side filter; without it
    # the chip stays a plain link. The href is kept either way so the control
    # still means something with JS off.
    attr = f' data-filter="{e(filter_slug)}"' if filter_slug else ""
    # min-h-11 = 44px: WCAG 2.5.5 / HIG minimum tap target. At px-5 py-2 these
    # measured 38px, which is a miss on a phone. The 44px floor is kept on
    # mobile (touch); on xl the chips shrink to min-h-9 / px-4 (Ahmed,
    # 2026-08-04) so the whole row fits BESIDE the sort pill without crowding
    # it — a mouse does not need 44px, and 36px clears the 24px WCAG 2.5.8 AA
    # floor comfortably.
    return (f'<a href="{href}"{attr} class="inline-flex items-center min-h-11 xl:min-h-9 px-5 xl:px-4 py-2 xl:py-1.5 border rounded-full '
            f'font-semibold text-sm xl:text-[13px] whitespace-nowrap transition-colors {style}">{e(label)}</a>')


_SORT_ICON = ('<svg viewBox="0 0 24 24" fill="none" class="w-4 h-4" aria-hidden="true">'
              '<path d="M7 4v16m0 0-3-3m3 3 3-3M17 20V4m0 0-3 3m3-3 3 3" '
              'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
              'stroke-linejoin="round"/></svg>')

# Down chevron for the sort pill — wrapper-driven (no size on the svg), so the
# w-3.5 span in sort_select owns its scale. Signals "this opens a menu".
_SORT_CHEVRON = ('<svg viewBox="0 0 24 24" fill="none" class="w-full h-full" '
                 'aria-hidden="true"><path d="m6 9 6 6 6-6" stroke="currentColor" '
                 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def sort_select(options, label="ترتيب حسب"):
    """Sort control.

    The mobile Collection frame (350:17805) shows this bare — a sort glyph and
    the current value, no chrome and no 'ترتيب حسب' prefix. Desktop keeps that
    minimal content and only adds the outlined pill around it (Ahmed,
    2026-07-27): the old desktop variant carried the full 'ترتيب حسب' prefix
    AND a native <select> (its own arrow, its own border inside the pill's
    border), which was wide enough to crowd the chip row beside it. Now both
    breakpoints read `↕ <value> ⌄`; only the pill chrome is xl-only.

    The chevron is drawn here, not by the browser: `appearance-none` on both
    breakpoints drops the native arrow so the glyph is consistent and sits
    inside the pill rather than at the select's own edge. The label survives as
    `aria-label` — the sort glyph and chevron carry the meaning visually.
    """
    opts = "".join(f'<option value="{e(v)}">{e(t)}</option>' for v, t in options)
    first_text = e(options[0][1]) if options else ""
    # Custom-dropdown option rows, rendered at build time so translateDocument
    # translates their labels in place (same Arabic keys as the native
    # <option>s). initFancySelect() in scripts.js only wires behaviour.
    li = "".join(f"""
                <li role="option" data-fancy-opt data-value="{e(v)}" aria-selected="{'true' if i == 0 else 'false'}"
                    class="flex items-center gap-2 px-3 py-2 rounded-xl cursor-pointer text-sm font-medium text-[#003616] hover:bg-interaction-base focus-visible:bg-interaction-base focus:outline-none transition-colors">
                  <span class="w-4 h-4 shrink-0 text-cta" data-fancy-check>{ICON['check']}</span>
                  <span data-opt-text class="whitespace-nowrap">{e(t)}</span>
                </li>""" for i, (v, t) in enumerate(options))
    return f"""
            <div class="relative shrink-0 text-start" data-fancy-select>
              <!-- Native select: the source of truth, the mobile control (the OS
                   picker beats a custom popover on a phone) and the no-JS
                   fallback. On desktop, initFancySelect() hides this and shows
                   the custom trigger; a pick there writes back here + fires
                   change, so the listing sort (which reads this value) is
                   untouched. -->
              <label class="inline-flex items-center gap-2 xl:bg-white px-0 xl:px-4 py-2 rounded-full" aria-label="{e(label)}" data-fancy-fallback>
                <span class="text-cta shrink-0">{_SORT_ICON}</span>
                <select class="select-sort bg-transparent font-semibold text-[#003616] text-sm outline-none cursor-pointer appearance-none border-0">{opts}</select>
                <span class="text-neutral-secondary w-3.5 h-3.5 shrink-0 pointer-events-none">{_SORT_CHEVRON}</span>
              </label>

              <!-- Custom dropdown (desktop). Starts fully hidden so no-JS keeps
                   the native select; JS switches it to `hidden xl:block`. -->
              <div class="hidden" data-fancy-ui>
                <button type="button" data-fancy-trigger aria-haspopup="listbox" aria-expanded="false" aria-label="{e(label)}"
                        class="inline-flex items-center gap-2 bg-interaction-base hover:bg-interaction-tertiary-hover px-4 py-2 rounded-full font-semibold text-[#003616] text-sm transition-colors">
                  <span class="text-cta shrink-0">{_SORT_ICON}</span>
                  <span data-fancy-label class="whitespace-nowrap">{first_text}</span>
                  <span class="text-neutral-secondary w-3.5 h-3.5 shrink-0 pointer-events-none">{_SORT_CHEVRON}</span>
                </button>
                <ul role="listbox" tabindex="-1" data-fancy-pop
                    class="hidden top-full end-0 z-40 absolute bg-white shadow-custom3 mt-2 p-1.5 border border-neutral-divider rounded-2xl min-w-[220px]">{li}
                </ul>
              </div>
            </div>"""


def page_header(heading, trail=None):
    """
    Breadcrumb + page title block used by every inner page.

    `heading` is empty on the pages that carry their own title further down
    (product, blog post, account, auth). Those must emit NO h1 here: an empty
    one is announced as a blank level-1 heading and left every one of those
    113 pages with two h1s, the first of them silent.
    """
    crumbs = f"{breadcrumb(trail)}" if trail else ""
    # Same Figma heading treatment as section_heading / the homepage h2s.
    head = (
        f'\n          <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] '
        f'leading-[1.2]">{e(heading)}</h1>'
        if heading
        else ""
    )
    return f"""
      <section class="pt-6">
        <div class="flex flex-col gap-4 mx-auto px-4 max-w-[1536px]">
          {crumbs}{head}
        </div>
      </section>"""


def product_grid(products, cols="grid-cols-2 md:grid-cols-3 xl:grid-cols-4", attrs="",
                 cat_of=None):
    """`attrs` lets a caller tag the grid (e.g. the favourites page marks its
    own with data-favs-grid) without duplicating the card markup.

    `cat_of(product) -> slug` overrides each card's `data-cat` — used by a
    category page to filter on a DERIVED sub-category instead of the top-level
    categorySlug (see shop_category.py)."""
    cards = "".join(
        product_card(p, slide=False, cat=(cat_of(p) if cat_of else None))
        for p in products
    )
    extra = (" " + attrs) if attrs else ""
    return f'<div data-product-grid{extra} class="gap-4 xl:gap-6 grid {cols}">{cards}\n          </div>'


def rating(score="4.8", count=None):
    """
    Five marks that actually show the score. 4.8 draws four full and the fifth
    filled 80% of the way across — a row of five identical full marks beside
    the text "4.8" contradicts itself, which is what this used to do.

    The partial mark is one glyph layered over another and clipped by width,
    not a second half-glyph asset: the empty and full states stay the same
    shape, so nothing can drift if the icon is ever redrawn. The clip is on the
    INLINE axis via a logical inset, so in RTL it fills from the right like the
    row does.

    Marks are STARS by Ahmed's direction (2026-07-22). They started as the
    brand heart; on the product page a row of hearts read as favourites, not
    reviews — the same glyph the card's save button uses, one gesture away.
    The heart stays for favourites only.
    """
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 0.0

    marks = []
    for i in range(5):
        # How much of THIS mark is filled: 1 for a whole one, the remainder on
        # the boundary mark, 0 after it.
        fill = max(0.0, min(1.0, value - i))
        if fill >= 0.999:
            marks.append(f'<span class="rating-mark is-full">{ICON["star"]}</span>')
        elif fill <= 0.001:
            marks.append(f'<span class="rating-mark">{ICON["star"]}</span>')
        else:
            pct = round(fill * 100)
            marks.append(
                f'<span class="rating-mark">{ICON["star"]}'
                f'<span class="rating-mark__fill" style="width:{pct}%">{ICON["star"]}</span>'
                f'</span>')
    tail = (f'<span class="text-neutral-secondary text-sm">(<span class="latin">{count}</span> تقييم)</span>'
            if count else "")
    return (f'<div class="flex items-center gap-1.5">'
            f'<span class="rating-marks flex items-center" role="img" '
            f'aria-label="{e(score)} من 5">{"".join(marks)}</span>'
            f'<span class="font-semibold text-[#003616] text-sm latin">{e(score)}</span>{tail}</div>')


def variant_chips(options, name="variant"):
    """Generic chip selector. options: [(label, active)] — no pricing."""
    items = "".join(
        f'<label class="cursor-pointer">'
        f'<input type="radio" name="{e(name)}" class="peer sr-only"{" checked" if active else ""} />'
        f'<span class="inline-flex items-center px-5 py-2 border border-neutral-divider rounded-full '
        f'font-semibold text-[#003616] text-sm transition-colors peer-checked:bg-cta '
        f'peer-checked:border-cta peer-checked:text-white">{e(label)}</span></label>'
        for label, active in options
    )
    return f'<div class="flex flex-wrap gap-2">{items}</div>'


def size_chips(p):
    """
    Real size options with real prices, from `sizes` in catalog.json
    (written by `fetch_sizes.py` — each one is a separate live SKU).

    Renders nothing at all unless the product genuinely has more than one size.
    The three chips this replaces — 500/250/100 جم — were invented, inert, and
    contradicted the 300 جم product they sat beneath.

    Each chip carries the size's own price and product id, so scripts.js can
    repoint the price AND the cart at the SKU actually chosen. Selecting 200 جم
    must not add the 100 جم SKU to the basket.
    """
    sizes = p.get("sizes") or []
    if len(sizes) < 2:
        return ""

    # Pre-select the size this page's product IS, not simply the first chip.
    current = p.get("id")
    if not any(str(s.get("id")) == str(current) for s in sizes):
        current = sizes[0].get("id")

    chips = "".join(
        f'<label class="cursor-pointer">'
        f'<input type="radio" name="size" class="peer sr-only"'
        f'{" checked" if str(s.get("id")) == str(current) else ""} '
        f'data-size-option data-size-id="{e(str(s.get("id")))}" '
        f'data-size-price="{s.get("price", 0)}" data-size-label="{e(s.get("label", ""))}" />'
        f'<span class="inline-flex items-center px-5 py-2 border border-neutral-divider rounded-full '
        f'font-semibold text-[#003616] text-sm transition-colors peer-checked:bg-cta '
        f'peer-checked:border-cta peer-checked:text-white latin">{e(s.get("label", ""))}</span>'
        f'</label>'
        for s in sizes
    )
    return f"""
            <div class="flex flex-col gap-2">
              <span class="font-semibold text-neutral-secondary text-xs">اختر الحجم</span>
              <div class="flex flex-wrap gap-2" data-size-chips>{chips}
              </div>
            </div>"""


def qty_stepper(cart_bound=False):
    """
    The reference Ahmed supplied draws the stepper as a padded container with
    the buttons as their own bordered shapes floating inside it — the padding
    between container and buttons is the point. Ours keeps that construction
    in this design system: circles rather than squares, the + carries the CTA
    fill (it is the "more" affordance, the louder of the two), the − stays
    quiet on a hairline. Buttons stay size-11: the reference's ~32px buttons
    would regress the audited 44px tap-target floor. THIS is the canonical
    counter; the product cards adopt it (Ahmed, 2026-08-18), not the reverse.

    `cart_bound=True` adds `data-cart-bound`, which changes who owns the
    number. A plain stepper owns its own count and hands it to whatever reads
    it; a cart-bound one writes straight to the store and reads the figure back
    from it — + is what puts the product in the basket, with no separate "add"
    press. initSteppers skips these deliberately: they are driven by the
    delegated handler in the cart section instead, so there is exactly one
    writer. Used by the product page.

    **It rests at 1, not 0** (Ahmed, 2026-07-26). 0 was the literal reading of
    "mirror the cart line", and it was right about the data and wrong about the
    page: a product page opens on a shopper who has not decided anything yet,
    and a zero there reads as out of stock.

    That leaves two states drawn with the same digit — "1, not in the basket"
    and "1, in the basket" — so the − button carries the difference, and it is
    the only thing that needs to:

        not in basket   − is disabled and dimmed, minus glyph
        1 in basket     − is live, trash glyph, error ink
        2+ in basket    − is live, minus glyph

    So the first + does not move the digit; it activates the −, throws the ghost
    to the cart and ticks the badge. The number is honest in both states and the
    press is still visibly answered — see syncBuyBlock in scripts.js.
    """
    bound = " data-cart-bound" if cart_bound else ""
    # Grey trash, not error red (Ahmed, 2026-07-26). Red reads as a warning,
    # and removing one line from a basket is not one — it is ordinary editing,
    # and reversible in a tap. neutral.secondary is the project's grey and
    # measures 6.39:1 on white, so it stays AA.
    dec_inner = (
        f"""<span class="w-5 h-5" data-line-dec-minus>{ICON['minus']}</span>"""
        f"""<span class="w-5 h-5 text-neutral-secondary" data-line-dec-trash hidden>{ICON['trash']}</span>"""
        if cart_bound else f"""<span class="w-5 h-5">{ICON['minus']}</span>"""
    )
    dec_attr = " data-line-dec" if cart_bound else ""
    return f"""
              <div data-stepper{bound} class="inline-flex items-center gap-1 bg-white p-1 border border-neutral-divider rounded-full">
                <button type="button" data-step="-1"{dec_attr} class="place-items-center grid border border-neutral-divider hover:bg-interaction-base rounded-full size-11 text-[#003616] transition-colors" aria-label="إنقاص">{dec_inner}</button>
                <span data-qty class="min-w-[2.5ch] font-bold text-[#003616] text-base text-center latin">1</span>
                <button type="button" data-step="1" class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-11 text-white transition-colors" aria-label="زيادة"><span class="w-5 h-5">{ICON['plus']}</span></button>
              </div>"""


def accordion(items, multi=False):
    """items: [(heading, inner_html)] — first is open."""
    rows = "".join(f"""
                <div class="faq-card accordion-item rounded-xl overflow-hidden{' is-open' if i == 0 else ''}">
                  <button type="button" class="accordion-trigger flex justify-between items-center gap-3 px-4 py-3.5 w-full text-start">
                    <span class="faq-q text-[15px] leading-snug">{e(heading)}</span>
                    <span class="place-items-center grid size-5 text-[#006328] shrink-0">
                      <span class="faq-plus w-4 h-4">{ICON['plus']}</span>
                      <span class="faq-minus w-4 h-4">{ICON['minus']}</span>
                    </span>
                  </button>
                  <div class="accordion-panel">
                    <div class="px-4 pb-4 text-[#4b5563] text-sm leading-[1.55]">{body}</div>
                  </div>
                </div>""" for i, (heading, body) in enumerate(items))
    return f'<div class="flex flex-col gap-2" data-accordion{" data-accordion-multi" if multi else ""}>{rows}\n              </div>'


def product_gallery(images, alt, p=None):
    """
    Main image with a selectable thumbnail strip — RTL puts thumbs on the far
    side. `images` is the product's real `images` list from catalog.json, main
    shot first; `fetch_galleries.py` fills it from the client's own CDN.

    `p` (optional) is the product dict; when given, the favourites heart is
    drawn on the main plate. It carries its OWN data-product/id/name/price/image
    because the gallery sits in a separate column from the details host, so
    productFrom() (which walks to the nearest [data-product]) would otherwise
    find nothing. The extra host is invisible to every other [data-product]
    consumer — they all guard on a child (price display, stepper, add button)
    the heart does not have.

    The strip is suppressed entirely at one image, because a lone thumbnail
    under a photo reads as a broken carousel rather than a choice. 26 of the 99
    products are in that state today (see DESIGN-NOTES) — they degrade to
    exactly the single-image layout this page had before.

    Selection state is `aria-pressed` on the button and nothing else, the same
    contract the favourites heart uses, so the accessible state and the painted
    state cannot drift; styles.css draws the ring off that selector.
    """
    images = [i for i in (images or []) if i]
    if not images:
        return ""
    main_img = images[0]

    # Favourites heart, overlaid on the main plate. top-4 end-4: inset by its
    # own padding, and `end` (a logical property) puts it top-left in RTL — the
    # mirror of the conventional top-right wishlist heart. Same fav-btn contract
    # as everywhere else; carries its own product data (see docstring).
    fav_btn = ""
    if p:
        fav_price = p.get("sale") or p.get("price") or 0
        fav_btn = (
            f'<button type="button" data-fav-toggle aria-pressed="false" aria-label="أضف إلى المفضلة" '
            f'data-product data-id="{p.get("id", 0)}" data-name="{e(title(p))}" '
            f'data-price="{fav_price}" data-image="{e(p["image"])}" '
            f'class="fav-btn btn-elevate absolute top-4 end-4 z-10 place-items-center grid '
            f'bg-white/90 hover:bg-white shadow-custom4 rounded-full text-cta size-11">'
            f'{ICON["heart"]}{ICON["heart_full"]}</button>'
        )

    # The main shot is a background-isolated cutout and has to sit INSIDE the
    # plate with padding, contained. Every other shot is a real photograph with
    # its own background, and containing those leaves the photo floating in a
    # letterboxed island of #FDF8F1 — the "weird appearance". Those fill the
    # frame edge to edge instead. `fetch_galleries.py` puts gallery shots in
    # their own directory, which is exactly the signal for which is which.
    def _is_photo(path):
        # products-styled/ holds full beige-linen scene photos (JAAD gallery
        # shots), so they fill the plate edge-to-edge like the /gallery/ ones
        # rather than sitting padded inside it as cut-outs (Ahmed, 2026-08-18).
        return "/gallery/" in path or "/products-styled/" in path

    if len(images) == 1:
        strip = ""
    else:
        thumb_html = "".join(f"""
                <button type="button" data-gallery-thumb aria-pressed="{'true' if i == 0 else 'false'}"
                        aria-label="عرض الصورة {i + 1} من {len(images)}"
                        data-fill="{'cover' if _is_photo(t) else 'contain'}"
                        class="gallery-thumb bg-interaction-base rounded-xl w-20 h-20 shrink-0 overflow-hidden{'' if _is_photo(t) else ' p-2'}">
                  <img src="{e(t)}" alt=""
                       class="w-full h-full {'object-cover' if _is_photo(t) else 'object-contain'}" loading="lazy" />
                </button>""" for i, t in enumerate(images))
        # The vertical strip is capped to the height of the plate beside it and
        # scrolls past that. Without the cap, nine 80px thumbnails stack 720px
        # tall, make themselves the tallest thing in the row and drag the whole
        # product header down with them — the richest galleries, which are the
        # ones worth having, broke the layout worst. The cap is the plate's own
        # box: p-6 + 300 at md, p-10 + 440 at xl.
        strip = f"""
            <div data-gallery-strip class="flex md:flex-col gap-3 md:max-h-[348px] xl:max-h-[520px]
                        overflow-x-auto md:overflow-x-hidden md:overflow-y-auto no-scrollbar shrink-0">{thumb_html}
            </div>"""

    return f"""
          <!-- The gallery is FIRST in the DOM (see product.py), so it needs no
               `order-*` override any more: it leads on mobile, which is what the
               Figma mobile frame (918:34326) asks for, and at lg it takes the
               RTL-right / LTR-left column. The old `order-first lg:order-none`
               pair existed only to pull it above an info column that used to
               come first; both are gone rather than left as no-ops.

               Sticky is no longer on the gallery itself: the gallery now shares
               a sticky COLUMN wrapper with the related-products list beneath it
               (see product.py), so the whole media side rides down together.
               The wrapper owns `lg:self-start lg:sticky lg:top-[60px]`; this
               only works because <main> is `overflow-x-clip` (see page()). -->
          <div data-gallery class="flex md:flex-row flex-col-reverse gap-4 min-w-0">{strip}
            <!-- The plate keeps its own padding for the cut-out main shot;
                 scripts.js swaps data-fill to "cover" for the photographs,
                 which drops the padding and lets them bleed to the rounded
                 corners. Both states are the same box, so switching between
                 them never resizes the column. -->
            <!-- Fixed height on the PLATE, not the image, with border-box
                 padding. The two fill modes then swap the padding without the
                 outer box moving a pixel — otherwise switching to a photograph
                 would shrink the column by the padding it just dropped, and
                 the whole page would jump on every thumbnail click. The height
                 is also what the thumbnail strip is capped to. -->
            <div data-gallery-plate data-fill="{'cover' if _is_photo(main_img) else 'contain'}"
                 class="gallery-plate relative flex-1 bg-interaction-base rounded-[20px] min-w-0 overflow-hidden
                        h-[348px] xl:h-[520px]">
              <img data-gallery-main src="{e(main_img)}" alt="{e(alt)}"
                   data-img-scene="{e(main_img)}" data-img-plain="{e(p['image']) if p else e(main_img)}"
                   class="mx-auto w-full h-full" />
              {fav_btn}
            </div>
          </div>"""


# --------------------------------------------------------------------------
# Social proof and reassurance
# --------------------------------------------------------------------------
# Below this rank a product stops being called a best seller. 20 of a real
# 653-product store is the top ~3%, which keeps the badge meaning something —
# a badge every product carries is decoration, not proof.
BEST_SELLER_RANK = 20


# How high a product must place inside its own category to be called a best
# seller there. Deliberately small, and paired with the CATEGORY_MIN below.
BEST_SELLER_CATEGORY_RANK = 3

# A category has to be big enough for "best seller in it" to mean anything.
# Top-3 of a four-product category is not a distinction, it is a rounding
# error — three quarters of the shelf would wear the badge.
BEST_SELLER_CATEGORY_MIN = 6


def _best_seller_label(p):
    """
    The badge text for a product, or "" if it has not earned one.

    Two tiers, both derived from the SAME real `popularityRank`
    (`fetch_popularity.py`, walking the Store API's `orderby=popularity` —
    WooCommerce's own total-sales ordering across the client's 653-product
    store). Nothing here is invented; the second tier just reads that ranking
    at a narrower scope.

      1. Top 20 store-wide      -> "الأكثر مبيعاً"
      2. Top 3 of its category  -> "الأكثر مبيعاً في <category>"

    Why the second tier exists: the store-wide top 20 is dominated by snacks
    and offers, so most categories had no badged product at all and a shopper
    browsing spices never saw the signal. A spice that outsells the other
    spices genuinely is the best selling spice.

    The store-wide label wins where both apply — it is the stronger claim, and
    two badges on one card would compete.
    """
    rank = p.get("popularityRank")
    if not rank:
        return ""
    if rank <= BEST_SELLER_RANK:
        return "الأكثر مبيعاً"
    if (
        p.get("categoryRank", 99) <= BEST_SELLER_CATEGORY_RANK
        and p.get("categorySize", 0) >= BEST_SELLER_CATEGORY_MIN
        and p.get("categoryAr")
    ):
        return f"الأكثر مبيعاً في {p['categoryAr']}"
    return ""


def best_seller_badge(p):
    """
    Shown VISIBLY on every product page (Ahmed, 2026-07-29 — "unified in all
    products" for the handoff). Where the client's store ranks the product high
    enough it carries the earned label (see `_best_seller_label`); everywhere
    else it falls back to the plain "الأكثر مبيعاً" so no page is missing the
    slot. The `data-best-seller` marker stays so a developer can wire the real
    rank-driven show/hide later.

    NOTE / DESIGN-NOTES: because it now paints on all 99 pages, the badge is a
    uniform UI element rather than a data-earned signal on its own — the ranked
    ones are still real, the rest are decoration at Ahmed's explicit request.
    """
    label = _best_seller_label(p) or "الأكثر مبيعاً"
    # self-start, or the badge stretches to the full column width: it is a
    # child of a flex-col, where the default align-items is stretch and
    # inline-flex does nothing to stop it.
    #
    # No glyph any more — the star was removed at Ahmed's request (2026-08-02),
    # so the label alone fills the pill.
    #
    # top-[2px]: Baloo Bhaijaan 2 carries a very deep descent (8px per 12px em
    # against an ink descent of ~3px for this label), so a vertically centred
    # line box paints the letters ~2px above the pill's optical centre — Ahmed
    # read the text as hugging the top. Measured with canvas actualBoundingBox
    # metrics, not eyeballed. `relative`, because transforms do not apply to
    # inline boxes.
    # Was nudged `top-[2px]` to offset Baloo Bhaijaan 2's deep descent on the
    # Arabic label — but that same nudge pushed the LATIN "Best selling" label
    # (a different font, no such descent) off-centre downward (Ahmed, 2026-08-19).
    # Centre with the flex line box + a fixed pill height instead, which reads
    # centred in both fonts without a per-language nudge.
    return ('<span data-best-seller class="inline-flex self-start items-center bg-[#8ACC3E] px-3 '
            'rounded-full h-7 font-bold text-[#003616] text-xs leading-none">'
            f'{e(label)}</span>')


def points_callout(p):
    """
    "Earn N points" pill, shown beside the best-seller badge on every product
    page (Ahmed, 2026-08-04).

    The rate is the site's OWN, not invented: the points page states "اكسب نقطة
    على كل جنيه" (1 EGP = 1 point) and redeems points 1:1 into the wallet, so N
    is simply the price the shopper pays, rounded. Keeping one rate across the
    product page, the points page and the wallet is the same discipline the
    wallet balance already follows — see my_account_point.py and DESIGN-NOTES §1.
    """
    price = p.get("sale") or p.get("price") or 0
    pts = int(round(price))
    if pts <= 0:
        return ""
    # Green "good news" pill, the same family as the discount/wallet chips, so
    # points read as a reward rather than as another price (which is yellow). A
    # leading hairline divider (matching the one sold_proof folds in) separates
    # it from the red proof line; the pill padding is trimmed and it centres in
    # the row rather than sitting to the top (Ahmed, 2026-08-04).
    return ('<span class="inline-flex items-center gap-2">'
            '<span aria-hidden="true" class="bg-neutral-divider w-px h-4"></span>'
            '<span class="inline-flex items-center gap-1 bg-[#E9F3E6] px-2.5 py-0.5 '
            'rounded-full font-bold text-[#00451C] text-xs">'
            '<img src="images/jaad/icons/points-3d.png" alt="" class="w-4 h-4 shrink-0 object-contain" />'
            f'<span>اكسب <span class="latin">{pts}</span> نقطة</span></span></span>')


def _sold_proof_label(p):
    """
    The encouragement sentence (as inner HTML) for a product, or None.

    Deliberately a RANK, not a unit count. The live-site pattern this mirrors
    reads "500+ sold this week", but no public endpoint carries absolute sales
    volume, and inventing one would be exactly the kind of fabricated metric
    this project keeps out. A rank is real, checkable, and carries the same
    "other people are buying this" push. Swap it for a true count the moment
    the client exposes one — see DESIGN-NOTES.
    """
    rank = p.get("popularityRank")
    if not rank:
        return None
    if rank <= BEST_SELLER_RANK:
        # Round up to a friendly bucket so the line reads as a claim, not a
        # lookup.
        bucket = 10 if rank <= 10 else BEST_SELLER_RANK
        scope = "في جاد"
    elif (
        p.get("categoryRank", 99) <= BEST_SELLER_CATEGORY_RANK
        and p.get("categorySize", 0) >= BEST_SELLER_CATEGORY_MIN
        and p.get("categoryAr")
    ):
        # Tracks the badge exactly, on purpose. A product wearing "best seller
        # in spices" with no proof line beside it, or the reverse, is the same
        # split-signal problem the badge tiers were added to remove.
        bucket = BEST_SELLER_CATEGORY_RANK
        scope = f"في {p['categoryAr']}"
    else:
        return None
    return f'ضمن أفضل <span class="latin">{bucket}</span> مبيعاً {e(scope)}'


def sold_proof(p):
    """
    The red encouragement line beside the rating.

    Shown VISIBLY on every product page (Ahmed, 2026-07-29 — same "unified in
    all products" call as best_seller_badge). Ranked products carry the real
    line; everywhere else it falls back to the non-numeric "ضمن الأكثر مبيعاً
    في جاد" so the slot is never empty. `data-sold-proof` stays as the
    developer's show/hide hook. Its leading hairline is folded INTO the element
    so it can never dangle beside the rating.

    The copy is ONE flex child, not loose text nodes beside the glyph. Bare text
    and the <span class="latin"> around the number were each their own flex
    item, so they wrapped independently — with a long category name the line
    broke as "ضمن / أفضل" with the numeral stranded. `items-start` keeps the
    flame on the first line rather than centring against a two-line block.
    """
    label = _sold_proof_label(p) or "ضمن الأكثر مبيعاً في جاد"
    return ('<span data-sold-proof class="inline-flex items-start gap-1.5 font-semibold text-accent-error text-sm">'
            '<span aria-hidden="true" class="bg-neutral-divider mt-0.5 me-0.5 w-px h-4 self-stretch"></span>'
            f'<span class="mt-0.5 w-4 h-4 shrink-0">{ICON["flame"]}</span>'
            f'<span>{label}</span></span>')


def trust_row(items):
    """
    The icon/title/subtitle reassurance strip that sits under the CTA.

    items: [(icon_key, title, subtitle)]. `subtitle` may be empty, in which
    case its line is not rendered at all — a benefit taken from the client's
    own copy is one sentence, not a title with a caption under it, and an
    empty span still costs its line-height and made those tiles sit unevenly
    against three-line neighbours.

    The column count follows the item count so a product with two benefits
    gets two columns rather than a hole where a third should be.

    Every claim here must already be made somewhere else on this site — these
    restate the delivery and returns policy and the real branch count, or they
    are the client's own product copy. Nothing asserts a new product claim
    like "third-party tested" that nobody has signed off.
    """
    if not items:
        return ""
    cols = {1: "grid-cols-1", 2: "grid-cols-2"}.get(len(items), "grid-cols-3")
    cells = ""
    for icon, title_, sub in items:
        sub_html = (
            f'\n                <span class="text-neutral-secondary text-xs leading-4">{e(sub)}</span>'
            if sub else ""
        )
        cells += f"""
              <div class="flex flex-col items-center gap-2 text-center">
                <span class="place-items-center grid bg-interaction-base rounded-full text-cta size-11 shrink-0">
                  <span class="w-5 h-5">{ICON[icon]}</span>
                </span>
                <span class="font-semibold text-[#003616] text-sm text-balance leading-5 line-clamp-3">{e(title_)}</span>{sub_html}
              </div>"""
    return f"""
            <div class="gap-4 grid {cols} pt-1">{cells}
            </div>"""


# Lines that are a spec, not a benefit. The client's benefit lists sometimes
# open or close with the pack weight ("100جرام"), which is already printed on
# the size chips and reads as filler in a benefit tile.
_SPEC_ONLY = re.compile(r"^[\d\s.,]*(جرام|جم|كجم|مل|لتر|g|gm|kg|ml)?[\d\s.,]*$", re.I)


def benefit_bullets(p, limit=3):
    """The client's own benefit lines for this product, cleaned to plain text."""
    raw = p.get("descHtmlAr") or ""
    out = []
    for frag in re.findall(r"<li[^>]*>(.*?)</li>", raw, re.S):
        text = re.sub(r"<[^>]+>", "", frag)
        text = " ".join(html_mod.unescape(text).split())
        if text and not _SPEC_ONLY.match(text):
            out.append(text)
    return out[:limit]


# Generic quality glyphs. Deliberately not claim-bearing — they decorate the
# client's sentence, they do not add a meaning of their own the way a "vegan"
# or "tested" mark would.
_BENEFIT_ICONS = ("leaf", "bolt", "shield")

# 3D-render variant of the three benefit glyphs (Ahmed, 2026-07-29). Same
# positional leaf/bolt/shield keys the benefit builders already emit, mapped to
# pre-rendered PNGs that carry their own transparency and soft shadow. Used only
# by trust_row_3d; the flat ICON glyphs above still drive the default row.
_BENEFIT_ICONS_3D = {
    "leaf": "images/jaad/icons/spec-leaf.png",
    "bolt": "images/jaad/icons/spec-bolt.png",
    "shield": "images/jaad/icons/spec-shield.png",
}


def trust_row_3d(items):
    """
    3D-icon variant of trust_row (Ahmed, 2026-07-29), selected by SPECS_VARIANT
    in product.py — flip that flag back and trust_row runs instead, this stays
    dormant. Same `items` contract: [(icon_key, title, subtitle)].

    Layout differs on purpose: each cell is a HORIZONTAL [icon | text] pair
    rather than the default's icon-over-text, right-aligned in RTL (the icon
    leads on the inline-start / right edge, the copy flows from it). The cells
    sit in one row on sm+ and stack to one column on mobile, where three
    horizontal pairs across a phone would be unreadable.

    Icons are the pre-rendered 3D PNGs, keyed by the same leaf/bolt/shield the
    benefit builders emit; an unknown key falls back to the leaf so a cell is
    never iconless.
    """
    if not items:
        return ""
    n = len(items)
    cols = {1: "sm:grid-cols-1", 2: "sm:grid-cols-2"}.get(n, "sm:grid-cols-3")
    cells = ""
    for icon, title_, sub in items:
        src = _BENEFIT_ICONS_3D.get(icon, _BENEFIT_ICONS_3D["leaf"])
        sub_html = (
            f'\n                  <span class="text-neutral-secondary text-xs leading-4">{e(sub)}</span>'
            if sub else ""
        )
        cells += f"""
              <div class="flex items-center gap-1">
                <img src="{src}" alt="" class="w-12 xl:w-14 h-12 xl:h-14 shrink-0 object-contain" loading="lazy" />
                <span class="flex flex-col min-w-0">
                  <span class="font-semibold text-[#003616] text-sm text-balance leading-5">{e(title_)}</span>{sub_html}
                </span>
              </div>"""
    return f"""
            <div class="gap-4 grid grid-cols-1 {cols} pt-1">{cells}
            </div>"""


def product_benefits(p, fallback, renderer=trust_row):
    """
    The strip under the CTA, built from the client's OWN benefit copy.

    Only the single hero product used to get product benefits here; the other
    98 got the site-service trio (delivery / returns / branch count), so a
    shopper moving from the hero to any other product saw the product tiles
    replaced by delivery notes and the page read as a different template.
    That was the complaint.

    Coverage is the honest limit of the data: 64 of 99 products have at least
    two usable benefit lines in `descHtmlAr`. The remaining 35 have none — the
    client never wrote them — so those keep the generic trio rather than
    getting invented copy. Absence over invention, same rule as the branch
    phone numbers.

    `renderer` is the row component — trust_row (default) or trust_row_3d —
    passed in by product.py's SPECS_VARIANT flag so the variant is one switch.
    """
    bullets = benefit_bullets(p)
    if len(bullets) < 2:
        return renderer(fallback)
    return renderer([(_BENEFIT_ICONS[i], b, "") for i, b in enumerate(bullets)])


def specs_block(tagline, desc, points):
    """
    The product "specs" strip, redrawn to Ahmed's 2026-08-02 brief.

    A leaf-marked TAGLINE with a one-line description, then three leaf BULLETS —
    full sentences, not the one-word labels the old icon/label tiles inherited
    from whatever benefit lines each product happened to carry — all sitting on
    a subtle rounded surface.

    Every mark is the SAME leaf glyph, not the old leaf/bolt/shield trio: the
    leaf is the brand's own mark and asserts nothing on its own, so repeating it
    reads as decoration rather than three competing promises. The copy is
    uniform across all 99 pages (see SPECS_* in product.py) so the strip is one
    component a developer meets once, not a section that changes shape per
    product — brand-level reassurance only, still OUR unsigned Arabic pending
    client sign-off (flagged in DESIGN-NOTES, same footing as the hero copy).
    """
    # The 3D leaf PNG marks each statement (Ahmed, 2026-08-02) — the same
    # pre-rendered asset the old 3D spec row used. The tagline no longer carries
    # its own icon; the copy leads.
    leaf3d = "images/jaad/icons/spec-leaf.png"
    bullets = "".join(f"""
                <li class="flex items-start gap-2.5">
                  <img src="{leaf3d}" alt="" class="mt-0.5 w-7 h-7 object-contain shrink-0" loading="lazy" />
                  <span class="text-[#003616] text-sm leading-6">{e(point)}</span>
                </li>""" for point in points)
    return f"""
            <div class="flex flex-col gap-4 bg-interaction-base p-5 rounded-2xl">
              <div class="flex flex-col gap-0.5">
                <h2 class="font-bold text-[#29612F] text-base xl:text-lg">{e(tagline)}</h2>
                <p class="text-neutral-secondary text-sm leading-6">{e(desc)}</p>
              </div>
              <ul class="flex flex-col gap-2.5">{bullets}
              </ul>
            </div>"""


# --------------------------------------------------------------------------
# Forms — Figma 'Input Field' section (150:4622)
# --------------------------------------------------------------------------
# Autofill tokens, inferred from the field name rather than passed at every
# call site — the names are already semantic, and doing it here means no
# checkout or auth field can be added later without one.
#
# Not cosmetic: with no autocomplete attribute anywhere, a browser or
# password manager could not fill a single field on the 10-field checkout,
# which on a phone is most of the work of ordering.
_AUTOCOMPLETE = {
    "first-name": "given-name",
    "last-name": "family-name",
    "name": "name",
    "email": "email",
    "phone": "tel",
    "city": "address-level2",
    "district": "address-level3",
    "area": "address-level3",
    "street": "address-line1",
    "floor": "address-line2",
    "apartment": "address-line2",
    "line1": "address-line1",
    "line2": "address-line2",
    "postcode": "postal-code",
}

# type=tel already summons a numeric keypad; these are the free-text fields
# that hold digits and would otherwise open a full QWERTY on a phone.
_INPUTMODE = {"floor": "numeric", "apartment": "numeric", "postcode": "numeric"}


def _field_hints(name, type_, autocomplete=None):
    ac = autocomplete or _AUTOCOMPLETE.get(name)
    if ac is None and type_ == "password":
        ac = "current-password"
    im = _INPUTMODE.get(name)
    out = ""
    if ac:
        out += f' autocomplete="{e(ac)}"'
    if im:
        out += f' inputmode="{e(im)}"'
    return out


def field(label, name, type_="text", required=False, value="", placeholder="",
          wrap="", autocomplete=None):
    star = '<span class="text-accent-error">*</span>' if required else ""
    hints = _field_hints(name, type_, autocomplete)
    return f"""
                <div class="flex flex-col gap-1.5 {wrap}">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}{star}</label>
                  <input type="{e(type_)}" id="{e(name)}" name="{e(name)}"{' required' if required else ''}{hints}
                         value="{e(value)}" placeholder="{e(placeholder)}"
                         class="bg-white border border-neutral-divider rounded-2xl px-4 h-12 w-full text-[#003616] text-base placeholder:text-neutral-secondary outline-none focus:border-primary focus:ring-2 focus:ring-[#98CA55] transition-colors" />
                </div>"""


def phone_field(label="رقم الموبايل", name="mobile", required=True, value="", help_text=""):
    """Mobile input with a fixed Egypt country prefix (Ahmed, 2026-08-04): a flag
    + +20 chip on the leading side, then an LTR number field. Egypt-only, so the
    prefix is fixed rather than a country picker. The whole control is `dir=ltr`
    so the +20 sits on the visual left and the digits read left-to-right, like a
    phone number, inside the RTL form."""
    star = '<span class="text-accent-error">*</span>' if required else ""
    hints = _field_hints(name, "tel")
    help_html = (f'<p class="text-neutral-secondary text-xs">{e(help_text)}</p>'
                 if help_text else "")
    return f"""
                <div class="flex flex-col gap-1.5">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}{star}</label>
                  <!-- Rebuilt clean (Ahmed, 2026-08-19): ONE rounded control, the
                       Egypt flag + +20 as a plain leading adornment on the SAME
                       white surface as the number. No inner cell and NO divider
                       rule — the old divider between the prefix and the input
                       read as a stray vertical line after "+20". The whole field
                       carries the green focus ring; the prefix is just text. -->
                  <div data-phone-field dir="ltr" class="flex items-center bg-white border border-neutral-divider focus-within:border-cta focus-within:ring-2 focus-within:ring-[#98CA55] rounded-2xl transition-colors">
                    <span class="flex items-center gap-2 ps-4 pe-2.5 shrink-0 font-semibold text-[#003616] text-base latin">
                      <img src="images/jaad/brand/flag-egypt.svg" alt="" class="w-5 h-5 rounded-full object-cover shrink-0" />
                      +20
                    </span>
                    <input type="tel" id="{e(name)}" name="{e(name)}"{' required' if required else ''}{hints} dir="ltr" value="{e(value)}"
                           placeholder="100 123 4567"
                           class="flex-1 bg-transparent py-3.5 pe-4 outline-none min-w-0 text-[#003616] text-base latin" />
                  </div>
                  {help_html}
                </div>"""


def select_field(label, name, options, required=False, wrap=""):
    star = '<span class="text-accent-error">*</span>' if required else ""
    opts = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in options)
    hints = _field_hints(name, "select")
    return f"""
                <div class="flex flex-col gap-1.5 {wrap}">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}{star}</label>
                  <select id="{e(name)}" name="{e(name)}"{' required' if required else ''}{hints}
                          class="select-control bg-white border border-neutral-divider rounded-2xl px-4 h-12 w-full text-[#003616] text-base placeholder:text-neutral-secondary outline-none focus:border-primary focus:ring-2 focus:ring-[#98CA55] transition-colors">
                    <option value="">اختر</option>{opts}
                  </select>
                </div>"""


GIFT_TERMS = [
    "عند الإرسال كهدية، لن تظهر الأسعار في الفاتورة.",
    "سيتم توصيل طلبك إلى العنوان المحدد.",
    "الدفع عند الاستلام غير متاح لطلبات الهدايا.",
]


def gift_toggle():
    """
    Gift order — ONE card with a switch, replacing the two-card
    normal/gift radio pair (Ahmed, 2026-07-26), and moved to sit after
    بيانات العميل rather than opening the form.

    Why one card. "Normal order" was never a choice anyone made: it is the
    default state of a shopping basket, so a card asking a shopper to select it
    spent a full row of the form confirming that nothing unusual is happening.
    A gift is the only real decision on that row, and a decision with one
    option is a switch.

    Why after the customer's own details. Gifting asks *who is receiving this*,
    which only makes sense once *who is ordering* has been answered. Opening
    the form with it put the recipient's name above the buyer's own.

    The terms are stated on the card because two of the three change what the
    shopper gets — no prices on the invoice, no cash on delivery — and finding
    that out at the payment step is finding out too late. They sit OUTSIDE the
    collapsing panel and are always visible: they describe what turning the
    switch on will do, so hiding them behind it would mean the consequences
    could only be read after accepting them. Only the recipient fields
    collapse, being the part that genuinely does not exist until you gift.

    The recipient fields are NOT `required`. The panel is collapsed when gifting
    is off, and a required field inside a collapsed panel blocks submission with
    a browser message pointing at something the shopper cannot see. scripts.js
    adds and removes `required` with the toggle instead.
    """
    terms = "".join(f"""
                  <li class="flex items-start gap-2">
                    <span class="mt-0.5 text-accent-green shrink-0 w-4 h-4">{ICON['check']}</span>
                    <span>{t}</span>
                  </li>""" for t in GIFT_TERMS)
    return f"""
              <!-- Order matters: input, then label, then panel, all SIBLINGS.
                   The CSS opens the panel with `[data-gift-switch]:checked ~
                   .gift-panel`, and `~` only reaches siblings — with the input
                   nested inside the label (the shape the wallet toggle uses)
                   the panel is not a sibling of it and never opened.

                   The label therefore points at the input by `for`, which also
                   keeps the recipient fields out of the label's own subtree: a
                   form control inside a <label> that labels a DIFFERENT control
                   gets claimed by it, so clicking the recipient's name would
                   have toggled gifting off. -->
              <div class="bg-white p-5 border border-neutral-divider rounded-xl">
                <input type="checkbox" id="gift-order" data-switch data-gift-switch class="sr-only" />
                <label for="gift-order" class="flex items-center gap-3 cursor-pointer">
                  <span class="place-items-center grid bg-accent-green/10 rounded-full text-accent-green size-10 shrink-0">
                    <span class="w-5 h-5">{ICON['gift']}</span>
                  </span>
                  <span class="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span class="font-semibold text-[#003616] text-base">إهداء الطلب</span>
                    <span class="text-neutral-secondary text-xs leading-5">أرسل الطلب كهدية لشخص تحبه</span>
                  </span>
                  <span class="switch shrink-0" aria-hidden="true"><span class="switch__knob"></span></span>
                </label>
                <!-- The terms sit OUTSIDE the collapsing panel, so they are
                     readable with the switch off (Ahmed, 2026-07-26). They
                     describe what turning it ON will do — no prices on the
                     invoice, no cash on delivery — so putting them behind it
                     meant you could only read the consequences after accepting
                     them. Only the recipient fields collapse, because those are
                     the part that genuinely does not exist until you gift. -->
                <ul class="flex flex-col gap-2 mt-4 pt-4 border-neutral-divider border-t text-neutral-secondary text-xs leading-5">{terms}
                </ul>
                <div class="gift-panel" data-gift-panel aria-hidden="true">
                  <div>
                    <div class="flex flex-col gap-4 mt-4">
                      <p class="font-semibold text-[#003616] text-sm">بيانات المستلم</p>
                      <div class="gap-4 grid sm:grid-cols-2">
{field("اسم المستلم", "recipient-name")}
{field("رقم هاتف المستلم", "recipient-phone", "tel")}
                      </div>
                    </div>
                  </div>
                </div>
              </div>"""


def checkout_summary(lines_html, subtotal, total, delivery_fee, interactive=True):
    """
    The order summary shared by checkout and payment.

    It lives here rather than in either page because those two screens must
    never be able to print different numbers for the same basket — which is
    exactly what happened when the cart page and the drawer each owned a copy
    of the delivery fee. Same hooks on both (`data-cart-lines`,
    `data-cart-subtotal`, `data-cart-discount`, `data-cart-total`), so
    renderCart in scripts.js remains the single renderer for all of them.

    The build-time figures are a pre-boot placeholder only: `data-cart-static`
    rows are dropped and every total is overwritten on the first `cart:change`.

    `interactive=False` is the payment step (Ahmed, 2026-08-04): the shopper
    must not be able to change anything about the MONEY there, so the wallet
    toggle and the promo field are dropped — each one's effect is already applied
    and survives only as a figure in the totals below. The order note is NOT
    money, so it stays on payment too (Ahmed, 2026-08-04): initOrderNotes reads
    the same stored note, so a note added on checkout carries over. It is fully
    EDITABLE on payment as well (Ahmed, 2026-08-05) — a shopper often remembers
    a delivery instruction at the last step, and the note changes nothing about
    the price, so there is no reason to lock it the way the money controls are.
    Checkout keeps all three (interactive=True), grouped together, and both add a
    "تعديل" link back to the cart page.
    """
    # #8 — a "تعديل" link back to the CART PAGE (not the drawer), on the title's
    # own line. On BOTH checkout and payment (Ahmed, 2026-08-04): even at payment
    # a shopper may want to jump back to the basket to change it.
    edit_link = '<a href="cart.html" class="link-sweep font-semibold text-cta text-sm">تعديل</a>'
    # #12 — wallet, promo and the note editor grouped together above the totals.
    # The note editor is on BOTH steps with the FULL editor; wallet and promo
    # (the money controls) are checkout-only — on payment their result is shown
    # as a figure in the totals. The note is editable at payment too (Ahmed,
    # 2026-08-05): it is not money, so there is nothing to lock.
    note_block = f"""
            <div class="pt-1">{order_notes()}
            </div>"""
    controls = (f"""
{wallet_toggle()}
{promo_field()}{note_block}""" if interactive else note_block)
    return f"""
          <aside class="lg:top-4 lg:sticky flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px] order-2 lg:order-none min-w-0">
            <div class="flex justify-between items-center gap-3">
              <h2 class="font-bold text-[#29612F] text-xl">ملخص السلة</h2>
              {edit_link}
            </div>
            <div class="flex flex-col gap-4" data-cart-lines>{lines_html}
            </div>
            {controls}
            <div class="flex flex-col gap-2 pt-3 border-neutral-divider border-t text-sm">
              <div class="flex justify-between">
                <span class="text-neutral-secondary">مصاريف التوصيل</span>
                <span class="font-semibold text-[#003616] latin" data-cart-delivery>EGP {money(delivery_fee)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-neutral-secondary">الإجمالي</span>
                <span class="font-semibold text-[#003616] latin" data-cart-subtotal>EGP {money(subtotal)}</span>
              </div>
              <div class="flex justify-between items-center" data-cart-discount-row hidden>
                <span class="text-neutral-secondary">خصم المحفظة</span>
                <span class="inline-flex items-center h-[13px] -me-2 bg-[#E9F3E6] px-2 rounded font-bold text-[#00451C] text-sm latin" data-cart-discount></span>
              </div>
              <div class="flex justify-between items-center" data-cart-promo-row hidden>
                <span class="text-neutral-secondary">خصم كود الخصم</span>
                <span class="inline-flex items-center h-[13px] -me-2 bg-[#E9F3E6] px-2 rounded font-bold text-[#00451C] text-sm latin" data-cart-promo-discount></span>
              </div>
            </div>
            <div class="flex justify-between items-center pt-3 border-neutral-divider border-t">
              <span class="font-bold text-[#003616] text-base">الإجمالي</span>
              <span class="font-bold text-[#003616] text-2xl latin" data-cart-total>EGP {money(total)}</span>
            </div>
          </aside>"""


def checkout_steps(current):
    """
    The four-step breadcrumb across checkout and payment. `current` is the
    0-based index of the active step.

    Shared for the same reason as the summary: two pages drawing their own
    copy is how a stepper ends up highlighting step 2 on the step-3 page.
    """
    sep = '<span aria-hidden="true" class="text-neutral-outline">/</span>'
    # A completed step is a real link back to its own page, so a shopper on
    # step 3 can return to step 1 from the stepper (Ahmed, 2026-08-04). Index-
    # aligned with CHECKOUT_STEPS; the current step and any step ahead are NOT
    # links — there is nothing to go forward to yet, and the active step is
    # where you already are. The final confirmation step has no page to return
    # to, so it stays None even when it is somehow "done".
    hrefs = ["cart.html", "checkout.html", "payment.html", None]
    parts = []
    for i, s in enumerate(CHECKOUT_STEPS):
        is_now = i == current
        # Passed steps read as done rather than as inactive — a shopper on step
        # 3 should be able to see that 1 and 2 are behind them.
        done = i < current
        can_go = done and hrefs[i]
        # #E9F3E6 opaque, NOT `bg-accent-green/15`. The alpha version renders
        # the same to the eye (#618F2B on it measures ~5.4:1) but the sweep's
        # `bgOf()` treats any non-zero alpha as an opaque colour, so it compared
        # the tick against its own ink and reported 1.00:1 — three standing
        # false failures against a baseline whose whole value is that it reads
        # zero. An opaque tint is legible to both. It is also the tint the
        # discount chip and the wallet card already use, so "good news" is one
        # colour across the checkout rather than two near-identical greens.
        dot = ("bg-cta text-white" if is_now
               else "bg-[#E9F3E6] text-accent-green" if done
               else "bg-interaction-base text-neutral-secondary")
        text = ("font-semibold text-[#003616]" if is_now
                else "text-accent-green" if done
                else "text-neutral-secondary")
        tail = "" if i == len(CHECKOUT_STEPS) - 1 else sep
        mark = "✓" if done else str(i + 1)
        # link-sweep gives a completed step the same hover underline as the
        # breadcrumb, so it visibly reads as a way back rather than static text.
        label_cls = f"{text} text-sm" + (" link-sweep" if can_go else "")
        inner = (
            f'<span class="place-items-center grid rounded-full size-5 text-xs latin {dot}">{mark}</span>'
            f'<span class="{label_cls}">{e(s)}</span>'
        )
        if can_go:
            parts.append(
                f'<a href="{hrefs[i]}" class="flex items-center gap-2 rounded-md focus-visible:outline-none">{inner}</a>{tail}'
            )
        else:
            parts.append(f'<span class="flex items-center gap-2">{inner}</span>{tail}')
    return "".join(parts)


CHECKOUT_STEPS = ["سلة التسوق", "بيانات العميل", "طريقة الدفع", "تأكيد عملية الشراء"]


def promo_field(readonly=False):
    """
    Promo code — the control that replaced a dead link.

    `readonly=True` is the payment step (Ahmed, 2026-08-03): a code is entered
    earlier, so payment must SHOW an applied code but never let you edit or
    remove it — and show nothing at all when none was applied. That is exactly
    the `data-promo-applied` chip with no trigger, no input and no إلغاء button.
    syncPromoUI already drives it (it only touches whichever of open/box/applied
    it finds), so the read-only wrapper just carries the chip. `contents` on the
    wrapper keeps it out of the summary's flex flow, so the whole block
    collapses to zero height — no stray gap — until a code is actually applied.
    """
    if readonly:
        return f"""
              <div data-promo class="contents">
                <div data-promo-applied hidden class="flex items-center gap-2 bg-[#E9F3E6] px-3 py-2 rounded-xl">
                  <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-auto h-8 shrink-0" />
                  <span class="min-w-0 text-[#00451C] text-sm truncate">تم تطبيق <span class="font-bold latin" data-promo-applied-code></span></span>
                </div>
              </div>"""

    # Full (editable) promo control below — used by the cart and checkout.
    # `هل لديك برومو كود؟` was once a dead <button>; it now opens a field and
    # applies a real discount through renderCart. NOT a <form>: on checkout it
    # sits inside the place-order form, where a nested form is invalid HTML that
    # browsers un-nest (the Apply button would submit the order) — a button plus
    # an Enter keydown handler gives the same feel. The only code is DISCOUNT10,
    # the one the site's announcement bar advertises; inventing a second would
    # invent an offer on the client's behalf.
    return f"""
              <div data-promo class="flex flex-col gap-2">
                <button type="button" data-promo-open class="flex items-center gap-2 self-start min-h-11 font-semibold text-cta text-sm underline">
                  <span class="inline-flex w-[18px] h-[18px] shrink-0" aria-hidden="true"><svg viewBox="0 0 25.2 25.2" fill="currentColor" class="w-full h-full"><path fill-rule="evenodd" clip-rule="evenodd" d="M14.5799 0.820101C13.4864 -0.273367 11.7136 -0.273367 10.6201 0.820101L9.87077 1.56943C9.08312 2.35708 8.01483 2.79958 6.90092 2.79958H5.6C4.0536 2.79958 2.8 4.05318 2.8 5.59958V6.9005C2.8 8.01441 2.3575 9.0827 1.56985 9.87035L0.8201 10.6201C-0.273368 11.7136 -0.273366 13.4864 0.820102 14.5799L1.56985 15.3296C2.3575 16.1173 2.8 17.1856 2.8 18.2995V19.5996C2.8 21.146 4.0536 22.3996 5.6 22.3996H6.90008C8.01399 22.3996 9.08228 22.8421 9.86993 23.6297L10.6201 24.3799C11.7136 25.4734 13.4864 25.4734 14.5799 24.3799L15.3301 23.6297C16.1177 22.8421 17.186 22.3996 18.2999 22.3996H19.6C21.1464 22.3996 22.4 21.146 22.4 19.5996V18.2995C22.4 17.1856 22.8425 16.1173 23.6301 15.3296L24.3799 14.5799C25.4734 13.4864 25.4734 11.7136 24.3799 10.6201L23.6301 9.87035C22.8425 9.0827 22.4 8.01441 22.4 6.90051V5.59958C22.4 4.05318 21.1464 2.79958 19.6 2.79958H18.2991C17.1852 2.79958 16.1169 2.35708 15.3292 1.56942L14.5799 0.820101ZM16.5649 9.17658C16.9938 8.53324 16.8199 7.66402 16.1766 7.23513C15.5332 6.80624 14.664 6.98008 14.2351 7.62342L8.63513 16.0234C8.20624 16.6668 8.38008 17.536 9.02342 17.9649C9.66676 18.3938 10.536 18.2199 10.9649 17.5766L16.5649 9.17658ZM7.7 11.2C8.8598 11.2 9.8 10.2598 9.8 9.1C9.8 7.9402 8.8598 7 7.7 7C6.5402 7 5.6 7.9402 5.6 9.1C5.6 10.2598 6.5402 11.2 7.7 11.2ZM19.6 16.1C19.6 17.2598 18.6598 18.2 17.5 18.2C16.3402 18.2 15.4 17.2598 15.4 16.1C15.4 14.9402 16.3402 14 17.5 14C18.6598 14 19.6 14.9402 19.6 16.1Z"/></svg></span>
                  هل لديك برومو كود؟
                </button>
                <div data-promo-box hidden class="flex flex-col gap-2">
                  <div class="flex items-center gap-2">
                    <input type="text" data-promo-input inputmode="latin" autocomplete="off"
                           placeholder="{e('أدخل كود الخصم')}"
                           class="flex-1 bg-white border border-neutral-divider rounded-2xl px-3 py-2 min-w-0 text-[#003616] text-sm placeholder:text-neutral-secondary outline-none focus:border-primary focus:ring-2 focus:ring-[#98CA55] transition-colors latin" />
                    <!-- Secondary (outline) button (Ahmed, 2026-08-05): the
                         Apply sits next to the primary green order CTA below, so
                         a second solid-green button competed with it for the
                         eye. An outline keeps it clearly actionable while the
                         filled CTA stays the one obvious next step. -->
                    <button type="button" data-promo-apply
                            class="bg-white hover:bg-interaction-base px-4 border border-cta rounded-full min-h-11 font-semibold text-cta text-sm whitespace-nowrap transition-colors">تطبيق</button>
                  </div>
                  <p data-promo-msg hidden class="text-xs leading-5"></p>
                </div>
                <!-- Applied state (Ahmed, 2026-08-02): the code as a removable
                     chip. renderCart -> syncPromoUI swaps between the trigger,
                     the input box and this on every change, so it is right on
                     load, after apply, and across cart -> checkout. -->
                <div data-promo-applied hidden class="flex justify-between items-center gap-2 bg-[#E9F3E6] px-3 py-2 rounded-xl">
                  <span class="flex items-center gap-2 min-w-0 text-[#00451C] text-sm">
                    <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-auto h-8 shrink-0" />
                    <span class="truncate">تم تطبيق <span class="font-bold latin" data-promo-applied-code></span></span>
                  </span>
                  <button type="button" data-promo-remove class="shrink-0 font-semibold text-accent-error text-xs underline">إلغاء</button>
                </div>
              </div>"""


def order_notes(readonly=False):
    """
    Order note — reworked from an accordion to the same trigger → input →
    applied pattern as the promo field (Ahmed, 2026-08-04), so it groups with
    the wallet and promo in the summary instead of standing apart. Shared by the
    cart and checkout; scripts.js persists it under jaad:orderNote and swaps
    the three states off the stored note (initOrderNotes -> syncNoteUI).

    `readonly=True` is the PAYMENT step (Ahmed, 2026-08-04): a note added on the
    previous step is shown but can't be edited or removed here — there is no
    trigger, no editor and no remove X, and the whole block is hidden when no
    note was left. syncNoteUI reveals it and fills the text.

    Three states (interactive only):
      - TRIGGER (default, closed): a "+ أضف ملاحظة على الطلب" button that opens
        the editor, mirroring the promo trigger's affordance (a glyph chip then
        the label).
      - EDIT: a textarea + save (+ cancel).
      - FILLED: the saved note drawn as a standard read-only field — a note glyph
        at the start and an X at the end to remove it. Clicking the field
        (anywhere but the X) reopens the editor; `.note-filled` (styles.css)
        gives it a hover cue so a shopper knows the note is editable.
    """
    if readonly:
        # Locked view for the payment step: note glyph + text, no controls.
        # Hidden until syncNoteUI finds a stored note.
        return f"""
              <div data-note data-note-readonly hidden class="flex flex-col gap-2">
                <span class="font-semibold text-neutral-secondary text-xs">ملاحظة الطلب</span>
                <div class="flex items-center gap-2 bg-interaction-base px-3 py-2.5 border border-neutral-divider rounded-2xl">
                  <span class="shrink-0 text-primary"><span class="block w-4 h-4">{ICON['note']}</span></span>
                  <span class="flex-1 min-w-0 text-[#003616] text-sm" data-note-text></span>
                </div>
              </div>"""
    return f"""
              <div data-note class="flex flex-col gap-2">
                <button type="button" data-note-open class="flex items-center gap-2 self-start min-h-11 font-semibold text-cta text-sm">
                  <span class="place-items-center grid bg-interaction-base rounded-full size-6 shrink-0"><span class="w-3.5 h-3.5">{ICON['plus']}</span></span>
                  أضف ملاحظة على الطلب
                </button>
                <div data-note-edit hidden class="flex flex-col gap-2">
                  <!-- aria-label, not placeholder alone: a placeholder disappears
                       the moment you type, so it cannot be the accessible name. -->
                  <textarea rows="3" placeholder="أضف ملاحظة على طلبك" aria-label="ملاحظات على الطلب" data-order-note
                            class="bg-white border border-neutral-divider rounded-2xl px-4 py-3 w-full text-[#003616] text-sm placeholder:text-neutral-secondary outline-none focus:border-primary focus:ring-2 focus:ring-[#98CA55] transition-colors"></textarea>
                  <!-- Compact buttons (Ahmed, 2026-08-04): the save was oversized
                       for a note editor. Padding-based height (~34px) — still well
                       above the 24px WCAG 2.5.8 floor. -->
                  <div class="flex items-center gap-1 self-end">
                    <button type="button" data-note-cancel class="px-3 py-1.5 font-semibold text-neutral-secondary text-xs">إلغاء</button>
                    <button type="button" data-order-note-save class="bg-cta hover:bg-cta-hover px-4 py-1.5 rounded-full font-semibold text-white text-xs transition-colors">حفظ الملاحظة</button>
                  </div>
                </div>
                <!-- Filled note: reads as a standard input. The flex-1 button is
                     the edit trigger (clicking the note text reopens the editor);
                     the X removes it. Hover cue lives on `.note-filled`. -->
                <div data-note-view hidden class="note-filled flex items-center gap-2 bg-white px-3 py-2.5 border border-neutral-divider rounded-2xl transition-colors">
                  <span class="shrink-0 text-primary"><span class="block w-4 h-4">{ICON['note']}</span></span>
                  <button type="button" data-note-edit-btn class="flex-1 min-w-0 text-start text-[#003616] text-sm truncate" aria-label="تعديل الملاحظة"><span data-note-text></span></button>
                  <button type="button" data-note-remove class="place-items-center grid shrink-0 rounded-full size-6 text-neutral-secondary hover:text-accent-error hover:bg-interaction-base transition-colors" aria-label="حذف الملاحظة"><span class="w-3.5 h-3.5">{ICON['close']}</span></button>
                </div>
              </div>"""


def freeship_bar():
    """
    Free-delivery progress bar (Ahmed, 2026-08-02).

    The "add X more for free delivery" caption sits ABOVE the bar (Ahmed,
    2026-08-04 — restored). Static shell only: scripts.js renderCart fills it
    from the LIVE basket toward FREE_SHIP and flips the caption to the success
    line at the threshold, where the delivery fee zeroes, so the incentive pays
    out. Hidden until the store paints, so an empty basket shows nothing to
    progress toward.
    """
    return """
              <div data-freeship hidden class="flex flex-col gap-1.5">
                <p class="text-[#003616] text-xs leading-5" data-freeship-msg></p>
                <div class="bg-interaction-base rounded-full w-full h-2 overflow-hidden">
                  <div data-freeship-fill class="bg-cta rounded-full h-full transition-[width] duration-500" style="width:0%"></div>
                </div>
              </div>"""


def radio_card(name, value, heading, sub="", icon="", checked=False, accent=False,
               blocked_note="", meta_key="", meta_prompt="", opens=""):
    """Big selectable card — order type, delivery time, delivery method.

    The trailing glyph is a real radio indicator (`.radio-dot`, styles.css),
    not the chevron this used to end with — a chevron promises navigation,
    but choosing here only selects (Ahmed asked for styled radio buttons,
    2026-07-22). `h-full` on the face: paired cards share a flex row, so the
    one without a subtitle used to stand shorter than its neighbour.

    accent=True is the gift treatment: the checked card takes a warm wash
    (`.radio-card-accent`), so إهداء reads as an occasion while the default
    order stays logistics.

    The glyph is bare on every card, gift included. It used to sit on an
    accent-yellow `rounded-full size-10` chip when accent=True, which made
    one option in a pick-one group carry a filled badge the other five did
    not — a circle around an icon reads as a token or an avatar, and next to
    the real `.radio-dot` on the same row it read as a second, competing
    indicator. Ahmed asked for it gone (2026-07-22). The wash still marks the
    gift card, and it only paints when the card is actually chosen, which is
    the distinction that was wanted in the first place.
    """
    sub_html = f'<span class="text-neutral-secondary text-xs">{e(sub)}</span>' if sub else ""
    icon_html = f'<span class="text-cta shrink-0">{icon}</span>'
    # `blocked_note` renders in the RADIO DOT's place, not under the card
    # (Ahmed, 2026-07-26): while the option is unavailable there is nothing to
    # indicate the state of, so the indicator is exactly the space the reason
    # should occupy. Which of the two shows is decided entirely by
    # `.option-blocked` on an ancestor (styles.css) — no JS toggles it, so the
    # dot and the note can never both be visible.
    note_html = (
        f'<span class="blocked-note shrink-0 text-neutral-secondary text-xs text-end leading-4">{e(blocked_note)}</span>'
        if blocked_note else ""
    )
    # The right-aligned status text (skill §3). Two states, and the distinction
    # carries real information: `--prompt` means "this choice is not finished,
    # press it" and is painted as a call to action; once a picker confirms, JS
    # writes the answer here and drops the modifier, so it becomes plain
    # resolved text. A row reading "اختر الفرع" and a row reading "فرع الزهور"
    # are then visibly different states rather than the same grey line.
    meta_html = (
        f'<span data-opt-meta="{e(meta_key)}" class="opt-meta is-prompt shrink-0 text-xs text-end leading-4">{e(meta_prompt)}</span>'
        if meta_key else ""
    )
    # `data-opens` makes selecting the row ALSO open its picker, so choosing
    # "pick up from a store" and choosing WHICH store are one gesture rather
    # than a selection followed by a hunt for the next control.
    opens_attr = f' data-opens="{e(opens)}"' if opens else ""
    return f"""
                <!-- min-w-0 on BOTH nested flex children. A flex item's
                     min-width is `auto`, so without these the label column
                     cannot shrink below its longest line and pushes the whole
                     checkout form wider than its grid track. Caught at 375 in
                     English, where the form ran 31px over and the page's
                     `overflow-x-hidden` swallowed it — clipped copy that no
                     amount of scrolling reveals, which is exactly why
                     CLAUDE.md calls this the most common bug class here.
                     Arabic never showed it: "أرسل الطلب كهدية لشخص تحبه" is
                     simply shorter than "Send this order as a gift to someone
                     you love". Latent until the site actually translated. -->
                <label class="flex-1 min-w-0 cursor-pointer"{opens_attr}>
                  <input type="radio" name="{e(name)}" value="{e(value)}" class="peer sr-only"{' checked' if checked else ''} />
                  <span class="flex justify-between items-center gap-3 bg-white px-5 py-4 border border-neutral-divider peer-checked:border-primary peer-checked:bg-primary-50 rounded-2xl transition-colors h-full{' radio-card-accent' if accent else ''}">
                    <span class="radio-card__body flex items-center gap-3 min-w-0">
                      {icon_html}
                      <span class="flex flex-col min-w-0">
                        <span class="font-semibold text-[#003616] text-base">{e(heading)}</span>
                        {sub_html}
                      </span>
                    </span>
                    {meta_html}<span class="radio-dot shrink-0" aria-hidden="true"></span>{note_html}
                  </span>
                </label>"""


# --------------------------------------------------------------------------
# Cart
# --------------------------------------------------------------------------
def price_sticker(price, size="md"):
    """The JAAD price sticker (Figma 9946:16778) — deep-green badge with the
    lime offset shadow and asymmetric corners, split EGP / whole / .dec. One
    badge everywhere a price shows. `size`: sm (cart rows, bundle, upsell) |
    md (product cards) | lg (product page)."""
    price = float(price or 0)
    whole = int(price)
    dec = f"{round((price - whole) * 100):02d}"
    variants = {
        "sm": ("px-1.5", "rounded-tl-[14px] rounded-br-[14px]", "shadow-[2px_3px_0px_#98CA55]", "text-[11px]", "text-[16px]"),
        "md": ("px-2", "rounded-tl-[20px] rounded-br-[20px]", "shadow-[3px_5px_0px_#98CA55]", "text-[15px]", "text-[24px]"),
        "lg": ("px-3 py-1", "rounded-tl-[22px] rounded-br-[22px]", "shadow-[3px_5px_0px_#98CA55]", "text-[19px]", "text-[32px]"),
    }
    pad, rad, sh, egp, wh = variants.get(size, variants["md"])
    return (f'<span class="inline-flex items-end gap-0.5 shrink-0 bg-[#006328] {sh} {pad} {rad} font-bold text-white latin">'
            f'<span class="{egp} leading-[1.4]">EGP</span>'
            f'<span class="{wh} leading-none">{whole}</span>'
            f'<span class="{egp} leading-[1.4]">.{dec}</span></span>')


def cart_line(p, qty=1, weight="250 جم"):
    from catalog import money, title as _title
    return f"""
              <!-- The thumb, stepper and price chip are all shrink-0 and with
                   gaps come to ~302px, so in a 295px column they squeezed the
                   title to zero width — product names vanished on mobile. Let
                   the row wrap below sm so the stepper and price drop to a
                   second line, and hold a floor under the title. -->
              <!-- data-cart-static: server-rendered so the page is not blank
                   without JS, but the cart store owns this list once it boots
                   and clears these on its first render. -->
              <article data-cart-static class="flex flex-wrap sm:flex-nowrap items-center gap-4 py-5 border-neutral-divider border-b">
                <img src="{e(p['image'])}" alt="{e(_title(p))}" class="bg-interaction-base p-2 rounded-xl w-20 h-20 object-contain shrink-0" loading="lazy" />
                <div class="flex flex-col flex-1 gap-1 min-w-[7rem]">
                  <h3 class="font-semibold text-[#29612F] text-base line-clamp-2">{e(_title(p))}</h3>
                  <span class="text-neutral-secondary text-xs">{e(weight)}</span>
                  <button type="button" class="mt-1 text-accent-error text-xs underline self-start">حذف</button>
                </div>
                <div data-stepper class="inline-flex items-center gap-1 p-1 border border-neutral-divider rounded-full shrink-0">
                  <button type="button" data-step="-1" class="place-items-center grid size-9 text-[#003616] transition-colors hover:bg-interaction-base rounded-full" aria-label="إنقاص"><span class="w-4 h-4">{ICON['minus']}</span></button>
                  <span data-qty class="min-w-[2ch] font-semibold text-[#003616] text-sm text-center latin">{qty}</span>
                  <button type="button" data-step="1" class="place-items-center grid size-9 bg-cta hover:bg-cta-hover text-white transition-colors rounded-full" aria-label="زيادة"><span class="w-4 h-4">{ICON['plus']}</span></button>
                </div>
                {price_sticker(p['price'], "sm")}
              </article>"""


def wallet_toggle(balance=WALLET_BALANCE):
    """
    "Pay from your wallet" — a switch, replacing the points banner (Ahmed,
    2026-07-26: simpler, a toggle, and the WALLET balance rather than points).

    Why the balance and not the points. The banner spoke in two currencies at
    once — "you have 100 points, so you can take EGP 100 off" — which asks the
    shopper to hold a conversion rate in their head to understand an offer.
    The wallet is already denominated in the same unit as the bill, so the
    switch can just say what it will do. The points balance has no endpoint
    behind it either way (DESIGN-NOTES §1); this at least stops the UI teaching
    a made-up exchange rate.

    Why a label + checkbox and never a button. On checkout this sits inside the
    place-order form, where a <button> with no explicit type submits it — the
    control would place the order. A checkbox is also the honest semantic: this
    is a persistent on/off choice, not an action, and it gets keyboard support,
    the right role and the right announced state for free.

    Two states, one line of copy each, and the card is a FIXED height (the
    `wallet-toggle` class in styles.css) so flipping it cannot resize the
    summary column. That is inherited from the banner this replaces, where the
    idle copy was a line longer than the used copy and pressing the button
    collapsed the block by 100px and shunted the whole summary up under the
    cursor. Same trap, same remedy — reserve the taller state.

    `balance` is written to a data attribute rather than baked into the copy
    alone, because scripts.js reads the amount from there at click time.
    """
    return f"""
            <!-- Light green, not the brand yellow it shipped as (Ahmed,
                 2026-07-26). #E9F3E6 is already this project's "good news"
                 tint — the discount chip in the summary directly below is drawn
                 on it — so the toggle and the saving it produces now read as
                 the same thought. Yellow is the PRICE colour here (every price
                 chip on the site is accent-yellow), which put the wallet in the
                 same visual family as the amounts it reduces. -->
            <!-- Minimised to ONE line (Ahmed, 2026-08-04): the balance sits
                 beside "الدفع من المحفظة" instead of stacked under it, so the
                 widget is a compact row rather than a two-line card. -->
            <label data-wallet-toggle data-wallet-balance="{balance}"
                   class="wallet-toggle flex items-center gap-3 bg-[#E9F3E6] px-4 py-3 rounded-xl cursor-pointer">
              <!-- The client's 3D wallet render (Ahmed, 2026-08-05), the same
                   glyph the account dashboard, the wallet page and the wallet
                   stat card already use — so the summary's "pay from wallet"
                   switch and the balance it spends read as one wallet across the
                   site. Kept at 36px (w-9), the exact footprint of the tinted
                   circle it replaces, so the fixed-height row does not shift. -->
              <img src="images/jaad/icons/wallet-3d.png" alt="" class="w-9 h-9 object-contain shrink-0" />
              <span class="flex flex-1 flex-wrap items-center gap-x-2 gap-y-0.5 min-w-0">
                <span class="font-semibold text-[#003616] text-sm">الدفع من المحفظة</span>
                <!-- Idle balance and the "deducted" caption share ONE grid cell,
                     so whichever shows, the row is the same height and a toggle
                     cannot resize the summary column. `invisible` (not the
                     `hidden` attribute) keeps both in flow while hiding the
                     inactive one from assistive tech. The balance carries
                     `accent-green` (#618F2B), the system's "Green Text" token,
                     NOT bright `success` (#16BB55) which fails AA on this tint.
                     data-wallet-amount stays so syncWalletBalance can update the
                     figure when redeemed points top the wallet up. -->
                <span class="grid">
                  <span class="col-start-1 row-start-1 inline-flex items-center self-start bg-white/70 px-2 rounded-full font-bold text-accent-green text-xs leading-5 latin" data-wallet-idle data-wallet-amount>EGP {balance}</span>
                  <span class="col-start-1 row-start-1 inline-flex items-center self-start font-semibold text-accent-green text-xs leading-5 invisible" data-wallet-used>تم الخصم</span>
                </span>
              </span>
              <!-- The real control. sr-only rather than display:none so it
                   stays focusable and announceable; the painted switch beside
                   it is aria-hidden decoration driven off :checked. -->
              <input type="checkbox" data-switch data-wallet-switch class="sr-only" />
              <span class="switch shrink-0" aria-hidden="true"><span class="switch__knob"></span></span>
            </label>"""


def bundle_item(p, checked=True):
    """
    One row of the 'frequently bought together' checklist.

    Carries the full `data-product` payload. It used to be presentation only,
    so the section's "أضف الجميع الى السلة" button had nothing to add:
    productFrom() walks up to the nearest [data-product] and bails without
    one, so the handler returned silently and the button did nothing — the
    same defect already fixed once on the upsell rail in scripts.js.
    """
    from catalog import money, title as _title
    return f"""
                <label data-product data-bundle-item
                       data-id="{e(p.get('id', 0))}" data-name="{e(_title(p))}"
                       data-price="{e(p['price'])}" data-image="{e(p['image'])}"
                       class="flex items-center gap-3 py-2 cursor-pointer">
                  <input type="checkbox" data-bundle-check{' checked' if checked else ''} class="accent-[#00451C] shrink-0 rounded w-5 h-5" />
                  <img src="{e(p['image'])}" alt="" class="bg-interaction-base shrink-0 p-1 rounded-lg w-12 h-12 object-contain" loading="lazy" />
                  <span class="flex-1 min-w-0 text-[#003616] text-sm leading-5 line-clamp-2">{e(_title(p))}</span>
                  {price_sticker(p['price'], "sm")}
                </label>"""


# --------------------------------------------------------------------------
# Commerce
# --------------------------------------------------------------------------
def product_card(p, slide=True, cat=None):
    """Back-compat shim → the canonical `product_widget` card (Ahmed, 2026-08-18).

    Every product card across the site — home rails, shop grid, category pages,
    cart/thank-you upsells and the product page's related rail — now renders the
    ONE Figma 'Product widget' design (green sticker price, orange cart→stepper
    button, bordered styled square, bold English name). Kept as a thin wrapper
    so existing call sites need no change. `cat` still overrides the listing
    filter key; a genuine discount on the product renders as an offer.
    """
    sale = p.get("sale")
    offer = sale if (sale and (p.get("price") or 0) > sale) else None
    return product_widget(p, sale=offer, slide=slide, cat=cat)


def product_widget(p, sale=None, slide=True, cat=None):
    """Figma 'Product widget' (Perfect Picks / Recently Viewed, node 9946:16778).

    A bordered rounded square image, a green sticker price badge with a lime
    offset shadow (rounded-tl + rounded-br only), a circular add-to-cart button
    straddling the image's bottom-right, and the English name below.

    Carries the same `data-*` the cart store reads (id/name/price/image), so the
    add button keeps the real add-to-cart UX (fly-to-cart + toast + badge).
    `sale` renders a discounted price with the original struck through.
    """
    pid = p.get("id", 0)
    en_name = p.get("name") or p.get("nameAr") or ""
    price = sale if sale is not None else (p.get("price") or 0)
    whole = int(price)
    dec = f"{round((price - whole) * 100):02d}"
    on_offer = sale is not None and (p.get("price") or 0) > sale
    old = (f'<span class="text-neutral-secondary text-sm line-through latin">EGP {money(p["price"])}</span>'
           if on_offer else "")
    width = "w-[258px] shrink-0 snap-start" if slide else "w-full"
    # Prefer the styled Figma photography where we have it (keyed by id).
    # Two sources for the image-style toggle: the in-scene styled shot (default)
    # and the white-background original. initImgStyleSwitch swaps [data-img-scene]
    # <img> between them; data-image (cart thumb) stays the scene hero.
    scene_img = (f"images/jaad/products-styled/{pid}.jpg"
                 if str(pid) in STYLED_IDS else p["image"])
    plain_img = p["image"]
    return f"""
          <article class="product-widget {width}" data-product data-cat="{e(cat if cat is not None else p.get('categorySlug',''))}"
                   data-price="{price}" data-id="{pid}" data-name="{e(p.get('nameAr') or en_name)}"
                   data-name-en="{e(en_name)}" data-image="{e(scene_img)}">
            <div class="relative">
              <a href="product-{pid}.html" class="block relative bg-white border border-[#C1C3C6] rounded-2xl aspect-square overflow-hidden">
                <img src="{e(scene_img)}" data-img-scene="{e(scene_img)}" data-img-plain="{e(plain_img)}" alt="{e(en_name)}" class="w-full h-full object-cover" loading="lazy" />
              </a>
              <!-- Add-to-cart uses the site CTA fill (.bg-cta) so it TRACKS the
                   runtime Green/Orange toggle (Ahmed, 2026-08-19): green in V1,
                   and html[data-btn="v2"] repaints every .bg-cta to orange — so
                   the card button and the primary CTAs never disagree. Once the
                   product is in the cart it swaps for a compact − N + counter
                   that edits the cart line (syncCardSteppers drives the swap). -->
              <div class="right-4 -bottom-5 z-10 absolute">
                <button type="button" data-add-to-cart aria-label="Add to cart"
                        class="btn-elevate place-items-center grid bg-cta hover:bg-cta-hover shadow-custom4 rounded-full size-10 text-white transition-colors">
                  <span class="w-[22px] h-[22px]">{ICON['cart']}</span>
                </button>
                <!-- The card counter is the SAME control as the product page's
                     qty_stepper (Ahmed, 2026-08-18): a white pill with a hairline
                     − and the green-filled +, scaled compact (size-8) to sit in
                     the add button's footprint. shadow-custom4 lifts it off the
                     photo the way the round add button was lifted. -->
                <div data-card-stepper hidden class="items-center gap-1 bg-white shadow-custom4 p-1 border border-neutral-divider rounded-full flex">
                  <button type="button" data-card-step="-1" aria-label="Decrease" class="place-items-center grid border border-neutral-divider hover:bg-interaction-base rounded-full size-10 sm:size-8 text-[#003616] shrink-0 transition-colors"><span class="w-5 h-5 sm:w-4 sm:h-4">{ICON['minus']}</span></button>
                  <span data-card-qty class="min-w-[1.5ch] font-bold text-[#003616] text-center latin">1</span>
                  <button type="button" data-card-step="1" aria-label="Increase" class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-10 sm:size-8 text-white shrink-0 transition-colors"><span class="w-5 h-5 sm:w-4 sm:h-4">{ICON['plus']}</span></button>
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-3 p-3 pt-9 sm:pt-3">
              <div class="flex flex-wrap items-center gap-2">
                <span class="items-end gap-0.5 self-start inline-flex bg-[#006328] shadow-[3px_5px_0px_#98CA55] px-2 rounded-tl-[20px] rounded-br-[20px] text-white latin">
                  <span class="text-[18px] leading-[1.4]">EGP</span>
                  <span class="text-[24px] leading-[1.2]">{whole}</span>
                  <span class="text-[18px] leading-[1.4]">.{dec}</span>
                </span>
                {old}
              </div>
              <h3 class="font-semibold text-black text-lg leading-snug">
                <a href="product-{pid}.html" data-product-title class="hover:text-[#29612F] transition-colors">{e(en_name)}</a>
              </h3>
            </div>
          </article>"""


def category_tile(cat, label=None, href="shop-category.html"):
    """
    Square (rounded) category tile — Figma Section 563:31568, switched from a
    circle to a rounded square at Ahmed's request (2026-08-02); the radius is
    the site's card `rounded-[20px]`, so the tiles match the product and hero
    cards. The CMS category images are photographs with their own backgrounds,
    not transparent cutouts, so they fill the square rather than float inside it.
    """
    name = label or cat["ar"]
    return f"""
        <a href="{href}" class="group flex flex-col items-center gap-3 sm:gap-4 w-full sm:w-[220px] xl:w-[250px] text-center">
          <span class="tile-lift relative bg-beige rounded-[20px] w-full aspect-square overflow-hidden group-hover:scale-[1.03]">
            <img src="{e(cat['image'])}" alt="{e(name)}" class="w-full h-full object-cover" loading="lazy" />
          </span>
          <span class="flex flex-col gap-1">
            <span class="font-bold text-[#003616] group-hover:text-primary text-base sm:text-xl xl:text-2xl transition-colors">{e(name)}</span>
            <span class="font-medium text-neutral-secondary text-sm sm:text-base xl:text-xl">تشكيلة متنوعة تبدا من <span class="latin">17</span> جنية</span>
          </span>
        </a>"""


def review_card(name, city, text, score="4.8"):
    """
    Dark testimonial card to Ahmed's reference (2026-07-29): a large accent-
    yellow opening quote, the testimonial, then an avatar with name and city.

    The avatar is the reviewer's INITIALS, not a photo — there are no real
    customer portraits and this project does not invent them (the same rule
    that left the branch phones missing). The star rating is dropped here on
    purpose; the quote glyph carries the section now. rating() still lives on
    the product page, so the two are just different treatments, not a drift.

    Colours are hand-checked for AA on the #14432f card: white/90 body ~8:1,
    white/75 city ~6.5:1, white initials on the #006328 avatar ~8:1.
    """
    parts = [w for w in name.split() if w]
    initials = "".join(w[0] for w in parts[:2])
    return f"""
          <!-- No h-full: on the mobile flex row it forced height:100% against an
               indefinite container and each card collapsed to its own content
               height (unequal). Dropping it lets the flex row (mobile) and the
               grid (md+) both stretch every card to the tallest — equal heights
               either way (Ahmed, 2026-08-02). -->
          <article class="flex flex-col gap-5 bg-[#14432f] p-6 xl:p-8 rounded-[20px] w-[80%] sm:w-[340px] md:w-auto shrink-0 snap-start">
            <span class="block w-10 xl:w-12 h-10 xl:h-12 text-accent-yellow" aria-hidden="true">{ICON['quote']}</span>
            <p class="flex-1 text-white/90 text-base xl:text-lg leading-8">{e(text)}</p>
            <div class="flex items-center gap-3">
              <span class="place-items-center grid bg-primary rounded-full font-bold text-white shrink-0 size-11" aria-hidden="true">{e(initials)}</span>
              <span class="flex flex-col min-w-0">
                <span class="font-bold text-white text-sm truncate">{e(name)}</span>
                <span class="text-white/75 text-xs truncate">{e(city)}</span>
              </span>
            </div>
          </article>"""


def article_card(img, tags, meta, title_, excerpt, href="blog.html", rail=False):
    """The ONE article card, Figma 'Latest from JAAD' (node 9974:21059).

    Lifted out of home.py (Ahmed, 2026-08-20) so the homepage rail and the blog
    index/related rails render the SAME card. Before this, the blog pages used a
    separate inherited Abu-Auf card — a horizontal image-beside-text strip in
    Arabic — so the blog looked like a different site from the homepage that
    linked to it.

    `rail=True` gives the card the fixed width + snap alignment a horizontally
    scrolling track needs; the grid variant fills its column.
    """
    tag_html = "".join(
        f'<span class="inline-flex items-center px-3 py-1 border border-[#29612F] '
        f'rounded-full font-medium text-[#29612F] text-xs">{e(t)}</span>'
        for t in tags
    )
    # On phones a rail card is a fixed slide; from md up it becomes a grid cell.
    width = ("w-[82vw] max-w-[330px] shrink-0 snap-start md:w-auto md:max-w-none"
             if rail else "")
    return f"""
              <a href="{e(href)}" class="group flex flex-col gap-4 bg-white shadow-[0px_8px_8px_rgba(0,0,0,0.03)] p-4 rounded-3xl {width}">
                <div class="relative rounded-2xl h-[200px] xl:h-[260px] overflow-hidden">
                  <img src="{e(img)}" alt="{e(title_)}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy" />
                </div>
                <div class="flex flex-wrap justify-between items-center gap-2">
                  <div class="flex flex-wrap gap-2">{tag_html}</div>
                  <span class="font-medium text-[#636959] text-[13px] whitespace-nowrap">{e(meta)}</span>
                </div>
                <h3 class="font-bold text-[#006328] text-lg leading-[1.4] group-hover:underline">{e(title_)}</h3>
                <p class="text-[#1e2219] text-sm leading-[1.5] line-clamp-3">{e(excerpt)}</p>
              </a>"""


# `recipe_card` lived here until 2026-08-20 — an inherited Abu-Auf horizontal
# card (Arabic CTA, image beside text) with no call sites left once the blog was
# rebuilt on `article_card`. Removed rather than kept, so there is exactly ONE
# article card in the codebase and no way to reintroduce the old look.


def info_card(img, heading, body, cta_label, cta_href, img_class="w-[100px] h-[100px]"):
    """The paired branches / export cards at the foot of the home page."""
    return f"""
            <div class="flex flex-col items-center gap-4 bg-interaction-base px-6 py-12 xl:py-16 rounded-[20px] text-center">
              <img src="{e(img)}" alt="" class="{img_class} object-contain" loading="lazy" />
              <h3 class="mt-4 font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2]">{e(heading)}</h3>
              <p class="max-w-[280px] text-neutral-800 text-base xl:text-lg leading-7">{body}</p>
              {button(cta_label, cta_href, "primary", "lg", "mt-4")}
            </div>"""


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
# Production origin, for canonical and og:url/og:image, which social
# scrapers need as absolute URLs.
#
# Deliberately EMPTY. The build is not deployed yet and jad.com is the
# client's existing live site, not this one — pointing canonical at it would
# tell search engines these pages are duplicates of somebody else's. While
# it is empty the shell emits the tags that work without a domain and skips
# the three that do not. Set it once the real host is known; DESIGN-NOTES
# tracks it as a pre-launch item.
SITE_ORIGIN = ""

OG_IMAGE = "images/jaad/brand/logo-jaad.svg"

# Keep this build out of search results.
#
# It is a pixel-close rebuild of a storefront that is live and trading at
# jad.com, and it still carries placeholder legal pages and invented
# reviews. Indexed, it would compete with the client's real site for their own
# brand terms and could land a customer on a demo they believe is real.
#
# NOTE this is a `noindex` META TAG, not a robots.txt `Disallow`. Those are not
# interchangeable and the difference is the usual mistake: `Disallow` stops
# Google *fetching* the page, which means it never reads the noindex — and it
# will still list a URL it has never fetched if something links to it. To be
# reliably absent you have to let the crawler IN and tell it no. robots.txt
# here therefore allows crawling on purpose.
#
# One line to flip when this becomes the real production site.
ALLOW_INDEXING = False


def _social_meta(title_text, description, path):
    """og:/twitter: block. Egypt shares storefront links on WhatsApp far more
    than anywhere else, and a link with no card is a bare grey URL."""
    tags = [
        '<meta name="theme-color" content="#00451C" />',
    ]
    if not ALLOW_INDEXING:
        tags.append('<meta name="robots" content="noindex, nofollow" />')
    tags += [
        f'<meta property="og:title" content="{e(title_text)}" />',
        f'<meta property="og:description" content="{e(description)}" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="جاد" />',
        '<meta property="og:locale" content="ar_EG" />',
        '<meta name="twitter:card" content="summary_large_image" />',
    ]
    if SITE_ORIGIN:
        url = SITE_ORIGIN.rstrip("/") + path
        tags.append(f'<link rel="canonical" href="{e(url)}" />')
        tags.append(f'<meta property="og:url" content="{e(url)}" />')
        tags.append(
            f'<meta property="og:image" content="{e(SITE_ORIGIN.rstrip("/") + "/" + OG_IMAGE)}" />'
        )
    return "\n    ".join(tags)


_SECTION_OPEN = re.compile(r"<section(?![^>]*\bdata-reveal\b)(\s|>)")


def _with_reveal(body):
    """
    Tag every top-level `<section>` for the scroll reveal.

    Done here rather than in 37 page files so the entrance is one decision and
    genuinely site-wide — it was previously hand-applied to home, product and
    the auth layout only, so most of the site scrolled dead.

    Sections that already carry `data-reveal` are skipped, so the few places
    that opted in by hand keep exactly the behaviour they had.

    Safe by construction: the hidden state lives behind `.js-reveal`, which JS
    puts on <html> at runtime, and the observer reveals anything already in
    the viewport without animating it. So a page still paints fully with JS
    off, and nothing fades in underneath the shopper on first load — only
    sections they scroll to.
    """
    return _SECTION_OPEN.sub(r"<section data-reveal\1", body)


_ASSET_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static-export")
_asset_v_cache = {}


def _asset_v(filename):
    """Short content hash appended to a built asset link as ?v=… for cache-
    busting (Ahmed, 2026-08-19). An edited styles.css/scripts.js then loads FRESH
    on the next normal reload instead of the browser serving a stale cached copy
    — the recurring "you have to hard-refresh" trap. The hash is of the file's
    CURRENT bytes, so the URL only changes when the file changes.

    Caveat: tailwind.css is regenerated AFTER the pages are written, so its hash
    here is the PREVIOUS build's; it settles on the next build. Utility changes
    are rare, so that one-build lag is acceptable. IMPORTANT: this is baked at
    build time, so a styles.css/scripts.js edit needs a rebuild to update the
    version — run build after touching those files."""
    if filename not in _asset_v_cache:
        try:
            with open(os.path.join(_ASSET_ROOT, filename), "rb") as f:
                _asset_v_cache[filename] = hashlib.md5(f.read()).hexdigest()[:8]
        except OSError:
            _asset_v_cache[filename] = "1"
    return _asset_v_cache[filename]


def page(title_text, description, body, page_id, path, main_class="overflow-x-clip"):
    """
    Standard document shell. Header, footer and overlays are mount points
    filled at runtime by scripts.js, so chrome changes need no rebuild.

    `overflow-x-clip`, NOT `overflow-x-hidden`. They clip identically, but
    `hidden` on one axis forces the other to `auto`, which makes <main> a
    scroll container — and a scroll container is what `position: sticky`
    sticks to. Any sticky descendant then measures itself against a box that
    never scrolls, so it silently does nothing: no error, no warning, the
    element simply sits there. That is what blocked the sticky product gallery.
    `clip` creates no scroll container and leaves the other axis visible, so
    sticky resolves against the viewport as intended.

    This is the same class of silent failure as the `[hidden]` and emit-order
    traps in CLAUDE.md — the markup looked right and lost anyway. If a sticky
    element ever "does nothing" here, walk its ancestors for an overflow that
    is not `visible` or `clip` before touching the element itself.
    """
    body = _with_reveal(body)
    social = _social_meta(title_text, description, path)
    return f"""<!doctype html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!-- Don't cache the HTML page itself (Ahmed, 2026-08-19). Asset links carry
         a ?v=<hash> so CSS/JS always load fresh, but the browser was still
         serving a stale cached COPY OF THE PAGE (old markup persisted after a
         fix). Revalidating the HTML means every reload picks up the current
         page — and thus the current versioned asset links — with no hard-refresh. -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>{e(title_text)}</title>
    <meta name="description" content="{e(description)}" />
    {social}
    <!-- Jaad design system. Tailwind is COMPILED AT BUILD TIME by
         `npm run css` (config: tailwind.config.js) into tailwind.css. It used
         to be the Play CDN, which Tailwind itself warns against in production:
         that shipped ~120KB of JavaScript which then had to scan the DOM and
         generate the stylesheet on every visit, so nothing was styled until it
         finished — a flash of unstyled content on exactly the slow mobile
         connections this storefront is for. Now it is one 30KB cacheable file.

         ORDER IS LOAD-BEARING: tailwind.css first, styles.css second.
         styles.css contains rules whose whole purpose is to beat a utility
         ([hidden] !important, the focus ring re-armed over `outline-none`,
         the sticky-nav selector). Reverse these two and they stop working. -->
    <link rel="stylesheet" href="tailwind.css?v={_asset_v('tailwind.css')}" />
    <link rel="stylesheet" href="styles.css?v={_asset_v('styles.css')}" />
    <!-- The client's 3D leaf mark as the tab icon (Ahmed, 2026-08-05) — the
         same spec-leaf.png the mega-panel bullets and product benefits use, so
         the favicon is a recognisable brand glyph rather than the white
         wordmark, which reads as a blank sliver at 16px. -->
    <link rel="icon" type="image/svg+xml" href="images/jaad/brand/favicon.svg" />
    <!-- The English dictionary, generated by build/i18n.py. Also `defer`, and
         listed FIRST: deferred scripts run in document order, so this has
         always defined window.JAAD_I18N by the time scripts.js boots and
         merges it. A plain script rather than a fetch, so the language switch
         still works from file://. -->
    <script defer src="i18n-en.js?v={_asset_v('i18n-en.js')}"></script>
    <script defer src="scripts.js?v={_asset_v('scripts.js')}"></script>
  </head>
  <body data-page="{e(page_id)}" data-path="{e(path)}" class="antialiased bg-white">
    <!-- First focusable thing on the page. The header is three bands and a
         mega-menu, so a keyboard shopper otherwise tabbed through the whole
         of it on every page before reaching any content. Visually hidden
         until focused. -->
    <a href="#main" class="skip-link">تخطي إلى المحتوى</a>

    <!-- Shared header is injected here by scripts.js -->
    <div id="site-header"></div>

    <main id="main" tabindex="-1" class="{main_class}">{body}
    </main>

    <!-- Shared footer is injected here by scripts.js -->
    <div id="site-footer"></div>
  </body>
</html>
"""
