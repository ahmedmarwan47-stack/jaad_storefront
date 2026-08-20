"""Contact — Figma 'Contact' (918:41498)."""
from components import field, page, page_header

SLUG = "contact-us.html"

# PLACEHOLDER contact channels, per the fork plan (Ahmed, 2026-08-20). The
# hotline, WhatsApp number and head-office address that shipped here until now
# were the FORK SOURCE's real, live details — a shopper tapping them reached a
# different, unrelated company. Removed for the same reason the footer and the
# social links were (see CONTACT/SOCIALS in scripts.js): absence over invention.
# The hotline below matches the placeholder the footer already uses; WhatsApp is
# dropped entirely rather than invented. Swap for Jaad's real details at launch.
CHANNELS = [
    ("الخط الساخن", "01200000000", "tel:01200000000"),
    ("البريد الالكتروني", "info@jad.com", "mailto:info@jad.com"),
]


def build():
    channels = "".join(f"""
              <a href="{href}" class="flex flex-col gap-1 bg-cream hover:bg-cream px-6 py-5 rounded-2xl transition-colors">
                <span class="text-muted text-sm">{label}</span>
                <span class="font-bold text-ink text-lg latin">{value}</span>
              </a>""" for label, value, href in CHANNELS)

    body = f"""{page_header("أتصل بنا", [("الرئيسية", "index.html"), ("أتصل بنا", None)])}

      <section class="py-8 xl:py-10">
        <div class="items-start gap-8 xl:gap-12 grid lg:grid-cols-2 mx-auto px-4 max-w-[1536px]">
          <div class="flex flex-col gap-6">
            <p class="text-neutral-800 text-base xl:text-lg leading-8">
              لو عندك أي استفسار أو اقتراح، إحنا هنا. اختار الطريقة اللي تناسبك أو ابعتلنا رسالة وهنرد عليك في أقرب وقت.
            </p>
            <div class="flex flex-col gap-3">{channels}
            </div>
            <!-- The head-office card is GONE (Ahmed, 2026-08-20): the address
                 it carried was the fork source's real factory address, and
                 i18n.py already records that it was removed, not reused. It
                 comes back when Jaad's own address exists. Working hours are
                 the honest thing to show in its place. -->
            <div class="flex flex-col gap-1 bg-white shadow-custom4 p-6 rounded-2xl">
              <span class="font-bold text-ink text-base">مواعيد العمل</span>
              <span class="text-muted text-sm leading-7">من السبت للخميس، من 9 صباحاً حتى 6 مساءً</span>
            </div>
          </div>

          <form class="flex flex-col gap-5 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]">
            <h2 class="font-bold text-heading text-xl">ابعتلنا رسالة</h2>
            <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم", "name", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
            </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("الموضوع", "subject")}
            <div class="flex flex-col gap-1.5">
              <label for="message" class="font-medium text-muted text-sm">الرسالة<span class="text-error">*</span></label>
              <textarea id="message" name="message" rows="5" required
                        class="bg-white px-4 py-3 border-2 border-divider focus:border-cta rounded-xl outline-none w-full text-ink text-base transition-colors"></textarea>
            </div>
            <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">أرسال</button>
          </form>
        </div>
      </section>"""

    return page("أتصل بنا | جاد", "تواصل مع خدمة عملاء جاد.",
                body, "contact-us", "/contact-us")
