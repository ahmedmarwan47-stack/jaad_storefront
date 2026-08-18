"""FAQs — Figma 'FAQs' (399:27159)."""
from components import accordion, page, page_header

SLUG = "faqs.html"

GROUPS = [
    ("الطلب والتوصيل", [
        ("إزاي أطلب من الموقع؟",
         "اختار المنتجات اللي تحبها وضيفها للسلة، بعدين اضغط على «أطلب الآن» واملأ بيانات "
         "التوصيل. هتوصلك رسالة تأكيد على البريد الالكتروني ورقم الهاتف."),
        ("الطلب بيوصل في قد إيه؟",
         "داخل القاهرة الكبرى التوصيل خلال ساعتين. باقي المحافظات من يوم لثلاثة أيام عمل "
         "حسب المنطقة."),
        ("كام الحد الأدنى للطلب؟",
         "الحد الأدنى للطلب 150 جنيه، ومصاريف التوصيل بتحسب حسب المنطقة وبتظهر قبل تأكيد الطلب."),
        ("بتوصلوا لكل المحافظات؟",
         "أيوه، بنوصل لكل محافظات مصر. مصاريف التوصيل ومدته بتختلف حسب المنطقة وبتظهر قبل تأكيد الطلب."),
    ]),
    ("الدفع", [
        ("طرق الدفع المتاحة إيه؟",
         "بنقبل الدفع عند الاستلام، بطاقات الائتمان (فيزا وماستركارد)، اتصالات كاش، "
         "وفاليو، بالإضافة لرصيد المحفظة."),
        ("الدفع أونلاين آمن؟",
         "أيوه، كل عمليات الدفع بتتم من خلال بوابة دفع مؤمنة، وإحنا مابنحتفظش ببيانات بطاقتك."),
    ]),
    ("المنتجات والاسترجاع", [
        ("المنتجات طازة إزاي؟",
         "بنحمص ونعبّي على دفعات صغيرة، والتغليف بيحافظ على النكهة والريحة لحد ما يوصلك."),
        ("أقدر أرجّع منتج؟",
         "تقدر تطلب استرجاع خلال 14 يوم من الاستلام طالما المنتج في حالته الأصلية وغير مفتوح. "
         "راجع سياسة الاسترجاع للتفاصيل."),
        ("إزاي أكسب نقاط؟",
         "بتكسب نقاط على كل جنيه بتشتريه، وتقدر تستبدلها كخصم على طلبك القادم من صفحة نقاطي."),
    ]),
]


def build():
    groups = "".join(f"""
            <div class="flex flex-col gap-3">
              <h2 class="font-bold text-[#003616] text-xl xl:text-2xl">{heading}</h2>
              <div class="bg-white shadow-custom4 px-6 rounded-[20px]">
                {accordion([(q, f'<p class="leading-8">{a}</p>') for q, a in qs], multi=True)}
              </div>
            </div>""" for heading, qs in GROUPS)

    body = f"""{page_header("الأسئلة الشائعة", [("الرئيسية", "index.html"), ("الأسئلة الشائعة", None)])}

      <section class="py-8 xl:py-10">
        <div class="flex flex-col gap-10 mx-auto px-4 xl:px-[190px] max-w-[1000px]">{groups}
          <div class="flex flex-col items-center gap-3 bg-interaction-base p-8 rounded-[20px] text-center">
            <h2 class="font-bold text-[#003616] text-xl">لسه عندك سؤال؟</h2>
            <p class="text-neutral-secondary text-sm">فريق خدمة العملاء جاهز يساعدك</p>
            <a href="contact-us.html" class="bg-cta hover:bg-cta-hover mt-2 px-8 py-3 rounded-full w-full sm:w-auto font-semibold text-white text-sm text-center transition-colors">تواصل معنا</a>
          </div>
        </div>
      </section>"""

    return page("الأسئلة الشائعة | جاد",
                "إجابات على أكثر الأسئلة شيوعاً عن الطلب والتوصيل والدفع والاسترجاع.",
                body, "faqs", "/faqs")
