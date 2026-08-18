"""Contact — Figma 'Contact' (918:41498)."""
from components import field, page, page_header

SLUG = "contact-us.html"

CHANNELS = [
    ("الخط الساخن", "19969", "tel:19969"),
    ("البريد الالكتروني", "info@jad.com", "mailto:info@jad.com"),
    ("واتساب", "+20 105 062 4300", "https://wa.me/+201050624300"),
]


def build():
    channels = "".join(f"""
              <a href="{href}" class="flex flex-col gap-1 bg-interaction-base hover:bg-beige px-6 py-5 rounded-2xl transition-colors">
                <span class="text-neutral-secondary text-sm">{label}</span>
                <span class="font-bold text-[#003616] text-lg latin">{value}</span>
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
            <div class="flex flex-col gap-1 bg-white shadow-custom4 p-6 rounded-2xl">
              <span class="font-bold text-[#003616] text-base">المقر الرئيسي</span>
              <span class="text-neutral-secondary text-sm leading-7">المنطقة الصناعية 31-33، التجمع الثالث، القاهرة الجديدة، مصر</span>
            </div>
          </div>

          <form class="flex flex-col gap-5 bg-white shadow-custom4 p-6 xl:p-8 rounded-[20px]">
            <h2 class="font-bold text-[#003616] text-xl">ابعتلنا رسالة</h2>
            <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم", "name", required=True)}
{field("رقم الهاتف", "phone", "tel", required=True)}
            </div>
{field("البريد الالكتروني", "email", "email", required=True)}
{field("الموضوع", "subject")}
            <div class="flex flex-col gap-1.5">
              <label for="message" class="font-medium text-neutral-secondary text-sm">الرسالة<span class="text-accent-error">*</span></label>
              <textarea id="message" name="message" rows="5" required
                        class="bg-white px-4 py-3 border-2 border-neutral-divider focus:border-cta rounded-xl outline-none w-full text-[#003616] text-base transition-colors"></textarea>
            </div>
            <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">أرسال</button>
          </form>
        </div>
      </section>"""

    return page("أتصل بنا | جاد", "تواصل مع خدمة عملاء جاد.",
                body, "contact-us", "/contact-us")
