"""Reset password."""
from _auth import auth_page, password_field

SLUG = "reset-password.html"


def build():
    form = f"""
              <p class="text-neutral-secondary text-sm text-center leading-7">
                اختر كلمة مرور جديدة لحسابك.
              </p>
{password_field("كلمة السر الجديدة", "password")}
{password_field("تأكيد كلمة السر", "password-confirm")}
              <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">حفظ كلمة المرور</button>"""
    return auth_page("إعادة تعيين كلمة المرور | جاد",
                     "اختر كلمة مرور جديدة لحسابك في جاد.",
                     "إعادة تعيين كلمة المرور", form, "reset-password",
                     "/reset-password", "إعادة تعيين كلمة المرور",
                     side=False, social=False)
