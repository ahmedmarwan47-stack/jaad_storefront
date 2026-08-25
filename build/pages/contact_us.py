"""Contact — rebuilt around a photographic hero (Ahmed, 2026-08-25).

Was a page_header strip over a two-column block: a text column of channel
tiles on one side and a full-height form on the other, both on flat cream.

Now: a hero photograph, and a body that is pulled UP over its lower edge so the
form is already in frame before you scroll — it reads as hanging off the hero
rather than starting below it. The photograph moves slower than the page as you
scroll, so the two layers separate.

The form sits on the END side (right in English, and it mirrors on its own in
Arabic, because the columns are grid order rather than hand-placed). The channel
cards take the START side as glass — they are over the photograph at the top of
the scroll, which is the only place a glass panel has anything to refract.
"""
from components import field, page

SLUG = "contact-us.html"

# PLACEHOLDER contact channels, per the fork plan (Ahmed, 2026-08-20). The
# hotline, WhatsApp number and head-office address that shipped here until now
# were the FORK SOURCE's real, live details — a shopper tapping them reached a
# different, unrelated company. Removed for the same reason the footer and the
# social links were (see CONTACT/SOCIALS in scripts.js): absence over invention.
# The hotline below matches the placeholder the footer already uses; WhatsApp is
# dropped entirely rather than invented. Swap for Jaad's real details at launch.
ICON_PHONE = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
              '<path d="M6.6 3.5 8.4 7l-1.9 1.9a12 12 0 0 0 5.6 5.6L14 12.6l3.5 1.8v3.3c0 1-.8 1.8-1.8 1.7'
              'A15.5 15.5 0 0 1 3.6 6.3c-.1-1 .7-1.8 1.7-1.8h1.3Z" stroke="currentColor" stroke-width="1.6" '
              'stroke-linejoin="round"/></svg>')
ICON_MAIL = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
             '<rect x="3" y="5.5" width="18" height="13" rx="2.5" stroke="currentColor" stroke-width="1.6"/>'
             '<path d="m4.5 8 6.6 4.6a1.6 1.6 0 0 0 1.8 0L19.5 8" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round"/></svg>')
ICON_CLOCK = ('<svg viewBox="0 0 24 24" fill="none" class="w-5 h-5">'
              '<circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.6"/>'
              '<path d="M12 7.5V12l3 1.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>')

CHANNELS = [
    (ICON_PHONE, "الخط الساخن", "01200000000", "tel:01200000000"),
    (ICON_MAIL, "البريد الالكتروني", "info@jad.com", "mailto:info@jad.com"),
]


def build():
    cards = "".join(f"""
              <a href="{href}" class="contact-card">
                <span class="contact-card__icon" aria-hidden="true">{icon}</span>
                <span class="contact-card__body">
                  <span class="contact-card__label">{label}</span>
                  <span class="contact-card__value latin">{value}</span>
                </span>
              </a>""" for icon, label, value, href in CHANNELS)

    # The head-office card is GONE (Ahmed, 2026-08-20): the address it carried
    # was the fork source's real factory address, and i18n.py already records
    # that it was removed, not reused. It comes back when Jaad's own address
    # exists. Working hours are the honest thing to show in its place.
    cards += f"""
              <div class="contact-card contact-card--static">
                <span class="contact-card__icon" aria-hidden="true">{ICON_CLOCK}</span>
                <span class="contact-card__body">
                  <span class="contact-card__label">مواعيد العمل</span>
                  <span class="contact-card__value">من السبت للخميس، من 9 صباحاً حتى 6 مساءً</span>
                </span>
              </div>"""

    body = f"""
      <section class="contact-hero" data-contact-hero>
        <!-- data-contact-parallax: moved by initContactParallax, which is why
             the image is taller than its frame and inset past both edges — it
             needs somewhere to travel without ever showing a gap. -->
        <img src="images/jaad/site/contact-hero.jpg" alt="" aria-hidden="true"
             class="contact-hero__img" data-contact-parallax />
        <span class="contact-hero__veil" aria-hidden="true"></span>
        <div class="contact-hero__inner">
          <h1 class="contact-hero__title">أتصل بنا</h1>
          <p class="contact-hero__sub">
            لو عندك أي استفسار أو اقتراح، إحنا هنا. اختار الطريقة اللي تناسبك أو ابعتلنا رسالة وهنرد عليك في أقرب وقت.
          </p>
        </div>
      </section>

      <section class="contact-body">
        <div class="contact-body__grid">
          <div class="contact-cards">{cards}
          </div>

          <form class="contact-form">
            <h2 class="contact-form__title">ابعتلنا رسالة</h2>
            <div class="gap-3 grid sm:grid-cols-2">
{field("الاسم", "name", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
            </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("الموضوع", "subject")}
            <div class="flex flex-col gap-1.5">
              <label for="message" class="font-medium text-muted text-sm">الرسالة<span class="text-error">*</span></label>
              <textarea id="message" name="message" rows="4" required
                        class="bg-white px-4 py-2.5 border border-divider focus:border-cta rounded-xl outline-none w-full text-ink text-sm transition-colors"></textarea>
            </div>
            <button type="submit" class="bg-cta hover:bg-cta-hover py-3 rounded-full font-semibold text-white text-sm transition-colors">أرسال</button>
          </form>
        </div>
      </section>"""

    return page("أتصل بنا | جاد", "تواصل مع خدمة عملاء جاد.",
                body, "contact-us", "/contact-us")
