"""
Shared auth layout — Figma 'Account Sign In/ Create Account' (205:10427).

login / register / forget-password / reset-password are the same two-card
shell with a different form in the primary card, so they share this builder.
"""
from catalog import e
from components import field, page, page_header

ICON_GOOGLE = ('<svg viewBox="0 0 24 24" class="w-5 h-5">'
               '<path fill="#4285F4" d="M22.6 12.2c0-.8-.1-1.6-.2-2.3H12v4.5h6c-.3 1.4-1.1 2.6-2.3 3.4v2.8h3.7c2.2-2 3.4-5 3.4-8.4Z"/>'
               '<path fill="#34A853" d="M12 23c3.1 0 5.7-1 7.6-2.8l-3.7-2.8c-1 .7-2.3 1.1-3.9 1.1-3 0-5.5-2-6.4-4.7H1.8v2.9C3.7 20.5 7.6 23 12 23Z"/>'
               '<path fill="#FBBC05" d="M5.6 13.8c-.2-.7-.4-1.4-.4-2.3s.1-1.6.4-2.3V6.3H1.8C1 7.9.5 9.9.5 11.5s.4 3.6 1.3 5.2l3.8-2.9Z"/>'
               '<path fill="#EA4335" d="M12 4.6c1.7 0 3.2.6 4.4 1.7l3.3-3.3C17.7 1.2 15.1 0 12 0 7.6 0 3.7 2.5 1.8 6.3l3.8 2.9c.9-2.7 3.4-4.6 6.4-4.6Z"/></svg>')
ICON_FB = ('<svg viewBox="0 0 24 24" fill="#1877F2" class="w-5 h-5">'
           '<path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06C2 17.06 5.66 21.21 10.44 22v-7.03H7.9v-2.9h2.54V9.85'
           'c0-2.51 1.49-3.9 3.78-3.9 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.87h2.78l-.44 2.9h-2.34V22'
           'C18.34 21.21 22 17.06 22 12.06Z"/></svg>')

ICON_HOME = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V10Z" '
             'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>')
ICON_BAG2 = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6ZM3 6h18M16 10a4 4 0 0 1-8 0" '
             'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><rect x="2" y="4" width="20" height="16" rx="2" '
             'stroke="currentColor" stroke-width="1.7"/><path d="m2 7 10 6 10-6" stroke="currentColor" stroke-width="1.7"/></svg>')


def password_field(label="كلمة السر", name="password", autocomplete="current-password"):
    """Password input with a reveal toggle (wired in scripts.js by data-reveal).

    `autocomplete` matters here: a password manager offers to *fill* on
    current-password and to *generate and save* on new-password, so sign-in
    and sign-up need different tokens. Register passes new-password.

    The reveal button was a 20x20 target — under the 24px WCAG 2.2 AA floor
    and awkward on a phone. It keeps its 20px glyph inside a 44px button.
    """
    return f"""
                <div class="flex flex-col gap-1.5">
                  <label for="{e(name)}" class="font-medium text-neutral-secondary text-sm">{e(label)}</label>
                  <div class="relative">
                    <input type="password" id="{e(name)}" name="{e(name)}" required autocomplete="{e(autocomplete)}"
                           class="bg-white px-4 py-3 pe-12 border-2 border-neutral-divider focus:border-cta rounded-xl outline-none w-full text-[#003616] text-base transition-colors" />
                    <!-- data-pw-toggle, NOT data-reveal: the site-wide entrance
                         animation keys off [data-reveal] on sections, and an eye
                         button that also carried data-reveal got swept into it —
                         initReveal rewrote its attribute to "in" (breaking the
                         toggle's input lookup) and the reveal transform overrode
                         the button's -translate-y-1/2, dropping the icon to the
                         field's bottom edge (Ahmed, 2026-08-03). -->
                    <button type="button" data-pw-toggle="{e(name)}" aria-label="إظهار كلمة السر"
                            class="top-1/2 end-1 absolute place-items-center grid w-11 h-11 text-neutral-secondary hover:text-cta -translate-y-1/2 transition-colors">
                      <svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">
                        <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z" stroke="currentColor" stroke-width="1.7"/>
                        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.7"/>
                      </svg>
                    </button>
                  </div>
                </div>"""


