"""Sign in — passwordless (mobile + OTP). Figma 'Account Sign In' (205:10427).

Ahmed, 2026-08-04: sign-in is now a mobile number only. Submitting it hands off
to the shared OTP page (verify.html), which is the real gate; there is no
password. The demo OTP is printed on the verify page, the way the old demo
credentials used to be printed here.
"""
from _auth import SOCIAL, auth_page
from components import phone_field

SLUG = "login.html"


def build():
    # Distributed layout (Ahmed, 2026-08-04): the mobile field sits in a flex-1
    # region CENTRED between the title and the CTA, the CTA sits between two equal
    # flex-1 regions so it lands on the same line as the create-account button,
    # and the "new account" link + social buttons fill the flex-1 region below.
    # form_contents=True makes the <form> a display:contents box so these three
    # blocks become direct flex children of the card.
    form = f"""
              <div class="flex flex-1 flex-col justify-center">
{phone_field("رقم الموبايل", "mobile", help_text="هنبعتلك كود تأكيد من 6 أرقام على رقمك — من غير كلمة مرور.")}
              </div>
              <button type="submit" class="btn-elevate bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base">متابعة</button>
              <div class="flex flex-1 flex-col justify-center gap-5">
                <p class="text-muted text-sm text-center">
                  لسه معندكش حساب؟ <a href="register.html" class="font-semibold text-cta underline">أنشئ حساب جديد</a>
                </p>
                {SOCIAL}
              </div>"""
    return auth_page("تسجيل الدخول | جاد",
                     "سجّل الدخول برقم موبايلك في جاد — رمز تحقق سريع بدون كلمة مرور.",
                     "تسجيل الدخول", form, "login", "/login", "تسجيل الدخول",
                     form_attrs="data-login-form", social=False, form_contents=True)
