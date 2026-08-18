"""OTP verification — the shared step after passwordless login and register
(Ahmed, 2026-08-04).

scripts.js (initAuthUI) reads the pending flow the login/register page stashed,
shows the mobile it was "sent" to, verifies the 6-digit code and — on success —
flips the button to a "verified" state before signing the user in and returning
them to `next` (e.g. checkout) or the dashboard. Arriving here with no pending
flow bounces to /login.
"""
from _auth import auth_page

SLUG = "verify.html"


def _otp_boxes(n=6):
    # Single-digit boxes that FILL the row (flex-1); scripts.js wires
    # auto-advance + backspace and combines them into the code. The empty
    # (placeholder-shown) state reads as inactive via `.otp-box` (styles.css);
    # focus/filled turns it active. autocomplete=one-time-code lets the OS offer
    # the SMS code on a real device.
    return "".join(
        '<input type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="1" '
        'placeholder=" " data-otp-box aria-label="خانة رقم ' + str(i + 1) + '" '
        'class="otp-box flex-1 min-w-0 h-14 rounded-xl text-center font-bold '
        'text-[#003616] text-2xl latin" />'
        for i in range(n)
    )


def build():
    form = f"""
              <p class="text-neutral-secondary text-sm text-center leading-6">
                أدخل رمز التحقق المكوّن من 6 أرقام المُرسل إلى
                <span class="font-semibold text-[#003616] latin" data-otp-mobile>—</span>
              </p>
              <div class="flex gap-2 sm:gap-3" dir="ltr">
{_otp_boxes()}
              </div>
              <p data-otp-msg hidden class="font-semibold text-accent-error text-sm text-center"></p>
              <button type="submit" data-otp-submit class="btn-elevate bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">تأكيد وتسجيل الدخول</button>
              <button type="button" data-resend-otp class="link-sweep self-center font-semibold text-cta text-sm">إعادة إرسال الرمز</button>"""
    # The 3D OTP icon sits bare above the heading (Ahmed, 2026-08-04) — no
    # tinted disc behind it.
    hero = '<img src="images/jaad/icons/otp-3d.png" alt="" class="w-20 h-20 object-contain" />'
    return auth_page("رمز التحقق | جاد",
                     "أدخل رمز التحقق المرسل إلى رقم موبايلك لإتمام تسجيل الدخول في جاد.",
                     "التحقق من رقم الموبايل", form, "verify", "/verify",
                     "التحقق", side=False, social=False, form_attrs="data-otp-form",
                     hero=hero)
