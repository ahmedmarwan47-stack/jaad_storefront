"""Create account — passwordless (mobile + OTP). Figma 'Create Account' (206:9768).

Ahmed, 2026-08-04: registration collects the name, mobile and email — no
password. Submitting hands off to the shared OTP page (verify.html) to verify
the MOBILE; once verified the account is created and signed in. The email is
NOT verified here — that is deferred to a prompt on the dashboard, since it is
not required to start ordering.
"""
from _auth import auth_page
from components import field, phone_field

SLUG = "register.html"


def build():
    form = f"""
              <div class="gap-4 grid sm:grid-cols-2">
{field("الاسم الأول", "first-name", required=True)}
{field("الاسم الاخير", "last-name", required=True)}
              </div>
{phone_field("رقم الموبايل", "phone")}
{field("البريد الالكتروني", "email", "email", required=True)}
              <label class="flex items-start gap-2 cursor-pointer">
                <input type="checkbox" required class="mt-1 accent-[#00451C] w-4 h-4" />
                <span class="text-neutral-secondary text-sm leading-6">
                  أوافق على <a href="terms-conditions.html" class="font-semibold text-cta underline">الشروط والأحكام</a>
                </span>
              </label>
              <button type="submit" class="bg-cta hover:bg-cta-hover py-4 rounded-full font-semibold text-white text-base transition-colors">إنشاء حساب</button>
              <p class="text-neutral-secondary text-sm text-center">
                لديك حساب بالفعل؟ <a href="login.html" class="font-semibold text-cta underline">تسجيل الدخول</a>
              </p>"""
    return auth_page("إنشاء حساب | جاد",
                     "أنشئ حساب في جاد برقم موبايلك واكسب نقاط في محفظتك مع كل طلب.",
                     "إنشاء حساب جديد", form, "register", "/register",
                     "إنشاء حساب", side=False, form_attrs="data-register-form")
