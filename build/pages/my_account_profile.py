"""Profile — Figma 'Account > Profile' (312:14548).

Rebuilt to the tighter, richer form Ahmed referenced (2026-08-04 screenshot): a
narrow, centred card with an avatar, first/last name, a read-only email, phone,
date of birth and gender, and a full-width save. The account content column is
wide, so the form is CAPPED and centred rather than stretched into 600px-wide
inputs (the "very wide inputs" complaint). The password card is gone — auth is
passwordless now (mobile + OTP), so there is no password to change.
"""
from _account import CUSTOMER, account_page, account_title, card
from components import field

SLUG = "my-account-profile.html"

_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
           "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]


def _sel(options, selected=""):
    """A bare select (no own label) for the date-of-birth row."""
    opts = "".join(
        f'<option{" selected" if str(o) == str(selected) else ""}>{o}</option>'
        for o in options
    )
    return ('<select class="select-control bg-white px-3 py-3 border-2 border-divider '
            'focus:border-cta rounded-xl outline-none w-full text-ink text-base '
            f'transition-colors">{opts}</select>')


def _gender_card(val, label, checked):
    # peer + .radio-dot is the project's established radio pattern (styles.css):
    # the input sits immediately before the card span, so `peer-checked` lights
    # the border and `input:checked + span .radio-dot` fills the dot.
    return f"""
                  <label class="cursor-pointer">
                    <input type="radio" name="gender" value="{val}"{' checked' if checked else ''} class="peer sr-only" />
                    <span class="flex items-center gap-2.5 bg-white px-4 py-3 border-2 border-divider peer-checked:border-cta rounded-xl transition-colors">
                      <span class="radio-dot shrink-0"></span>
                      <span class="font-medium text-ink text-sm">{label}</span>
                    </span>
                  </label>"""


def build():
    # Demo DOB — placeholder like the rest of CUSTOMER (no profile endpoint).
    dob_day, dob_month, dob_year = 12, "أبريل", 1996

    form = f"""
              <form class="flex flex-col gap-5">
                <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", value="محمد", required=True, i18n_value=True)}
{field("الاسم الاخير", "last-name", value="عادل", required=True, i18n_value=True)}
                </div>

                <!-- Email is not EDITED here (a span, not an input — read-only
                     text truncates cleanly rather than scrolling inside a
                     fixed-width field), but it is now VERIFIED here. -->
                <!-- The unverified state is ACTIONABLE now (Ahmed, 2026-08-23).
                     It used to be a red "غير مؤكد" chip and nothing else: the row
                     told you something was wrong and gave you no way to put it
                     right — the only control was a banner on a different page.
                     The chip now sits beside a "تأكيد" button, and pressing it
                     flips the row to the verified state in place (initAuthUI).
                     data-verify-email is the SAME hook the dashboard banner uses,
                     so both routes go through Auth.verifyEmail() and cannot
                     disagree about the state. -->
                <div class="flex flex-col gap-1.5">
                  <span class="font-medium text-muted text-sm">البريد الالكتروني</span>
                  <div data-email-row class="flex items-center gap-2 bg-cream px-4 py-3 border-2 border-transparent rounded-xl">
                    <span class="flex-1 min-w-0 truncate text-muted text-base latin">{CUSTOMER['email']}</span>
                    <!-- Opaque tint, NOT bg-error/10: an alpha tint reads
                         ~1:1 to the contrast sweep (ink on its own colour); the
                         opaque blend (#F6E9E7 ≈ error at 10% over white) is
                         legible to both the eye and the checker — the same trap
                         the checkout stepper's #E9F3E6 documents. -->
                    <span data-email-state="unverified" class="inline-flex items-center shrink-0 bg-blush px-2 py-0.5 rounded-full font-semibold text-error text-[11px]">غير مؤكد</span>
                    <button type="button" data-verify-email data-email-state="unverified"
                            class="shrink-0 bg-cta hover:bg-cta-hover px-3 py-1 rounded-full font-semibold text-white text-[11px] whitespace-nowrap transition-colors">تحقق</button>
                    <span data-email-state="verified" hidden class="inline-flex items-center gap-1 shrink-0 bg-mint px-2 py-0.5 rounded-full font-semibold text-heading text-[11px]">✓ مؤكد</span>
                  </div>
                </div>

{field("رقم الهاتف", "phone", "tel", value=CUSTOMER['phone'], required=True)}

                <div class="flex flex-col gap-1.5">
                  <span class="font-medium text-muted text-sm">تاريخ الميلاد</span>
                  <div class="gap-3 grid grid-cols-3">
                    {_sel(range(1, 32), dob_day)}
                    {_sel(_MONTHS, dob_month)}
                    {_sel(range(2010, 1949, -1), dob_year)}
                  </div>
                </div>

                <div class="flex flex-col gap-1.5">
                  <span class="font-medium text-muted text-sm">النوع</span>
                  <div class="gap-3 grid grid-cols-2">
{_gender_card("female", "أنثى", True)}
{_gender_card("male", "ذكر", False)}
                  </div>
                </div>

                <button type="submit" class="bg-cta hover:bg-cta-hover mt-1 py-3.5 rounded-full w-full font-semibold text-white text-sm transition-colors">حفظ التعديلات</button>
              </form>"""

    content = f"""
            {account_title(SLUG, "بيانات الحساب")}
            <!-- Capped and hugged to the inline START (right in RTL) with
                 me-auto, so the form sits directly under the title rather than
                 floating in the centre of the column (Ahmed, 2026-08-04). The
                 cap keeps the inputs a comfortable width. -->
            <div class="me-auto w-full max-w-[600px]">
              {card("المعلومات الشخصية", form)}
            </div>"""

    return account_page("بيانات الحساب | جاد", "عدّل بياناتك الشخصية.",
                        content, "my-account-profile", "/my-account/profile",
                        "بيانات الحساب", "my-account-profile.html")
