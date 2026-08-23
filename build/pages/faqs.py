"""FAQs — Figma 'FAQs' (399:27159).

Restructured (Ahmed, 2026-08-20). It used to be three headed CATEGORY sections
("الطلب والتوصيل", "الدفع", "المنتجات والاسترجاع"), each a 40px heading over its
own white card. That read as three separate mini-pages and buried the questions
under chrome, and on a phone the card wrapper added a border-and-shadow box
around what is already a list of bordered rows.

Now: one title + subtitle, a SEGMENTED filter directly beneath them, and a flat
list of questions — no per-category headings, no card around the list. The
categories survive only as filter values, which is the job they were actually
doing. "All" leads so the page still shows everything by default.

The segmented control is the same `.pp-tabs` + initTabs contract the homepage's
Perfect Picks uses (sliding pill, no reflow), so there is one segmented control
in the codebase rather than a second one that merely looks similar.
"""
from components import accordion, page, page_header

SLUG = "faqs.html"

# (filter key, filter label, [(question, answer)])
GROUPS = [
    ("delivery", "الطلب والتوصيل", [
        ("إزاي أطلب من الموقع؟",
         "اختار المنتجات اللي تحبها وضيفها للسلة، بعدين اضغط على «أطلب الآن» واملأ بيانات "
         "التوصيل. هتوصلك رسالة تأكيد على البريد الالكتروني ورقم الهاتف."),
        ("الطلب بيوصل في قد إيه؟",
         "داخل القاهرة الكبرى التوصيل خلال ساعتين. باقي المحافظات من يوم لثلاثة أيام عمل "
         "حسب المنطقة."),
        # The 150 EGP minimum was removed from the store on 2026-08-23, so this
        # answer had to go with it — the site cannot keep quoting a rule it no
        # longer applies. Re-pointed at the question the row was really being
        # asked: what delivery costs. ⚠️ Ahmed: this is a CLIENT-FACING policy
        # statement — confirm the wording with them.
        ("في حد أدنى للطلب؟",
         "لا، مفيش حد أدنى للطلب. مصاريف التوصيل بتتحسب حسب المنطقة وبتظهر قبل تأكيد الطلب، "
         "والتوصيل بيبقى مجاني فوق مبلغ معيّن بيظهرلك في السلة."),
        ("بتوصلوا لكل المحافظات؟",
         "أيوه، بنوصل لكل محافظات مصر. مصاريف التوصيل ومدته بتختلف حسب المنطقة وبتظهر قبل تأكيد الطلب."),
    ]),
    ("payment", "الدفع", [
        ("طرق الدفع المتاحة إيه؟",
         "بنقبل الدفع عند الاستلام، بطاقات الائتمان (فيزا وماستركارد)، اتصالات كاش، "
         "وفاليو، بالإضافة لرصيد المحفظة."),
        ("الدفع أونلاين آمن؟",
         "أيوه، كل عمليات الدفع بتتم من خلال بوابة دفع مؤمنة، وإحنا مابنحتفظش ببيانات بطاقتك."),
    ]),
    ("products", "المنتجات والاسترجاع", [
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
    # "All" first, then one segment per category. Same tab-btn/tab-panel
    # contract initTabs already drives — no FAQ-specific JS.
    tabs = [("all", "الكل")] + [(k, label) for k, label, _qs in GROUPS]
    chips = "".join(
        f'<button type="button" class="tab-btn{" is-active" if i == 0 else ""}" '
        f'data-tab="{k}">{label}</button>'
        for i, (k, label) in enumerate(tabs)
    )

    def rows(qs):
        # accordion() renders the bordered rows themselves; nothing wraps them,
        # so the questions sit directly on the page (Ahmed, 2026-08-20).
        return accordion([(q, f'<p class="leading-8">{a}</p>') for q, a in qs], multi=True)

    all_qs = [qa for _k, _l, qs in GROUPS for qa in qs]
    panels = "".join(
        f'<div class="tab-panel" data-panel="{k}"{"" if i == 0 else " hidden"}>{rows(qs)}</div>'
        for i, (k, qs) in enumerate(
            [("all", all_qs)] + [(k, qs) for k, _l, qs in GROUPS])
    )

    # No page_header: the breadcrumb band it used to emit sat on its own
    # background between the masthead and this section and read as a seam
    # (Ahmed, 2026-08-20). The title below is this page's h1.
    body = f"""
      <section class="py-10 xl:py-14">
        <div class="flex flex-col gap-8 mx-auto px-4 xl:px-[60px] max-w-[860px]">
          <div class="flex flex-col items-center gap-3 text-center">
            <h1 class="font-medium text-heading text-[32px] md:text-[40px] leading-[1.2]">الأسئلة الشائعة</h1>
            <p class="max-w-[520px] text-bodyMuted text-base leading-[1.6]">
              كل اللي محتاج تعرفه عن الطلب والتوصيل والدفع والاسترجاع.
            </p>
          </div>

          <!-- Segmented filter, directly under the title/subtitle. -->
          <div data-tabs class="flex flex-col gap-6">
            <!-- The scroll lives on this WRAPPER, never on .pp-tabs itself
                 (Ahmed, 2026-08-20). Putting `overflow-x-auto max-w-full` on
                 the .pp-tabs element made initTabs measure the active chip at
                 zero width, so the sliding white pill collapsed and never
                 painted — the control looked like plain text on a green track
                 while the homepage's identical control showed its pill. Keeping
                 .pp-tabs byte-identical to the homepage's keeps the pill
                 geometry (and its 14px corner radius) identical too. -->
            <div class="flex justify-center max-w-full overflow-x-auto no-scrollbar">
              <div class="pp-tabs relative inline-flex items-center gap-1 bg-greenTintSoft p-1 rounded-full">
                <span data-tab-indicator aria-hidden="true"></span>{chips}
              </div>
            </div>
{panels}
          </div>

          <div class="flex flex-col items-center gap-3 bg-cream p-8 rounded-[20px] text-center">
            <h2 class="font-bold text-heading text-xl">لسه عندك سؤال؟</h2>
            <p class="text-muted text-sm">فريق خدمة العملاء جاهز يساعدك</p>
            <a href="contact-us.html" class="bg-cta hover:bg-cta-hover mt-2 px-8 py-3 rounded-full w-full sm:w-auto font-semibold text-white text-sm text-center transition-colors">تواصل معنا</a>
          </div>
        </div>
      </section>"""

    return page("الأسئلة الشائعة | جاد",
                "إجابات على أكثر الأسئلة شيوعاً عن الطلب والتوصيل والدفع والاسترجاع.",
                body, "faqs", "/faqs")