SIDE_CARD = f"""
            <!-- DOM-first so RTL puts it in the right column at lg. The Figma
                 auth frame (368:21314) leads with the sign-in form on mobile
                 and drops this beneath it, so below lg it moves to the end. -->
            <!-- Layout mirrors the sign-in card so the two primary buttons land
                 on the same line (Ahmed, 2026-08-04): heading, then a flex-1
                 region for the blurb, the CTA, then a flex-1 region for the
                 notes. The CTA sits between two equal-growing regions, so it
                 centres at the same offset as the sign-in card's button (both
                 cards are equal height). -->
            <aside class="flex flex-col gap-6 bg-interaction-base p-8 xl:p-10 rounded-[20px] order-last lg:order-none min-w-0">
              <h2 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2] text-center">إنشاء حساب جديد</h2>
              <div class="flex flex-1 flex-col justify-center gap-6">
                <div class="flex justify-center items-center gap-3">
                  <span class="place-items-center grid bg-white rounded-full text-cta size-11">{ICON_HOME}</span>
                  <span class="place-items-center grid bg-white rounded-full text-cta size-11">{ICON_BAG2}</span>
                  <span class="place-items-center grid bg-white rounded-full text-cta size-11">{ICON_MAIL}</span>
                </div>
                <p class="text-neutral-800 text-base text-center leading-8">
                  عند إنشاء حساب، هتكسب نقاط خصم في محفظتك ويمكنك الدفع بشكل أسرع
                  والاحتفاظ بأكثر من عنوان وتتبع الطلبات والمزيد.
                </p>
              </div>
              <!-- Secondary to the sign-in CTA (Ahmed, 2026-08-04): sign-in is
                   the primary action, so create-account is an outline button —
                   same size (py-4) so it aligns with متابعة, lighter weight. -->
              <a href="register.html" class="bg-transparent hover:bg-white py-4 border-2 border-cta rounded-full font-semibold text-cta text-base text-center transition-colors">إنشاء حساب</a>
              <div class="flex flex-1 flex-col justify-center gap-4 pt-6 border-neutral-divider border-t">
                <p class="flex items-start gap-3 text-neutral-secondary text-sm leading-6">
                  <span class="mt-0.5 text-cta shrink-0">{ICON_MAIL}</span>
                  في حالة عمل طلب من قبل كضيف (بدون حساب)، الرجاء عمل حساب الآن بنفس الإيميل المستخدم في الطلب لمتابعة حالة الشحن.
                </p>
                <p class="flex items-start gap-3 text-neutral-secondary text-sm leading-6">
                  <span class="mt-0.5 text-cta shrink-0">{ICON_BAG2}</span>
                  الدخول بقى برقم موبايلك ورمز تحقق سريع — من غير كلمة مرور. لو عندك حساب قديم، سجّل الدخول بنفس رقم موبايلك المسجّل.
                </p>
              </div>
            </aside>"""

SOCIAL = f"""
                <div class="flex flex-col gap-3 pt-6 border-neutral-divider border-t">
                  <div class="gap-3 grid sm:grid-cols-2">
                    <button type="button" class="flex justify-center items-center gap-2 hover:bg-interaction-base py-3 border border-neutral-divider rounded-full font-semibold text-[#003616] text-sm transition-colors">
                      {ICON_GOOGLE}<span>سجل بأستخدام جوجل</span>
                    </button>
                    <button type="button" class="flex justify-center items-center gap-2 hover:bg-interaction-base py-3 border border-neutral-divider rounded-full font-semibold text-[#003616] text-sm transition-colors">
                      {ICON_FB}<span>سجل بأستخدام فيسبوك</span>
                    </button>
                  </div>
                </div>"""


def auth_page(title_text, description, heading, form_html, page_id, path,
              crumb, side=True, social=True, form_attrs="", hero="",
              form_contents=False):
    # `form_attrs` lets a page tag its form for a specific handler — the
    # sign-in page uses data-login-form, which runs a real (demo) credential
    # check rather than the generic data-demo-form success toast.
    # `hero` is an optional visual rendered ABOVE the heading (the verify page
    # puts its 3D icon there, sitting bare over the title — no tinted disc).
    # `form_contents` makes the <form> a `display:contents` box so its children
    # become direct flex items of the card — the sign-in page uses this to place
    # its own flex-1 regions and centre the CTA in line with the create-account
    # card's button (see login.py).
    attrs = (" " + form_attrs) if form_attrs else ""
    form_class = "contents" if form_contents else "flex flex-col gap-5"
    hero_html = f'<div class="flex justify-center">{hero}</div>' if hero else ""
    body = f"""{page_header("", [("الرئيسية", "index.html"), (crumb, None)])}

      <section class="py-8 xl:py-12">
        <div class="items-stretch gap-6 xl:gap-8 grid grid-cols-1 {'lg:grid-cols-2' if side else 'max-w-[560px] mx-auto'} mx-auto px-4 max-w-[1536px]">
          {SIDE_CARD if side else ''}
          <!-- The two auth cards are equal-height (items-stretch on the grid).
               Titles pin to the top (aligned); the sign-in page passes
               form_contents=True and its own flex-1 regions so the CTA centres
               on the same line as the create-account button (Ahmed, 2026-08-04). -->
          <div class="flex flex-col gap-6 bg-white shadow-custom4 p-8 xl:p-10 rounded-[20px] min-w-0">
            {hero_html}
            <h1 class="font-medium text-[#29612F] text-[32px] md:text-[40px] leading-[1.2] text-center">{e(heading)}</h1>
            <form class="{form_class}"{attrs}>{form_html}
            </form>
            {SOCIAL if social else ''}
          </div>
        </div>
      </section>"""
    return page(title_text, description, body, page_id, path)
