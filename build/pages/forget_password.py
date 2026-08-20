"""Forgot password."""
from _auth import auth_page
from components import field

SLUG = "forget-password.html"


def build():
    form = f"""
              <p class="text-muted text-sm text-center leading-7">
                أدخل البريد الالكتروني المسجل وهنبعتلك رابط لإعادة تعيين كلمة المرور.
              </p>
{field("البريد الالكتروني", "email", "email", required=True)}
              <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">أرسال</button>
              <a href="login.html" class="font-semibold text-cta text-sm text-center underline">العودة لتسجيل الدخول</a>"""
    return auth_page("نسيت كلمة المرور | جاد",
                     "استعد كلمة المرور الخاصة بحسابك في جاد.",
                     "نسيت كلمة المرور", form, "forget-password",
                     "/forget-password", "نسيت كلمة المرور",
                     side=False, social=False)
