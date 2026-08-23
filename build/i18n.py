"""English dictionary for the language switch — generated into i18n-en.js.

WHY THIS FILE EXISTS
--------------------
`scripts.js` used to carry the whole dictionary as one inline literal, and it
covered the chrome only: 1,457 of the 1,524 distinct Arabic strings on the
built site had no entry, so switching to English left roughly 70% of every
page in Arabic. Ahmed asked for the switch to reach everything
(2026-07-22).

Three of those surfaces could not be fixed by adding keys to that literal at
all, and are handled by the engine in `translateDocument()` instead — see the
comment there. What is left is the dictionary itself, and it belongs here
rather than in `scripts.js` for two reasons:

  * It is the only place that can read `catalog.json`, so all 99 product names
    resolve to the client's OWN English `name` field. Retyping them into a JS
    literal would be inventing data that we already have (CLAUDE.md, "real
    data over invented data").
  * Whole families of strings are formulaic — gallery labels, governorate
    rows — and are better looped than listed. `GALLERY` alone would be 40
    hand-written entries.

STATUS OF THE ENGLISH IN HERE
-----------------------------
Split deliberately into two dicts, because they do not carry the same
authority and must not be signed off as if they did:

  UI    — our own interface copy. Standard commerce terminology, written
          in-house. Placeholder pending client sign-off, same as the chrome
          strings always were.
  COPY  — the CLIENT'S OWN marketing and product prose, translated in-house.
          There is no English source for any of it: the Store API returns
          English names but never English descriptions. This is the one place
          in the project where we write English for text the client wrote in
          Arabic, and it is flagged in DESIGN-NOTES §1 as needing their
          approval before launch. Nothing here is machine-translated and
          nothing invents a claim the Arabic does not make, but it is still
          our words for their product.

Branch street addresses are deliberately NOT translated (310 of them). A
postal address is not copy — transliterating "برج نفرتيتى - تقاطع جمال عبد
الناصر" would produce something a courier cannot use. Governorate NAMES are
translated because they are also section headings.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(os.path.dirname(HERE), "static-export")

# --------------------------------------------------------------------------
# UI — our own interface copy
# --------------------------------------------------------------------------
UI = {
    # --- global chrome / actions
    "اضف الى السلة": "Add to cart",
    "عرض المزيد": "Show more",
    "شاهد الوصفة": "View recipe",
    "الوصفات": "Recipes",
    "الرئيسية": "Home",
    "تخطي إلى المحتوى": "Skip to content",
    "الإجمالي": "Total",
    "اشتري الان": "Buy now",
    "تغيير المنطقة": "Change area",
    "القائمة": "Menu",
    "تأكيد": "Confirm",
    "حذف": "Remove",
    "تعديل": "Edit",
    "عرض": "View",
    "اختر": "Select",
    "نسخ": "Copy",
    "أرسال": "Send",
    "اعرف المزيد": "Learn more",
    "اعرف أكثر": "Learn more",
    "المنتجات": "Products",
    "الفروع": "Branches",
    "المكافآت": "Rewards",
    "قصتنا": "Our Story",
    "البلوج": "Blog",
    "تواصل معنا": "Contact us",
    "أتصل بنا": "Contact Us",
    "اتصل بنا": "Contact Us",
    "ميديا": "Media",
    "100% Natural Based Products": "100% Natural Based Products",
    "الأسئلة الشائعة": "Frequently asked questions",
    "الأسئلة المتداولة": "FAQs",
    "تحتاج مساعدة؟": "Need help?",
    "الشروط والأحكام": "Terms & Conditions",
    "سياسة الخصوصية": "Privacy Policy",
    "سياسة الاسترجاع": "Return Policy",
    "سياسة التوصيل والاسترجاع": "Delivery & Returns",
    "تسوق منتجاتنا": "Shop our products",
    "تسوق اكتر": "Shop more",
    "تسوق اكتر من جاد": "More from Jaad",
    "كل المنتجات": "All products",
    "تصفح المنتجات": "Browse products",
    "قائمة المنتجات": "Product list",
    "المنتجات المحفوظة": "Saved products",
    "المفضلة": "Favourites",

    # --- product page
    "عادة ما يتم شراؤه معاً: أضف هذه العناصر": "Frequently bought together: add these items",
    "أضف الجميع الى السلة": "Add all to cart",
    "وصفات بالمنتج": "Recipes with this product",
    "منتجات مشابهة": "Similar products",
    "اختر الحجم": "Choose a size",
    "الفوائد": "Benefits",
    "الفوائد:": "Benefits:",
    "الوصف:": "Description:",
    "المحتويات": "Contents",
    "طريقة الحفظ": "How to store",
    "الوزن الصافي:": "Net weight:",
    "معلومات إضافية:": "Additional information:",
    "معلومات إضافية عن المنتج:": "More about this product:",
    "مقاس البوكس:": "Box size:",
    "نسبة الخصم:": "Discount:",
    "تفاصيل العرض:": "Offer details:",
    "طرق الاستمتاع:": "Ways to enjoy:",
    "طرق الأستمتاع:": "Ways to enjoy:",
    "كيفية الاستمتاع:": "How to enjoy:",
    "كيفية الاستخدام:": "How to use:",
    "طريقة التحضير:": "How to prepare:",
    "الرائحة والطعم:": "Aroma and taste:",
    "نوع القهوة:": "Coffee type:",
    "النكهة": "Flavour",
    "نصائح": "Tips",
    "مخبوزة": "Baked",
    "نوع مقرمشات بافس:": "Puffs type:",
    "نكهة المقرمشات:": "Puffs flavour:",
    "حجم المقرمشات:": "Puffs size:",
    "حجم المنتج:": "Product size:",
    "النكهة: رائحة البيتزا الغنية مع القرمشة في كل قضمة":
        "Flavour: rich pizza aroma with a crunch in every bite",
    "النكهة: جبنة": "Flavour: cheese",

    # --- weights (units, kept as their own strings)
    "35 جم": "35 g",
    "40 جرام": "40 g",
    "50 جم": "50 g",
    "75 جم": "75 g",
    "90 جم": "90 g",
    "100 جم": "100 g",
    "100 جرام": "100 g",
    "200 جم": "200 g",
    "225 جم": "225 g",
    "250 جم": "250 g",

    # --- best-seller headings
    "الأكثر مبيعاً": "Best selling",
    "وصل حديثاً": "New arrivals",

    # --- promises strip
    "توصيل خلال ساعتين": "Delivery within two hours",
    "في القاهرة الكبرى": "across Greater Cairo",
    "استرجاع خلال 14 يوم": "Returns within 14 days",
    "من تاريخ الاستلام": "from the delivery date",

    # --- categories — Jaad's real 3, no Abu Auf's dates/snacks/gifting/etc.
    "القهوة": "Coffee",
    "المكسرات": "Nuts",
    "البهارات": "Spices",
    "قهوة": "Coffee",
    "تغذية": "Nutrition",

    # --- account
    "حسابي": "My account",
    "الحساب": "Account",
    "طلباتي": "My orders",
    "محفظتي": "My wallet",
    "نقاطي": "My points",
    "بيانات الحساب": "Account details",
    "عناويني": "My addresses",
    "بياناتي": "My details",
    "عضوية ذهبية": "Gold membership",
    "مرحبا محمد": "Welcome, Mohamed",
    "تسجيل الدخول": "Sign in",
    "تسجيل الخروج": "Sign out",
    "إنشاء حساب": "Create account",
    "إنشاء حساب جديد": "Create a new account",
    "كلمة السر": "Password",
    "كلمة المرور": "Password",
    "كلمة السر الجديدة": "New password",
    "تأكيد كلمة السر": "Confirm password",
    "نسيت كلمة المرور": "Forgot password",
    "نسيت كلمة المرور الخاصة بي": "I forgot my password",
    "إعادة تعيين كلمة المرور": "Reset password",
    "تغيير كلمة المرور": "Change password",
    "حفظ كلمة المرور": "Save password",
    "العودة لتسجيل الدخول": "Back to sign in",
    "سجل بأستخدام جوجل": "Sign in with Google",
    "سجل بأستخدام فيسبوك": "Sign in with Facebook",
    "المعلومات الشخصية": "Personal information",
    "حفظ التعديلات": "Save changes",
    "اختر كلمة مرور جديدة لحسابك.": "Choose a new password for your account.",
    "أدخل البريد الالكتروني المسجل وهنبعتلك رابط لإعادة تعيين كلمة المرور.":
        "Enter your registered email and we will send you a link to reset your password.",
    "لتغيير كلمة المرور، أدخل كلمة المرور الحالية ثم الجديدة.":
        "To change your password, enter your current password and then the new one.",
    "عند إنشاء حساب، هتكسب نقاط خصم في محفظتك ويمكنك الدفع بشكل أسرع والاحتفاظ بأكثر من عنوان وتتبع الطلبات والمزيد.":
        "Create an account to earn points in your wallet, check out faster, save more than one address, track your orders and more.",
    "حساب تجريبي للاختبار": "Demo account for testing",
    "استخدم البيانات دي لتجربة تسجيل الدخول والمفضلة:":
        "Use these details to try signing in and favourites:",
    "املأ البيانات تلقائياً": "Fill automatically",
    "نظرة عامة": "Overview",
    # Email verification on the profile row. "تحقق" rather than the shared
    # "تأكيد" (Confirm) key: this is a distinct action — prove the address is
    # yours — and it needs to read "Verify" in English without dragging every
    # other confirm button on the site with it.
    "تحقق": "Verify",
    "✓ مؤكد": "✓ Verified",
    "يمكنك إدارة الطلبات والمحفظة ومعلومات الحساب الخاصة بك هنا.":
        "Manage your orders, wallet and account details here.",
    "شكرا لتسجيلك حساب معنا !": "Thank you for creating an account with us!",
    "شارك الموقع مع الأصحاب والعائلة": "Share the site with friends and family",
    "أنسخ الرابط أدناه وشاركه مع عائلتك وأصدقائك واحصل على خصومات حصرية":
        "Copy the link below, share it with family and friends, and get exclusive discounts",
    "لا توجد منتجات في المفضلة": "No saved products yet",
    "المنتجات اللي تحفظها هتظهر هنا.": "Products you save will appear here.",

    # --- orders
    "طلباتي الحالية": "My current orders",
    "كل الطلبات": "All orders",
    "تفاصيل الطلب": "Order details",
    "حالة الطلب": "Order status",
    "متابعة التسوق": "Continue shopping",
    "رقم الطلب": "Order number",
    "التاريخ": "Date",
    "المجموع": "Subtotal",
    "تم الطلب": "Order placed",
    "تحت التحضير": "In preparation",
    "جاري التحضير": "Being prepared",
    "جاري تجهيز الطلب": "Order being prepared",
    "في الطريق إليك": "On its way to you",
    "تم التسليم": "Delivered",
    "مكتمل": "Completed",
    "ملغي": "Cancelled",
    "الميعاد المتوقع للتوصيل": "Estimated delivery",
    "بيانات التوصيل": "Delivery details",
    "عنوان التوصيل": "Delivery address",

    # --- wallet / points
    "رصيد محفظتي": "My wallet balance",
    "رصيد النقاط": "Points balance",
    "استبدال النقاط": "Redeem points",
    "إزاي تكسب نقاط؟": "How do you earn points?",
    "اكسب نقطة على كل جنيه تشتريه من الموقع":
        "Earn a point for every pound you spend on the site",
    "نقاط إضافية عند تقييم المنتجات اللي اشتريتها":
        "Extra points for reviewing products you have bought",
    "مكافأة ترحيبية عند إنشاء حساب جديد": "A welcome bonus when you create an account",
    "سجل المعاملات": "Transaction history",
    "استرداد من طلب #30941": "Refund from order #30941",
    "خصم على طلب #30942": "Discount on order #30942",
    "مكافأة تسجيل": "Sign-up bonus",
    "خصم المحفظة": "Wallet discount",
    "خصم كود الخصم": "Promo code discount",
    "خصم المبلغ": "Apply discount",
    "إلغاء الخصم": "Remove discount",
    "الدفع من المحفظة": "Pay from wallet",
    "هل لديك برومو كود؟": "Have a promo code?",
    "اكتب الكود": "Enter code",
    "تطبيق": "Apply",
    "تم تطبيق الكود": "Code applied",
    "كود غير صالح": "Invalid code",
    "اختر الفرع": "Choose a branch",
    "تأكيد الفرع": "Confirm branch",
    "المحافظة": "Governorate",
    "لا توجد فروع في هذه المحافظة": "No branches in this governorate",
    "حدد اليوم والوقت": "Pick a day & time",
    "تأكيد الموعد": "Confirm time",
    "اليوم": "Today",
    "تم الخصم من رصيدك": "Deducted from your balance",
    "اجمع نقاط مع كل عملية شراء من جاد":
        "Collect points with every purchase from Jaad",
    "اجمع نقاطك مع كل طلب من جاد، وتابع رصيدك ومستوى عضويتك من صفحة النقاط في حسابك.":
        "Collect points with every Jaad order, and track your balance and membership tier from the points page in your account.",

    # --- cart / checkout
    "سلة التسوق": "Shopping cart",
    "ملخص السلة": "Cart summary",
    "مصاريف التوصيل": "Delivery fee",
    "هل لديك برومو كود؟": "Have a promo code?",
    "أضف ملاحظات على الطلب": "Add order notes",
    "أطلب الآن": "Order now",
    "أكمل إلى الدفع": "Continue to payment",
    "إتمام عملية الشراء بأمان": "Secure checkout",
    "تأكيد عملية الشراء": "Confirm purchase",
    "طريقة الدفع": "Payment method",
    "بيانات العميل": "Customer details",
    "نوع الطلب": "Order type",
    "طلب عادي": "Standard order",
    "إهداء الطلب": "Send as a gift",
    "أرسل الطلب كهدية لشخص تحبه": "Send this order as a gift to someone you love",
    "وقت التوصيل": "Delivery time",
    "في غضون 60 دقيقة": "Within 60 minutes",
    "أختار تاريخ": "Choose a date",
    "حدد اليوم والوقت المناسب": "Pick the day and time that suits you",
    "طريقة التوصيل": "Delivery method",
    "توصيل": "Delivery",
    "بإضافة مصاريف اضافية": "An extra fee applies",
    "الاستلام من المتجر": "Pick up in store",
    "الاستلام من الفرع": "Pick up from a branch",
    "مواعيد التوصيل": "Delivery times",
    "خطوات الشراء": "Checkout steps",
    "بيانات شخصية": "Personal info",
    # Card form on the payment step. PROTOTYPE fields — see the module
    # docstring in build/pages/payment.py before this goes anywhere live.
    "رقم البطاقة": "Card number",
    "الاسم على البطاقة": "Name on card",
    "تاريخ الانتهاء": "Expiry date",
    "رمز التحقق CVV": "CVV",

    # --- runtime strings scripts.js writes into the page
    # These are toasts, countdown labels and inline validation that JS SETS
    # after the translation pass has run, so they are never reached by the
    # text-node walker and can only be translated through t(). Every one of
    # them was missing (Ahmed, 2026-08-23) — which is why the English OTP
    # screen showed an Arabic "إعادة الإرسال خلال 30 ثانية" the moment it
    # loaded: the resend cooldown starts on arrival and writes its own label.
    "إعادة الإرسال خلال": "Resend in",
    "ثانية": "seconds",
    "تم التحقق": "Verified",
    "رمز التحقق غير صحيح، حاول مرة أخرى": "That code is not right — please try again",
    "تم إرسال رمز جديد": "A new code has been sent",
    "من فضلك أدخل رقم موبايل صحيح": "Please enter a valid mobile number",
    "تم تسجيل الدخول بنجاح": "Signed in successfully",
    "تم تسجيل الخروج": "Signed out",
    "تم تأكيد بريدك الإلكتروني بنجاح": "Your email address has been verified",
    "خانة رقم 1": "Digit 1",
    "خانة رقم 2": "Digit 2",
    "خانة رقم 3": "Digit 3",
    "خانة رقم 4": "Digit 4",
    "خانة رقم 5": "Digit 5",
    "خانة رقم 6": "Digit 6",
    "لا توجد عناوين محفوظة بعد.": "No saved addresses yet.",
    "تعديل العنوان": "Edit address",

    # --- forms
    "الاسم الأول": "First name",
    "اسم العائلة": "Last name",
    "الاسم الاخير": "Last name",
    "الاسم": "Name",
    "رقم الهاتف": "Phone number",
    "البريد الالكتروني": "Email",
    "الموضوع": "Subject",
    "الرسالة": "Message",
    "المدينة": "City",
    "الحي": "District",
    "المنطقة": "Area",
    "رقم العقار و الشارع": "Building number and street",
    "نوع العقار": "Property type",
    "رقم الشقة": "Apartment number",
    "الشقة": "Apartment",
    "شقة": "Apartment",
    "فيلا": "Villa",
    "الطابق": "Floor",
    "قبول الشروط": "Accept the terms",
    "اضف عنوان": "Add address",
    "العنوان الافتراضي": "Default address",
    "عنواني الافتراضي": "My default address",
    "اجعله العنوان الافتراضي": "Make it the default address",
    "تم تعيين العنوان الافتراضي": "Default address updated",

    # --- demo record values
    "محمد": "Mohamed",
    "عادل": "Adel",
    "محمد عادل": "Mohamed Adel",
    "شقة 3 - 220 شارع الحرية - الدور الأول": "Apt 3 - 220 El Horreya Street - First floor",
    "مبنى 12 - شارع التسعين الشمالي": "Building 12 - North Ninety Street",
    "التجمع الخامس، القاهرة": "Fifth Settlement, Cairo",
    "مصر الجديدة، القاهرة": "Heliopolis, Cairo",
    "مصر الجديدة": "Heliopolis",
    "القاهرة، مصر": "Cairo, Egypt",
    "القاهرة الجديدة": "New Cairo",
    "شارع 5 عقار رقم 4": "Street 5, building 4",
    "23 مارس 2026": "23 March 2026",
    "28 مارس 2026": "28 March 2026",
    "21 مارس 2026": "21 March 2026",
    "14 مارس 2026": "14 March 2026",

    # --- listing
    "ترتيب حسب": "Sort by",
    "السعر: من الأقل": "Price: low to high",
    "السعر: من الأعلى": "Price: high to low",
    "لا توجد منتجات في هذا القسم حالياً.": "No products in this section yet.",

    # --- home
    "20٪": "20%",
    "أراء العملاء": "Customer reviews",
    "كل التعليقات": "All reviews",
    "آخر الأخبار": "Latest news",
    "عن جاد": "About Jaad",
    "المتجر مغلق حالياً": "The store is currently closed",

    # --- store copy (ours)
    "من الطبيعة إليك": "From nature to you",
    "جودة في كل خطوة": "Quality at every step",
    "نغذي العقل والروح": "Nourishing mind and spirit",

    # --- reviews (in-house placeholder personas) — no branches/dates
    # mentions, matching the rewritten home.py REVIEWS list.
    "القهوة والمكسرات دايماً طازة وجودتها ثابتة، وبتوصل بسرعة.":
        "The coffee and nuts are always fresh and consistently good, and they arrive quickly.",
    "منى عبد الله — القاهرة": "Mona Abdallah — Cairo",
    "القهوة التركي بتاعتهم من أحلى حاجة جربتها، والتغليف بيحافظ على الريحة.":
        "Their Turkish coffee is one of the best I have tried, and the packaging holds the aroma.",
    "أحمد فؤاد — الجيزة": "Ahmed Fouad — Giza",
    "البهارات ريحتها قوية وطعمها فرق معايا في الأكل، هطلب تاني أكيد.":
        "The spices have a strong aroma and really changed my cooking — I will definitely order again.",
    "سارة محمود — الإسكندرية": "Sara Mahmoud — Alexandria",
    "تشكيلة المكسرات ممتازة والأسعار كويسة مقارنة بالجودة اللي بتاخدها.":
        "The nuts selection is excellent and the prices are good for the quality you get.",
    "كريم سمير — المنصورة": "Karim Samir — Mansoura",

    # --- blog
    "كل المقالات": "All articles",
    "أحدث المقالات": "Latest articles",
    "مقالات ذات صلة": "Related articles",
    "قراءة ٥ دقائق": "5 min read",
    "نصائح سريعة": "Quick tips",
    "فوائد المكسرات النيئة لصحة القلب": "The heart benefits of raw nuts",
    "المكسرات مصدر غني بالدهون الصحية والألياف، وإضافتها لنظامك اليومي أسهل مما تتخيل.":
        "Nuts are a rich source of healthy fats and fibre, and working them into your day is easier than you think.",
    "دليلك لاختيار درجة تحميص القهوة": "Your guide to choosing a coffee roast",
    "من التحميص الفاتح للغامق، كل درجة ليها طابع مختلف. تعرف على الفرق واختار اللي يناسب ذوقك.":
        "From light to dark, every roast has its own character. Learn the difference and pick the one that suits your taste.",
    "تشكيلة سناكس تجمع بين الطعم اللذيذ والقيمة الغذائية، سهلة التحضير وبتفضل طازة.":
        "A range of snacks that combine good taste with real nutrition — easy to prepare and they stay fresh.",
    "دليل البهارات: إزاي تختار وتحفظ": "A spice guide: how to choose and store",
    "البهارات الطازة بتفرق في أي طبق. اعرف إزاي تختارها وتحفظها عشان تحافظ على نكهتها.":
        "Fresh spices change any dish. Learn how to choose and store them so they keep their flavour.",
    "جرانولا بيتي بالمكسرات والعسل": "Homemade granola with nuts and honey",
    "وصفة بسيطة تعملها في البيت وتفضل معاك أسبوع كامل، مثالية للفطار السريع.":
        "A simple recipe you can make at home that keeps for a week — ideal for a quick breakfast.",
    "المكسرات من أقدم الأطعمة اللي عرفها الإنسان، ولحد النهارده فضلت واحدة من أغنى المصادر الطبيعية للدهون الصحية والبروتين والألياف. الدراسات بتشير إن تناول حفنة صغيرة يومياً بيرتبط بتحسن في صحة القلب ومستويات الكوليسترول.":
        "Nuts are among the oldest foods people have eaten, and they remain one of the richest natural sources of healthy fats, protein and fibre. Studies link a small handful a day with better heart health and cholesterol levels.",
    "الفرق بين المكسرات النيئة والمحمصة مش بس في الطعم. التحميص على درجات حرارة عالية ممكن يقلل نسبة بعض الفيتامينات الحساسة للحرارة، وعشان كده بنحمص على دفعات صغيرة وبدرجات محسوبة تحافظ على القيمة الغذائية والنكهة في نفس الوقت.":
        "The difference between raw and roasted nuts is not only taste. Roasting at high temperatures can reduce some heat-sensitive vitamins, which is why we roast in small batches at measured temperatures that protect the nutrition and the flavour at once.",
    "أحسن طريقة تدخل بيها المكسرات في يومك إنك تخليها في متناول إيدك — علبة صغيرة على المكتب أو في شنطة الشغل. جربها كمان فوق الزبادي أو السلطة، أو اطحنها وحطها في العجين للمخبوزات.":
        "The best way to work nuts into your day is to keep them within reach — a small tub on your desk or in your work bag. Try them over yoghurt or salad too, or grind them into dough for baking.",
    "ابدأ بكمية صغيرة — حفنة يومياً كفاية": "Start small — a handful a day is enough",
    "نوّع بين اللوز والكاجو وعين الجمل عشان تنوع العناصر":
        "Mix almonds, cashews and walnuts so you vary the nutrients",
    "احفظها في برطمان محكم بعيد عن الحرارة والضوء":
        "Keep them in an airtight jar away from heat and light",
    "جرانولا بار بالتمر والمكسرات": "Date and nut granola bars",
    "قهوة مثلجة بزبدة الفول السوداني": "Iced coffee with peanut butter",
    "وصفة سريعة تجمع بين القهوة المطحونة الطازة وزبدة الفول السوداني لمشروب غني ومنعش.":
        "A quick recipe pairing freshly ground coffee with peanut butter for a rich, refreshing drink.",
    "كيكة التمر بالقرفة والشيكولاتة البيضاء": "Date cake with cinnamon and white chocolate",
    "وصفة سهلة تجمع بين حلاوة التمر ودفء القرفة، جاهزة في أقل من ساعة.":
        "An easy recipe pairing the sweetness of dates with the warmth of cinnamon, ready in under an hour.",
    "فتوتشيني ألفريدو دجاج مع الكاجو": "Chicken alfredo fettuccine with cashews",
    "طبق كريمي غني بالمكسرات، مناسب لعشاء سريع في نص ساعة.":
        "A creamy dish rich with nuts, right for a quick dinner in half an hour.",

    # --- about
    # PLACEHOLDER (Ahmed, 2026-08-17): the founding-year/nut-butter/export
    # copy that lived here before the fork was Abu Auf's real company
    # history and their real Gulfood/Anuga/SIAL trade-fair record — none of
    # it true for Jaad. Removed rather than rebranded. Matches the rewrite
    # in about.py: real tagline, no invented facts.
    "من الطبيعة إليك — جاد تقدم قهوة ومكسرات وبهارات طبيعية عالية الجودة، مصدرها الأصلي في قلب كل منتج.":
        "From nature to you — Jaad offers high-quality natural coffee, nuts and spices, sourced at the heart of every product.",
    "فلكل مُنتَج حكايته الخاصة؛ وبسبب اهتمامنا المستمر بالتفاصيل، فإن كل خطوة في عملية الإنتاج في جاد تُدار بعناية لضمان إنتاج منتجات عالية الجودة يتم توصيلها بحب وملئها بالمكونات المغذية من الطبيعة الأم.":
        "Every product has its own story, and because we pay constant attention to detail, every step of production at Jaad is handled carefully to ensure high-quality products, delivered with care and filled with nourishing ingredients from mother nature.",
    "نعطي الأولوية لابتكار المنتجات ونأخذ في الاعتبار اتجاهات السوق ورغبات العملاء وتغيُّر الأذواق، كما نشجع دائمًا نمط الحياة الصحي؛ لأن هدفنا ليس فقط تغذية الجسم، بل تغذية العقل والروح أيضًا.":
        "We put product innovation first, taking account of market trends, customer wishes and changing tastes, and we always encourage a healthy lifestyle — because our aim is not only to nourish the body, but the mind and spirit too.",

    # --- contact
    # PLACEHOLDER: Abu Auf's real head-office address was here before the
    # fork — removed, not reused (per the "generate placeholders" call on
    # contact info; see the CONTACT object in scripts.js).
    "لو عندك أي استفسار أو اقتراح، إحنا هنا. اختار الطريقة اللي تناسبك أو ابعتلنا رسالة وهنرد عليك في أقرب وقت.":
        "If you have a question or a suggestion, we are here. Choose whichever way suits you, or send us a message and we will reply as soon as we can.",
    "الخط الساخن": "Hotline",
    "واتساب": "WhatsApp",
    "ابعتلنا رسالة": "Send us a message",
    "فريق خدمة العملاء جاهز يساعدك": "Our customer service team is ready to help",
    "لسه عندك سؤال؟": "Still have a question?",

    # --- FAQ
    "الطلب والتوصيل": "Delivery",
    "إزاي أطلب من الموقع؟": "How do I order from the site?",
    "اختار المنتجات اللي تحبها وضيفها للسلة، بعدين اضغط على «أطلب الآن» واملأ بيانات التوصيل. هتوصلك رسالة تأكيد على البريد الالكتروني ورقم الهاتف.":
        "Choose the products you like and add them to the cart, then press “Order now” and fill in your delivery details. You will get a confirmation by email and text message.",
    "الطلب بيوصل في قد إيه؟": "How long does delivery take?",
    "داخل القاهرة الكبرى التوصيل خلال ساعتين. باقي المحافظات من يوم لثلاثة أيام عمل حسب المنطقة.":
        "Within Greater Cairo, delivery takes two hours. Other governorates take one to three working days depending on the area.",
    "في حد أدنى للطلب؟": "Is there a minimum order?",
    "لا، مفيش حد أدنى للطلب. مصاريف التوصيل بتتحسب حسب المنطقة وبتظهر قبل تأكيد الطلب، والتوصيل بيبقى مجاني فوق مبلغ معيّن بيظهرلك في السلة.":
        "No, there is no minimum order. Delivery is charged by area and is shown before you confirm, "
        "and it is free above the amount shown in your cart.",
    "أقدر أستلم من الفرع؟": "Can I pick up from a branch?",
    "أيوه — اختار «الاستلام من المتجر» في صفحة إتمام الشراء وحدد الفرع الأقرب ليك.":
        "Yes — choose “Pick up in store” at checkout and select the branch nearest to you.",
    "الدفع": "Payment",
    "طرق الدفع المتاحة إيه؟": "Which payment methods can I use?",
    "بنقبل الدفع عند الاستلام، بطاقات الائتمان (فيزا وماستركارد)، اتصالات كاش، وفاليو، بالإضافة لرصيد المحفظة.":
        "We accept cash on delivery, credit cards (Visa and Mastercard), Etisalat Cash, ValU, and your wallet balance.",
    "الدفع أونلاين آمن؟": "Is paying online secure?",
    "أيوه، كل عمليات الدفع بتتم من خلال بوابة دفع مؤمنة، وإحنا مابنحتفظش ببيانات بطاقتك.":
        "Yes. All payments go through a secured payment gateway, and we do not store your card details.",
    "المنتجات والاسترجاع": "Products",
    "المنتجات طازة إزاي؟": "How are the products kept fresh?",
    "بنحمص ونعبّي على دفعات صغيرة، والتغليف بيحافظ على النكهة والريحة لحد ما يوصلك.":
        "We roast and pack in small batches, and the packaging holds the flavour and aroma until it reaches you.",
    "أقدر أرجّع منتج؟": "Can I return a product?",
    "تقدر تطلب استرجاع خلال 14 يوم من الاستلام طالما المنتج في حالته الأصلية وغير مفتوح. راجع سياسة الاسترجاع للتفاصيل.":
        "You can request a return within 14 days of delivery as long as the product is unopened and in its original condition. See the return policy for details.",
    "إزاي أكسب نقاط؟": "How do I earn points?",
    "بتكسب نقاط على كل جنيه بتشتريه، وتقدر تستبدلها كخصم على طلبك القادم من صفحة نقاطي.":
        "You earn points on every pound you spend, and you can redeem them as a discount on your next order from the My points page.",

    # --- legal (already in-house placeholder; see DESIGN-NOTES)
    "البيانات اللي بنجمعها": "The data we collect",
    "إزاي بنستخدم بياناتك": "How we use your data",
    "مشاركة البيانات": "Sharing data",
    "حقوقك": "Your rights",
    "بنجمع البيانات اللي بتدخلها بنفسك عند إنشاء حساب أو إتمام طلب: الاسم، البريد الالكتروني، رقم الهاتف، وعناوين التوصيل.":
        "We collect the data you enter yourself when creating an account or completing an order: name, email, phone number and delivery addresses.",
    "بنجمع كمان بيانات تقنية عن استخدامك للموقع زي نوع المتصفح والصفحات اللي بتزورها، وده بيساعدنا نحسّن التجربة.":
        "We also collect technical data about your use of the site, such as browser type and the pages you visit, which helps us improve the experience.",
    "بنستخدم بياناتك عشان نجهز طلباتك ونوصّلها، ونتواصل معاك بخصوص حالة الطلب، ونبعتلك عروض لو اخترت تشترك في النشرة البريدية.":
        "We use your data to prepare and deliver your orders, to contact you about order status, and to send you offers if you have chosen to subscribe to the newsletter.",
    "مابنبيعش بياناتك لأي طرف ثالث. بنشاركها بس مع شركات الشحن وبوابات الدفع بالقدر اللازم لإتمام طلبك.":
        "We do not sell your data to any third party. We share it only with couriers and payment gateways, and only as far as is needed to complete your order.",
    "تقدر تطلب الاطلاع على بياناتك أو تعديلها أو حذفها في أي وقت من خلال التواصل معنا على info@jad.com.":
        "You can ask to see, correct or delete your data at any time by contacting us at info@jad.com.",
    "الأسعار والمنتجات": "Prices and products",
    "الطلبات والإلغاء": "Orders and cancellation",
    "باستخدامك لموقع جاد أو بإتمام طلب من خلاله، فإنك توافق على الشروط والأحكام الموضحة في هذه الصفحة.":
        "By using the Jaad site or placing an order through it, you agree to the terms and conditions set out on this page.",
    "أنت مسؤول عن الحفاظ على سرية بيانات الدخول الخاصة بحسابك، وعن كل النشاط اللي بيتم من خلاله.":
        "You are responsible for keeping your account login details confidential, and for all activity that takes place through it.",
    "كل الأسعار بالجنيه المصري وشاملة الضرائب المطبقة. بنحتفظ بحقنا في تعديل الأسعار أو إيقاف أي منتج في أي وقت.":
        "All prices are in Egyptian pounds and include applicable taxes. We reserve the right to change prices or discontinue any product at any time.",
    "بنبذل مجهود إن صور ووصف المنتجات تكون دقيقة، لكن ممكن يحصل اختلاف بسيط في اللون أو الشكل عن الصورة المعروضة.":
        "We make every effort to keep product images and descriptions accurate, but slight differences in colour or shape from the image shown are possible.",
    "بنحتفظ بحقنا في رفض أو إلغاء أي طلب في حالة عدم توفر المنتج أو وجود خطأ في السعر. في الحالة دي هيتم رد المبلغ بالكامل.":
        "We reserve the right to refuse or cancel any order where the product is unavailable or the price is wrong. In that case the amount is refunded in full.",
    "داخل القاهرة الكبرى: التوصيل خلال ساعتين من تأكيد الطلب.":
        "Within Greater Cairo: delivery within two hours of order confirmation.",
    "باقي المحافظات: من يوم إلى ثلاثة أيام عمل حسب المنطقة.":
        "Other governorates: one to three working days depending on the area.",
    "مصاريف التوصيل بتتحدد حسب المنطقة وبتظهر واضحة في صفحة إتمام الشراء قبل تأكيد الطلب.":
        "Delivery charges are set by area and are shown clearly at checkout before you confirm the order.",
    "تقدر تختار «الاستلام من المتجر» وتستلم طلبك من أقرب فرع ليك بدون مصاريف توصيل.":
        "You can choose “Pick up in store” and collect your order from your nearest branch with no delivery charge.",
    "تقدر تطلب استرجاع أي منتج خلال 14 يوم من تاريخ الاستلام، بشرط إن المنتج يكون في حالته الأصلية وغير مفتوح.":
        "You can request a return on any product within 14 days of delivery, provided it is unopened and in its original condition.",
    "المنتجات الغذائية المفتوحة لا يمكن استرجاعها لأسباب تتعلق بالسلامة الغذائية.":
        "Opened food products cannot be returned, for food safety reasons.",
    "بيتم رد المبلغ بنفس طريقة الدفع خلال 7 أيام عمل من استلام المنتج المرتجع.":
        "Refunds are issued to the original payment method within 7 working days of us receiving the returned product.",

    # --- thank you
    "شكراً لك": "Thank you",
    "تم تقديم طلبك بنجاح": "Your order was placed successfully",
    "بأنتظار تأكيد متجر": "Awaiting store confirmation",
    "سيتم تجهيز الطلب قريباً": "Your order will be prepared shortly",
    "طلبك في الطريق إليك": "Your order is on its way",
    "تم تسليم الطلب": "Order delivered",
    "سعدنا بخدمتك ونود أن تراك مرة أخرى":
        "It was a pleasure serving you — we hope to see you again",

    # --- hero product copy (generic coffee-care tips only — the "Brazilian
    # light roast" variant copy that lived here was an Abu Auf-only SKU;
    # Jaad's coffee line is light/medium/dark, no Brazilian designation)
    "تحميص فاتح": "Light roast",
    "نكهة خفيفة ومشرقة": "Light, bright flavour",
    "حبوب مختارة بعناية": "Carefully selected beans",
    "مذاق ناعم": "Smooth taste",
    "مناسب للتحضير اليومي": "Right for everyday brewing",
    "يحفظ في عبوة محكمة الغلق بعيداً عن الرطوبة":
        "Keep in an airtight container away from moisture",
    "بعيداً عن أشعة الشمس المباشرة ومصادر الحرارة":
        "Away from direct sunlight and sources of heat",
    "يفضل الطحن قبل التحضير مباشرة للحفاظ على النكهة":
        "Best ground just before brewing to preserve the flavour",

}

# --------------------------------------------------------------------------
# Templates — keyed on the element's content with element children as slots
# --------------------------------------------------------------------------
TPL = {
    "({0} تقييم)": "({0} reviews)",
    "{0} التوصيل خلال ساعتين في القاهرة الكبرى":
        "{0} Delivery within two hours across Greater Cairo",
    "ضمن أفضل {0} مبيعاً في جاد": "Among the top {0} best sellers at Jaad",
    "ضمن أفضل {0} مبيعاً في القهوة": "Among the top {0} best sellers in Coffee",
    "ضمن أفضل {0} مبيعاً في المكسرات": "Among the top {0} best sellers in Nuts",
    "ضمن أفضل {0} مبيعاً في البهارات": "Among the top {0} best sellers in Spices",
    "{0}الرئيسية": "{0}Home",
    "{0}طلباتي": "{0}My orders",
    "{0}المفضلة": "{0}Favourites",
    "{0}عناويني": "{0}My addresses",
    "{0}محفظتي": "{0}My wallet",
    "{0}نقاطي": "{0}My points",
    "{0}بيانات الحساب": "{0}Account details",
    "{0} تسجيل الخروج": "{0} Sign out",
    "البريد الالكتروني{0}": "Email{0}",
    "رقم الهاتف{0}": "Phone number{0}",
    "الاسم الأول{0}": "First name{0}",
    "الاسم الاخير{0}": "Last name{0}",
    "الاسم{0}": "Name{0}",
    "الرسالة{0}": "Message{0}",
    "المدينة{0}": "City{0}",
    "الحي{0}": "District{0}",
    "المنطقة{0}": "Area{0}",
    "رقم العقار و الشارع{0}": "Building number and street{0}",
    "نوع العقار{0}": "Property type{0}",
    "رقم الشقة{0}": "Apartment number{0}",
    "تشكيلة متنوعة تبدا من {0} جنية": "A varied range starting from EGP {0}",
    "الوزن الصافي: {0}": "Net weight: {0}",
    "رصيدك {0}": "Your balance {0}",
    "طلب رقم {0}": "Order number {0}",
    "250 جم · عدد {0}": "250 g · qty {0}",
    "{0} منتج": "{0} products",
    "({0} منتج)": "({0} products)",
    "عدد {0}": "Qty {0}",
    "يوجد أكثر من {0} فرع لجاد في {1} محافظة في مصر — اختر محافظتك لتجد أقرب فرع إليك.":
        "There are more than {0} Jaad branches across {1} governorates in Egypt — choose your governorate to find the one nearest you.",
    "يوجد أكثر من {0} فرع جاد في مصر, أكتشف الأقرب اليك":
        "There are more than {0} Jaad branches in Egypt — find the one nearest you",
    "{0}متبقي {1} لاستكمال الحد الأدنى للطلب":
        "{0}{1} to go to reach the minimum order",
    "هل لديك حساب بالفعل؟ {0}": "Already have an account? {0}",
    "لديك حساب بالفعل؟ {0}": "Already have an account? {0}",
    "أوافق على {0}": "I agree to the {0}",
    "خصم يصل إلى {0} على قسم": "Up to {0} off in",
    "يمكنك خصم {0} من طلبك القادم": "You can take {0} off your next order",
    "{0} في حالة عمل طلب من قبل كضيف (بدون حساب)، الرجاء عمل حساب الآن بنفس الإيميل المستخدم في الطلب لمتابعة حالة الشحن.":
        "{0} If you have ordered before as a guest (without an account), please create an account now with the same email used on the order so you can track its status.",
    "{0} إذا كان لديك حساب على موقعنا السابق، فبرجاء إنشاء اسم مستخدم وكلمة مرور جديدين على هذا الموقع الجديد.":
        "{0} If you had an account on our previous site, please create a new username and password on this new one.",
    "مواعيد العمل من {0} صباحاً حتى {1} مساءً يومياً. تقدر تتصفح المنتجات دلوقتي وتكمل طلبك في المواعيد.":
        "Opening hours are {0}am to {1}pm daily. You can browse the products now and complete your order during those hours.",
    "إذا كانت لديك أسئلة حول طلبك، يمكنك مراسلتنا عبر البريد الإلكتروني على {0} أو الاتصال بنا على {1}":
        "If you have questions about your order, email us at {0} or call us on {1}",
}

# --------------------------------------------------------------------------
# COPY — the client's own product prose. In-house English, needs sign-off.
# --------------------------------------------------------------------------
COPY = {
    # PLACEHOLDER (Ahmed, 2026-08-17): this was Abu Auf's real product
    # marketing/description prose before the fork (~245 lines, explicitly
    # documented above as "the client's own marketing and product prose"
    # for Abu Auf's catalogue) — none of it describes Jaad's products.
    # Emptied rather than carried over. Jaad's own descAr/descHtmlAr text
    # doesn't exist yet (no scrape, no client copy), so there is nothing
    # real to translate here until that exists — absence over invention.
}


# --------------------------------------------------------------------------
# CHROME — Arabic literals that live in scripts.js template literals
#
# These never appear in the generated HTML, so the HTML scan cannot see them:
# the mega-menu subcategory lists, the toasts, the drawers, the country and
# address data. They reach the page through the injected chrome and are picked
# up by translateDocument()'s walk of <body>, so they only need dictionary
# entries — no code change at the call sites.
# --------------------------------------------------------------------------
CHROME = {
    "جاد": "Jaad",
    "السلة": "Cart",
    "بحث": "Search",
    "إغلاق": "Close",
    "إنقاص": "Decrease",
    "زيادة": "Increase",
    "السابق": "Previous",
    "التالي": "Next",
    "مسار التنقل": "Breadcrumb",
    "4.8 من 5": "4.8 out of 5",
    "اقرأ المزيد": "Read more",
    "إظهار كلمة السر": "Show password",
    "إخفاء كلمة السر": "Hide password",
    "أضف ملاحظة": "Add a note",
    "ملاحظات على الطلب": "Order notes",
    "فرع جاد": "Jaad branch",
    "جميع حقوق النشر تنتمي إلى جاد,": "All rights reserved, Jaad,",
    # Size-variant SKU names that are not a catalogue `nameAr`, so
    # _catalog_names() cannot reach them; they survive only in card alt text.
    "بن برازيلى فاتح محوج - 100 جم": "Light Spiced Brazilian Coffee - 100 g",
    "بهارات فراخ - 75 جم": "Chicken Spices - 75 g",
    "العدد:": "Qty:",
    "أضف": "Add",
    # mega-menu subcategories
    "مكسرات": "Nuts",
    "مكسرات نيئة": "Raw nuts",
    "مكسرات محمصة ومملحة": "Roasted and salted nuts",
    "مكسرات بنكهات": "Flavoured nuts",
    "تشكيلة مكسرات": "Nut selections",
    "حبوب ومقرمشات": "Seeds and crackers",
    "قهوة تركي": "Turkish coffee",
    "قهوه تركي": "Turkish coffee",
    "قهوه": "Coffee",
    "مشروبات": "Drinks",
    "مطبخ": "Kitchen",
    "وصفات": "Recipes",
    "اليوم": "Today",
    "الشوكولاتة": "Chocolate",
    "التجمع": "The Settlement",
    # locale / country
    "العربية": "Arabic",
    "مصر": "Egypt",
    "الامارات": "UAE",
    "الامارات العربية المتحدة": "United Arab Emirates",
    # location sheet
    "أختار منطقة التوصيل": "Choose a delivery area",
    "تأكيد المنطقة": "Confirm area",
    "التوصيل الى الشروق - القاهرة": "Delivery to El Shorouk - Cairo",
    "تم تحديث منطقة التوصيل.": "Delivery area updated.",
    # addresses
    "المنزل": "Home",
    "العمل": "Work",
    "المنزل، العمل…": "Home, Work…",
    "المنطقة، المدينة": "Area, city",
    "رقم الشقة والمبنى واسم الشارع": "Apartment, building and street name",
    "تمت إضافة العنوان": "Address added",
    "تم تعديل العنوان": "Address updated",
    "تم حذف العنوان": "Address deleted",
    # search
    "الأكثر بحثاً": "Most searched",
    "أدخل عنوان البريد الالكتروني": "Enter your email address",
    # newsletter / footer
    "اشترك لتعرف على أجدد العروض والخصومات":
        "Subscribe to hear about the newest offers and discounts",
    "كن أول من يعرف كل ما هو جديد في جاد":
        "Be the first to know what is new at Jaad",
    "تم الاشتراك بنجاح! 🎉": "Subscribed successfully! 🎉",
    "تم الإرسال بنجاح.": "Sent successfully.",
    "انستجرام": "Instagram",
    "فيسبوك": "Facebook",
    "يوتيوب": "YouTube",
    "لينكد إن": "LinkedIn",
    # payment methods
    "الدفع عند الاستلام": "Cash on delivery",
    "اتصالات كاش": "Etisalat Cash",
    # toasts
    "تمت الإضافة إلى السلة": "Added to cart",
    "تمت الإزالة من السلة": "Removed from cart",
    "تمت إضافة ملاحظتك على الطلب": "Your order note was added",
    "تمت إزالة الملاحظات": "Notes removed",
    "تم تطبيق التفضيلات": "Preferences applied",
    "تم إلغاء خصم المحفظة": "Wallet discount removed",
    "تم خصم": "Discounted",
    "من الإجمالي": "from the total",
    "متبقي": "remaining",
    "لاستكمال الحد الأدنى للطلب": "to reach the minimum order",
    "تعذر النسخ — انسخ الرابط يدوياً": "Could not copy — copy the link manually",
    # FAQ / contact intros
    "عندك اي اسئلة؟ كل حاجة هنا..": "Got questions? Everything is here…",
    "لو عندك أي استفسار أو عايز تطرح أي سؤال ، هتلاقي كل حاجة هنا":
        "If you have a query or want to ask a question, you will find everything here",
    # banner alt text
    "تشكيلة جاد المميزة": "The Jaad signature selection",
}

# --------------------------------------------------------------------------
# COPY2 — the remaining client product prose (see COPY above; same status).
# --------------------------------------------------------------------------
COPY2 = {
    # PLACEHOLDER (Ahmed, 2026-08-17): "the remaining client product
    # prose" (~450 lines: spices, snacks, dates, maamoul, pretzels, nuts,
    # popcorn, coffee, protein bars — none of it Jaad's products) per the
    # original comment above. Emptied, same reasoning as COPY.
}

# --------------------------------------------------------------------------
# TPL2 — the remaining templates (mostly client benefit lists).
# --------------------------------------------------------------------------
TPL2 = {
    # PLACEHOLDER (Ahmed, 2026-08-17): "the remaining templates (mostly
    # client [Abu Auf] benefit lists)" per the original comment above —
    # emptied along with COPY2, same reasoning.
}


def _catalog_names():
    """Product names, from the client's own English `name` field.

    Covers the card titles, the product page h1, cart and drawer lines, the
    bundle rows, and every `alt` that repeats the name — which is why this is
    worth more than its 99 entries suggest.
    """
    path = os.path.join(EXPORT, "data", "catalog.json")
    with open(path, encoding="utf-8") as f:
        cat = json.load(f)
    out = {}
    for p in cat["products"]:
        ar, en = (p.get("nameAr") or "").strip(), (p.get("name") or "").strip()
        if ar and en:
            out[ar] = en
        for s in p.get("sizes") or []:
            sar, sen = (s.get("nameAr") or "").strip(), (s.get("name") or "").strip()
            if sar and sen:
                out[sar] = sen
    return out


def _generated():
    """Formulaic families — looped rather than listed.

    GALLERY is 40 entries on its own (every thumbnail on every gallery length),
    and the governorate rows are a name plus a count. Writing these by hand
    would be forty chances to typo a number.
    """
    out = {}
    # gallery thumbnail labels: "عرض الصورة 3 من 7"
    for total in range(1, 13):
        for i in range(1, total + 1):
            out["عرض الصورة %d من %d" % (i, total)] = "View image %d of %d" % (i, total)

    # The mega-menu and footer build these by CONCATENATION in scripts.js
    # ("تسوق كل " + name), so the string that reaches the DOM is not a literal
    # anywhere and cannot be keyed by hand without guessing. Generated from
    # the same category list the nav uses, so adding a category cannot leave a
    # link stranded in Arabic — the exact failure mode the concatenation trap
    # in CLAUDE.md describes for Tailwind classes, in a different register.
    for ar, en in NAV_CATEGORIES.items():
        out["تسوق كل " + ar] = "Shop all " + en
        out["جميع " + ar] = "All " + en
    return out


NAV_CATEGORIES = {
    "العروض و الخصومات": "Offers & Discounts",
    "المكسرات": "Nuts",
    "القهوة": "Coffee",
    "الوجبات صحية": "Healthy Snacks",
    "المشروبات": "Beverages",
    "البهارات والزيوت": "Spices & Oils",
    "الهدايا": "Gifting",
}


GOVERNORATES = {
    "القاهرة": "Cairo", "الجيزة": "Giza", "الجيزه": "Giza",
    "الإسكندرية": "Alexandria", "الاسكندريه": "Alexandria",
    "البحر الأحمر": "Red Sea", "البحر الاحمر": "Red Sea",
    "القليوبية": "Qalyubia", "القليوبيه": "Qalyubia",
    "الدقهلية": "Dakahlia", "الدقهليه": "Dakahlia",
    "الغربية": "Gharbia", "الغربيه": "Gharbia",
    "الشرقية": "Sharqia", "الشرقيه": "Sharqia",
    "المنوفية": "Monufia", "المنوفيه": "Monufia",
    "البحيرة": "Beheira", "البحيره": "Beheira",
    "بورسعيد": "Port Said", "السويس": "Suez", "دمياط": "Damietta",
    "المنيا": "Minya", "أسيوط": "Asyut", "اسيوط": "Asyut",
    "أسوان": "Aswan", "اسوان": "Aswan",
    "جنوب سيناء": "South Sinai", "شمال سيناء": "North Sinai",
    "الفيوم": "Fayoum", "كفر الشيخ": "Kafr El Sheikh",
    "الغردقة": "Hurghada", "طنطا": "Tanta",
    "الأقصر": "Luxor", "الاقصر": "Luxor",
    "الاسماعليه": "Ismailia", "بني سويف": "Beni Suef",
    "سوهاج": "Sohag", "قنا": "Qena",
    "الوادي الجديد": "New Valley", "مرسي مطروح": "Marsa Matrouh",
    "دبي": "Dubai", "الشارقة": "Sharjah", "ديرا": "Deira",
}

# Cairo districts used by the delivery-area sheet and the branches list.
DISTRICTS = {
    "15 من مايو": "15th of May City", "العباسيه": "Abbassia",
    "عين شمس الشرقيه": "East Ain Shams", "عين شمس الغربيه": "West Ain Shams",
    "الظاهر": "El Zaher", "المطريه": "Matareya", "الرحاب": "Al Rehab",
    "الحلميه الجديده": "New Helmeya", "وسط البلد": "Downtown",
    "الشروق": "El Shorouk", "النزهه الجديده": "New Nozha",
    "جاردن سيتي": "Garden City", "حدائق القبه": "Hadayek El Kobba",
    "هليوبوليس": "Heliopolis", "حلوان": "Helwan", "القطاميه": "Katameya",
    "المعادي": "Maadi", "المعادي الجديده": "New Maadi", "مدينتي": "Madinaty",
    "المنيل": "Manial", "المقطم": "Mokattam", "مدينه نصر": "Nasr City",
    "شيراتون": "Sheraton", "شبرا": "Shubra",
    "التجمع الاول": "First Settlement", "التجمع الثالث": "Third Settlement",
    "التجمع الخامس": "Fifth Settlement",
    "زهراء المعادي": "Zahraa El Maadi", "زهراء مدينه نصر": "Zahraa Nasr City",
    "الزمالك": "Zamalek", "الزيتون": "Zeitoun",
}


def build_dictionary():
    text = {}
    text.update(_generated())
    text.update(GOVERNORATES)
    text.update(DISTRICTS)
    text.update(_catalog_names())
    text.update(COPY)
    text.update(COPY2)
    text.update(CHROME)
    text.update(UI)  # our own UI wins any collision with scraped copy

    # i18n_extra.json — English for every page-body string the audit found
    # untranslated (Ahmed, 2026-08-18: "every text respects the en/ar swap").
    # Loaded last so it fills any remaining gaps; a flat {arabic: english} map.
    _extra_path = os.path.join(HERE, "i18n_extra.json")
    if os.path.exists(_extra_path):
        with open(_extra_path, encoding="utf-8") as _f:
            text.update(json.load(_f))

    tpl = dict(TPL)
    tpl.update(TPL2)
    # "<governorate> {0}" rows on the branches page
    for ar, en in GOVERNORATES.items():
        tpl.setdefault(ar + " {0}", en + " {0}")
    return text, tpl


def write(dest=None):
    text, tpl = build_dictionary()
    dest = dest or os.path.join(EXPORT, "i18n-en.js")
    payload = json.dumps({"text": text, "tpl": tpl}, ensure_ascii=False,
                         sort_keys=True, separators=(",", ":"))
    banner = (
        "/* GENERATED by build/i18n.py - do not edit.\n"
        "   %d text entries, %d templates.\n"
        "   English is in-house and awaits client sign-off (DESIGN-NOTES). */\n"
    ) % (len(text), len(tpl))
    with open(dest, "w", encoding="utf-8") as f:
        f.write(banner + "window.JAAD_I18N=" + payload + ";\n")
    return len(text), len(tpl), os.path.getsize(dest)


if __name__ == "__main__":
    n, m, size = write()
    print("i18n-en.js: %d text, %d templates, %s bytes" % (n, m, format(size, ",")))
