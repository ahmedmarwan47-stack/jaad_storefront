/* =====================================================================
   scripts.js — shared behaviour for the static Jaad build.

   Forked from the upstream storefront build (same architecture — see the
   order-base-ecommerce repo for the original). Historical/dated comments
   below (measurements, fix notes) describe that original build and have
   not all been individually re-verified against Jaad's own Figma yet.

   Replaces the React runtime with vanilla JS:
     • Injects the shared header, footer and overlay chrome into every
       page (each page only ships a #site-header / #site-footer mount
       point, so markup stays DRY and works from the file:// protocol).
     • Re-implements the interactive pieces that were React components:
       mobile menu drawer, cart drawer, search modal, location bottom
       sheet, sticky-on-scroll navbar and mega-menu hover.
     • Provides page-level helpers: carousels (replacing Swiper),
       accordions, tabs, quantity steppers, toasts and demo forms.

   The document is Arabic-first and renders RTL. Anything that positions
   against a physical edge must use logical properties (ms/me, ps/pe,
   start/end) so it mirrors correctly.

   Menus and footer columns below mirror the Jaad Figma; socials and
   contact details are PLACEHOLDER (no real Jaad accounts/hotline exist
   yet — left as "#"/example values rather than inherited Jaad ones).
   Product data lives in data/catalog.json.
   ===================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------
     Placeholder content (formerly fetched from the CMS)
     --------------------------------------------------------------- */
  /*
   * Jaad has no live store/API (unlike the WooCommerce catalog this was
   * forked from) — categories are the 3 hand-built groups from the
   * 26-SKU table: Coffee, Nuts, Spices. Arabic labels follow the Figma nav.
   */
  // Rebuilt from the Jaad Figma header (utility bar: "OUR STORY / MEDIA /
  // FAQs / CONTACT US"), replacing the FORK SOURCE's rewards/branches/export
  // links — Jaad has no branches (dropped entirely), no export program.
  const SUPPORT_MENU = [
    { title: "قصتنا", url: "/about" },
    { title: "ميديا", url: "/blogs" },
    { title: "الأسئلة المتداولة", url: "/faqs" },
    { title: "اتصل بنا", url: "/contact-us" },
  ];

  // Jaad sells exactly 3 categories (Coffee/Spices/Nuts, 26 SKUs total) — no
  // mega-menu children, no dates/healthy-snacks/gifting/hot-drinks/offers
  // tiles like the 12-category, ~99-product catalog this was forked from.
  // Order matches the Figma nav: COFFEE, SPICES, NUTS.
  const MAIN_MENU = [
    { name: "القهوة", url: "/shop/coffee", image: "images/jaad/categories/coffee-a.png" },
    { name: "البهارات", url: "/shop/spices", image: "images/jaad/categories/spices-a.png" },
    { name: "المكسرات", url: "/shop/nuts", image: "images/jaad/categories/nuts-a.png" },
  ];

  /* Column order is RTL reading order: rightmost column first.
     Matches the Jaad Figma footer exactly (Categories / Company / Support) —
     no distributors/partners/careers/mobile-app links like the fork's. */
  const FOOTER_COLUMNS = [
    {
      name: "الأقسام",
      links: [
        { title: "القهوة", url: "/shop/coffee" },
        { title: "المكسرات", url: "/shop/nuts" },
        { title: "البهارات", url: "/shop/spices" },
      ],
    },
    {
      name: "الشركة",
      links: [
        { title: "قصتنا", url: "/about" },
        // Was "فرص وظائف" (/careers) until 2026-08-20 — no careers page is
        // built, and an unmapped url falls through to index.html, so the link
        // silently dropped you on the homepage instead of doing nothing
        // visible. Replaced with the blog, which is a real page and was the
        // one utility destination the footer never listed.
        { title: "ميديا", url: "/blogs" },
        { title: "اتصل بنا", url: "/contact-us" },
      ],
    },
    {
      name: "المساعدة",
      links: [
        { title: "الاسئلة الشائعة", url: "/faqs" },
        { title: "سياسة الاسترجاع", url: "/return-policy" },
        { title: "الشروط والاحكام", url: "/terms-conditions" },
        { title: "سياسة الخصوصية", url: "/privacy-policy" },
      ],
    },
  ];

  /* Contact details from the Figma footer. */
  // PLACEHOLDER, per the fork plan (Ahmed, 2026-08-17): Jaad has no real
  // hotline/address yet. These were the FORK SOURCE's actual live hotline +
  // factory address before the fork — do not reintroduce them; they reach a
  // different, unrelated company. (They had crept back into the contact and
  // thank-you pages and were removed again 2026-08-20.) Matches the
  // placeholder phone already set in the Figma footer.
  const CONTACT = {
    hotline: "01200000000",
    email: "info@jad.com",
    address: "",
  };

  /* PLACEHOLDER, per the fork plan (Ahmed, 2026-08-17): these were the FORK
     SOURCE's real, live social accounts — pointing Jaad's footer at them
     would send shoppers to a different, unrelated brand. Left as "#"
     (absence over invention) until Jaad's real handles exist. */
  const SOCIALS = [
    {
      title: "فيسبوك",
      href: "#",
      icon: "images/jaad/social/icon-facebook.svg",
    },
    {
      title: "انستجرام",
      href: "#",
      icon: "images/jaad/social/icon-instagram.svg",
    },
    {
      title: "تيك توك",
      href: "#",
      icon: "images/jaad/social/icon-tiktok.svg",
    },
    {
      title: "يوتيوب",
      href: "#",
      icon: "images/jaad/social/icon-youtube.svg",
    },
  ];

  /* ---------------------------------------------------------------
     Route → static-file mapping
     --------------------------------------------------------------- */
  /* The one category page that was actually built, by slug. */
  const CATEGORY_PAGE = { "coffee-beverage": "shop-category.html" };

  /* Sub-category slug → parent category slug, taken from the nav itself so the
     two cannot drift apart. */
  const CHILD_TO_PARENT = (function () {
    const m = {};
    MAIN_MENU.forEach(function (i) {
      const parent = (i.url || "").replace("/shop/", "");
      (i.children || []).forEach(function (c) {
        m[(c.url || "").replace("/shop/", "")] = parent;
      });
    });
    // المشروبات rides on /shop/hot-drinks but hot-drinks is no longer a listed
    // coffee child (our sample has none), so alias it to the coffee category so
    // that tab still lands on the coffee page rather than an unfiltered shop.
    m["hot-drinks"] = "coffee-beverage";
    return m;
  })();

  /* Children of a category that has its OWN listing page (CATEGORY_PAGE) route
     to that page with the child slug as a hash, so the page's sub-category chip
     is applied on arrival — this is what makes the coffee sub-categories filter
     from the mega menu. Children of every other category have no dedicated page,
     so they fall through to CHILD_TO_PARENT and filter their parent on shop.html
     (the same path التمور / المكسرات already take). */
  const CHILD_PAGE_HASH = (function () {
    const m = {};
    MAIN_MENU.forEach(function (i) {
      const page = CATEGORY_PAGE[(i.url || "").replace("/shop/", "")];
      if (!page) return;
      (i.children || []).forEach(function (c) {
        m[(c.url || "").replace("/shop/", "")] = page;
      });
    });
    return m;
  })();

  /* Pages the chrome must NOT link to, because no such page is built.
     Anything listed here renders as "#" wherever the header, footer or mobile
     drawer would otherwise link it.

     History (Ahmed, 2026-08-02 -> 2026-08-20): this started as a demo stub that
     also held about/faqs/contact-us/policies/blogs/rewards, so a client
     walkthrough stayed on the shopping flow instead of wandering into
     then-unfinished content pages. Those pages are all real and finished now,
     so keeping them here just made Our Story, FAQs, Contact Us and the blog
     unreachable from every surface at once — header, footer and drawer alike.
     Freed. Only genuinely absent pages remain: Jaad has no branches (see
     SUPPORT_MENU) and no export programme, so nothing is built for either.
     `store-closed.html` exists but is a STATE page the site redirects to, not
     somewhere to navigate to by hand. */
  const DEMO_DEAD_PAGES = new Set([
    "branches.html", "export.html", "store-closed.html",
  ]);
  function pageHref(url) {
    const href = pageHrefRaw(url);
    return DEMO_DEAD_PAGES.has(href) ? "#" : href;
  }
  function pageHrefRaw(url) {
    if (!url) return "#";
    if (/^https?:\/\//.test(url) || url.startsWith("#") || url.endsWith(".html"))
      return url;
    const clean = "/" + url.replace(/^\/+/, "").replace(/\/+$/, "");
    const map = {
      "/": "index.html",
      "/about": "about.html",
      "/branches": "branches.html",
      "/faqs": "faqs.html",
      "/contact-us": "contact-us.html",
      "/privacy-policy": "privacy-policy.html",
      "/terms-conditions": "terms-conditions.html",
      "/return-policy": "return-policy.html",
      "/blogs": "blogs.html",
      "/rewards": "rewards.html",
      "/export": "export.html",
      "/shop": "shop.html",
      "/cart": "cart.html",
      "/checkout": "checkout.html",
      "/thank-you": "thank-you.html",
      "/login": "login.html",
      "/register": "register.html",
      "/verify": "verify.html",
      "/forget-password": "forget-password.html",
      "/reset-password": "reset-password.html",
      "/store-closed": "store-closed.html",
      "/my-account": "my-account.html",
    };
    if (map[clean]) return map[clean];
    /*
     * Category routes. Only one category page exists — shop-category.html, the
     * Figma Collection worked example for coffee — and every /shop/<slug> used
     * to resolve to it, so tapping "المكسرات" in the nav landed you on coffee.
     * Real category slugs now open the listing filtered to that category.
     * Sub-category slugs have no field in catalog.json, so they fall back to
     * their parent, which MAIN_MENU already records.
     */
    if (clean.startsWith("/shop/")) {
      const slug = clean.slice("/shop/".length);
      // A sub-category of a category that has its own page (coffee) opens that
      // page with its chip pre-applied; everything else filters its parent.
      if (CHILD_PAGE_HASH[slug]) return CHILD_PAGE_HASH[slug] + "#" + slug;
      const cat = CHILD_TO_PARENT[slug] || slug;
      return CATEGORY_PAGE[cat] || "shop.html#" + cat;
    }
    if (clean.startsWith("/products/")) return "product.html";
    if (clean.startsWith("/blogs/")) return "blog.html";
    if (clean.startsWith("/my-account/"))
      return "my-account-" + clean.split("/")[2] + ".html";
    return "index.html";
  }

  const esc = (s) =>
    String(s == null ? "" : s).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );

  /* ---------------------------------------------------------------
     SVG icons (ported from the React icon components)

     Every glyph is `w-full h-full` and paints in `currentColor`, so **the
     wrapper decides the size and the colour** — one rule, no surprises.

     They used to carry their own `w-4`/`w-5`/`w-6`, which silently fought the
     wrapper: the masthead chevrons sat in a `w-6 h-6` span but drew at 16px,
     and the breadcrumb arrows drew at 20px inside a 16px box and overflowed
     it. `menu` was worse — hardcoded `width="31" height="30"` and
     `stroke="white"`, so it ignored both.
     --------------------------------------------------------------- */
  const ICON = {
    account:
      '<svg viewBox="0 0 29 29" fill="none" class="w-full h-full"><path d="M4.47 22.96C7.43 21.29 10.85 20.33 14.5 20.33s7.07.96 10.03 2.63M18.88 11.58a4.38 4.38 0 1 1-8.75 0 4.38 4.38 0 0 1 8.75 0ZM27.63 14.5A13.13 13.13 0 1 1 1.38 14.5a13.13 13.13 0 0 1 26.25 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    search:
      '<svg viewBox="0 0 29 29" fill="none" class="w-full h-full"><path d="M27.63 27.63 18.88 18.88M21.79 11.58a10.21 10.21 0 1 1-20.42 0 10.21 10.21 0 0 1 20.42 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    location:
      '<svg viewBox="0 0 22 20" fill="none" class="w-full h-full"><path d="M16.75 11.75c-3 0-4 2-4 2h-3l-.14-.22c-.86-1.35-1.29-2.03-1.87-2.52-.51-.43-1.11-.76-1.75-.96-.72-.23-1.53-.23-3.13-.23H.75M16.75 11.75c3 0 4 2 4 2M16.75 11.75 15.23 3.38c-.17-.94-.26-1.4-.5-1.75a2 2 0 0 0-.84-.71c-.39-.17-.86-.17-1.81-.17h-.33M3.75 6.75h2M.75 3.75h4M15.75 5.75h1.42a1.5 1.5 0 0 0 .58-2.9c-.2-.09-.42-.1-.58-.1H15.25M6.75 15.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM18.75 16.75a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M20 7H7M20 12H4M16 17H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    /* An actual globe. The asset named icon-globe.svg is a chevron-down (a
       misnamed Figma export) — using it as a globe put a dropdown arrow
       beside every language row in the locale popup. */
    globe:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M3 12h18M12 3c2.5 2.4 3.8 5.6 3.8 9S14.5 18.6 12 21c-2.5-2.4-3.8-5.6-3.8-9S9.5 5.4 12 3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    /* Stepper glyphs — same SVGs as components.py's ICON. Text −/+ sit on a
       baseline and centre visibly low in their buttons; a viewBox-centred
       path cannot drift. */
    plus: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    minus: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    // Rounded warning triangle (Ahmed's alert-01.svg) — the below-minimum
    // notice. currentColor so it inherits the error ink from its wrapper.
    alert:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M5.32171 9.68293C7.73539 5.41199 8.94222 3.27651 10.5983 2.72681C11.5093 2.4244 12.4907 2.4244 13.4017 2.72681C15.0578 3.27651 16.2646 5.41199 18.6783 9.68293C21.092 13.9539 22.2988 16.0893 21.9368 17.8293C21.7376 18.7866 21.2469 19.6549 20.535 20.3097C19.241 21.5 16.8274 21.5 12 21.5C7.17265 21.5 4.75897 21.5 3.46496 20.3097C2.75308 19.6549 2.26239 18.7866 2.06322 17.8293C1.70119 16.0893 2.90803 13.9539 5.32171 9.68293Z" stroke="currentColor" stroke-width="1.5"/><path d="M12.2422 17V13C12.2422 12.5286 12.2422 12.2929 12.0957 12.1464C11.9493 12 11.7136 12 11.2422 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M11.992 9H12.001" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    close:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    chevronDown:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    /* ONE cart glyph site-wide (Ahmed, 2026-08-19): the Perfect-Picks card add
       button's cart (Figma node 4994:7438), identical to components.ICON['cart'].
       Was a solid shopping BAG here, which made the JS-rendered cards (recently
       viewed, drawer upsell), the mobile masthead and the fly-to-cart clone
       disagree with the server-rendered product cards. Now they all match. */
    cart:
      '<svg viewBox="0 0 20 19" fill="none" class="w-full h-full">' +
      '<path d="M3.75 3.75V9.43333C3.75 10.9735 3.75 11.7436 4.04973 12.3318C4.31338 12.8493 4.73408 13.27 5.25153 13.5336C5.83978 13.8333 6.60986 13.8333 8.15 13.8333H12.7308C13.745 13.8333 14.2521 13.8333 14.697 13.676C15.0903 13.5369 15.4468 13.3102 15.7396 13.0129C16.0707 12.6767 16.2857 12.2175 16.7157 11.299L17.3165 10.0157C18.2915 7.93326 18.7789 6.89207 18.6388 6.04904C18.5164 5.31257 18.0998 4.65752 17.4847 4.23437C16.7806 3.75 15.631 3.75 13.3316 3.75H3.75ZM3.75 3.75V3.6757C3.75 2.89117 3.75 2.4989 3.63192 2.18601C3.44591 1.69313 3.05687 1.30409 2.56399 1.11809C2.2511 1 1.85883 1 1.0743 1H1M5.58333 17.5H6.5M12 17.5H12.9167" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
      "</svg>",
    arrowRight:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m9 6 6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    arrowLeft:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m15 6-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    phone:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    // Stroked to match minus/plus, which it swaps places with on a cart line
    // at quantity 1 — a filled glyph there would read as a different control
    // arriving rather than the same one changing meaning.
    trash:
      '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M4 7h16M10 4h4M9 7v11m6-11v11M6 7l.8 12.1A2 2 0 0 0 8.8 21h6.4a2 2 0 0 0 2-1.9L18 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };

  const isCheckout = () => document.body.getAttribute("data-page") === "checkout";
  const currentPath = () => document.body.getAttribute("data-path") || "/";

  /* ---------------------------------------------------------------
     Country / currency selector.
     Egypt-only in this build; the markup carries the full control so the
     export drops straight into the real storefront.
     --------------------------------------------------------------- */
  /*
   * Country / language switcher. The live site opens a 288px panel headed
   * اللغة with English and العربية rows, a flag per row and a check on the
   * active one — replicated here, measured off jad.com rather than eyeballed.
   *
   * The toggle really does flip `dir` and `lang` on <html>, which is the point:
   * it makes the RTL↔LTR layout testable. It does NOT translate page copy —
   * see initLangSwitcher and DESIGN-NOTES.
   */
  /*
   * English chrome strings, keyed by the Arabic original so the existing data
   * literals do not have to be restructured. `t()` returns the Arabic unchanged
   * unless the document is in English mode.
   *
   * IMPORTANT: these English strings are written in-house — standard commerce
   * terminology, not the client's approved wording. They are placeholder and
   * flagged as such in DESIGN-NOTES. Page body copy is NOT translated: there is
   * no English source for it and machine-translating a storefront would be
   * inventing content. See the "Language" section in DESIGN-NOTES.
   */
  const EN = {
    // primary nav — Jaad's real 3 categories, matching MAIN_MENU
    "المكسرات": "Nuts",
    "القهوة": "Coffee",
    "البهارات": "Spices",
    "ميديا": "Media",
    "الأقسام": "Categories",
    "الشركة": "Company",
    // search
    "اقتراحات البحث": "Search suggestions",
    "ابحث عن قهوة، مكسرات، بهارات…": "Search for coffee, nuts, spices…",
    "نتيجة": "results",
    "لا توجد نتائج لـ": "No results for",
    "تعذر تحميل نتائج البحث. حاول مرة أخرى.": "Could not load search results. Please try again.",
    "منتجات أُضيفت إلى السلة": "products added to cart",
    // masthead + utility
    "المنتجات": "Products",
    "الحساب": "Account",
    "تسجيل الدخول": "Sign in",
    "قصتنا": "Our Story",
    "سياسة التوصيل والاسترجاع": "Delivery & Returns",
    "أتصل بنا": "Contact Us",
    // footer columns
    "المساعدة": "Support",
    "فرص وظائف": "Careers",
    "الاسئلة الشائعة": "FAQs",
    "تعليقات العملاء": "Reviews",
    "الشروط والاحكام": "Terms & Conditions",
    "سياسة الخصوصية": "Privacy Policy",
    "سياسة الاسترجاع": "Return Policy",
    // cart / overlays
    "سلة التسوق": "Shopping Cart",
    "قد يعجبك أيضا": "You may also like",
    "مصاريف التوصيل": "Delivery fee",
    "الإجمالي": "Total",
    "خصم المحفظة": "Wallet discount",
    "خصم كود الخصم": "Promo code discount",
    "الدفع من المحفظة": "Pay from wallet",
    "تم الخصم من رصيدك": "Deducted from your balance",
    // locale popup + addresses
    "الدولة واللغة": "Country & Language",
    "الدولة و العملة": "Country & currency",
    "تطبيق": "Apply",
    "اضف عنوان": "Add Address",
    "تعديل العنوان": "Edit address",
    "اسم العنوان": "Address name",
    "العنوان": "Address",
    "المنطقة والمدينة": "Area & city",
    "اجعله العنوان الافتراضي": "Make it the default address",
    "حفظ العنوان": "Save address",
    "العنوان الافتراضي": "Default address",
    "عنوان افتراضي": "Default",
    "تم تعيين العنوان الافتراضي": "Default address updated",
    "لازم يفضل عندك عنوان افتراضي واحد على الأقل": "You need to keep one default address",
    "تعديل": "Edit",
    "لا توجد عناوين محفوظة بعد.": "No saved addresses yet.",
    "تم النسخ ✓": "Copied ✓",
    "عرض السلة": "View cart",
    "اتمام الشراء": "Checkout",
    // Heading has no full stop; the older "سلتك فارغة." entry is kept because
    // translateDocument() may still meet that exact string in stored copy.
    "سلتك فارغة.": "Your cart is empty.",
    "سلتك فارغة": "Your cart is empty",
    "المنتجات اللي تضيفها هتظهر هنا.": "Products you add will appear here.",
    "حذف": "Remove",
    "اضف": "Add",
    "القائمة": "Menu",
    "روابط أخرى": "More links",
    "الاكثر مبيعا": "Best sellers",
    "اللغة": "Language",
    // build-time UI strings — these live in the generated HTML, and are picked
    // up by translateDocument()'s text-node pass rather than by t()
    "خصم 10% لما تستخدم برومو كود": "10% off with promo code",
    // Demo sign-in
    "تم تسجيل الدخول بنجاح": "Signed in successfully",
    "البريد الإلكتروني أو كلمة المرور غير صحيحة": "Incorrect email or password",
    "تم تسجيل الخروج": "Signed out",
    "تسجيل الخروج": "Sign out",
    "حساب تجريبي للاختبار": "Demo account for testing",
    "استخدم البيانات دي لتجربة تسجيل الدخول والمفضلة:": "Use these details to try signing in and favourites:",
    "املأ البيانات تلقائياً": "Fill automatically",
    "اضف الى السلة": "Add to cart",
    "أضف إلى المفضلة": "Add to favourites",
    "إزالة من المفضلة": "Remove from favourites",
    "تمت الإضافة إلى المفضلة": "Added to favourites",
    "تمت الإزالة من المفضلة": "Removed from favourites",
    "لا توجد منتجات في المفضلة": "No saved products yet",
    "المنتجات اللي تحفظها هتظهر هنا.": "Products you save will appear here.",
    "تصفح المنتجات": "Browse products",
    "عرض المزيد": "Show more",
    "تسوق اكتر": "Shop more",
    "تسوق منتجاتنا": "Shop our products",
    "كل المنتجات": "All products",
    "الرئيسية": "Home",
    "المنتجات": "Products",
    "منتج": "products",
    "ترتيب حسب": "Sort by",
    "الأكثر مبيعاً": "Best selling",
    "وصل حديثاً": "New arrivals",
    "السعر: من الأقل": "Price: low to high",
    "السعر: من الأعلى": "Price: high to low",
    "سلة التسوق": "Shopping Cart",
    "ملخص السلة": "Cart Summary",
    "تعديل": "Edit",
    "الإجمالي": "Total",
    "مصاريف التوصيل": "Delivery fee",
    "أطلب الآن": "Order now",
    "اشتري الان": "Buy now",
    "هل لديك برومو كود؟": "Have A Promo Code?",
    "توصيل خلال ساعتين": "Delivered within 2 hours",
    "داخل القاهرة الكبرى، ولباقي المحافظات حسب المنطقة": "Within Greater Cairo, and to other governorates by area",
    "داخل القاهرة الكبرى": "Within Greater Cairo",
    "إتمام الطلب": "Checkout",
    "مواصلة التسوق": "Continue shopping",
    "أضف": "Add",
    "لتحصل على شحن مجاني": "to get free shipping",
    "مبروك! توصيل طلبك مجاني": "Your order ships free!",
    "اكتشف تشكيلة": "Discover JAAD's full",
    "كاملة من جاد.": "collection.",
    "تسوّق الكل": "Shop all",
    "أضف كود قسيمة": "Add Voucher Code",
    "الكود": "Code",
    "الكود صالح للاستخدام مرة واحدة فقط.": "Code valid for one-time use only.",
    "أضف القسيمة": "Add voucher",
    "تفعيل القسيمة": "Activate Voucher",
    "سيتم إضافة": "Will add",
    "إلى رصيد محفظتك": "to your wallet balance",
    "حوّل نقاطك إلى رصيد في محفظتك": "Convert your points into wallet balance",
    "نقطة متاحة": "points available",
    "عدد النقاط": "Number of points",
    "كل النقاط": "All points",
    "القيمة": "Value",
    "تأكيد الاستبدال": "Confirm redemption",
    "تيك توك": "TikTok",
    "أيام سابقة": "Previous days",
    "أيام تالية": "Next days",
    "مثال: JAAD150": "e.g. JAAD150",
    "الاستلام من المتجر غير متاح لطلبات الهدايا": "Store pickup isn't available for gift orders",
    "تم إرسال رمز جديد": "A new code has been sent",
    "تم إلغاء الكود": "Code removed",
    "تم تأكيد بريدك الإلكتروني بنجاح": "Your email has been confirmed",
    "تم تحويل": "Converted",
    "تم تفعيل القسيمة وإضافتها لمحفظتك": "Voucher activated and added to your wallet",
    "تمت إضافة القسيمة إلى قائمتك": "Voucher added to your list",
    "تمت إضافة منتجات الطلب إلى السلة": "Order items added to your cart",
    "رمز التحقق غير صحيح، حاول مرة أخرى": "Incorrect code — please try again",
    "من فضلك أدخل رقم موبايل صحيح": "Please enter a valid mobile number",
    "أدخل كود الخصم": "Enter discount code",
    "تم تطبيق": "Applied",
    "إلغاء": "Remove",
    "أضف ملاحظات على الطلب": "Add order notes",
    "لا توجد منتجات في هذا القسم حالياً.": "No products in this section yet.",
    "شكراً لك": "Thank you",
    "الاسئلة و الاجابات": "FAQs",
    "اشتراك": "Subscribe",
    "أشتراك": "Subscribe",
    "تسجيل الخروج": "Sign out",
    "تحتاج مساعدة؟": "Need help?",
    "الأسئلة المتداولة": "FAQs",
    "تواصل معنا": "Contact us",
    "مرحبا": "Welcome",
    "تأكيد": "Confirm",
    "إغلاق": "Close",
    "بحث": "Search",
  };

  /* The BULK of the dictionary is generated, not written above: build/i18n.py
     emits static-export/i18n-en.js, because it is the only place that can
     read catalog.json — so all 99 product names come from the client's own
     English `name` field instead of being retyped here, and the formulaic
     families (gallery labels, governorate rows) are looped rather than listed.
     See DESIGN-NOTES for which parts of it are client copy awaiting sign-off.

     A plain script, deliberately not a fetch: translation therefore still
     works from file://, where search — the one runtime reader of
     catalog.json — does not.

     The literals above are the FLOOR and win any collision. If i18n-en.js
     fails to load, the chrome still switches languages instead of the whole
     feature dying silently. */
  const EN_TPL = {};
  (function mergeGeneratedDictionary() {
    const g = window.JAAD_I18N;
    if (!g) return;
    if (g.text) {
      Object.keys(g.text).forEach((k) => {
        if (!(k in EN)) EN[k] = g.text[k];
      });
    }
    if (g.tpl) Object.assign(EN_TPL, g.tpl);
  })();

  function currentLang() {
    return document.documentElement.getAttribute("lang") === "en" ? "en" : "ar";
  }

  /*
   * Build-time copy lives in the generated HTML, so t() cannot reach it.
   * translateDocument() is the pass that does, and it runs in three parts
   * because build-time copy shows up in three shapes.
   *
   * It used to be ONE part: walk text nodes, swap any whose exact trimmed
   * text has a dictionary entry. That left most of the site in Arabic even
   * where a translation existed, for two structural reasons rather than for
   * want of dictionary keys (Ahmed: "the language transition doesn't work in
   * every text node", 2026-07-22):
   *
   *   1. A run of copy broken by ANY inline child is several text nodes, and
   *      no fragment of it matches anything. `4.8 (126 تقييم)` is three nodes
   *      because the rating and the count are `.latin` spans, so it could
   *      never match however the dictionary was written. Same for the
   *      best-seller badge, the delivery promise, every account-menu row
   *      (icon + label), and every form label with a required marker. The
   *      TEMPLATE pass below fixes that by keying on the element with its
   *      element children replaced by {0}, {1}… — one key covers every
   *      product, price and rank, and the original child nodes are spliced
   *      back in, so `.latin` spans and their digits survive untouched.
   *
   *   2. Text in ATTRIBUTES was never looked at at all — 86 distinct Arabic
   *      placeholder/aria-label/title/alt values across the site, including
   *      every gallery thumbnail's label and every form's placeholder.
   *
   * Everything is stashed on first translation so switching back is lossless,
   * and every pass is still exact-match: a string with no entry is left in
   * Arabic rather than half-translated.
   */
  const I18N_STASH = new WeakMap(); // text node  -> original nodeValue
  const TPL_STASH = new WeakMap(); // element    -> { ar, slots }
  const ATTR_STASH = new WeakMap(); // element    -> { attr: original }

  const I18N_SKIP = { SCRIPT: 1, STYLE: 1, TITLE: 1, NOSCRIPT: 1, svg: 1 };
  const I18N_ATTRS = ["placeholder", "aria-label", "title", "alt"];
  const collapse = (s) => s.replace(/\s+/g, " ").trim();

  const inSkipped = (el) => {
    for (let n = el; n; n = n.parentElement) {
      // SVG is skipped wholesale: the icon sprites carry <title>s and stray
      // labels that must not be rewritten, and there are hundreds of them.
      // An <svg data-i18n> is the deliberate exception — the hero badge's ring
      // is real copy on a path, and without this it stayed Arabic on the
      // English build (Ahmed, 2026-08-25).
      if (I18N_SKIP[n.tagName] && !(n.tagName === "svg" && n.hasAttribute("data-i18n"))) return true;
      // Opt-out hook: an element (or any ancestor) tagged data-no-i18n is left
      // exactly as rendered. Used by the header language toggle, which must keep
      // showing the native script "العربية" even while the page reads English.
      if (n.hasAttribute && n.hasAttribute("data-no-i18n")) return true;
    }
    return false;
  };

  /* An element's content as a template: text kept verbatim, each element
     child replaced by a positional slot. Returns null unless there is BOTH
     real text and at least one slot — anything else is already covered by the
     plain text-node pass.

     The KEY is whitespace-collapsed so a dictionary entry can be written on
     one line regardless of how the generator happened to indent the markup.
     The element's own leading and trailing whitespace is kept aside and put
     back on apply, so a round trip does not quietly eat the space that
     separated this element's last word from whatever follows it.

     Whitespace BETWEEN the parts is normalised to single spaces and does not
     survive a round trip — that is the price of a collapsed key, and it is
     the right price: HTML collapses runs of whitespace in text anyway, so
     nothing moves on screen. Measured on ar -> en -> ar: textContent, element
     count and comment count all restore exactly, and index.html and cart.html
     come back byte-identical. */
  function templateOf(el) {
    let raw = "";
    const slots = [];
    let hasText = false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3) {
        raw += n.nodeValue;
        if (n.nodeValue.trim()) hasText = true;
      } else if (n.nodeType === 1) {
        raw += "{" + slots.length + "}";
        slots.push(n);
      }
      // comments contribute nothing to copy and are dropped on rebuild
    }
    if (!hasText || !slots.length) return null;
    return {
      tpl: collapse(raw),
      slots,
      lead: raw.match(/^\s*/)[0],
      tail: raw.match(/\s*$/)[0],
    };
  }

  /* Rebuild an element from a template, re-inserting the ORIGINAL child
     elements rather than clones — so a `.latin` span keeps its class, its
     digits, and any listener or state attached to it. */
  function applyTemplate(el, tpl, slots, lead, tail) {
    // Refuse to apply a translation that would drop a slot: losing a price or
    // a product image to a typo'd dictionary entry is far worse than leaving
    // the string in Arabic.
    for (let i = 0; i < slots.length; i++) {
      if (tpl.indexOf("{" + i + "}") === -1) return false;
    }
    const frag = document.createDocumentFragment();
    (lead || "") &&
      frag.appendChild(document.createTextNode(lead));
    tpl.split(/(\{\d+\})/).forEach((part) => {
      if (!part) return;
      const m = /^\{(\d+)\}$/.exec(part);
      if (m) frag.appendChild(slots[+m[1]]);
      else frag.appendChild(document.createTextNode(part));
    });
    if (tail) frag.appendChild(document.createTextNode(tail));
    el.textContent = "";
    el.appendChild(frag);
    return true;
  }

  function translateTemplates(en) {
    document.querySelectorAll("*").forEach((el) => {
      if (inSkipped(el)) return;
      const stashed = TPL_STASH.get(el);
      if (stashed) {
        // Already handled once; drive it from the stash so repeated switches
        // stay lossless and never re-key off already-translated text.
        const target = en ? EN_TPL[stashed.ar] : stashed.ar;
        if (target) {
          applyTemplate(el, target, stashed.slots, stashed.lead, stashed.tail);
        }
        return;
      }
      const t = templateOf(el);
      if (!t || !EN_TPL[t.tpl]) return;
      TPL_STASH.set(el, { ar: t.tpl, slots: t.slots, lead: t.lead, tail: t.tail });
      if (en) applyTemplate(el, EN_TPL[t.tpl], t.slots, t.lead, t.tail);
    });
  }

  function translateTextNodes(en) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        const p = node.parentElement;
        if (!p || inSkipped(p)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);

    nodes.forEach((node) => {
      const original = I18N_STASH.has(node) ? I18N_STASH.get(node) : node.nodeValue;
      const key = collapse(original);
      if (!EN[key]) return;
      if (!I18N_STASH.has(node)) I18N_STASH.set(node, original);
      if (!en) {
        node.nodeValue = original;
        return;
      }
      // Preserve the node's own leading/trailing whitespace: it is often the
      // only thing separating it from an adjacent inline element.
      const lead = original.match(/^\s*/)[0];
      const tail = original.match(/\s*$/)[0];
      node.nodeValue = lead + EN[key] + tail;
    });
  }

  /* Pre-filled DEMO values in text inputs (Ahmed, 2026-08-23).

     `value` is deliberately not in I18N_ATTRS: translating every input's value
     would rewrite whatever the shopper had typed the moment they switched
     language, which is the one thing a translator must never touch. So it is
     opt-in — only inputs the page marks `data-i18n-value` are considered, and
     the only things carrying that marker are the placeholder identities the
     demo ships with (the profile form's "محمد" / "عادل", which sat in Arabic on
     the English personal-info tab).

     Setting the ATTRIBUTE rather than the property on purpose: once a field is
     dirty — the shopper has typed in it — the attribute no longer drives what
     is displayed, so an edit in progress survives a language switch untouched. */
  function translateValues(en) {
    document.querySelectorAll("[data-i18n-value]").forEach((el) => {
      if (inSkipped(el)) return;
      let stash = ATTR_STASH.get(el);
      const cur = el.getAttribute("value");
      if (cur === null) return;
      const original = stash && "value" in stash ? stash.value : cur;
      const key = collapse(original);
      if (!EN[key]) return;
      if (!stash) {
        stash = {};
        ATTR_STASH.set(el, stash);
      }
      if (!("value" in stash)) stash.value = original;
      el.setAttribute("value", en ? EN[key] : original);
    });
  }

  function translateAttributes(en) {
    translateValues(en);
    document.querySelectorAll("[placeholder],[aria-label],[title],[alt]").forEach((el) => {
      if (inSkipped(el)) return;
      let stash = ATTR_STASH.get(el);
      I18N_ATTRS.forEach((a) => {
        const cur = el.getAttribute(a);
        if (cur === null) return;
        const original = stash && a in stash ? stash[a] : cur;
        const key = collapse(original);
        if (!EN[key]) return;
        if (!stash) {
          stash = {};
          ATTR_STASH.set(el, stash);
        }
        if (!(a in stash)) stash[a] = original;
        el.setAttribute(a, en ? EN[key] : original);
      });
    });
  }

  /* The tab title and the meta description are copy too — a page that reads
     English and titles itself in Arabic is half-switched. */
  let headStash = null;
  function translateHead(en) {
    const meta = document.querySelector('meta[name="description"]');
    if (!headStash) {
      headStash = { title: document.title, desc: meta ? meta.content : null };
    }
    const tk = collapse(headStash.title);
    document.title = en && EN[tk] ? EN[tk] : headStash.title;
    if (meta && headStash.desc !== null) {
      const dk = collapse(headStash.desc);
      meta.content = en && EN[dk] ? EN[dk] : headStash.desc;
    }
  }

  function translateDocument() {
    const en = currentLang() === "en";
    // Templates FIRST: it rebuilds child lists, which would invalidate a text
    // node list collected before it ran.
    translateTemplates(en);
    translateTextNodes(en);
    translateAttributes(en);
    translateHead(en);
  }
  function t(s) {
    return currentLang() === "en" && EN[s] ? EN[s] : s;
  }

  const LANGS = [
    { code: "en", label: "English", dir: "ltr" },
    { code: "ar", label: "العربية", dir: "rtl" },
  ];

  /*
   * Country + currency, mirroring the live site's switcher. Selecting a
   * country is DEMO state beyond the header label: every price in this build
   * is the client's real EGP figure and no AED price list exists to convert
   * to honestly — flagged in DESIGN-NOTES. `short` is what fits in the
   * masthead pill; `ar` is the full name the popup shows.
   */
  const COUNTRIES = [
    { code: "EG", currency: "EGP", ar: "مصر", short: "مصر", en: "Egypt", flag: "images/jaad/brand/flag-egypt.svg" },
    { code: "AE", currency: "AED", ar: "الامارات العربية المتحدة", short: "الامارات", en: "UAE", flag: "images/jaad/brand/flag-uae.svg" },
  ];
  const COUNTRY_KEY = "jaad:country";
  function currentCountry() {
    let code = "EG";
    try {
      code = localStorage.getItem(COUNTRY_KEY) || "EG";
    } catch (e) {
      /* ignore */
    }
    return COUNTRIES.find((c) => c.code === code) || COUNTRIES[0];
  }

  /* The masthead pill. It used to own a dropdown of languages; both the
     country and the language now live in the locale POPUP (see overlaysHTML),
     because Ahmed wants to change the two together and apply once — the
     dropdown applied each row the moment it was clicked. */
  function countryButton() {
    const c = currentCountry();
    // Rendered FROM state, never hardcoded: repaintForLang rebuilds this
    // markup after applyLang has already run, so a literal here would
    // overwrite the freshly-applied label with a stale one.
    const label = currentLang() === "ar" ? c.short + " (العربية)" : c.en + " (English)";
    // No trailing chevron: despite its name, icon-globe.svg IS a
    // chevron-down (a misnamed Figma export), and a down-chevron promises a
    // dropdown. This opens a popup now, so the pill ends at its label
    // (Ahmed, 2026-07-22).
    return `
      <button type="button" data-open="locale" class="flex items-center gap-1.5 min-h-11 px-4 py-0.5 rounded-full hover:bg-black/5 transition-colors shrink-0">
        <img src="${c.flag}" alt="" data-country-flag class="rounded-full w-4 h-4 object-cover" />
        <span class="font-semibold text-ink-800 text-base leading-[26px] whitespace-nowrap" data-lang-label>${esc(label)}</span>
      </button>`;
  }

  /* ---------------------------------------------------------------
     Header
     --------------------------------------------------------------- */
  /*
   * A nav tab. The 4px underline is the Figma "Highlight" element — it sits in
   * the layout at all times and only changes transform, so tabs never shift
   * vertically on hover or when the active page changes.
   *
   * The current page and a hovered tab are drawn DIFFERENTLY on purpose; see
   * `.nav-underline` in styles.css. Ahmed reported the navbar as looking
   * permanently hovered three times, and the cause was that the two states
   * were pixel-identical: on a category page one tab carries a solid bar
   * forever, and with nothing to distinguish it from the hover bar it simply
   * reads as stuck. Same lesson as the mega-menu column.
   */
  function desktopNavItem(item) {
    const href = pageHref(item.url);
    const isActive = currentPath() === item.url;
    /* The discount glyph renders BEFORE the label in the DOM, which in RTL
       puts it on the right-hand side of the text — where Ahmed wants it. It
       used to come after, so it sat on the left. 24px to sit level with the
       16px label rather than towering over it. */
    const markIcon = item.icon
      ? `<img src="${item.icon}" alt="" class="shrink-0 w-6 h-6" />`
      : "";

    /* This column must sum to EXACTLY the bar's 48px: pt-3 (12) + label h-6
       (24) + gap-2 (8) + underline h-1 (4). It used to be pt-3.5 + gap-3 =
       54px, and because the ul's overflow-x-auto forces overflow-y to
       compute to auto as well, the last 6px were CLIPPED — the underline
       (hover and current-page alike) was being painted 2px below the visible
       bar on every page. Ahmed reported the hover states as simply not
       working; they worked, invisibly. If the bar height or any of these
       four numbers changes, re-do this sum. */
    const label = `
      <a href="${href}" class="flex flex-col gap-2 pt-3 shrink-0 group">
        <span class="flex items-center gap-1.5 h-6">
          ${markIcon}
          <span class="font-semibold text-white/90 group-hover:text-white text-base leading-6 whitespace-nowrap transition-colors duration-200">${esc(t(item.name))}</span>
        </span>
        <span class="nav-underline h-1 w-full rounded-full origin-center${isActive ? " is-current" : ""}"></span>
      </a>`;

    // Every nav tab is now a PLAIN LINK to its category page — the per-tab
    // hover dropdown was removed at Ahmed's request (2026-08-05). The big
    // "المنتجات" mega-panel (data-megamenu-toggle) already lists every main
    // category AND its sub-categories in one place, so a second per-tab
    // dropdown repeating the same sub-categories was redundant. `item.children`
    // is still consumed by megaPanelHTML and CHILD_TO_PARENT; it is
    // intentionally ignored here so a tab is only ever a route to its category.
    return `<li class="flex items-center gap-2.5 shrink-0">${label}</li>`;
  }

  /*
   * Products mega-panel (desktop) — the full-width dropdown under المنتجات.
   *
   * REDESIGN (Ahmed, 2026-08-03). The old three-column layout (categories →
   * sub-categories → a product rail, RTL) forced the pointer to travel almost
   * the full panel width to reach anything, and because categories switch on
   * hover, any vertical drift on that journey crossed a sibling row and swapped
   * the whole panel out from under the cursor — the "I have to travel to the
   * left to choose" complaint.
   *
   * It is a RAIL + STAGE. The rail (RTL start / right) is one LINK per category,
   * each carrying its own photo. Hovering a row opens that category's tiles in
   * the stage beside it; clicking the row shops the whole category in one hit,
   * so the commonest goal needs no reach at all. initMegaMenu adds the
   * hover-intent that makes crossing rows safe.
   *
   * PART 2 (same day). Two changes that finish off the reach:
   *   - The branded photo used to sit on the FAR side of the stage — the very
   *     end of the reach. It is now a COMPACT PROMO card docked UNDER the rail,
   *     so the stage is sub-category tiles alone, sitting immediately beside the
   *     rail (shortest possible move).
   *   - The visible card is capped (~980) and hugged to the start edge with
   *     me-auto, instead of spanning the full 1536 container, so it opens BESIDE
   *     the categories rather than stretching the tiles across the whole width.
   *     The full-bleed #mega-panel stays (sticky nav untouched) but is now a
   *     pointer-transparent positioning layer only.
   * Phones are untouched — the drawer is still the right control there.
   */
  function megaPanelHTML() {
    // RAIL — one link per category, carrying its photo. The row is a real <a>
    // to the category page: hover/focus opens its preview (initMegaMenu), a
    // click shops the whole category with no reach into the stage. Selected and
    // hover stay DIFFERENT treatments (styles.css, rule 8): selected = brand
    // bar + ink + a ring on the thumb; hover = a faint transient wash.
    const rail = MAIN_MENU.map((item, i) => {
      const thumb = item.image
        ? `<img src="${item.image}" alt="" class="w-full h-full object-cover" loading="lazy" decoding="async" />`
        : `<span class="grid place-items-center w-full h-full text-primary-300"><span class="w-5 h-5">${ICON.arrowRight}</span></span>`;
      return `<li>
        <a href="${pageHref(item.url)}" data-mega-cat="${i}" data-active="${i === 0}"
           class="mega-cat flex items-center gap-3 ps-2 pe-3 py-2 rounded-2xl w-full min-h-[60px] text-start">
          <span class="mega-cat__thumb place-items-center grid bg-cream rounded-xl w-12 h-12 overflow-hidden shrink-0">${thumb}</span>
          <span class="flex-1 min-w-0 font-semibold text-ink text-[15px] leading-tight truncate">${esc(t(item.name))}</span>
          <span class="mega-cat__arrow place-items-center grid w-5 h-5 text-primary rtl:scale-flip shrink-0">${ICON.arrowRight}</span>
        </a>
      </li>`;
    }).join("");

    // PROMO — the resized category "widget", docked UNDER the sub-category tiles
    // (Ahmed, 2026-08-03 part 2). It lives INSIDE each stage, so it shows and
    // hides with the stage it belongs to — no separate toggling.
    //
    // The photo sits in a SQUARE frame, not a wide banner. Every category shot
    // is a square 600×600 bowl; a wide banner cropped them to a thin strip and
    // cut the bowl off — worst for the many-sub-category rows (nuts, coffee),
    // whose tiles left the banner shortest. A square frame shows the whole shot
    // for every category (square source into a square box never crops). Text and
    // CTA sit beside it. It links to the whole category (same target as the rail
    // row); the photo reinforces which category the pointer has settled on.
    const promoCard = (item) => {
      const name = esc(t(item.name));
      return `
        <a href="${pageHref(item.url)}" class="group/promo flex items-center gap-4 tile-lift mt-4 p-3 bg-cream rounded-2xl overflow-hidden">
          <span class="flex flex-col flex-1 gap-1.5 min-w-0 ps-3">
            <span class="block font-bold text-ink text-xl leading-tight">${name}</span>
            <span class="text-muted text-[13px] leading-snug">${esc(t("اكتشف تشكيلة"))} ${name} ${esc(t("كاملة من جاد."))}</span>
            <span class="inline-flex items-center gap-1.5 mt-1 font-semibold text-ink-800 text-sm">
              ${esc(t("تسوّق الكل"))}
              <span class="w-4 h-4 rtl:scale-flip">${ICON.arrowRight}</span>
            </span>
          </span>
          <span class="block shrink-0 w-40 aspect-square rounded-xl overflow-hidden">
            <img src="${item.image}" alt="" class="w-full h-full object-cover" loading="lazy" decoding="async" />
          </span>
        </a>`;
    };

    // STAGE — sub-category tiles, then the promo beneath them. With the photo
    // gone from the far side, the tiles sit immediately beside the rail and the
    // pointer no longer crosses a wide panel to reach them. Categories with no
    // sub-categories get a single prominent "shop all" tile above the promo so
    // the stage is never empty.
    const stages = MAIN_MENU.map((item, i) => {
      const href = pageHref(item.url);
      const name = esc(t(item.name));
      const kids = item.children || [];
      const shown = i === 0 ? "" : "hidden";

      // No sub-categories: the promo banner IS the whole stage — its "تسوّق
      // الكل" is the shop-everything action, so no separate tile is needed.
      if (!kids.length) {
        return `<div data-mega-sub="${i}" ${shown} class="flex flex-col flex-1 mega-stage">
          ${promoCard(item)}
        </div>`;
      }

      // No truncate: two lines fit inside the 52px tile, so a long name wraps
      // and stays whole rather than losing its tail.
      const tiles = kids.map((c) => `<a href="${pageHref(c.url)}" class="mega-tile group/tile flex justify-between items-center gap-2 px-4 py-2 rounded-xl min-h-[52px] text-ink">
            <span class="min-w-0 leading-tight">${esc(t(c.name))}</span>
            <span class="w-4 h-4 text-muted rtl:scale-flip shrink-0 mega-tile__arrow">${ICON.arrowRight}</span>
          </a>`).join("");

      return `<div data-mega-sub="${i}" ${shown} class="flex flex-col flex-1 mega-stage">
        <!-- No uppercase/tracking: both are Latin-centric and letter-spacing
             breaks Arabic's cursive joining. -->
        <h3 class="mb-3 font-bold text-muted text-[13px]">تصفّح ${name}</h3>
        <div class="content-start gap-2 grid grid-cols-2">${tiles}</div>
        ${promoCard(item)}
      </div>`;
    }).join("");

    return `
      <!-- The panel stays full-bleed (start-0 end-0) so the sticky nav is
           untouched, but it is now a POINTER-TRANSPARENT layer: the visible
           card is capped and hugged to the start edge with me-auto, so it opens
           beside the categories instead of spanning the whole 1536 container.
           The cap is deliberately tight (800) — the tiles then sit right next to
           the rail, so choosing a sub-category is a short move, not a trek to
           the far edge.
           start-0 end-0, NOT inset-inline-0: the latter is not a real Tailwind
           class and compiled to nothing. -->
      <div id="mega-panel" data-megamenu hidden class="hidden lg:block top-full start-0 end-0 z-40 absolute pointer-events-none">
        <div class="mx-auto px-4 max-w-[1536px]">
          <!-- Rail is a fixed 300; the stage (tiles + promo) takes the rest, up
               to the 800 cap, so the tiles stay right beside the rail. -->
          <div class="pointer-events-auto gap-6 grid grid-cols-[300px_minmax(0,1fr)] bg-white shadow-custom3 p-5 rounded-b-2xl max-w-[800px] me-auto">
            <ul data-mega-rail class="flex flex-col gap-0.5 pe-5 border-divider border-e">${rail}</ul>
            <div data-mega-stages class="relative flex flex-col min-w-0">${stages}</div>
          </div>
        </div>
      </div>`;
  }

  function headerHTML() {
    const checkout = isCheckout();

    /* --- flash-sale promo -------------------------------------------------
       Relocated INTO the utility bar (Ahmed, 2026-08-25). It used to be the
       header's own topmost band, which made the masthead three stacked bars
       before the page had said anything. The promo is not worth a third of the
       header, so it now rides in the utility bar's start slot — the space the
       "100% Natural Based Products" line held, which was a claim nobody came
       here to read.

       Contents are deliberately down to three things: the icon, the words, the
       clock. The discount pill, the "ends in" phrase, and the "shop now" link
       with its chevron are all gone — at utility-bar scale they turned a glance
       into a paragraph. The whole thing is still an <a> to the sale, so the
       click target the chevron used to advertise survives without it.

       Units render inline rather than stacked over their labels: the bar is
       ~30px tall and the old two-line unit needed 33px on its own. Labels drop
       below lg, where the support nav and the promo start competing for width;
       the digits and colons still read as a clock without them. */
    const flashUnit = (key, label) =>
      `<span class="inline-flex items-baseline gap-1">
         <span class="font-bold tabular-nums latin" data-flash="${key}">00</span>
         <span class="hidden lg:inline text-[10px] uppercase">${esc(t(label))}</span>
       </span>`;
    /* No opacity dimming on the label or the separator. The obvious way to
       recess them is opacity-70 / opacity-40, but the promo's ink is already a
       dark green on a light bar, and knocking it back that far put the colon at
       1.8:1 — a fail that the earlier sweeps could not have caught, since it
       arrived with this markup. Hierarchy comes from weight and size instead:
       bold tabular digits against 10px uppercase labels, all at full ink. */
    const flashSep = `<span class="font-bold">:</span>`;
    /* text-heading rather than a literal colour: the bar is cream in v1 and
       lime in v2/v3, and the existing `.bg-limeFigma .text-heading` rule plus
       the v3 override already resolve an AA-passing ink for each ground. */
    const promo = checkout
      ? ""
      : `<a href="${pageHref("/shop")}" data-flash-sale
             class="flex items-center gap-2 min-w-0 text-heading text-xs whitespace-nowrap hover:opacity-70 transition-opacity">
           <img src="images/jaad/icons/flash-sale.png" alt="" class="w-[18px] h-[18px] object-contain shrink-0" />
           <span class="font-bold uppercase tracking-[0.5px]">${esc(t("عروض فلاش"))}</span>
           <span class="flex items-center gap-1.5">
             ${flashUnit("days", "يوم")}${flashSep}${flashUnit("hours", "ساعة")}${flashSep}${flashUnit("mins", "دقيقة")}
           </span>
         </a>`;
    /* Phones carry no utility bar, so the promo would disappear with the band
       it used to live in. It keeps its own slim strip there instead — same
       three elements, so the two never drift apart. */
    const promoBand = checkout
      ? ""
      : `<div class="md:hidden flex justify-center bg-limeFigma px-4 py-1.5">${promo}</div>`;

    /* --- support (utility) menu --- */
    const support = SUPPORT_MENU.map(
      (i) =>
        `<a href="${pageHref(i.url)}" class="font-medium text-black hover:text-heading text-sm uppercase whitespace-nowrap transition-colors">${esc(t(i.title))}</a>`,
    ).join("");

    /* --- desktop primary nav --- */
    const nav = MAIN_MENU.map(desktopNavItem).join("");
    // Figma header (node 4995:5998): plain COFFEE / SPICES / NUTS tabs, white
    // bold, straight to each category — no mega panel.
    const navTabs = MAIN_MENU.map(
      (i) =>
        `<a href="${pageHref(i.url)}" class="font-bold text-white hover:text-[#ACD574] text-lg uppercase whitespace-nowrap transition-colors">${esc(t(i.name))}</a>`,
    ).join("");

    const desktop = `
      <div class="hidden md:block">
        ${
          checkout
            ? ""
            : `<div data-utility-bar class="bg-limeFigma">
                 <div class="flex justify-between items-center gap-6 mx-auto px-4 xl:px-[60px] py-1.5 max-w-[1512px]">
                   ${promo}
                   <nav class="flex items-center gap-4 xl:gap-6 min-w-0 overflow-hidden">
                     ${support}
                     <button type="button" data-lang-toggle data-no-i18n class="shrink-0 font-medium text-heading text-sm underline whitespace-nowrap">${currentLang() === "ar" ? "English" : "العربية"}</button>
                   </nav>
                 </div>
               </div>`
        }
        <div data-navbar class="relative z-40 bg-heading">
          <div class="flex ${checkout ? "justify-center" : "items-center justify-between"} gap-4 mx-auto px-4 xl:px-[60px] h-[56px] max-w-[1512px]">
            ${
              checkout
                ? ""
                : `<nav class="hidden lg:flex flex-1 items-center gap-6 xl:gap-8 min-w-0">${navTabs}</nav>`
            }
            <!-- Logo is much taller than the 56px bar on purpose (Figma): it
                 overflows well above and below. z-10 keeps it above the bands. -->
            <a href="index.html" class="masthead-logo relative z-10 block shrink-0" aria-label="Jaad">
              <img src="images/jaad/brand/logo-jaad-full.svg" alt="Jaad" class="w-auto h-[96px] xl:h-[116px] object-contain" />
            </a>
            ${
              checkout
                ? ""
                : `<div class="flex flex-1 justify-end items-center gap-5 xl:gap-8">
                     <a href="login.html" data-account-link data-fav-target aria-label="${esc(t("الحساب"))}" class="hover:opacity-80 transition-opacity">
                       <img src="images/jaad/icons/hdr-user.svg" alt="" class="w-6 h-6" />
                     </a>
                     <!-- Only the CART rides along on scroll (Ahmed, 2026-08-19):
                          search stays in the masthead and scrolls away with it, so
                          it is NOT inside [data-sticky-actions] and the parked pill
                          is cart-only. -->
                     <button type="button" data-open="search" aria-label="${esc(t("بحث"))}" class="place-items-center grid hover:opacity-80 rounded-full size-11 transition-opacity">
                       <img src="images/jaad/icons/hdr-search.svg" alt="" class="w-6 h-6" />
                     </button>
                     <div data-sticky-actions class="flex items-center gap-5 xl:gap-6">
                       <button type="button" data-open="cart" aria-label="${esc(t("السلة"))}" class="relative place-items-center grid bg-white shadow-custom4 rounded-full size-11">
                         <span class="w-6 h-6 text-ink">${ICON.cart}</span>
                         <span class="-top-1 -end-1 absolute place-items-center grid bg-[#ACD574] px-1 rounded-full min-w-[20px] h-5 font-semibold text-ink-800 text-xs latin" data-cart-count>2</span>
                       </button>
                     </div>
                   </div>`
            }
          </div>
        </div>
      </div>`;

    /* --- mobile header (refined against the Figma Mobile page later) --- */
    const mobile = `
      <div class="md:hidden block">
        <!-- Both side groups are flex-1, so the logo sits dead-centre no
             matter how many controls each side holds — matching the live
             site's mx-auto logo without a transform, which keeps it RTL-safe.
             min-w-0 because a flex-1 child otherwise cannot shrink below its
             content (the most common bug class in this codebase).
             Live packs these at 36x36; ours stay 44x44 for WCAG 2.5.5, which
             is the project's standing accessibility deviation. -->
        <div class="relative flex items-center ${checkout ? "justify-center" : "justify-between"} gap-2 bg-primary px-4 py-2 text-white">
          ${
            checkout
              ? ""
              : `<div class="flex flex-1 items-center gap-1 min-w-0">
                   <button type="button" data-open="menu" class="place-items-center grid shrink-0 size-11 -ms-2" aria-label="Menu"><span class="w-6 h-6">${ICON.menu}</span></button>
                 </div>`
          }
          <a href="index.html" class="block shrink-0"><img src="images/jaad/brand/logo-jaad.svg" alt="جاد" class="w-auto h-[40px] object-contain" /></a>
          ${
            checkout
              ? ""
              : `<!-- Same data-sticky-actions hook as the desktop masthead, so one
                       scroll handler drives both and they can never disagree about
                       whether the page has scrolled. The mobile masthead scrolls
                       away completely - there is no sticky nav at this width - so
                       without this, search and cart leave the screen entirely and
                       the only way back to the cart is to scroll to the top. It
                       also gives the fly-to-cart flight a real on-screen target on
                       mobile instead of the clamp-to-edge fallback. Parked and
                       painted by the max-width rule in styles.css. -->
                 <div class="flex flex-1 justify-end items-center gap-1 min-w-0">
                   <button type="button" data-open="search" class="place-items-center grid shrink-0 size-11" aria-label="بحث">
                     <img src="images/jaad/icons/hdr-search.svg" alt="" class="w-5 h-5" />
                   </button>
                   <div data-sticky-actions class="flex items-center">
                   <button type="button" data-open="cart" class="relative place-items-center grid bg-cta shrink-0 rounded-full text-white size-11" aria-label="السلة">
                     <span class="w-7 h-7" data-cart-glyph>${ICON.cart}</span>
                     <!-- Yellow chip ringed in the masthead green, matching the
                          desktop badge so the two mastheads never disagree. -->
                     <span class="-top-1 -end-1 absolute place-items-center grid bg-lime ring-2 ring-primary rounded-full w-5 h-5 font-bold text-[10px] text-ink-800 latin" data-cart-count>2</span>
                   </button>
                   </div>
                 </div>`
          }
        </div>
      </div>
      ${
        checkout
          ? ""
          : `<!-- No utility strip on mobile (Ahmed, 2026-08-20). One briefly
                  lived here mirroring the desktop lime bar, but it added a
                  fourth stacked band to a phone masthead that already carries
                  the flash bar, the masthead and the delivery row. Our Story /
                  Media / FAQs / Contact Us live in the drawer instead, where
                  they now render at full row weight, and the language control
                  stays reachable via the drawer's sticky country button. -->
             <div class="md:hidden block bg-cream px-4 py-2">
               <button type="button" data-open="location" class="flex justify-between items-center gap-1 bg-cta px-5 py-2.5 rounded-full w-full min-h-11 text-white">
                 <span class="font-semibold text-xs truncate">التوصيل الى الشروق - القاهرة</span>
                 <span class="shrink-0 w-4 h-4 chevron">${ICON.chevronDown}</span>
               </button>
             </div>`
      }`;

    return `<header>${desktop}${promoBand}${mobile}</header>`;
  }

  /* ---------------------------------------------------------------
     Footer
     --------------------------------------------------------------- */
  /*
   * Payment marks, shared by the footer bar and the checkout summary.
   * Sizes are explicit px rather than percentages: these sit inside centred
   * flex/grid boxes where a percentage height resolves against the wrong
   * containing block and distorts the mark.
   */
  function paymentMarks(size) {
    const sm = size === "sm";
    const card = sm ? "w-[23px] h-4" : "w-[35px] h-6";
    const radius = sm ? "rounded-sm" : "rounded";
    const glyphW = sm ? 15 : 22;
    const glyphH = sm ? 9 : 14;
    const cod = sm ? "w-[41px] h-4" : "w-[61px] h-6";
    return `
      <div class="flex items-center gap-1 md:gap-2">
        <!-- Etisalat Cash ships as white artwork on its own opaque black
             plate, so it gets no white chip — it would read as a black box. -->
        <img src="images/jaad/payments/pay-etisalat-cash.png" alt="اتصالات كاش" class="${card} ${radius} object-cover shrink-0" />
        <span class="inline-flex justify-center items-center bg-white border border-divider ${card} ${radius} shrink-0">
          <img src="images/jaad/payments/pay-mastercard-alt.svg" alt="Mastercard" style="width:${glyphW}px;height:${glyphH}px" />
        </span>
        <img src="images/jaad/payments/pay-visa.svg" alt="Visa" class="${card} ${radius} shrink-0" />
        <img src="images/jaad/payments/pay-cod.png" alt="الدفع عند الاستلام" class="${cod} object-contain shrink-0" />
      </div>`;
  }

  function footerHTML() {
    const copyright = `جميع حقوق النشر تنتمي إلى جاد, <span class="latin">${YEAR}</span>`;

    if (isCheckout()) {
      return `<footer class="bg-black py-6">
        <div class="mx-auto px-4 max-w-[1392px] text-onBlack text-xs text-center">${copyright}</div>
      </footer>`;
    }

    /* Phone and email sit under SUPPORT, not under the logo (Ahmed,
       2026-08-24). Two reasons, and the second is the one that shows: getting
       in touch is support, so that is the column a shopper scans for it — and
       with the contact rows stacked under the brand block that column ran far
       taller than the three beside it, which is what made the footer look
       lopsided. Moving them evens the columns and puts them where they belong.

       Rendered as a block appended INSIDE the Support column rather than as a
       fourth column, so it inherits the column's heading rhythm and the mobile
       accordion keeps working unchanged. */
    const contact = `
      <div class="flex flex-col gap-2.5 mt-2 pt-4 border-t border-white/10">
        <a href="tel:${CONTACT.hotline}" class="group flex items-center gap-2.5 text-white hover:text-lime text-sm transition-colors">
          <span class="place-items-center grid bg-white/10 group-hover:bg-white/15 rounded-full size-8 shrink-0 transition-colors">
            <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><path d="M6.5 3h3l1.5 4-2 1.5a12 12 0 0 0 6.5 6.5l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.2 2 2 0 0 1 6.5 3Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
          </span>
          <span class="latin">${CONTACT.hotline}</span>
        </a>
        <a href="mailto:${CONTACT.email}" class="group flex items-center gap-2.5 text-white hover:text-lime text-sm transition-colors">
          <span class="place-items-center grid bg-white/10 group-hover:bg-white/15 rounded-full size-8 shrink-0 transition-colors">
            <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.7"/><path d="m3.5 7.5 7.9 5.3a1 1 0 0 0 1.2 0l7.9-5.3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
          </span>
          <span class="latin">${CONTACT.email}</span>
        </a>
      </div>`;

    // `contact` is appended to the LAST column so the phone and email land
    // under Support. It has to be defined ABOVE this: .map() runs immediately,
    // so the template literal is evaluated here and not later.
    const columns = FOOTER_COLUMNS.map(
      (col, ci) => `
      <div class="flex flex-col gap-6 min-w-[142px]">
        <h2 class="font-normal text-white text-lg leading-tight">${esc(t(col.name))}</h2>
        <ul class="flex flex-col gap-2">
          ${col.links
            .map(
              (l) =>
                `<li><a href="${pageHref(l.url)}" class="font-normal text-white hover:text-lime text-base transition-colors whitespace-nowrap">${esc(t(l.title))}</a></li>`,
            )
            .join("")}
        </ul>
        ${ci === FOOTER_COLUMNS.length - 1 ? contact : ""}
      </div>`,
    ).join("");

    /* Mobile-only accordion (Ahmed, 2026-08-03): below md the 3 groups above
       become 3 full-width collapsible rows with a chevron, all closed by
       default — the whole point of an accordion on a phone is the vertical
       space it gives back versus every link printed at once. Reuses the
       SAME .accordion-item/.accordion-trigger/.accordion-chevron/
       .accordion-panel contract the FAQ page and product page already use
       (styles.css owns the open/close transition and the chevron rotation,
       initAccordions() in this file wires the click), rather than a second
       accordion implementation. data-accordion-multi so a shopper can have
       more than one group open — nothing here makes them mutually exclusive.
       The chevron SVG is inlined because this file's own ICON object has no
       chevron entry (that one lives only in build/components.py's
       build-time ICON dict). Border is white/10, not the light-grey
       neutral-divider the same component uses on white cards elsewhere —
       that grey barely shows against this footer's dark green. */
    const columnsMobile = `
      <div data-accordion data-accordion-multi class="md:hidden flex flex-col">
        ${FOOTER_COLUMNS.map(
          (col) => `
        <div class="accordion-item border-white/10 border-b">
          <button type="button" class="accordion-trigger flex justify-between items-center gap-4 py-4 w-full text-start">
            <span class="font-bold text-white text-base leading-[22px]">${esc(t(col.name))}</span>
            <span class="accordion-chevron text-white shrink-0"><svg viewBox="0 0 24 24" fill="none" class="w-5 h-5"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          </button>
          <div class="accordion-panel">
            <ul class="flex flex-col gap-2 pb-4">
              ${col.links
                .map(
                  (l) =>
                    `<li><a href="${pageHref(l.url)}" class="font-normal text-white hover:text-lime text-base leading-6 transition-colors">${esc(t(l.title))}</a></li>`,
                )
                .join("")}
            </ul>
          </div>
        </div>`,
        ).join("")}
        <!-- Outside the accordion on purpose: a phone number a shopper has to
             open a collapsed panel to find is a phone number they do not find.
             The desktop layout can afford to nest it under Support because the
             column is open; on a phone the panel is closed by default. -->
        ${contact}
      </div>`;

    const socials = SOCIALS.map(
      (s) =>
        `<li><a href="${s.href}" target="_blank" rel="noopener noreferrer" aria-label="${esc(s.title)}" class="block opacity-90 hover:opacity-100 transition-opacity">
           <img src="${s.icon}" alt="" class="w-6 h-6" />
         </a></li>`,
    ).join("");

    /* The newsletter, as a BAND across the top of the footer.
       
       It used to be a saturated orange card floating in the right-hand column,
       with a blue-and-purple envelope inside it. Both came from the fork: the
       orange is the one place on the site that colour appears at that size, and
       against the deep green it read as a panel belonging to a different site
       that had been pasted in. As a full-width band in the footer's own greens
       it introduces the footer instead of interrupting it, and the form gets
       the room to be a real target rather than a squeezed pill.
       Keeps the [data-newsletter] hook, so subscribing still toasts. */
    const newsletter = `
      <div class="flex md:flex-row flex-col md:items-center gap-6 bg-white/[0.06] p-6 xl:p-8 border border-white/10 rounded-[20px]">
        <img src="images/jaad/icons/newsletter-3d.png" alt="" aria-hidden="true"
             class="w-16 xl:w-20 h-auto shrink-0" />
        <div class="flex flex-col gap-1 min-w-0 md:flex-1">
          <p class="font-medium text-white text-lg xl:text-xl leading-snug">${esc(t("اشترك واعرف كل جديد وعروضنا الحصرية"))}</p>
          <p class="text-white/60 text-sm">${esc(t("كن أول من يعرف كل ما هو جديد في جاد"))}</p>
        </div>
        <form data-newsletter class="flex items-center gap-2 bg-white ps-4 pe-2 py-2 rounded-full w-full md:w-auto md:min-w-[380px] shrink-0">
          <input type="email" required aria-label="${esc(t("البريد الالكتروني"))}" placeholder="${esc(t("أدخل عنوان البريد الالكتروني"))}"
                 class="flex-1 bg-transparent outline-none min-w-0 text-ink text-sm placeholder:text-muted" />
          <button type="submit" class="bg-heading hover:bg-[#1f4a24] px-6 min-h-10 rounded-full font-semibold text-white text-sm whitespace-nowrap transition-colors">${esc(t("اشتراك"))}</button>
        </form>
      </div>`;

    /* The brand column. The logo, what JAAD is, how to reach it and where to
       follow it, in one block — rather than the logo alone on the left with the
       phone and email floated to the far right of the same row, which is where
       they were and which read as a header, not a footer.

       The contact rows are LABELLED and carry their own glyph. Unlabelled
       digits in the corner of a dark band are not a phone number anyone finds
       when they need one. */
    const brand = `
      <div class="flex flex-col gap-5 md:max-w-[300px]">
        <img src="images/jaad/brand/logo-jaad-mark.svg" alt="جاد" class="w-[72px] xl:w-[84px] h-auto" />
        <p class="text-white/70 text-sm leading-relaxed">${esc(t("قهوة ومكسرات وبهارات طبيعية، مصدرها الأصلي في قلب كل منتج."))}</p>
        <ul class="flex items-center gap-3">${socials}</ul>
      </div>`;


    /* Scattered leaves — the third leaf field (with Our Story + Reviews). They
       drift with the cursor via initLeafWind, same as the page-body leaves.
       Visible at every width so the leaves-on-scroll wind runs on phones too;
       the inline max-width in vw caps the fixed px widths below md, and at
       >=768px 9vw always exceeds the largest leaf, so desktop is unaffected. */
    const footerLeaves = [
      ["leaf-1.svg", "6%", "1%", "w-12", 20],
      ["leaf-3.svg", "70%", "2%", "w-16", -150],
      ["leaf-2.svg", "2%", "92%", "w-12", -70],
      ["leaf-4.svg", "74%", "88%", "w-11", 55],
      ["leaf-5.svg", "42%", "3%", "w-8", -95],
      ["leaf-2.svg", "8%", "47%", "w-9", 30],
    ]
      .map(
        (l) =>
          `<img src="images/jaad/decor/${l[0]}" alt="" aria-hidden="true" data-leaf class="leaf-wind block absolute ${l[3]} h-auto opacity-90 brightness-150 pointer-events-none z-0" style="top:${l[1]};left:${l[2]};--lr:${l[4]}deg;max-width:9vw" />`,
      )
      .join("");

    return `<footer class="relative bg-greenDeepest overflow-hidden">
      <div class="relative flex flex-col gap-10 xl:gap-12 mx-auto px-4 xl:px-[60px] pt-12 xl:pt-[60px] pb-6 max-w-[1512px]">
        ${footerLeaves}
        ${newsletter}

        <!-- Brand block, then the link columns. A 4-track grid from md, the
             brand track wider than the three link tracks: the columns used to be
             three narrow min-w-[142px] boxes crowded against the inline start
             with a large dead gap after them. -->
        <div class="gap-10 xl:gap-12 grid md:grid-cols-[1.4fr_repeat(3,1fr)]">
          ${brand}
          <div class="hidden md:contents">${columns}</div>
        </div>
        ${columnsMobile}

        <!-- Bottom bar. The rule is what separates the legal line from the
             footer proper; before, the copyright simply floated under the
             payment marks. -->
        <div class="flex flex-wrap justify-between items-center gap-4 pt-6 border-t border-white/10">
          ${paymentMarks("sm")}
          <p class="text-white/50 text-xs text-end">© JAAD <span class="latin">${YEAR}</span> · ${esc(t("جميع الحقوق محفوظة"))}</p>
        </div>
      </div>
    </footer>`;
  }

  const YEAR = 2026; // static build stamp (Date.now avoided for determinism)

  /* ---------------------------------------------------------------
     Overlays: backdrop, cart drawer, mobile menu, search, location
     --------------------------------------------------------------- */
  function overlaysHTML() {
    const menuLinks = MAIN_MENU.map(
      (i) => `
      <li class="border-b border-neutral-100">
        <a href="${pageHref(i.url)}" class="flex items-center justify-between min-h-11 py-3.5 text-textSecondary font-medium">${esc(t(i.name))}${i.children ? `<span class="w-4 h-4 text-muted">${ICON.arrowRight}</span>` : ""}</a>
      </li>`,
    ).join("");
    // Same weight and tap target as the category rows above them (Ahmed,
    // 2026-08-20). These were `text-muted text-sm` with no divider — secondary
    // styling for what is, on a phone, the ONLY way to reach Our Story, the
    // blog, FAQs and Contact Us. They read as fine print and got missed.
    const supportLinks = SUPPORT_MENU.map(
      (i) =>
        `<li class="border-b border-neutral-100 last:border-0"><a href="${pageHref(i.url)}" class="flex items-center justify-between min-h-11 py-3.5 text-textSecondary font-medium">${esc(t(i.title))}<span class="w-4 h-4 text-muted">${ICON.arrowRight}</span></a></li>`,
    ).join("");

    /* Seed contents for a first-ever visit, so the drawer and cart page are
       not empty on a fresh browser. Real catalogue items. Once the shopper
       touches the cart this is never consulted again — Cart owns state. */
    /* (kept in CART_SEED at module scope) */

    /* "You may also like" upsell — real JAAD catalogue items.
     *
     * Each row is a `[data-product]` host carrying the real catalogue id,
     * name, price and image, because `productFrom()` walks up to the nearest
     * `[data-product]` and bails when there isn't one — without it the add
     * button would have no product behind it and silently do nothing.
     *
     * Seven impulse-priced picks (EGP 30–65) spanning spices and coffee, each
     * copied from data/catalog.json with its styled product shot. Literals
     * here because the drawer is built at boot and scripts.js has no
     * build-time access to the catalogue; if these drift from catalog.json,
     * the prices on the card are what goes stale. */
    const upsell = [
      { id: "16", name: "Coriander",     price: 30, img: "images/jaad/products-styled/16.jpg" },
      { id: "13", name: "Chili Peppers", price: 35, img: "images/jaad/products-styled/13.jpg" },
      { id: "14", name: "Turmeric",      price: 35, img: "images/jaad/products-styled/14.jpg" },
      { id: "23", name: "Cumin",         price: 35, img: "images/jaad/products-styled/23.jpg" },
      { id: "17", name: "Nutmeg",        price: 40, img: "images/jaad/products-styled/17.jpg" },
      { id: "21", name: "Cardamom",      price: 55, img: "images/jaad/products-styled/21.jpg" },
      { id: "7",  name: "Espresso",      price: 65, img: "images/jaad/products-styled/7.jpg" },
    ]
      // ONE card design across the whole site (Ahmed, 2026-08-17): the drawer
      // upsell now renders the canonical product card (recentCardHTML, which
      // mirrors components.product_widget / Figma 9946:16778) instead of the
      // old forked mini-card — same bordered square shot, green sticker price
      // badge with the lime offset shadow, and orange cart→stepper button as
      // Perfect Picks and Recently Viewed. The array carries `img`;
      // recentCardHTML wants `image`.
      .map((p) =>
        recentCardHTML({ id: p.id, name: p.name, price: p.price, image: p.img }, true),
      )
      .join("");

    /* Static shell only — the numbers and disabled state are filled in by
       renderCart() on every cart:change. */
    const cartFooter = `
        <!-- Free-delivery progress. renderCart fills the bar toward FREE_SHIP
             and flips the copy to the success line once earned; hidden on an
             empty basket. -->
        <!-- Free-delivery progress: the "add X more" caption sits ABOVE the bar
             (Ahmed, 2026-08-04). The discount rows that used to sit directly
             UNDER the bar were moved down into the totals group, so nothing
             clutters right below the bar. -->
        <div data-freeship hidden class="flex flex-col gap-1.5">
          <p class="text-ink text-xs leading-5" data-freeship-msg></p>
          <div class="bg-cream rounded-full w-full h-2 overflow-hidden">
            <div data-freeship-fill class="bg-limeFigma rounded-full h-full transition-[width] duration-500" style="width:0%"></div>
          </div>
        </div>
        <!-- Promo code — same [data-promo*] contract as the cart-page field, so
             renderCart's syncPromoUI keeps the drawer and the page in step and a
             code applied here drops the total below. The handlers scope to the
             clicked [data-promo], so the two fields never cross wires. -->
        <div data-promo class="flex flex-col gap-2 py-1 border-divider border-y">
          <button type="button" data-promo-open class="flex items-center gap-2 self-start min-h-11 font-semibold text-cta text-sm underline">
            <span class="inline-flex w-[18px] h-[18px] shrink-0" aria-hidden="true"><svg viewBox="0 0 25.2 25.2" fill="currentColor" class="w-full h-full"><path fill-rule="evenodd" clip-rule="evenodd" d="M14.5799 0.820101C13.4864 -0.273367 11.7136 -0.273367 10.6201 0.820101L9.87077 1.56943C9.08312 2.35708 8.01483 2.79958 6.90092 2.79958H5.6C4.0536 2.79958 2.8 4.05318 2.8 5.59958V6.9005C2.8 8.01441 2.3575 9.0827 1.56985 9.87035L0.8201 10.6201C-0.273368 11.7136 -0.273366 13.4864 0.820102 14.5799L1.56985 15.3296C2.3575 16.1173 2.8 17.1856 2.8 18.2995V19.5996C2.8 21.146 4.0536 22.3996 5.6 22.3996H6.90008C8.01399 22.3996 9.08228 22.8421 9.86993 23.6297L10.6201 24.3799C11.7136 25.4734 13.4864 25.4734 14.5799 24.3799L15.3301 23.6297C16.1177 22.8421 17.186 22.3996 18.2999 22.3996H19.6C21.1464 22.3996 22.4 21.146 22.4 19.5996V18.2995C22.4 17.1856 22.8425 16.1173 23.6301 15.3296L24.3799 14.5799C25.4734 13.4864 25.4734 11.7136 24.3799 10.6201L23.6301 9.87035C22.8425 9.0827 22.4 8.01441 22.4 6.90051V5.59958C22.4 4.05318 21.1464 2.79958 19.6 2.79958H18.2991C17.1852 2.79958 16.1169 2.35708 15.3292 1.56942L14.5799 0.820101ZM16.5649 9.17658C16.9938 8.53324 16.8199 7.66402 16.1766 7.23513C15.5332 6.80624 14.664 6.98008 14.2351 7.62342L8.63513 16.0234C8.20624 16.6668 8.38008 17.536 9.02342 17.9649C9.66676 18.3938 10.536 18.2199 10.9649 17.5766L16.5649 9.17658ZM7.7 11.2C8.8598 11.2 9.8 10.2598 9.8 9.1C9.8 7.9402 8.8598 7 7.7 7C6.5402 7 5.6 7.9402 5.6 9.1C5.6 10.2598 6.5402 11.2 7.7 11.2ZM19.6 16.1C19.6 17.2598 18.6598 18.2 17.5 18.2C16.3402 18.2 15.4 17.2598 15.4 16.1C15.4 14.9402 16.3402 14 17.5 14C18.6598 14 19.6 14.9402 19.6 16.1Z"/></svg></span>
            ${esc(t("هل لديك برومو كود؟"))}
          </button>
          <div data-promo-box hidden class="flex flex-col gap-2">
            <div class="flex items-center gap-2">
              <input type="text" data-promo-input inputmode="latin" autocomplete="off"
                     placeholder="${esc(t("أدخل كود الخصم"))}"
                     class="flex-1 bg-white px-3 py-2 border border-divider focus:border-cta rounded-xl outline-none min-w-0 text-ink text-sm transition-colors latin" />
              <button type="button" data-promo-apply
                      class="bg-white hover:bg-cream px-4 border border-cta rounded-full min-h-11 font-semibold text-cta text-sm whitespace-nowrap transition-colors">${esc(t("تطبيق"))}</button>
            </div>
            <p data-promo-msg hidden class="text-xs leading-5"></p>
          </div>
          <div data-promo-applied hidden class="flex justify-between items-center gap-2 bg-mint px-3 py-2 rounded-xl">
            <span class="flex items-center gap-2 min-w-0 text-ink-800 text-sm">
              <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-auto h-8 shrink-0" />
              <span class="truncate">${esc(t("تم تطبيق"))} <span class="font-bold latin" data-promo-applied-code></span></span>
            </span>
            <button type="button" data-promo-remove class="shrink-0 font-semibold text-error text-xs underline">${esc(t("إلغاء"))}</button>
          </div>
        </div>
        <!-- Delivery fee sits WITH the total now (Ahmed, 2026-08-04): free
             delivery zeroes it here (renderCart writes "مجاني"), so the progress
             bar completing is reflected right where the shopper reads the bill.
             No top border — the promo field directly above already carries a
             bottom border, and a second line here would read as a double rule. -->
        <div class="flex flex-col gap-2 pt-1">
          <!-- The wallet-discount row is intentionally NOT in the drawer (Ahmed,
               2026-08-04): the drawer is a quick preview, so it shows only the
               promo discount (a code the shopper actively entered) and the final
               total. The full wallet breakdown lives on the cart/checkout pages.
               The total below still reflects the wallet spend. -->
          <div class="flex justify-between items-center text-sm" data-cart-promo-row hidden>
            <span class="text-muted">${esc(t("خصم كود الخصم"))}</span>
            <span class="inline-flex items-center h-[13px] -me-2 bg-mint px-2 rounded font-bold text-ink-800 text-sm latin" data-cart-promo-discount></span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-muted">${esc(t("مصاريف التوصيل"))}</span>
            <span class="font-semibold text-ink latin" data-cart-delivery>${egp(DELIVERY_FEE)}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-muted text-sm">${esc(t("الإجمالي"))}</span>
            <span class="font-bold text-ink text-lg latin" data-cart-total>${egp(0)}</span>
          </div>
        </div>
        <!-- Two full-width buttons stacked, not side by side (Ahmed,
             2026-08-02). "عرض السلة" moved up to the header; its old slot here
             is now "مواصلة التسوق", which browses all products. Primary label is
             "إتمام الطلب" (Ahmed, 2026-08-04), matching the cart page. -->
        <div class="flex flex-col gap-2 mt-1">
          <a href="checkout.html" data-cart-checkout class="flex justify-center items-center bg-cta hover:bg-cta-hover rounded-full w-full min-h-11 font-semibold text-white text-sm text-center transition-colors">${esc(t("إتمام الطلب"))}</a>
          <a href="shop.html" class="flex justify-center items-center border-cta hover:bg-cream border rounded-full w-full min-h-11 font-semibold text-cta text-sm transition-colors">${esc(t("مواصلة التسوق"))}</a>
        </div>
        <!-- One-line delivery note, no background box (Ahmed, 2026-08-02): the
             boxed two-line version ate too much of the drawer's height. Scooter
             icon + a single line; truncates rather than wrapping. -->
        <div class="flex items-center gap-2 mt-1 min-w-0">
          <img src="images/jaad/icons/spec-delivery.png" alt="" class="w-6 h-6 shrink-0 object-contain" loading="lazy" />
          <p class="text-muted text-xs leading-5 truncate">
            <span class="font-semibold text-ink">${esc(t("توصيل خلال ساعتين"))}</span> ${esc(t("داخل القاهرة الكبرى"))}
          </p>
        </div>
        <!-- The red "you still need EGP X to reach the minimum" line used to sit
             here. Removed with the minimum-order rule itself (Ahmed,
             2026-08-23) — see MIN_ORDER above. -->`;

    return `
    <div data-backdrop class="overlay-backdrop"></div>

    <!-- Cart drawer -->
    <aside data-drawer="cart" class="side-drawer side-drawer--right" aria-label="سلة التسوق">
      <!-- Close sits OUTSIDE the panel now (Ahmed, 2026-08-02): a white circle
           floated just past the drawer's inner edge, over the backdrop. Its old
           header slot is taken by a "view cart" link to the full cart page. -->
      <button type="button" data-close aria-label="إغلاق"
              class="drawer-close place-items-center grid bg-white shadow-custom3 rounded-full size-8 text-ink"><span class="w-3.5 h-3.5">${ICON.close}</span></button>
      <div class="flex justify-between items-center px-5 py-4 border-divider border-b">
        <h2 class="font-bold text-ink text-lg">${esc(t("سلة التسوق"))}</h2>
        <a href="cart.html" class="link-sweep font-semibold text-cta text-sm underline">${esc(t("عرض السلة"))}</a>
      </div>
      <div class="flex-1 px-5 overflow-y-auto">
        <div data-cart-lines></div>
        <!-- Upsell rail. Portrait cards in a looping carousel, with the arrows
             sitting on the opposite end of the heading row rather than floating
             over the slides (Ahmed, 2026-07-26). Overlaid arrows are what the
             page rails do, but they can afford to: they are 1536px wide with
             room outside the track. In a 420px drawer an overlaid arrow covers
             a card.

             Reuses the .carousel contract from components.py rather than a
             second implementation - the class names ARE the API, and this way
             the drawer inherits the RTL logical-axis scrolling, the once-per-
             frame update and the idempotent init for free. -->
        <div class="mt-4 carousel" data-carousel-loop style="--carousel-gap:8px">
          <div class="flex justify-between items-center gap-2 mb-2">
            <p class="font-bold text-ink text-sm">${esc(t("قد يعجبك أيضا"))}</p>
            <div class="flex items-center gap-1.5 shrink-0">
              <button type="button" class="place-items-center grid bg-cream hover:bg-cream-hover rounded-full text-cta transition size-8 carousel-prev" aria-label="السابق">
                <span class="w-4 h-4 rtl:scale-flip">${ICON.arrowLeft}</span>
              </button>
              <button type="button" class="place-items-center grid bg-cream hover:bg-cream-hover rounded-full text-cta transition size-8 carousel-next" aria-label="التالي">
                <span class="w-4 h-4 ltr:scale-flip">${ICON.arrowLeft}</span>
              </button>
            </div>
          </div>
          <div class="carousel-track">${upsell}</div>
        </div>
      </div>
      <div class="flex flex-col gap-2 shadow-cart-overview px-5 py-4 border-divider border-t">
        ${cartFooter}
      </div>
    </aside>

    <!-- Mobile menu drawer -->
    <aside data-drawer="menu" class="side-drawer side-drawer--left" aria-label="Menu">
      <div class="flex justify-between items-center bg-primary px-5 py-4 border-neutral-100 border-b text-white">
        <img src="images/jaad/brand/logo-jaad.svg" alt="جاد" class="w-[29px] h-[28px] object-contain" />
        <button type="button" data-close class="place-items-center grid size-11 -me-2 text-white">${ICON.close}</button>
      </div>
      <!-- Only the category/support links scroll; the account + language row is
           pulled OUT into the sticky footer below so it stays reachable no matter
           how long the menu grows (Ahmed, 2026-08-05). -->
      <div class="flex-1 px-5 py-4 overflow-y-auto">
        <ul>${menuLinks}</ul>
        <div class="mt-6">
          <p class="mb-1 text-muted text-xs">${esc(t("روابط أخرى"))}</p>
          <ul>${supportLinks}</ul>
        </div>
      </div>
      <!-- Sticky footer: pinned to the bottom of the drawer (the aside is a
           flex column, this is shrink-0), opaque so the scrolling list passes
           behind it. Account access on mobile (Ahmed, 2026-08-05): the utility-
           bar account link is desktop-only (hidden lg:flex), so paintAccountLinks
           toggles this anon/authed pair here — sign-in out, dashboard in — the
           same mechanism the header already uses, always within thumb reach. -->
      <div class="flex flex-col gap-3 bg-white shadow-[0_-4px_12px_rgba(0,0,0,0.06)] px-5 pt-4 pb-5 border-divider border-t shrink-0">
        <a href="login.html" data-anon-only class="flex justify-center items-center min-h-11 py-2.5 border border-cta rounded-full font-medium text-cta text-sm text-center">تسجيل الدخول</a>
        <a href="my-account.html" data-authed-only hidden class="flex justify-center items-center gap-2 min-h-11 py-2.5 bg-cta rounded-full font-medium text-white text-sm text-center">
          <img src="images/jaad/icons/hdr-user.svg" alt="" class="w-5 h-5" />
          <span>حسابي</span>
        </a>
        <div class="flex justify-center">${countryButton()}</div>
      </div>
    </aside>

    <!-- Search modal -->
    <div data-modal="search" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[640px] overflow-hidden" data-modal-box>
        <!-- Header: overlay title + close. The close is delegated via
             [data-close], so it works from here just as it did in the row. -->
        <div class="flex justify-between items-center gap-3 px-6 pt-6 pb-4">
          <h2 class="font-bold text-ink text-lg">${esc(t("بحث"))}</h2>
          <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-11 h-11 -me-2 text-ink shrink-0" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
        </div>

        <!-- Roomy JAAD search field: neutral outline that turns green on focus.
             focus-within lets the wrapper react while the real focus stays on the
             input inside. No lime ring any more (Ahmed, 2026-08-23) — see the
             "one focused edge" note in styles.css; every text field on the site
             now signals focus by darkening its OWN border and nothing else. -->
        <div class="px-6">
          <div class="flex items-center gap-3 bg-white px-4 py-3.5 border-2 border-outline rounded-2xl transition-colors focus-within:border-cta search-row">
            <span class="w-5 h-5 text-muted shrink-0">${ICON.search}</span>
            <label class="sr-only" for="site-search">${esc(t("ابحث عن قهوة، مكسرات، بهارات…"))}</label>
            <input type="search" id="site-search" data-search-input autocomplete="off"
                   placeholder="ابحث عن قهوة، مكسرات، بهارات…"
                   class="flex-1 bg-transparent outline-none min-w-0 text-ink placeholder:text-muted text-base" />
          </div>
        </div>

        <!-- Idle state: the query is empty. These were five links that all
             pointed at the same category page; they now seed the box.

             The label is NOT "الأكثر بحثاً" — there is no search analytics
             behind this, so claiming these are the most-searched would be
             inventing data. These three are Jaad's actual categories (not
             the fork's 5-term set, which included تمر/معمول/بروتين — dates,
             maamoul, protein — none of which are Jaad products), so a chip
             always lands on real results. -->
        <div class="px-6 py-6" data-search-idle>
          <p class="mb-3 text-muted text-xs">${esc(t("اقتراحات البحث"))}</p>
          <div class="flex flex-wrap gap-2">
            ${["Coffee", "Nuts", "Spices"]
              .map(
                (s) =>
                  `<button type="button" data-search-seed="${esc(s)}" class="bg-limeFigma hover:bg-cta px-4 py-2 rounded-full min-h-11 font-medium text-ink hover:text-white text-sm transition-colors">${esc(s)}</button>`,
              )
              .join("")}
          </div>
        </div>

        <!-- Result count is a live region so a screen reader hears the list
             change; the list itself is plain anchors, which stay operable if
             the fetch or the JS ever fails. -->
        <p class="px-6 text-muted text-xs" data-search-status role="status" aria-live="polite" hidden></p>
        <div class="max-h-[52vh] overflow-y-auto overscroll-contain" data-search-results hidden></div>
      </div>
    </div>

    <!-- Locale picker: country/currency + language, applied TOGETHER.
         Not the dropdown it replaced: the live site's dropdown applies each
         row the moment it is clicked, which repaints the page once per
         choice - Ahmed wants to pick both and pay the repaint once, so the
         rows here only set radios and nothing happens until تطبيق.

         A BOTTOM SHEET on phones and tablets, a centred dialog from xl
         (Ahmed, 2026-07-22). It was a .modal-shell at every width, so on a
         phone a control reached from the bottom of the menu drawer opened as
         a small floating card in the middle of the screen - a desktop popup
         shape on a surface where the thumb is nowhere near it. This is the
         same .bottom-sheet--modal pattern the location sheet already uses,
         reused rather than re-invented, so the site has ONE sheet system and
         one breakpoint at which sheets become dialogs.

         Stacking: .bottom-sheet and .side-drawer both sit at z-100 and the
         sheet is emitted later, so it lands above the still-open menu drawer
         it was launched from rather than behind it. Verified, not assumed. -->
    <div data-sheet="locale" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-labelledby="locale-sheet-title">
      <!-- Drag affordance: meaningless once this is a centred dialog. -->
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 id="locale-sheet-title" class="font-bold text-ink text-lg">${esc(t("الدولة واللغة"))}</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <div class="flex flex-col gap-5">
        <fieldset class="flex flex-col gap-2">
          <legend class="mb-2 font-bold text-ink text-sm">${esc(t("الدولة و العملة"))}</legend>
          ${COUNTRIES.map(
            (c) => `
          <label class="cursor-pointer">
            <input type="radio" name="locale-country" value="${c.code}" class="peer sr-only"${c.code === currentCountry().code ? " checked" : ""} />
            <span class="flex items-center gap-3 px-4 py-2.5 border-2 border-divider peer-checked:border-cta rounded-xl min-h-11 transition-colors">
              <img src="${c.flag}" alt="" class="rounded-full w-6 h-6 object-cover shrink-0" />
              <span class="flex-1 min-w-0 text-ink text-sm">${esc(c.ar)} <span class="latin">(${c.currency})</span></span>
              <span class="radio-dot shrink-0" aria-hidden="true"></span>
            </span>
          </label>`,
          ).join("")}
        </fieldset>
        <fieldset class="flex flex-col gap-2">
          <legend class="mb-2 font-bold text-ink text-sm">${esc(t("اللغة"))}</legend>
          ${LANGS.map(
            (l) => `
          <label class="cursor-pointer">
            <input type="radio" name="locale-lang" value="${l.code}" class="peer sr-only"${l.code === currentLang() ? " checked" : ""} />
            <span class="flex items-center gap-3 px-4 py-2.5 border-2 border-divider peer-checked:border-cta rounded-xl min-h-11 transition-colors">
              <span class="w-5 h-5 text-muted shrink-0" aria-hidden="true">${ICON.globe}</span>
              <span class="flex-1 min-w-0 text-ink text-sm">${l.label}</span>
              <span class="radio-dot shrink-0" aria-hidden="true"></span>
            </span>
          </label>`,
          ).join("")}
        </fieldset>
        <button type="button" data-locale-apply class="bg-cta hover:bg-cta-hover py-3 rounded-full w-full font-semibold text-white text-sm transition-colors">${esc(t("تطبيق"))}</button>
      </div>
    </div>

    <!-- Address form: add and edit share it; data-address-id says which. -->
    <!-- Bottom sheet on phones, centred dialog from xl (Ahmed, 2026-08-05) —
         the account popups all use the same sheet pattern as the location/locale
         pickers so a thumb reaches them from the bottom edge on mobile. -->
    <div data-sheet="address" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-labelledby="address-sheet-title">
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 id="address-sheet-title" class="font-bold text-ink text-lg" data-address-form-title>${esc(t("اضف عنوان"))}</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <form data-address-form data-address-id="" class="flex flex-col gap-3">
          <label class="block">
            <span class="label">${esc(t("اسم العنوان"))}</span>
            <input type="text" name="label" required placeholder="المنزل، العمل…"
                   class="mt-1 px-3 border border-divider focus:border-cta rounded-lg outline-none w-full h-12 text-ink text-sm transition-colors" />
          </label>
          <label class="block">
            <span class="label">${esc(t("العنوان"))}</span>
            <input type="text" name="line1" required placeholder="رقم الشقة والمبنى واسم الشارع"
                   class="mt-1 px-3 border border-divider focus:border-cta rounded-lg outline-none w-full h-12 text-ink text-sm transition-colors" />
          </label>
          <label class="block">
            <span class="label">${esc(t("المنطقة والمدينة"))}</span>
            <input type="text" name="line2" required placeholder="المنطقة، المدينة"
                   class="mt-1 px-3 border border-divider focus:border-cta rounded-lg outline-none w-full h-12 text-ink text-sm transition-colors" />
          </label>
          <label class="flex items-center gap-2 py-1 cursor-pointer">
            <input type="checkbox" name="main" class="accent-ink-800 size-4" />
            <span class="text-ink text-sm">${esc(t("اجعله العنوان الافتراضي"))}</span>
          </label>
          <button type="submit" class="bg-cta hover:bg-cta-hover mt-1 py-3 rounded-full font-semibold text-white text-sm transition-colors">${esc(t("حفظ العنوان"))}</button>
        </form>
    </div>

    <!-- Location bottom sheet -->
    <!-- Bottom sheet on phones, centred dialog from xl — the live site opens
         this as a popup on desktop, where a full-width sheet pinned to the
         bottom of a 1440px window reads as a mobile pattern out of place. -->
    <div data-sheet="location" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-label="أختار منطقة التوصيل">
      <!-- Drag affordance: meaningless once this is a centred dialog. -->
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="font-bold text-ink text-lg">أختار منطقة التوصيل</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <form data-location-form class="flex flex-col gap-3">
        <label class="block">
          <span class="label">المدينة</span>
          <select class="select-control mt-1 px-3 border border-divider rounded-lg w-full h-12 text-ink">
            ${["القاهرة", "الجيزه", "الاسكندريه", "القليوبيه", "الشرقيه", "الدقهليه", "المنوفيه", "الغربيه"]
              .map((c) => `<option>${c}</option>`)
              .join("")}
          </select>
        </label>
        <label class="block">
          <span class="label">المنطقة</span>
          <select class="select-control mt-1 px-3 border border-divider rounded-lg w-full h-12 text-ink">
            ${["التجمع الخامس", "مدينه نصر", "المعادي", "الزمالك", "هليوبوليس", "الشروق", "الرحاب", "المقطم"]
              .map((a) => `<option>${a}</option>`)
              .join("")}
          </select>
        </label>
        <button type="submit" class="bg-cta hover:bg-cta-hover mt-2 py-3 rounded-full font-semibold text-white transition-colors">تأكيد المنطقة</button>
      </form>
    </div>

    <!-- Store picker (checkout). Governorate -> branch, on the client's real
         316 branches; see the note in build/pages/checkout.py for why there is
         no third level. Confirm stays disabled until a branch is chosen, so
         the row's meta can never resolve to nothing. -->
    <div data-modal="storepicker" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[480px] overflow-hidden" data-modal-box>
        <div class="flex justify-between items-center px-5 py-4 border-divider border-b">
          <h2 class="font-bold text-ink text-lg">${esc(t("اختر الفرع"))}</h2>
          <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
        </div>
        <div class="flex flex-col gap-3 p-5">
          <label class="block">
            <span class="label">${esc(t("المحافظة"))}</span>
            <select data-store-gov class="select-control mt-1 px-3 border border-divider rounded-lg w-full h-12 text-ink"></select>
          </label>
          <div data-store-list class="flex flex-col gap-2 pe-1 max-h-[280px] overflow-y-auto"></div>
        </div>
        <div class="px-5 pb-5">
          <button type="button" data-store-confirm disabled
                  class="disabled:opacity-40 bg-cta hover:bg-cta-hover py-3 rounded-full w-full font-semibold text-white transition-colors disabled:cursor-not-allowed">${esc(t("تأكيد الفرع"))}</button>
        </div>
      </div>
    </div>

    <!-- Schedule picker (checkout). Days are computed at RUNTIME from today,
         never baked at build time — a build-time date list is wrong the next
         morning and silently offers a delivery slot in the past. -->
    <div data-modal="schedule" class="modal-shell">
      <div class="bg-white shadow-custom3 rounded-2xl w-full max-w-[480px] overflow-hidden" data-modal-box>
        <div class="flex justify-between items-center px-5 py-4 border-divider border-b">
          <h2 class="font-bold text-ink text-lg">${esc(t("حدد اليوم والوقت"))}</h2>
          <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
        </div>
        <div class="flex flex-col gap-4 p-5">
          <!-- The arrows sit OUTSIDE [data-sched-days] deliberately:
               renderSchedule() replaces that container's innerHTML on every
               day and slot press, so anything inside it is destroyed and would
               lose its listeners. -->
          <div class="flex items-center gap-2">
            <button type="button" data-sched-nav="-1" aria-label="أيام سابقة"
                    class="sched-arrow place-items-center grid shrink-0 border border-divider rounded-full size-8 text-cta transition-colors">
              <span class="w-4 h-4 rtl:scale-flip">${ICON.arrowLeft}</span>
            </button>
            <div data-sched-days class="flex flex-1 gap-2 -mx-1 px-1 min-w-0 overflow-x-auto no-scrollbar scroll-smooth"></div>
            <button type="button" data-sched-nav="1" aria-label="أيام تالية"
                    class="sched-arrow place-items-center grid shrink-0 border border-divider rounded-full size-8 text-cta transition-colors">
              <span class="w-4 h-4 rtl:scale-flip">${ICON.arrowRight}</span>
            </button>
          </div>
          <div data-sched-slots class="gap-2 grid grid-cols-2"></div>
        </div>
        <div class="px-5 pb-5">
          <button type="button" data-sched-confirm disabled
                  class="disabled:opacity-40 bg-cta hover:bg-cta-hover py-3 rounded-full w-full font-semibold text-white transition-colors disabled:cursor-not-allowed">${esc(t("تأكيد الموعد"))}</button>
        </div>
      </div>
    </div>

    <!-- Account modals (Ahmed, 2026-08-04): add/activate a voucher, redeem
         points. All demo — activating a voucher or redeeming points lands the
         value in the wallet (initVouchers / initPointsRedeem). -->
    <div data-sheet="voucherAdd" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-labelledby="voucherAdd-sheet-title">
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 id="voucherAdd-sheet-title" class="font-bold text-ink text-lg">${esc(t("أضف كود قسيمة"))}</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <form data-voucher-add-form class="flex flex-col gap-3">
        <label class="block">
          <span class="label">${esc(t("الكود"))}</span>
          <input type="text" name="code" required placeholder="مثال: JAAD150" dir="ltr"
                 class="mt-1 px-3 border border-divider focus:border-cta rounded-lg outline-none w-full h-12 text-ink text-sm text-start transition-colors latin" />
        </label>
        <p class="text-muted text-xs">${esc(t("الكود صالح للاستخدام مرة واحدة فقط."))}</p>
        <button type="submit" class="bg-cta hover:bg-cta-hover mt-1 py-3 rounded-full font-semibold text-white text-sm transition-colors">${esc(t("أضف القسيمة"))}</button>
      </form>
    </div>

    <div data-sheet="voucherActivate" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-labelledby="voucherActivate-sheet-title">
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-center mb-4">
        <h2 id="voucherActivate-sheet-title" class="font-bold text-ink text-lg">${esc(t("تفعيل القسيمة"))}</h2>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <div class="flex flex-col items-center gap-3 text-center">
        <img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-16 h-16 object-contain" />
        <p class="text-ink text-sm leading-6">${esc(t("سيتم إضافة"))} <span class="font-bold text-cta latin" data-voucher-activate-value></span> ${esc(t("إلى رصيد محفظتك"))}</p>
        <button type="button" data-voucher-activate-confirm class="bg-cta hover:bg-cta-hover mt-1 py-3 rounded-full w-full font-semibold text-white text-sm transition-colors">${esc(t("تفعيل القسيمة"))}</button>
      </div>
    </div>

    <div data-sheet="pointsRedeem" class="bottom-sheet bottom-sheet--modal" role="dialog" aria-modal="true" aria-labelledby="pointsRedeem-sheet-title">
      <div class="xl:hidden bg-neutral-200 mx-auto mb-4 rounded-full w-10 h-1"></div>
      <div class="flex justify-between items-start mb-4">
        <div class="flex flex-col">
          <h2 id="pointsRedeem-sheet-title" class="font-bold text-ink text-lg">${esc(t("استبدال النقاط"))}</h2>
          <span class="text-muted text-xs">${esc(t("حوّل نقاطك إلى رصيد في محفظتك"))}</span>
        </div>
        <button type="button" data-close class="place-items-center grid hover:bg-cream rounded-full w-9 h-9 -me-1.5 text-ink" aria-label="إغلاق"><span class="w-5 h-5">${ICON.close}</span></button>
      </div>
      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-2 bg-cream px-3 py-2 rounded-xl">
          <img src="images/jaad/icons/points-3d.png" alt="" class="w-6 h-6 object-contain" />
          <span class="text-ink text-sm"><span class="font-bold latin" data-redeem-available>0</span> ${esc(t("نقطة متاحة"))}</span>
        </div>
        <div class="flex items-end gap-2">
          <label class="flex flex-col flex-1 gap-1">
            <span class="font-medium text-muted text-xs">${esc(t("عدد النقاط"))}</span>
            <input type="number" inputmode="numeric" data-redeem-input min="0" step="10"
                   class="bg-white px-3 border-2 border-divider focus:border-cta rounded-xl outline-none w-full h-11 text-ink text-base transition-colors latin" />
          </label>
          <button type="button" data-redeem-all class="bg-cream hover:bg-cream-hover px-4 border border-divider rounded-xl h-11 font-semibold text-cta text-xs whitespace-nowrap transition-colors">${esc(t("كل النقاط"))}</button>
        </div>
        <p class="text-muted text-sm">${esc(t("القيمة"))}: <span class="font-bold text-cta latin" data-redeem-egp>EGP 0</span></p>
        <p data-redeem-msg hidden class="font-semibold text-error text-xs"></p>
        <div class="pt-1">
          <button type="button" data-redeem-confirm class="bg-cta hover:bg-cta-hover px-6 py-3 rounded-full w-full font-semibold text-white text-sm transition-colors">${esc(t("تأكيد الاستبدال"))}</button>
        </div>
      </div>
    </div>

    <div id="toast-container"></div>`;
  }

  /* ---------------------------------------------------------------
     Overlay open/close plumbing
     --------------------------------------------------------------- */
  const openMap = {
    storepicker: '[data-modal="storepicker"]',
    schedule: '[data-modal="schedule"]',
    cart: '[data-drawer="cart"]',
    order: '[data-drawer="order"]',
    menu: '[data-drawer="menu"]',
    search: '[data-modal="search"]',
    locale: '[data-sheet="locale"]',
    address: '[data-sheet="address"]',
    location: '[data-sheet="location"]',
    accountMenu: '[data-sheet="account-menu"]',
    voucherAdd: '[data-sheet="voucherAdd"]',
    voucherActivate: '[data-sheet="voucherActivate"]',
    pointsRedeem: '[data-sheet="pointsRedeem"]',
  };
  let openEl = null;

  function openOverlay(key) {
    const sel = openMap[key];
    if (!sel) return;
    const el = document.querySelector(sel);
    const backdrop = document.querySelector("[data-backdrop]");
    if (!el) return;
    openEl = el;
    el.classList.add("is-open");
    if (backdrop) backdrop.classList.add("is-open");
    document.body.classList.add("no-scroll");
    const input = el.querySelector("[data-search-input]");
    if (input) {
      // Warm the catalogue while the shopper is still reaching for the
      // keyboard, so the first keystroke renders instead of waiting on I/O.
      loadCatalog();
      setTimeout(() => input.focus(), 80);
    }
  }

  function closeOverlay() {
    document
      .querySelectorAll(".side-drawer.is-open, .modal-shell.is-open, .bottom-sheet.is-open")
      .forEach((el) => el.classList.remove("is-open"));
    const backdrop = document.querySelector("[data-backdrop]");
    if (backdrop) backdrop.classList.remove("is-open");
    document.body.classList.remove("no-scroll");
    openEl = null;
  }

  /* ---------------------------------------------------------------
     Site search

     The magnifier was in the masthead of all 130 pages and did nothing:
     the modal took focus and had no handler, no results and no empty
     state, so every query was a dead end.

     This is the one place scripts.js reads catalog.json at runtime.
     Everywhere else the catalogue is baked in at build time on purpose,
     but search cannot be — it has to reach products that are not on the
     current page. Fetched once, lazily, on first open, and cached; a
     failed fetch degrades to a message rather than a spinner that never
     resolves.
     --------------------------------------------------------------- */
  let catalogPromise = null;

  function loadCatalog() {
    if (!catalogPromise) {
      catalogPromise = fetch("data/catalog.json")
        .then((r) => {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then((d) => d.products || [])
        .catch(() => null);
    }
    return catalogPromise;
  }

  /*
   * Arabic needs folding before it can be matched the way a shopper types.
   * The catalogue writes قهوة with a ة and shoppers type ه; ى and ي, أ إ آ
   * and ا are used interchangeably; and the tashkeel that appears in a few
   * product names is never typed at all. Without this, searching "قهوه"
   * returns nothing while "قهوة" returns twelve products, which reads as a
   * broken search rather than a spelling difference.
   */
  function fold(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/[ً-ْـ]/g, "")
      .replace(/[أإآٱ]/g, "ا")
      .replace(/ى/g, "ي")
      .replace(/ة/g, "ه")
      .replace(/[ؤئ]/g, "ء")
      .replace(/\s+/g, " ")
      .trim();
  }

  function searchProducts(products, q) {
    const needle = fold(q);
    if (!needle) return [];
    const terms = needle.split(" ");
    const scored = [];
    products.forEach((p) => {
      const ar = fold(p.nameAr);
      const en = fold(p.name);
      // Every term must appear somewhere, so "قهوه تركي" narrows rather
      // than widening the way an OR match would.
      if (!terms.every((t2) => ar.includes(t2) || en.includes(t2))) return;
      // A prefix match is what the shopper is most likely reaching for, so
      // it outranks a match buried mid-name; popularityRank breaks ties
      // with the client's real sales order rather than catalogue order.
      const starts = ar.startsWith(terms[0]) || en.startsWith(terms[0]);
      scored.push({ p: p, score: (starts ? 0 : 1000) + (p.popularityRank || 999) });
    });
    scored.sort((a, b) => a.score - b.score);
    return scored.slice(0, 24).map((x) => x.p);
  }

  function searchResultHTML(p) {
    const name = currentLang() === "en" ? p.name || p.nameAr : p.nameAr || p.name;
    const img = (p.images && p.images[0]) || p.image || "";
    return `
      <a href="product-${esc(String(p.id))}.html"
         class="flex items-center gap-3 hover:bg-cream px-5 py-3 border-divider border-b last:border-b-0 transition-colors">
        <img src="${esc(img)}" alt="" loading="lazy"
             class="bg-cream shrink-0 p-1 rounded-lg w-12 h-12 object-contain" />
        <span class="flex-1 min-w-0 font-semibold text-ink text-sm line-clamp-2">${esc(name)}</span>
        <span class="bg-lime shrink-0 px-2 py-0.5 rounded font-bold text-ink text-xs latin">EGP ${esc(
          String(p.price),
        )}</span>
      </a>`;
  }

  function initSearch() {
    const modal = document.querySelector('[data-modal="search"]');
    if (!modal) return;
    const input = modal.querySelector("[data-search-input]");
    const results = modal.querySelector("[data-search-results]");
    const status = modal.querySelector("[data-search-status]");
    const idle = modal.querySelector("[data-search-idle]");
    if (!input || !results || !status || !idle) return;

    let timer = null;
    let token = 0;

    function render(q) {
      const mine = ++token;
      if (!fold(q)) {
        results.hidden = true;
        status.hidden = true;
        results.innerHTML = "";
        idle.hidden = false;
        return;
      }
      idle.hidden = true;
      loadCatalog().then((products) => {
        // A slow response for an abandoned query must not overwrite the
        // results of the one the shopper is actually looking at.
        if (mine !== token) return;
        status.hidden = false;
        if (!products) {
          results.hidden = true;
          results.innerHTML = "";
          status.textContent = t("تعذر تحميل نتائج البحث. حاول مرة أخرى.");
          return;
        }
        const hits = searchProducts(products, q);
        if (!hits.length) {
          results.hidden = true;
          results.innerHTML = "";
          status.textContent = t("لا توجد نتائج لـ") + ' "' + q.trim() + '"';
          return;
        }
        status.textContent = hits.length + " " + t("نتيجة");
        results.innerHTML = hits.map(searchResultHTML).join("");
        results.hidden = false;
        results.scrollTop = 0;
      });
    }

    input.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => render(input.value), 140);
    });

    // Enter with a single hit is unambiguous — go there rather than making
    // the shopper reach for the mouse to click the only row on screen.
    input.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      const first = results.querySelector("a");
      if (first) {
        e.preventDefault();
        window.location.href = first.getAttribute("href");
      }
    });

    modal.addEventListener("click", (e) => {
      const seed = e.target.closest("[data-search-seed]");
      if (!seed) return;
      input.value = seed.dataset.searchSeed;
      input.focus();
      render(input.value);
    });
  }

  /* ---------------------------------------------------------------
     Toast
     --------------------------------------------------------------- */
  /* Toasts carry a glyph and an accent keyed to the ACTION, not just a generic
     "done" (Ahmed, 2026-08-05). A credit to the wallet, a spend against it and
     an undo of that spend used to read as three identical green bars; now the
     icon and the ink say which one happened at a glance. `type` is one of
     success | error | info | wallet | spend | cart; anything else falls back to
     success, and the old `"error"` call sites keep working unchanged. */
  const TOAST_ICONS = {
    success: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 8v5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="16.5" r="1.3" fill="currentColor"/><path d="M10.3 3.9 2.5 18a1.9 1.9 0 0 0 1.7 2.8h15.6A1.9 1.9 0 0 0 21.5 18L13.7 3.9a2 2 0 0 0-3.4 0Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 11v5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="7.8" r="1.2" fill="currentColor"/></svg>',
    wallet: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H18a1 1 0 0 1 1 1v1.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 7.5v9A2.5 2.5 0 0 0 5.5 19H19a1 1 0 0 0 1-1v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 10.5h-4a2 2 0 0 0 0 4h4a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    spend: '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M3 7.5A2.5 2.5 0 0 1 5.5 5H18a1 1 0 0 1 1 1v1.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 7.5v9A2.5 2.5 0 0 0 5.5 19H19a1 1 0 0 0 1-1v-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14.5 12.5h6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
    cart: '<svg viewBox="0 0 20 19" fill="none" class="w-full h-full"><path d="M3.75 3.75V9.43333C3.75 10.9735 3.75 11.7436 4.04973 12.3318C4.31338 12.8493 4.73408 13.27 5.25153 13.5336C5.83978 13.8333 6.60986 13.8333 8.15 13.8333H12.7308C13.745 13.8333 14.2521 13.8333 14.697 13.676C15.0903 13.5369 15.4468 13.3102 15.7396 13.0129C16.0707 12.6767 16.2857 12.2175 16.7157 11.299L17.3165 10.0157C18.2915 7.93326 18.7789 6.89207 18.6388 6.04904C18.5164 5.31257 18.0998 4.65752 17.4847 4.23437C16.7806 3.75 15.631 3.75 13.3316 3.75H3.75ZM3.75 3.75V3.6757C3.75 2.89117 3.75 2.4989 3.63192 2.18601C3.44591 1.69313 3.05687 1.30409 2.56399 1.11809C2.2511 1 1.85883 1 1.0743 1H1M5.58333 17.5H6.5M12 17.5H12.9167" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  };
  function toast(msg, type) {
    // Toast pop-ups removed site-wide (Ahmed, 2026-08-18). Every call site is
    // left intact — add-to-cart already gives feedback via the fly-to-cart
    // animation and the cart badge — but no notification is ever shown.
    return;
    const c = document.getElementById("toast-container");
    if (!c) return;
    const kind = TOAST_ICONS[type] ? type : "success";
    const el = document.createElement("div");
    el.className = "toast toast--" + kind;
    el.setAttribute("role", kind === "error" ? "alert" : "status");
    const icon = document.createElement("span");
    icon.className = "toast__icon";
    icon.setAttribute("aria-hidden", "true");
    icon.innerHTML = TOAST_ICONS[kind];
    const text = document.createElement("span");
    text.className = "toast__msg";
    // Translate here so EVERY toast is localized (Ahmed, 2026-08-17), including
    // the many call sites that pass a raw Arabic literal. Already-t()'d or
    // English messages fall through unchanged (t() returns its input when the
    // string is not a dictionary key).
    text.textContent = t(msg);
    el.append(icon, text);
    c.appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transition = "opacity .3s";
      setTimeout(() => el.remove(), 300);
    }, 3000);
  }
  window.kToast = toast;

  /* ---------------------------------------------------------------
     Carousel (Swiper replacement)
     --------------------------------------------------------------- */
  /*
   * Browsers disagree on how scrollLeft is reported inside an RTL container.
   * Detect it once, then express every position as a *logical* offset where
   * 0 is the start of the track and `maxPos()` is the end — in both
   * directions. Everything below is written against that logical axis.
   */
  const rtlScrollType = (function detect() {
    const probe = document.createElement("div");
    probe.dir = "rtl";
    probe.style.cssText =
      "position:absolute;top:-9999px;width:100px;height:1px;overflow:scroll;visibility:hidden";
    probe.innerHTML = '<div style="width:200px;height:1px"></div>';
    document.body.appendChild(probe);
    let type = "negative"; // spec: 0 at the right edge, negative going left
    if (probe.scrollLeft > 0) {
      type = "positive"; // legacy WebKit: starts at max, counts down
    } else {
      probe.scrollLeft = 1;
      if (probe.scrollLeft !== 0) type = "positive";
    }
    probe.remove();
    return type;
  })();

  function initCarousel(root) {
    const track = root.querySelector(".carousel-track");
    if (!track) return;

    /* kInit() re-runs across the whole document on every language switch, and
       nothing here used to be idempotent. So each toggle bound a SECOND
       scroll listener, a second resize listener and a second autoplay timer
       to every rail on the page — scroll work that compounded with each
       toggle, and autoplay timers that then fought each other over the same
       scrollLeft. Bind once. */
    if (root.dataset.carouselReady === "true") return;
    root.dataset.carouselReady = "true";

    const prev = root.querySelector(".carousel-prev");
    const next = root.querySelector(".carousel-next");
    const dotsWrap = root.querySelector(".carousel-dots");

    /* `data-carousel-loop` — wrap around instead of stopping at the ends.
       Wrap-around, NOT cloned slides. Cloning would put a second element
       carrying the same `data-id` in the DOM, and both the cart store and
       syncCardSteppers key off that id; a rail of two products would end up
       with duplicate hosts for one line. Jumping the scroll position is the
       same affordance with none of that. */
    const loop = root.hasAttribute("data-carousel-loop");

    /* Direction is read off <html>, not off the track's computed style.
       getComputedStyle forces a style recalc, and this used to sit inside
       getPos() — which runs on every scroll frame, twice per update(). `dir`
       is only ever set on the root element (verified across all 130 pages),
       so an attribute read is an exact substitute for a computed one here and
       costs nothing. It also stays correct across a language switch, which a
       value cached at init time would not. */
    const isRTL = () => document.documentElement.getAttribute("dir") === "rtl";

    /* The gap DOES need computed style, so it is read once and re-read only
       on resize — it cannot change otherwise. */
    let gap = 16;
    function measureGap() {
      const style = getComputedStyle(track);
      gap = parseFloat(style.columnGap || style.gap || "16") || 16;
    }
    measureGap();

    /* Fit whole cards — the rail never rests showing a half "cropped" card at
       the trailing edge (Ahmed, 2026-08-02). Product rails size each slide to
       fill an integer number of columns for the current width, so only whole
       cards are ever in view. Skipped for the hero (full-width slides) and the
       looping drawer rail; the target is a paged rail of fixed-width product
       cards. If the script never runs, the slides keep their Tailwind widths —
       the current no-JS behaviour. */
    const firstSlide0 = track.querySelector(".carousel-slide");
    const fitCols = !loop && !!firstSlide0 && firstSlide0.hasAttribute("data-product");
    function applyFit() {
      if (!fitCols) return;
      const w = track.clientWidth;
      const cols = w >= 1280 ? 5 : w >= 1024 ? 4 : w >= 640 ? 3 : 2;
      const cardW = Math.max(1, Math.floor((w - (cols - 1) * gap) / cols));
      track.querySelectorAll(".carousel-slide").forEach((s) => {
        s.style.flex = "0 0 " + cardW + "px";
        s.style.width = cardW + "px";
      });
    }
    applyFit();

    /* Seamless infinite loop for the hero (Ahmed, 2026-08-02): a clone of the
       first banner is appended so autoplay can advance PAST the last banner
       into a copy of the first, then silently reset to the real first with no
       animation — the shopper never sees the rail rewind to the start. Scoped
       to data-carousel-seamless (the hero only); the clone carries no data-id,
       so the duplicate-host concern that rules out cloning on product rails
       does not apply. */
    const seamless = root.hasAttribute("data-carousel-seamless");
    if (seamless && firstSlide0) {
      const clone = firstSlide0.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      clone.setAttribute("data-carousel-clone", "");
      clone
        .querySelectorAll("a,button,input,select,textarea,[tabindex]")
        .forEach((el) => el.setAttribute("tabindex", "-1"));
      track.appendChild(clone);
    }
    function jumpInstant(pos) {
      const prevBehavior = track.style.scrollBehavior;
      track.style.scrollBehavior = "auto";
      setPos(pos);
      void track.offsetWidth; // commit the jump before smooth is restored
      track.style.scrollBehavior = prevBehavior;
    }
    function seamlessNext() {
      if (getPos() >= maxPos() - 1) jumpInstant(0);
      setPos(getPos() + slideStep());
    }
    function seamlessPrev() {
      if (getPos() <= 1) jumpInstant(maxPos());
      setPos(getPos() - slideStep());
    }

    const maxPos = () =>
      Math.max(0, track.scrollWidth - track.clientWidth - 1);

    // Physical scrollLeft -> logical offset (0 = start of track).
    function getPos() {
      const sl = track.scrollLeft;
      if (!isRTL()) return sl;
      return rtlScrollType === "negative" ? -sl : maxPos() - sl;
    }

    // Logical offset -> physical scrollLeft.
    function setPos(pos) {
      const p = Math.max(0, Math.min(maxPos(), pos));
      if (!isRTL()) track.scrollLeft = p;
      else if (rtlScrollType === "negative") track.scrollLeft = -p;
      else track.scrollLeft = maxPos() - p;
    }

    /* One card's worth of scroll — the step the arrows move, and the unit
       atStart()/atEnd() measure "an end" in.

       The fallback to the first CHILD matters (Ahmed, 2026-08-23): the product
       rails render `product_widget()` cards, which carry `snap-start` but NOT
       the `.carousel-slide` class, so this returned `track.clientWidth` and the
       arrows paged a WHOLE viewport at a time — five cards vanishing per press.
       It also made atStart/atEnd read "within half a viewport of the end", which
       is most of a short rail, so the new wrap-around fired far too eagerly.
       Falling back to the first child gives the real card width on those rails
       and changes nothing on the ones that do use the class. */
    function slideStep() {
      const first = track.querySelector(".carousel-slide") || track.firstElementChild;
      if (!first) return track.clientWidth;
      return first.getBoundingClientRect().width + gap;
    }

    /* Every geometry read happens before the first class write. Interleaving
       them — read scrollLeft, toggle a class, read scrollWidth, toggle
       another — invalidates layout between reads, so each later read forces a
       synchronous re-layout. On the home page that was four rails paying it
       on every scroll frame. */
    function update() {
      const pos = getPos();
      const max = maxPos();
      const idx = Math.round(pos / slideStep());
      // A looping OR seamless rail has no ends to be at, so its arrows never
      // disable — greying one out would say "you cannot go that way" about the
      // one direction that always works.
      if (prev && !loop && !seamless) prev.classList.toggle("is-disabled", pos <= 1);
      if (prev && (loop || seamless)) prev.classList.remove("is-disabled");
      if (next) next.classList.toggle("is-disabled", !loop && !seamless && pos >= max);
      if (dotsWrap) {
        const dots = dotsWrap.querySelectorAll(".carousel-dot");
        const n = dots.length || 1;
        // Modulo so the clone position (idx === real slide count) lights the
        // first dot rather than none while the seamless hero sits on it.
        dots.forEach((d, i) => d.classList.toggle("is-active", i === (((idx % n) + n) % n)));
      }
    }

    /* One update per FRAME, not one per event. The scroll handler used to
       call requestAnimationFrame unconditionally, so a burst of scroll events
       arriving inside a single frame queued a callback each — every one of
       them repeating the same layout reads to arrive at the same answer.
       Momentum scrolling and scroll-snap settling both produce exactly that
       burst. */
    let ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(() => {
        ticking = false;
        update();
      });
    }

    let resizing = false;
    function onResize() {
      if (resizing) return;
      resizing = true;
      window.requestAnimationFrame(() => {
        resizing = false;
        measureGap();
        applyFit();
        update();
      });
    }

    /* "Within half a slide of the end" — not an exact comparison, and not a
       fixed pixel slop either. A snap-settled rail does not park on its own
       maximum: measured here it sat 4px short of the end, and 18px past the
       start right after a wrap. A fixed tolerance big enough for one of those
       was still too small for the other.

       Half a slide is the honest rule. Resting positions are multiples of the
       step (144px here), so anything inside 72px of an end IS that end, and no
       genuine mid-rail position can be mistaken for one. It also scales with
       the card size instead of needing a new magic number per rail. */
    const atStart = (pos) => pos <= slideStep() / 2;
    const atEnd = (pos) => pos >= maxPos() - slideStep() / 2;
    if (prev)
      prev.addEventListener("click", () => {
        if (seamless) return seamlessPrev();
        const pos = getPos();
        if (loop && atStart(pos)) setPos(maxPos());
        else setPos(pos - slideStep());
      });
    if (next)
      next.addEventListener("click", () => {
        if (seamless) return seamlessNext();
        const pos = getPos();
        if (loop && atEnd(pos)) setPos(0);
        else setPos(pos + slideStep());
      });

    if (dotsWrap) {
      const slides = track.querySelectorAll(".carousel-slide:not([data-carousel-clone])");
      const perView = Math.max(1, Math.round(track.clientWidth / slideStep()));
      const pages = Math.max(1, slides.length - perView + 1);
      dotsWrap.innerHTML = "";
      for (let i = 0; i < pages; i++) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "carousel-dot" + (i === 0 ? " is-active" : "");
        dot.addEventListener("click", () => setPos(i * slideStep()));
        dotsWrap.appendChild(dot);
      }
    }

    /* passive: this handler never calls preventDefault, and saying so up
       front lets the compositor start the scroll without waiting to find
       out. */
    track.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize, { passive: true });
    update();

    /* ---------------------------------------------------------------
       Touch scrolls the rail NATIVELY; the pointer-drag below is MOUSE-only.

       History: a vertical swipe STARTING on a rail once failed to scroll the
       page on iOS/WebKit, and the fix was `touch-action: pan-x` plus a
       JS pointer-drag that drove scrollLeft by hand. That fixed the freeze but
       traded away native touch scrolling — the finger-drag had no momentum, no
       fling, and a slightly-diagonal thumb swipe would stall — so the rails
       "swiped oddly" next to the home-page review row, which is a plain native
       scroller and always felt right (Ahmed, 2026-08-05).

       The review row is the proof that native is the answer: it is a
       `touch-action: auto` scroll-snap container and it neither stalls nor
       traps a vertical swipe. The earlier WebKit trap was specific to `pan-x`,
       which forbids vertical panning ON the element — `auto` lets the browser
       disambiguate the axis and hand vertical straight to the page. So the
       rails now scroll natively on touch too (styles.css sets the track's
       `touch-action`, and `overscroll-behavior-x: contain` keeps a fling from
       chaining into a back-navigation).

       The pointer-drag stays, but only for a MOUSE: a desktop click-drag is the
       one gesture the browser will NOT turn into a scroll on a scrollbar-hidden
       rail, so we still drive that by hand. Touch and pen fall through to the
       native scroller above. */

    let dragActive = false; // a pointer is down and being tracked
    let dragScroll = false; // it has crossed the slop into a real drag
    let dragStartX = 0, dragStartSL = 0, dragMoved = 0, dragId = null;

    track.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse") return; // touch/pen scroll natively
      if (e.button !== 0) return;
      dragActive = true;
      dragScroll = false;
      dragMoved = 0;
      dragStartX = e.clientX;
      dragStartSL = track.scrollLeft;
      dragId = e.pointerId;
    });

    track.addEventListener("pointermove", (e) => {
      if (!dragActive || e.pointerId !== dragId) return;
      const dx = e.clientX - dragStartX;
      /* 4px of slop before we claim the gesture: below it a tap is still a tap,
         and a nascent vertical swipe still belongs to the page (the browser
         will pointercancel us the instant it decides the drag is vertical). */
      if (!dragScroll && Math.abs(dx) > 4) {
        dragScroll = true;
        track.classList.add("is-dragging"); // suspends snap + smooth mid-drag
        try { track.setPointerCapture(dragId); } catch (_) {}
      }
      if (dragScroll) {
        dragMoved = dx;
        // Physical scrollLeft, moved opposite the finger so content follows it.
        // A physical coordinate needs no RTL branch — unlike getPos/setPos.
        track.scrollLeft = dragStartSL - dx;
        e.preventDefault();
      }
    });

    const endDrag = () => {
      if (!dragActive) return;
      dragActive = false;
      if (!dragScroll) return;
      dragScroll = false;
      track.classList.remove("is-dragging"); // restores snap + smooth
      // Settle on the nearest slide rather than wherever the finger stopped.
      setPos(Math.round(getPos() / slideStep()) * slideStep());
    };
    track.addEventListener("pointerup", endDrag);
    track.addEventListener("pointercancel", endDrag);

    /* A drag must not also click the card under it. Capture phase, so this
       beats the link/button's own handler; only a real drag (past the tap
       slop) is suppressed, so a genuine tap still activates the card. */
    track.addEventListener(
      "click",
      (e) => {
        if (Math.abs(dragMoved) > 4) {
          e.preventDefault();
          e.stopPropagation();
        }
        dragMoved = 0;
      },
      true,
    );

    if (root.hasAttribute("data-autoplay")) {
      /* Was a bare setInterval that ran for the life of the page. Three
         problems, all of them paid on the main thread:

         - It kept ticking in a hidden or backgrounded tab, queueing a smooth
           scroll animation every 4.5s that nobody could see.
         - It kept ticking while the visitor was reading the rail or dragging
           it, yanking the slide out from under them mid-gesture.
         - It ran under prefers-reduced-motion, where an unbidden auto-advance
           is precisely the motion the preference asks us not to make.

         Now it stops on hidden, stops while a pointer or the keyboard is
         inside the carousel, and never starts at all under reduced motion. */
      let timer = null;
      const stop = () => {
        if (timer) clearInterval(timer);
        timer = null;
      };
      const start = () => {
        if (timer || reduceMotion() || document.hidden) return;
        timer = setInterval(() => {
          if (seamless) {
            if (getPos() >= maxPos() - 1) {
              // On the clone (a copy of slide 1) — reset to the real slide 1
              // with no animation, then advance. The rail never rewinds.
              jumpInstant(0);
              setPos(slideStep());
            } else {
              setPos(getPos() + slideStep());
            }
          } else if (getPos() >= maxPos()) {
            setPos(0);
          } else {
            setPos(getPos() + slideStep());
          }
        }, 4500);
      };
      root.addEventListener("pointerenter", stop);
      root.addEventListener("pointerleave", start);
      root.addEventListener("focusin", stop);
      root.addEventListener("focusout", start);
      document.addEventListener("visibilitychange", () =>
        document.hidden ? stop() : start(),
      );
      start();
    }
  }

  /* Plain drag-to-scroll for a horizontal overflow row that ISN'T a carousel
     (no slides, no snap, no arrows) — the category filter-chip row on shop
     listing pages. MOUSE-only, exactly like the carousel: a desktop click-drag
     is the one gesture the browser won't turn into a scroll on a
     scrollbar-hidden row, so we drive it by hand. Touch and pen scroll the row
     natively (styles.css leaves it a native `touch-action` scroller), which is
     smoother and never stalls a slightly-diagonal swipe — the same move the
     carousel made (Ahmed, 2026-08-05). Kept separate from initCarousel rather
     than forcing the chip row to become a one-slide carousel it doesn't need. */
  function initDragScroll(el) {
    let active = false;
    let dragging = false;
    let startX = 0, startSL = 0, moved = 0, id = null;

    el.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse") return; // touch/pen scroll natively
      if (e.button !== 0) return;
      // Nothing to drag once xl wraps the chips instead of scrolling them —
      // bail before arming, so a jittery click near the tap-slop threshold
      // never eats a chip's own click on desktop.
      if (el.scrollWidth <= el.clientWidth) return;
      active = true;
      dragging = false;
      moved = 0;
      startX = e.clientX;
      startSL = el.scrollLeft;
      id = e.pointerId;
    });

    el.addEventListener("pointermove", (e) => {
      if (!active || e.pointerId !== id) return;
      const dx = e.clientX - startX;
      if (!dragging && Math.abs(dx) > 4) {
        dragging = true;
        try { el.setPointerCapture(id); } catch (_) {}
      }
      if (dragging) {
        moved = dx;
        el.scrollLeft = startSL - dx;
        e.preventDefault();
      }
    });

    const endDrag = () => {
      active = false;
      dragging = false;
    };
    el.addEventListener("pointerup", endDrag);
    el.addEventListener("pointercancel", endDrag);

    /* Same guard as the carousel: a real drag must not also fire the chip's
       own click/navigation underneath it. */
    el.addEventListener(
      "click",
      (e) => {
        if (Math.abs(moved) > 4) {
          e.preventDefault();
          e.stopPropagation();
        }
        moved = 0;
      },
      true,
    );
  }

  /* ---------------------------------------------------------------
     Accordion / tabs / steppers / forms
     --------------------------------------------------------------- */
  function initAccordions(scope) {
    scope.querySelectorAll("[data-accordion]").forEach((acc) => {
      acc.querySelectorAll(".accordion-item").forEach((item) => {
        const btn = item.querySelector(".accordion-trigger");
        if (!btn) return;
        btn.addEventListener("click", () => {
          const isOpen = item.classList.contains("is-open");
          if (!acc.hasAttribute("data-accordion-multi")) {
            acc
              .querySelectorAll(".accordion-item.is-open")
              .forEach((o) => o.classList.remove("is-open"));
          }
          item.classList.toggle("is-open", !isOpen);
        });
      });
    });
  }

  function initTabs(scope) {
    scope.querySelectorAll("[data-tabs]").forEach((tabs) => {
      const btns = tabs.querySelectorAll(".tab-btn");
      const panels = tabs.querySelectorAll(".tab-panel");
      // Optional sliding pill (Perfect Picks segmented control): one element
      // that moves to sit behind the active chip, so nothing reflows.
      const indicator = tabs.querySelector("[data-tab-indicator]");
      const moveIndicator = () => {
        if (!indicator) return;
        const active = tabs.querySelector(".tab-btn.is-active");
        if (!active) return;
        // A zero measurement means the control is not laid out yet (hidden
        // ancestor, font still swapping, scroll container still resolving).
        // Writing it would COLLAPSE the pill to nothing and leave it that way,
        // since nothing re-measures until the next resize — the failure mode
        // that made the FAQ filter render with no pill at all. Skip instead and
        // let the load/fonts/resize hooks below try again.
        if (!active.offsetWidth) return;
        indicator.style.width = active.offsetWidth + "px";
        indicator.style.transform = "translateX(" + active.offsetLeft + "px)";
      };
      btns.forEach((btn) => {
        btn.addEventListener("click", () => {
          const target = btn.getAttribute("data-tab");
          btns.forEach((b) => b.classList.toggle("is-active", b === btn));
          panels.forEach((p) =>
            p.toggleAttribute("hidden", p.getAttribute("data-panel") !== target),
          );
          moveIndicator();
        });
      });
      if (indicator) {
        moveIndicator();
        window.addEventListener("resize", moveIndicator, { passive: true });
        // Chip widths shift once the web font loads — reposition then.
        if (document.fonts && document.fonts.ready) {
          document.fonts.ready.then(moveIndicator);
        }
        // Belt and braces for the first paint: one more pass on the next frame
        // and again at window load. moveIndicator is idempotent and bails on a
        // zero measurement, so extra calls are free and only ever fix a pill
        // that had nothing to measure the first time.
        requestAnimationFrame(moveIndicator);
        window.addEventListener("load", moveIndicator, { once: true });
      }
    });
  }

  /* ---------------------------------------------------------------
     Product gallery

     Thumbnails swap the main image. Selection is `aria-pressed` and nothing
     else — styles.css draws the ring off that selector — so the accessible
     state and the painted state are the same attribute and cannot drift. The
     same contract the favourites heart uses.

     The swap cross-fades: the main image is faded out, the src is changed
     while it is invisible, and it fades back in once the new file has
     decoded. Waiting on decode matters — swapping src on a visible <img>
     paints a blank frame while the next photo loads, and these are real
     900px photographs, not sprites.
     --------------------------------------------------------------- */
  function initGallery(scope) {
    scope.querySelectorAll("[data-gallery]").forEach((gallery) => {
      const main = gallery.querySelector("[data-gallery-main]");
      const thumbs = [...gallery.querySelectorAll("[data-gallery-thumb]")];
      if (!main || !thumbs.length) return;

      const plate = gallery.querySelector("[data-gallery-plate]");

      const show = (btn) => {
        const img = btn.querySelector("img");
        const src = img && img.getAttribute("src");
        if (!src || src === main.getAttribute("src")) return;

        thumbs.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        /* Carry the fill mode across with the image. The main shot is a
           background-isolated cut-out and has to sit inside the plate's
           padding; the gallery shots are photographs with their own
           backgrounds and fill the frame. Painting a photograph "contain"
           leaves it marooned in a border of plate colour. */
        if (plate) plate.dataset.fill = btn.dataset.fill || "contain";

        const swap = () => {
          main.setAttribute("src", src);
          // Only reveal once the bitmap is ready. decode() is unsupported on
          // older Safari, hence the fallback to the load event.
          const reveal = () => main.removeAttribute("data-swapping");
          if (main.decode) main.decode().then(reveal, reveal);
          else main.addEventListener("load", reveal, { once: true });
        };

        if (reduceMotion()) {
          swap();
          return;
        }
        main.dataset.swapping = "true";
        // One frame of fade-out before the src changes, so the old photo is
        // gone rather than cut. The timeout matches the CSS transition.
        setTimeout(swap, 180);
      };

      thumbs.forEach((btn) => btn.addEventListener("click", () => show(btn)));
    });
  }

  /* ---------------------------------------------------------------
     Size + quantity -> price

     The size chips are real SKUs (see build/fetch_sizes.py), each carrying its
     own live price and product id. Choosing one has to do three things, and
     missing any of them leaves the page lying to the shopper:

       1. repoint the displayed price at that size's price,
       2. repoint `data-price` AND `data-id` on the [data-product] host, so the
          cart adds the SKU that was actually chosen rather than whichever one
          the page happened to render with,
       3. survive the quantity multiplier without compounding.

     (3) is why the unit price lives in its own attribute. Multiplying the
     DISPLAYED number would square it on the second press.
     --------------------------------------------------------------- */
  function initSizeAndPrice(scope) {
    (scope || document).querySelectorAll("[data-product]").forEach((host) => {
      const display = host.querySelector("[data-price-display]");
      if (!display) return;
      const breakdown = host.querySelector("[data-price-breakdown]");
      const qtyEl = host.querySelector("[data-stepper] [data-qty]");
      const chips = [...host.querySelectorAll("[data-size-option]")];

      const paint = () => {
        // Show the SINGLE-ITEM price only (Ahmed, 2026-08-02). Quantity no
        // longer multiplies the figure on the product page — the number the
        // shopper reads here is the unit price of the chosen SKU, and the
        // running order total lives in the cart drawer and summary instead.
        // Size chips still repoint this at the selected SKU's own price.
        const unit = Number(display.dataset.unitPrice) || 0;
        display.textContent = egp(unit);
        if (breakdown) {
          breakdown.hidden = true;
          breakdown.textContent = "";
        }
      };

      chips.forEach((chip) => {
        chip.addEventListener("change", () => {
          if (!chip.checked) return;
          const price = Number(chip.dataset.sizePrice) || 0;
          display.dataset.unitPrice = price;
          // Point the cart at the chosen SKU, not the rendered one.
          host.dataset.price = price;
          if (chip.dataset.sizeId) host.dataset.id = chip.dataset.sizeId;
          paint();
          if (!reduceMotion() && display.animate) {
            display.animate(
              [{ transform: "scale(1)" }, { transform: "scale(1.06)" }, { transform: "scale(1)" }],
              { duration: 240, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
            );
          }
        });
      });

      // The stepper owns the number; this just recomputes after it changes.
      // Listening on the host rather than the buttons keeps it working if the
      // stepper is ever re-rendered.
      host.addEventListener("click", (e) => {
        if (e.target.closest("[data-stepper] [data-step]")) setTimeout(paint, 0);
      });

      paint();
    });
  }

  /* `:not([data-cart-bound])` — a cart-bound stepper is a view of the cart
     line, not an independent counter, so it is driven by the delegated
     handler in the cart section. Binding this one too would give the same
     button two writers: this one would move the local digit while the other
     moved the store, and whichever painted last would win. */
  function initSteppers(scope) {
    scope.querySelectorAll("[data-stepper]:not([data-cart-bound])").forEach((st) => {
      const qtyEl = st.querySelector("[data-qty]");
      st.querySelectorAll("[data-step]").forEach((b) => {
        b.addEventListener("click", () => {
          const delta = parseInt(b.getAttribute("data-step"), 10);
          let v = parseInt(qtyEl.textContent, 10) || 1;
          const next = Math.max(1, v + delta);
          const changed = next !== v;
          qtyEl.textContent = next;
          /* The number slides in from the direction you pressed, so which way
             it moved is legible without reading the digit. At the floor of 1
             nothing changed, so nothing animates — the press is a no-op and
             animating it would imply otherwise. */
          if (changed && !reduceMotion() && qtyEl.animate) {
            qtyEl.animate(
              [
                { transform: "translateY(" + (delta > 0 ? 8 : -8) + "px)", opacity: 0 },
                { transform: "translateY(0)", opacity: 1 },
              ],
              { duration: 200, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
            );
          }
        });
      });
    });
  }

  /* ---------------------------------------------------------------
     Scroll reveal

     Sections fade and rise once, the first time they come into view. This is
     the bulk of what makes the page feel current, and it is cheap: one
     IntersectionObserver, unobserved after firing, and entirely skipped when
     the user asks for reduced motion.

     Anything already on screen at load is revealed immediately without
     animation, so the fold never appears to animate in after the fact.
     --------------------------------------------------------------- */
  function initReveal(scope) {
    const els = [...(scope || document).querySelectorAll("[data-reveal]")];
    if (!els.length) return;
    // Only now does the hidden state exist at all — see the .js-reveal gate in
    // styles.css. Set here rather than in markup so a JS failure degrades to
    // "no animation" instead of "no content".
    document.documentElement.classList.add("js-reveal");
    if (reduceMotion() || !("IntersectionObserver" in window)) {
      els.forEach((el) => el.setAttribute("data-reveal", "in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.setAttribute("data-reveal", "in");
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.06 },
    );
    const pending = [];
    els.forEach((el) => {
      if (el.getBoundingClientRect().top < window.innerHeight) {
        el.setAttribute("data-reveal", "in"); // above the fold: no animation
      } else {
        pending.push(el);
        io.observe(el);
      }
    });

    /*
     * Failsafe. The reveal now applies to every <section> on all 130 pages,
     * so the cost of the observer not firing went from "one home page rail
     * stays faded" to "most of the site does" — and IntersectionObserver
     * does NOT fire in every context (it is inert in a hidden/background
     * document, which is exactly where this was being tested; a
     * default-config control observer did not fire either).
     *
     * The guiding rule for this system has always been that a failure
     * degrades to UNANIMATED, never to INVISIBLE. The .js-reveal gate gives
     * that when JS is off entirely; this gives it when JS runs but the
     * observer never reports. Worst case the shopper gets no animation on
     * content they had not reached yet — which they cannot tell apart from
     * having already scrolled past it.
     *
     * Deliberately not rAF- or scroll-driven: a backgrounded tab throttles
     * both, and this has to survive precisely the case where the observer
     * has already failed.
     */
    if (pending.length) {
      setTimeout(() => {
        pending.forEach((el) => {
          if (el.getAttribute("data-reveal") !== "in") {
            el.setAttribute("data-reveal", "in");
            io.unobserve(el);
          }
        });
      }, 2500);
    }
  }

  function initDemoForms(scope) {
    scope.querySelectorAll("[data-newsletter]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        f.reset();
        toast("تم الاشتراك بنجاح! 🎉");
      }),
    );
    scope.querySelectorAll("[data-location-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        closeOverlay();
        toast("تم تحديث منطقة التوصيل.");
      }),
    );
    scope.querySelectorAll("[data-demo-form]").forEach((f) =>
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        toast(f.getAttribute("data-demo-form") || "تم الإرسال بنجاح.");
        if (f.getAttribute("data-reset") !== "false") f.reset();
        // Optional: navigate to another page after the toast (mock success flow).
        const redirect = f.getAttribute("data-redirect");
        if (redirect) setTimeout(() => (window.location.href = redirect), 850);
      }),
    );
  }

  /* ---------------------------------------------------------------
     Sticky navbar on scroll (desktop) — mirrors useWindowScroll(150)
     --------------------------------------------------------------- */
  function initStickyNav() {
    const nav = document.querySelector("[data-navbar]");
    const actions = Array.prototype.slice.call(
      document.querySelectorAll("[data-sticky-actions]"),
    );
    if (!nav && !actions.length) return;
    let placeholder = null;
    if (nav) {
      placeholder = document.createElement("div");
      nav.parentNode.insertBefore(placeholder, nav.nextSibling);
    }
    let stuck = null;
    function onScroll() {
      const should = window.scrollY > 150;
      if (should === stuck) return;
      stuck = should;
      if (!nav) {
        actions.forEach((el) => {
          if (should) el.dataset.stuck = "true";
          else delete el.dataset.stuck;
        });
        return;
      }
      /* Positioning is driven by data-stuck, not by Tailwind's `fixed`.
         The bar's base classes include `relative`, which ties `.fixed` on
         specificity and wins on source order, so the utility never took
         effect and this bar never actually stuck. styles.css carries the
         real rule. No inline padding either: the <nav> inside is already
         mx-auto px-4 max-w-[1536px], so it centres itself once fixed. */
      const stickyClasses = ["shadow-md", "animate-slideDown"];
      if (should) {
        placeholder.style.height = nav.offsetHeight + "px";
        nav.dataset.stuck = "true";
        nav.classList.add(...stickyClasses);
      } else {
        placeholder.style.height = "0px";
        delete nav.dataset.stuck;
        nav.classList.remove(...stickyClasses);
      }
      // Actions INSIDE the sticky navbar ride along with it (do not re-park them
      // as a floating pill — that would rip them out of the now-fixed bar). Only
      // actions outside the navbar (the mobile masthead, which has no sticky nav)
      // park on scroll.
      document.querySelectorAll("[data-sticky-actions]").forEach((el) => {
        if (nav && nav.contains(el)) { delete el.dataset.stuck; return; }
        if (should) el.dataset.stuck = "true";
        else delete el.dataset.stuck;
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------------------------------------------------------
     Global click / key delegation
     --------------------------------------------------------------- */
  function initDelegation() {
    document.addEventListener("click", (e) => {
      const opener = e.target.closest("[data-open]");
      if (opener) {
        e.preventDefault();
        openOverlay(opener.getAttribute("data-open"));
        return;
      }
      if (e.target.closest("[data-close]")) {
        closeOverlay();
        return;
      }
      if (e.target.classList.contains("overlay-backdrop")) {
        closeOverlay();
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && openEl) closeOverlay();
    });
  }

  /* ---------------------------------------------------------------
     Public re-init hook for dynamically added markup
     --------------------------------------------------------------- */
  /* Password reveal toggles on the auth forms. */
  function initPasswordReveals(scope) {
    // [data-pw-toggle], not [data-reveal]: the latter is the section entrance-
    // animation hook (initReveal), and sharing it swept the eye buttons into
    // that system — see the note in _auth.py password_field.
    scope.querySelectorAll("[data-pw-toggle]").forEach((btn) => {
      const input = scope.getElementById
        ? scope.getElementById(btn.getAttribute("data-pw-toggle"))
        : document.getElementById(btn.getAttribute("data-pw-toggle"));
      if (!input) return;
      btn.addEventListener("click", () => {
        const shown = input.type === "text";
        input.type = shown ? "password" : "text";
        btn.setAttribute(
          "aria-label",
          shown ? "إظهار كلمة السر" : "إخفاء كلمة السر",
        );
      });
    });
  }

  /* ---------------------------------------------------------------
     Listing filter + sort

     The export is static, so filtering happens over the cards already in the
     DOM — no fetch, still works from file://. Cards carry data-cat / data-price
     / data-id from catalog.json.

     Only chips rendered with a `data-filter` slug take part. Sub-category
     chips deliberately have none: the catalogue has no sub-category field, so
     filtering by them would empty the grid (see DESIGN-NOTES).
     --------------------------------------------------------------- */
  const CHIP_ON = ["bg-cta", "text-white", "border-cta"];
  const CHIP_OFF = ["chip-filter", "bg-white", "text-ink",
                    "border-divider", "hover:border-cta"];

  /* ---------------------------------------------------------------
     Cart store

     Single source of truth for cart state, persisted to localStorage so it
     survives navigation between the standalone pages. No fetch — the store
     reads product details straight off `[data-product]` markup, so it works
     from file:// like the rest of the export.

     Every mutation dispatches a `cart:change` CustomEvent on `document`:

       document.addEventListener("cart:change", (e) => {
         e.detail.reason   // "add" | "qty" | "remove" | "clear" | "init"
         e.detail.product  // the item involved (absent for clear/init)
         e.detail.items    // full array after the change
         e.detail.count    // total units
         e.detail.subtotal // EGP
       });

     That event is the hook for micro-interactions — fly-to-cart, badge bounce,
     row collapse — none of which belong in here.
     --------------------------------------------------------------- */
  const CART_KEY = "jaad:cart";

  /*
   * Seed for a first-ever visit only, so a fresh browser does not land on an
   * empty cart and lose the design. Real catalogue items. Written once, on the
   * first load where no cart key exists; after that the shopper owns the cart,
   * including deliberately emptying it.
   */
  /*
   * `id` MUST be the catalog.json product id — the same value product cards
   * carry in `data-id`. These were previously the barcodes lifted off the
   * image filenames ("6223006310759", "2000102000000"), which match no card,
   * so adding a seeded product from its own card created a SECOND line
   * instead of incrementing the first. Keep these in sync with the catalogue.
   */
  // Real Jaad SKUs (catalog.json) — seeds the cart on a first-ever visit so the
  // drawer isn't empty. English names for English-first.
  const CART_SEED = [
    { id: "1", name: "Light Roasted Coffee", price: 45, image: "images/jaad/products-styled/1.jpg", qty: 1 },
    { id: "12", name: "Walnut", price: 65, image: "images/jaad/products-styled/12.jpg", qty: 1 },
  ];

  const Cart = (function () {
    let items = [];

    function load() {
      try {
        const raw = localStorage.getItem(CART_KEY);
        // No key at all = first ever visit, so seed. An empty array is a
        // shopper who emptied their cart on purpose — leave it alone.
        items = raw === null ? CART_SEED.slice() : JSON.parse(raw);
        if (!Array.isArray(items)) items = [];
      } catch (e) {
        items = [];
      }
    }

    function save() {
      try {
        localStorage.setItem(CART_KEY, JSON.stringify(items));
      } catch (e) {
        /* private mode — state still lives for this page view */
      }
    }

    function subtotal() {
      return items.reduce((s, it) => s + Number(it.price) * it.qty, 0);
    }
    function count() {
      return items.reduce((s, it) => s + it.qty, 0);
    }

    function emit(reason, product) {
      save();
      document.dispatchEvent(
        new CustomEvent("cart:change", {
          detail: { reason: reason, product: product || null, items: items.slice(), count: count(), subtotal: subtotal() },
        }),
      );
    }

    return {
      init: function () {
        load();
        emit("init");
      },
      items: function () {
        return items.slice();
      },
      count: count,
      subtotal: subtotal,
      find: function (id) {
        return items.find((it) => String(it.id) === String(id)) || null;
      },
      add: function (product, qty) {
        qty = Math.max(1, parseInt(qty, 10) || 1);
        const existing = items.find((it) => String(it.id) === String(product.id));
        if (existing) existing.qty += qty;
        else items.push({ id: product.id, name: product.name, price: Number(product.price), image: product.image, qty: qty });
        emit("add", product);
        return this;
      },
      setQty: function (id, qty) {
        const it = items.find((x) => String(x.id) === String(id));
        if (!it) return this;
        qty = parseInt(qty, 10) || 0;
        if (qty < 1) return this.remove(id);
        it.qty = qty;
        emit("qty", it);
        return this;
      },
      remove: function (id) {
        const i = items.findIndex((x) => String(x.id) === String(id));
        if (i === -1) return this;
        const [gone] = items.splice(i, 1);
        emit("remove", gone);
        return this;
      },
      clear: function () {
        items = [];
        emit("clear");
        return this;
      },
    };
  })();

  window.jaadCart = Cart;

  /* ---------------------------------------------------------------
     Favourites store

     Deliberately the same shape as the cart store above: localStorage, no
     fetch, product details read straight off `[data-product]` markup so it
     works from file://. Items are {id, name, price, image} — no qty, a
     product is either saved or it isn't.

     Every mutation dispatches a `favs:change` CustomEvent on `document`:

       document.addEventListener("favs:change", (e) => {
         e.detail.reason   // "add" | "remove" | "clear" | "init"
         e.detail.product  // the item involved (absent for clear/init)
         e.detail.items    // full array after the change
         e.detail.count    // number saved
       });

     Before this the heart button on every product card was inert markup —
     184 of them across 7 pages, with no handler anywhere in this file.
     --------------------------------------------------------------- */
  const FAVS_KEY = "jaad:favs";

  /*
   * Seeded on a first-ever visit only, exactly like CART_SEED and for the
   * same reason: my-account-favorites.html used to hard-code six products,
   * so a fresh browser would otherwise land on an empty favourites page and
   * lose the design. These are those same six, by real catalogue id. Once
   * the shopper touches a heart this is never consulted again.
   */
  // Real Jaad SKUs (catalog.json) — seeds the favourites demo and pads the
  // recently-viewed rail so it is never sparse. English names for English-first.
  const FAVS_SEED = [
    { id: "1", name: "Light Roasted Coffee", price: 45, image: "images/jaad/products-styled/1.jpg" },
    { id: "2", name: "Medium Roasted Coffee", price: 45, image: "images/jaad/products-styled/2.jpg" },
    { id: "3", name: "Dark Roasted Coffee", price: 45, image: "images/jaad/products-styled/3.jpg" },
    { id: "12", name: "Walnut", price: 65, image: "images/jaad/products-styled/12.jpg" },
    { id: "11", name: "Almond", price: 85, image: "images/jaad/products-styled/11.jpg" },
  ];

  /* White-background original per SKU id, for the product-image style toggle.
     JS-built cards (Recently Viewed) carry only the scene path in their seed /
     Recent store, and the originals are slug-named, so this maps id -> original.
     Generated from catalog.json; keep in sync if the catalog SKUs change. */
  /* Pack weight per product id, mirroring `weight` in data/catalog.json.
     PLACEHOLDER figures — see catalog.weight() in build/catalog.py for why they
     exist and what has to replace them.

     A literal for the same reason PLAIN_BY_ID below is one: the drawer, the
     cart page and the recent rail are all built before any fetch could land,
     and they are handed product objects from localStorage and from the cart
     store, neither of which carries a weight. Keyed by id so whatever a caller
     hands over, the size shown is the catalogue's.

     KEEP IN STEP with catalog.json — this is a copy, and a SKU whose weight
     changes there and not here will show the old figure in the cart while the
     card shows the new one. */
  const WEIGHT_BY_ID = {"1":250,"2":250,"3":250,"4":250,"5":250,"6":250,"7":250,"8":250,"9":200,"10":200,"11":250,"12":200,"13":75,"14":100,"15":75,"16":100,"17":50,"18":75,"19":100,"20":100,"21":50,"22":50,"23":100,"24":75,"25":75,"26":75};
  function weightOf(id) {
    const w = WEIGHT_BY_ID[String(id)];
    return w ? w + " " + t("جم") : "";
  }

  const PLAIN_BY_ID = {"1":"images/jaad/products/coffee-light-plain.png","2":"images/jaad/products/coffee-medium-plain.png","3":"images/jaad/products/coffee-dark-plain.png","4":"images/jaad/products/coffee-light-cardamom.png","5":"images/jaad/products/coffee-medium-cardamom.png","6":"images/jaad/products/coffee-dark-cardamom.png","7":"images/jaad/products/coffee-espresso.png","8":"images/jaad/products/nuts-cashew.png","9":"images/jaad/products/nuts-hazelnut.png","10":"images/jaad/products/nuts-pistachio.png","11":"images/jaad/products/nuts-almond.png","12":"images/jaad/products/nuts-walnut.png","13":"images/jaad/products/spices-chili.png","14":"images/jaad/products/spices-turmeric.png","15":"images/jaad/products/spices-ginger.png","16":"images/jaad/products/spices-coriander.png","17":"images/jaad/products/spices-nutmeg.png","18":"images/jaad/products/spices-cinnamon.png","19":"images/jaad/products/spices-paprika.png","20":"images/jaad/products/spices-black-pepper.png","21":"images/jaad/products/spices-cardamom.png","22":"images/jaad/products/spices-cloves.png","23":"images/jaad/products/spices-cumin.png","24":"images/jaad/products/spices-meat.png","25":"images/jaad/products/spices-chicken.png","26":"images/jaad/products/spices-fish.png"};

  const Favs = (function () {
    let items = [];

    function load() {
      try {
        const raw = localStorage.getItem(FAVS_KEY);
        // No key = first ever visit, so seed. An empty array is a shopper who
        // cleared their favourites on purpose — leave it alone.
        items = raw === null ? FAVS_SEED.slice() : JSON.parse(raw);
        if (!Array.isArray(items)) items = [];
      } catch (e) {
        items = [];
      }
    }

    function save() {
      try {
        localStorage.setItem(FAVS_KEY, JSON.stringify(items));
      } catch (e) {
        /* private mode — state still lives for this page view */
      }
    }

    function emit(reason, product) {
      save();
      document.dispatchEvent(
        new CustomEvent("favs:change", {
          detail: { reason: reason, product: product || null, items: items.slice(), count: items.length },
        }),
      );
    }

    return {
      init: function () {
        load();
        emit("init");
      },
      items: function () {
        return items.slice();
      },
      count: function () {
        return items.length;
      },
      has: function (id) {
        return items.some((it) => String(it.id) === String(id));
      },
      add: function (product) {
        if (this.has(product.id)) return this;
        items.push({ id: product.id, name: product.name, price: Number(product.price), image: product.image });
        emit("add", product);
        return this;
      },
      remove: function (id) {
        const i = items.findIndex((x) => String(x.id) === String(id));
        if (i === -1) return this;
        const [gone] = items.splice(i, 1);
        emit("remove", gone);
        return this;
      },
      /* Returns the new state, so callers can react without re-querying. */
      toggle: function (product) {
        if (this.has(product.id)) {
          this.remove(product.id);
          return false;
        }
        this.add(product);
        return true;
      },
      clear: function () {
        items = [];
        emit("clear");
        return this;
      },
    };
  })();

  window.jaadFavs = Favs;

  /* ---------------------------------------------------------------
     Recently viewed — window.jaadRecent, localStorage `jaad:recent`.

     Same store contract as Cart and Favs: load once, mutate through one
     object, persist to localStorage, broadcast a `recent:change`
     CustomEvent on every write. No seed data, unlike Cart/Favs — those
     exist so a first-ever visit is not empty by design; a shopper who has
     genuinely viewed nothing yet SHOULD see nothing here.

     Holds each product's own id/name/price/image, captured off the page's
     `[data-record-view]` host at view time (via `productFrom`, the same
     helper the cart uses) rather than a bare id resolved against
     catalog.json later. `loadCatalog()` is documented as the ONE feature
     that fetches the catalogue, and everything else works from file:// —
     keeping this store self-contained, like the cart and favourites cards,
     means the "previously seen" rail does not quietly become a second
     fetch dependency.
     --------------------------------------------------------------- */
  const RECENT_KEY = "jaad:recent";
  const RECENT_MAX = 12;

  const Recent = (function () {
    let items = [];

    function load() {
      try {
        const raw = localStorage.getItem(RECENT_KEY);
        items = raw === null ? [] : JSON.parse(raw);
        if (!Array.isArray(items)) items = [];
      } catch (e) {
        items = [];
      }
    }

    function save() {
      try {
        localStorage.setItem(RECENT_KEY, JSON.stringify(items));
      } catch (e) {
        /* private mode — state still lives for this page view */
      }
    }

    function emit(reason) {
      save();
      document.dispatchEvent(
        new CustomEvent("recent:change", {
          detail: { reason: reason, items: items.slice(), count: items.length },
        }),
      );
    }

    return {
      init: function () {
        load();
      },
      items: function () {
        return items.slice();
      },
      // Most-recently-viewed first, with `id` excluded — a product's own
      // page must never list itself among "شاهدت هذا مؤخراً".
      exclude: function (id) {
        return items.filter((x) => String(x.id) !== String(id));
      },
      add: function (product) {
        if (!product || !product.id) return this;
        items = items.filter((x) => String(x.id) !== String(product.id));
        items.unshift({
          id: product.id,
          name: product.name,
          price: Number(product.price) || 0,
          image: product.image,
        });
        if (items.length > RECENT_MAX) items.length = RECENT_MAX;
        emit("add");
        return this;
      },
      clear: function () {
        items = [];
        emit("clear");
        return this;
      },
    };
  })();

  window.jaadRecent = Recent;

  /* ---------------------------------------------------------------
     Demo auth

     A local stand-in for a real session so the account and favourites
     flows can actually be walked end to end. Same contract as the two
     stores above: localStorage, no fetch, an `auth:change` event.

     THIS IS NOT AUTHENTICATION. The credentials are hard-coded below and
     printed on the sign-in page; the check happens in client-side JS that
     anyone can read. It exists so the logged-in chrome and the favourites
     flow are demonstrable in a static export. **Rip this out and replace it
     with the real backend before launch** — see DESIGN-NOTES.
     --------------------------------------------------------------- */
  const AUTH_KEY = "jaad:auth";
  const PENDING_KEY = "jaad:authPending";
  // Passwordless now (Ahmed, 2026-08-04): sign-in is a mobile number then an
  // OTP. This is still a static export with no SMS backend, so verification is
  // a stand-in — any mobile is accepted and any well-formed 6-digit code passes
  // (the on-screen "test code" hint was removed, Ahmed 2026-08-04). Rip this out
  // with the rest of the demo auth before launch (DESIGN-NOTES).
  const DEMO_USER = {
    email: "demo@jad.com",
    name: "محمد عادل",
    nameEn: "Mohamed Adel",
    mobile: "01000000000",
  };

  const Auth = (function () {
    let user = null;

    function emit(reason) {
      try {
        if (user) localStorage.setItem(AUTH_KEY, JSON.stringify(user));
        else localStorage.removeItem(AUTH_KEY);
      } catch (e) {
        /* private mode — the session still holds for this page view */
      }
      document.dispatchEvent(
        new CustomEvent("auth:change", { detail: { reason: reason, user: user } }),
      );
    }

    // A pending flow survives the hop to the OTP page (which is a separate
    // document), so the verify page knows the mobile, the mode and where to
    // return afterwards.
    function readPending() {
      try {
        return JSON.parse(localStorage.getItem(PENDING_KEY) || "null");
      } catch (e) {
        return null;
      }
    }
    function writePending(p) {
      try {
        if (p) localStorage.setItem(PENDING_KEY, JSON.stringify(p));
        else localStorage.removeItem(PENDING_KEY);
      } catch (e) {
        /* ignore */
      }
    }

    return {
      demo: DEMO_USER,
      init: function () {
        try {
          const raw = localStorage.getItem(AUTH_KEY);
          user = raw ? JSON.parse(raw) : null;
        } catch (e) {
          user = null;
        }
        emit("init");
      },
      user: function () {
        return user ? Object.assign({}, user) : null;
      },
      isAuthed: function () {
        return !!user;
      },
      pending: readPending,
      /* Passwordless login: stash the mobile (and where to return afterwards)
         and hand off to the OTP page, which is the real gate. */
      startLogin: function (mobile, next) {
        const p = { mode: "login", mobile: String(mobile || "").trim(), next: next || "" };
        writePending(p);
        return p;
      },
      startRegister: function (data, next) {
        const p = {
          mode: "register",
          next: next || "",
          firstName: String(data.firstName || "").trim(),
          lastName: String(data.lastName || "").trim(),
          mobile: String(data.mobile || "").trim(),
          email: String(data.email || "").trim(),
        };
        writePending(p);
        return p;
      },
      /* Verify the OTP against the pending flow. On success the user is signed
         in — created from the pending record on register, with the email left
         UNVERIFIED so the dashboard can prompt for it — and pending is cleared.
         Returns { ok, next } / { ok:false, reason }. */
      verifyOtp: function (code) {
        const p = readPending();
        if (!p) return { ok: false, reason: "no-pending" };
        // No SMS backend: any well-formed 6-digit code passes (demo).
        if (!/^\d{6}$/.test(String(code || "").trim())) return { ok: false, reason: "bad-otp" };
        if (p.mode === "register") {
          const full = [p.firstName, p.lastName].filter(Boolean).join(" ") || DEMO_USER.name;
          user = {
            name: p.firstName || DEMO_USER.name,
            full: full,
            nameEn: DEMO_USER.nameEn,
            email: p.email || "",
            mobile: p.mobile,
            emailVerified: false,
          };
        } else {
          user = {
            name: DEMO_USER.name,
            full: DEMO_USER.name,
            nameEn: DEMO_USER.nameEn,
            email: DEMO_USER.email,
            mobile: p.mobile || DEMO_USER.mobile,
            emailVerified: true,
          };
        }
        writePending(null);
        emit("login");
        return { ok: true, next: p.next || "" };
      },
      /* Mark the signed-in user's email verified — the dashboard banner. */
      verifyEmail: function () {
        if (!user) return false;
        user.emailVerified = true;
        emit("email-verified");
        return true;
      },
      logout: function () {
        user = null;
        writePending(null);
        emit("logout");
        return this;
      },
    };
  })();

  window.jaadAuth = Auth;

  /* Read a product off the nearest [data-product] element. */
  function productFrom(el) {
    const host = el.closest("[data-product]");
    if (!host) return null;
    const d = host.dataset;
    if (!d.id || !d.name) return null;
    return { id: d.id, name: d.name, price: Number(d.price) || 0, image: d.image || "" };
  }

  const egp = (n) => "EGP " + (Math.round(n * 100) / 100).toFixed(2);

  /* ---------------------------------------------------------------
     Language switcher

     Flips `dir` and `lang` on <html> so the RTL↔LTR layout can actually be
     exercised, and remembers the choice across pages via localStorage.

     It does NOT translate copy. Every string in this build is Arabic — there
     is no English content to switch to, and machine-translating the client's
     store into English would be inventing copy. So English mode is an
     honest direction/layout test: the writing direction, logical properties
     and mirrored components all flip, the words do not. Real bilingual
     support is a separate piece of work needing English copy (DESIGN-NOTES).
     --------------------------------------------------------------- */
  const LANG_KEY = "jaad:lang";

  function applyLang(code) {
    const l = LANGS.find((x) => x.code === code) || LANGS[1];
    const c = currentCountry();
    document.documentElement.setAttribute("lang", l.code);
    document.documentElement.setAttribute("dir", l.dir);
    document.querySelectorAll("[data-lang-label]").forEach((el) => {
      el.textContent = l.code === "ar" ? c.short + " (العربية)" : c.en + " (English)";
    });
    document.querySelectorAll("[data-country-flag]").forEach((el) => {
      el.src = c.flag;
    });
    try {
      localStorage.setItem(LANG_KEY, l.code);
    } catch (e) {
      /* private mode — the toggle still works for this page view */
    }
  }

  /*
   * Re-render the JS-injected chrome in the new language and swap product
   * titles to the English names that already exist in catalog.json. Body copy
   * baked into the page stays Arabic — there is no English source for it.
   */
  /* Apply the current language to build-time page content: the catalogue's
     real English product names, then the exact-match dictionary pass.

     Split out of repaintForLang() so it can ALSO run on first paint. Without
     that, opening any page with English already stored left every build-time
     string in Arabic — the JS-injected chrome came out English because it is
     rendered through t() at render time, but translateDocument() only ever
     ran on a toggle click, never on load. So the language appeared to change
     on the page you clicked and then half-revert on every page you navigated
     to. */
  function applyLangToContent() {
    // data-name is Arabic, data-name-en is the catalogue's real English
    // name. Nothing invented here.
    const en = currentLang() === "en";
    document.querySelectorAll("[data-product][data-name-en]").forEach((card) => {
      const target = card.querySelector("[data-product-title]");
      if (!target) return;
      target.textContent = en ? card.dataset.nameEn : card.dataset.name;
    });
    translateDocument();
  }

  function repaintForLang() {
    const header = document.getElementById("site-header");
    const footer = document.getElementById("site-footer");
    const overlays = document.getElementById("site-overlays");
    if (header) header.innerHTML = headerHTML();
    if (footer) footer.innerHTML = footerHTML();
    if (overlays) overlays.innerHTML = overlaysHTML();

    applyLangToContent();

    initMegaMenu();
    initFlashCountdown();
    initLangSwitcher(true);
    window.kInit(document);
    renderCart();
    document.dispatchEvent(new CustomEvent("auth:change", { detail: { reason: "lang", user: Auth.user() } }));
    // Heart aria-labels come from t(), so they have to be re-derived here —
    // repaint replaces the chrome but the cards are build-time markup.
    syncFavButtons();
  }

  function initLangSwitcher(skipApply) {
    if (!skipApply) {
      let stored = "ar";
      try {
        stored = localStorage.getItem(LANG_KEY) || "en";
      } catch (e) {
        /* ignore */
      }
      applyLang(stored);
    }

    /* The choices live in the locale modal now and commit on تطبيق alone —
       one repaint however much changed. Delegated on document (bound once,
       via the guard below) so it survives the chrome re-render that apply
       itself triggers. */
    if (initLangSwitcher._bound) return;
    initLangSwitcher._bound = true;
    document.addEventListener("click", (e) => {
      const apply = e.target.closest("[data-locale-apply]");
      if (!apply) return;
      const modal = apply.closest('[data-sheet="locale"]');
      const country = modal.querySelector('input[name="locale-country"]:checked');
      const lang = modal.querySelector('input[name="locale-lang"]:checked');
      const langChanged = lang && lang.value !== currentLang();
      const countryChanged = country && country.value !== currentCountry().code;
      if (country) {
        try {
          localStorage.setItem(COUNTRY_KEY, country.value);
        } catch (err) {
          /* ignore */
        }
      }
      closeOverlay();
      if (!langChanged && !countryChanged) return;
      // One repaint covers both: applyLang re-reads the country for the
      // masthead label, and repaintForLang rebuilds the chrome (including
      // this modal, whose checked states are written at render time).
      applyLang(lang ? lang.value : currentLang());
      repaintForLang();
      toast("تم تطبيق التفضيلات");
    });

    // Direct language toggle in the top strip (Ahmed, 2026-08-18): clicking
    // "العربية" / "English" flips the language immediately — no locale popup.
    document.addEventListener("click", (e) => {
      const tog = e.target.closest("[data-lang-toggle]");
      if (!tog) return;
      applyLang(currentLang() === "ar" ? "en" : "ar");
      repaintForLang();
    });
  }

  /* ---------------------------------------------------------------
     Cart rendering — drawer body, badge, cart page

     Everything here is a pure function of Cart state and re-runs on
     `cart:change`. Nothing mutates state; the handlers below do that.
     --------------------------------------------------------------- */
  const DELIVERY_FEE = 30;
  /* The 150 EGP minimum-order rule is GONE (Ahmed, 2026-08-23). It blocked the
     checkout CTA on every basket under 150 and printed a red "you still need
     EGP X" line in the drawer, the cart page and the summary — a rule the store
     no longer enforces, so a EGP 45 bag of coffee is now a complete order. The
     free-DELIVERY threshold (FREE_SHIP) is untouched: that one rewards a bigger
     basket rather than refusing a small one. */
  /* Free delivery above this basket subtotal (Ahmed, 2026-08-02). The cart's
     progress bar counts up to it, and renderCart zeroes the delivery fee — and
     therefore the total — the moment it is reached, so the bar is a real
     incentive rather than decoration. */
  const FREE_SHIP = 500;

  /* ---------------------------------------------------------------
     Fly-to-target

     Clones a bit of the page, arcs it to a destination, and resolves when it
     lands. Used for add-to-cart (the product image flies to the cart) and for
     favouriting (a heart flies to the account button).

     Deliberately a ghost clone on `position: fixed` rather than moving the
     real node: the real card must stay put and keep working, and a fixed
     ghost is immune to whatever scroll container it started in.
     --------------------------------------------------------------- */
  const reduceMotion = () =>
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let badgeHold = 0;

  /*
   * Directional roll for a counter. The new value slides in from below on an
   * increment and from above on a decrement, so the motion itself says which
   * way the number went — a swap-and-pulse only says "something changed".
   * The write happens unconditionally; only the motion is optional, so
   * reduced-motion users get the same truth without the ride.
   */
  function rollTo(el, value, dir) {
    const next = String(value);
    if (el.textContent === next) return;
    el.textContent = next;
    if (reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "translateY(" + (dir < 0 ? "-0.55em" : "0.55em") + ")", opacity: 0 },
        { transform: "translateY(0)", opacity: 1 },
      ],
      { duration: 240, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  function syncCartBadges() {
    const n = Cart.count();
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      const old = parseInt(el.textContent, 10) || 0;
      // Only a badge the shopper can currently see earns the roll — animating
      // inside a hidden badge, or on first paint, is motion with no witness.
      if (el.hidden || !el.offsetParent || old === n) el.textContent = n;
      else rollTo(el, n, n > old ? 1 : -1);
      el.hidden = n === 0;
    });
  }

  /* The catch: the destination dips under the landing's weight and springs
     back. Deliberately smaller travel than pulse() — it plays on the whole
     48px cart button, where a 1.28 spike reads as a glitch, not a catch. */
  function squash(el) {
    if (!el || reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(0.9)", offset: 0.3 },
        { transform: "scale(1.06)", offset: 0.65 },
        { transform: "scale(1)" },
      ],
      { duration: 360, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  /* A short scale pulse on the destination, so the landing is felt. */
  function pulse(el) {
    if (!el || reduceMotion() || !el.animate) return;
    el.animate(
      [
        { transform: "scale(1)" },
        { transform: "scale(1.28)", offset: 0.4 },
        { transform: "scale(0.94)", offset: 0.72 },
        { transform: "scale(1)" },
      ],
      { duration: 420, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
    );
  }

  /* A small burst from the centre of `el` — the "you just saved money" beat on
     the wallet toggle. Deliberately modest: a dozen 6px dots on the brand
     greens over roughly half a second, no sound, no full-screen confetti. It
     marks a discount on a shopping cart, not a prize.

     Fixed-position particles appended to <body>, like the fly-to-cart ghost,
     so no ancestor's overflow can clip them — the toggle sits inside the
     summary column, which is exactly the kind of box that would. They are
     removed on their own animation end, and the wrapper is pointer-events:none
     so it can never swallow a click on the switch underneath.

     Skipped entirely under reduced motion, where the toast is the whole
     feedback. Also skipped when Element.animate is missing rather than
     hand-rolling a fallback: this is decoration, and its absence costs the
     shopper nothing. */
  function celebrate(el) {
    if (!el || reduceMotion() || !el.animate) return;
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const wrap = document.createElement("div");
    wrap.style.cssText =
      "position:fixed;left:0;top:0;width:0;height:0;z-index:120;pointer-events:none";
    const colors = ["#00451C", "#006328", "#618F2B", "#8ACC3E", "#ffffff"];
    for (let i = 0; i < 12; i++) {
      const dot = document.createElement("span");
      const angle = (Math.PI * 2 * i) / 12 + Math.random() * 0.4;
      const dist = 46 + Math.random() * 38;
      dot.style.cssText =
        "position:fixed;width:6px;height:6px;border-radius:9999px;left:" +
        cx + "px;top:" + cy + "px;background:" + colors[i % colors.length];
      wrap.appendChild(dot);
      dot.animate(
        [
          { transform: "translate(-50%,-50%) scale(0.4)", opacity: 1 },
          {
            transform:
              "translate(calc(-50% + " + Math.cos(angle) * dist + "px), calc(-50% + " +
              Math.sin(angle) * dist + "px)) scale(1)",
            opacity: 1,
            offset: 0.55,
          },
          {
            transform:
              "translate(calc(-50% + " + Math.cos(angle) * (dist + 16) + "px), calc(-50% + " +
              Math.sin(angle) * (dist + 16) + "px)) scale(0.3)",
            opacity: 0,
          },
        ],
        { duration: 520 + Math.random() * 220, easing: "cubic-bezier(0.2,0.8,0.2,1)" },
      );
    }
    document.body.appendChild(wrap);
    setTimeout(() => wrap.remove(), 900);
    pulse(el);
  }

  /*
   * `ghostHTML` overrides what flies; by default the source element is cloned.
   * Resolves as soon as the ghost lands (or immediately when motion is
   * reduced / the geometry is unusable), so callers can chain the landing
   * beat without caring which happened.
   *
   * The flight is two staged movements, not one:
   *
   *   1. PICK UP — the ghost stays exactly where the source is and condenses
   *      into a small rounded, shadowed white tile. The product visibly
   *      gathers into something pocket-sized before anything is thrown.
   *   2. THROW — the tile arcs to the target and shrinks the rest of the way
   *      into the cart, carrying its gathered scale the whole distance.
   *
   * Splitting them is the whole reason this reads as smooth. One keyframe
   * list that both gathers and travels has to compromise its easing across the
   * two, and the throw ends up starting before the eye has found the thing
   * being thrown — which is exactly what the single-stage version did.
   *
   * opts.card   — draw the tile chrome. Hearts fly bare (opts omitted).
   * opts.quick  — tighter and faster, for repeat taps on a card stepper.
   * opts.tag    — small text chip riding along with the tile, e.g. "+1".
   */
  /* Fly-to-cart style, chosen at the switch (default the inherited arc). Only the
     THROW stage differs between them — pick-up, clamp, ghost/plate scaffolding
     and the landing resolve are shared. */
  function currentFlyStyle() {
    const s = document.documentElement.getAttribute("data-fly");
    return s === "drop" || s === "comet" ? s : "arc";
  }

  function flyTo(sourceEl, targetEl, ghostHTML, opts) {
    opts = opts || {};
    const style = currentFlyStyle();
    if (!sourceEl || !targetEl || reduceMotion() || !document.body.animate) {
      return Promise.resolve(false);
    }
    const s = sourceEl.getBoundingClientRect();
    const t = targetEl.getBoundingClientRect();
    if (!s.width || !s.height || !t.width) return Promise.resolve(false);

    const ghost = document.createElement("div");
    ghost.className = "fly-ghost" + (opts.card ? " fly-ghost--card" : "");
    ghost.style.cssText =
      "position:fixed;z-index:200;pointer-events:none;left:" +
      s.left + "px;top:" + s.top + "px;width:" + s.width + "px;height:" + s.height + "px;";

    /* The plate is a separate node from the ghost so the two stages never
       fight over one transform: the plate owns the pick-up scale (a CSS
       transition), the ghost owns the travel (a WAAPI animation). */
    const plate = document.createElement("div");
    plate.className = "fly-ghost__plate";
    if (ghostHTML) plate.innerHTML = ghostHTML;
    else {
      const clone = sourceEl.cloneNode(true);
      clone.removeAttribute("id");
      clone.style.width = "100%";
      clone.style.height = "100%";
      plate.appendChild(clone);
    }
    ghost.appendChild(plate);
    if (opts.tag) {
      const tag = document.createElement("span");
      tag.className = "fly-ghost__tag latin";
      tag.textContent = opts.tag;
      ghost.appendChild(tag);
    }
    document.body.appendChild(ghost);

    /*
     * Clamp the destination into the viewport.
     *
     * Normally the cart button is on screen wherever you are on the page:
     * [data-sticky-actions] goes position:fixed once you scroll and parks it
     * at top 68. But that only happens on a scroll *handler*, so there is a
     * window — a click landing in the same tick as a programmatic scroll, or
     * any page without that bar — where the only cart button is the masthead
     * one, sitting a thousand-odd pixels above the viewport. Measured at -1514
     * from the home page's first rail. Unclamped, the item is thrown off the
     * top of the screen and the shopper sees nothing but the badge tick.
     * Clamping keeps the heading and stops the item at the edge instead; when
     * the target is already visible this is inert.
     */
    const edge = 24;
    const tx = t.left + t.width / 2;
    const ty = Math.min(Math.max(t.top + t.height / 2, edge), window.innerHeight - edge);

    const dx = tx - (s.left + s.width / 2);
    const dy = ty - (s.top + s.height / 2);
    // Arc height scales with distance but is capped, so a short hop does not
    // loop absurdly and a long one still reads as a throw rather than a slide.
    const lift = Math.min(160, Math.hypot(dx, dy) * 0.32) + 40;

    const pickupMs = opts.card ? (opts.quick ? 150 : 230) : 0;
    const flightMs = (opts.quick ? 560 : 700) * (style === "comet" ? 0.7 : 1);

    /* Force a style flush so the transition has a resolved start value to
       move away from. Deliberately NOT requestAnimationFrame: rAF does not
       fire in a backgrounded tab, so the pick-up would be skipped there and
       could then land *after* the throw had already removed the class. */
    if (pickupMs) {
      void ghost.offsetWidth;
      ghost.classList.add("is-picked");
    }

    return new Promise((resolve) => {
      let done = false;
      const finish = () => {
        if (done) return;
        done = true;
        ghost.remove();
        resolve(true);
      };

      const throwIt = () => {
        // `is-picked` deliberately STAYS on for the whole flight. It is what
        // holds the plate at its gathered-up scale, and dropping it here would
        // ease the tile back to full size just as it starts travelling — the
        // ghost would visibly swell in mid-air. The ghost's own scale keyframes
        // multiply with the plate's, so the tile keeps shrinking all the way
        // into the cart.
        //
        // The path is SAMPLED, not three-point. WAAPI interpolates keyframes
        // linearly in transform space, so with only start/apex/end the "arc"
        // was two straight lines with a corner at the apex — visible on every
        // long throw. Sixteen samples along a real parabola cost nothing and
        // the corner disappears. Time-easing rides on the sample spacing
        // (easeInOut on p), so the overall easing stays: gathers speed,
        // crests, decelerates into the cart.
        const N = 16;
        const frames = [];
        for (let i = 0; i <= N; i++) {
          const t = i / N;
          let x, y, sx, sy, rot, op;
          if (style === "drop") {
            /* DROP-&-BAG: horizontal settles fast, vertical accelerates like
               gravity, and the tile splats — squashing wide-and-flat over the
               last stretch — as it drops into the cart. */
            const px = 1 - (1 - t) * (1 - t);
            const py = t * t;
            const hop = Math.min(40, lift * 0.35);
            x = dx * px;
            y = dy * py - hop * Math.sin(Math.PI * t);
            const base = 1 - 0.72 * t;
            sx = base; sy = base;
            if (t > 0.82) { const k = (t - 0.82) / 0.18; sx = base * (1 + 0.55 * k); sy = base * (1 - 0.5 * k); }
            rot = 0;
            op = t < 0.86 ? 1 : 1 - ((t - 0.86) / 0.14) * 0.85;
          } else if (style === "comet") {
            /* COMET STREAK: a dead-straight, fast shot to the cart — no arc.
               The speed read comes from the fading trail discs spawned below. */
            const p = t;
            x = dx * p;
            y = dy * p;
            sx = sy = 1 - 0.72 * p;
            rot = 0;
            op = p < 0.85 ? 1 : 1 - ((p - 0.85) / 0.15) * 0.9;
          } else {
            /* ARC (default, inherited): sampled parabola with a held tilt.
               sin(pi*p) peaks at `lift` mid-flight and lands at 0 — a real
               curve, no corner at the apex. */
            const p = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
            x = dx * p;
            y = dy * p - lift * Math.sin(Math.PI * p);
            sx = sy = 1 - 0.84 * p;
            rot = -7 * Math.sin(Math.PI * p) + 4 * p;
            op = p < 0.8 ? 1 : 1 - ((p - 0.8) / 0.2) * 0.85;
          }
          frames.push({
            transform:
              "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px) " +
              "scale(" + sx.toFixed(3) + "," + sy.toFixed(3) + ") rotate(" + rot.toFixed(2) + "deg)",
            opacity: op,
            offset: t,
          });
        }

        /* Comet tail: a handful of shrinking, fading discs fired down the same
           straight vector, each lagging a little further behind the head. Tinted
           to the active button theme so the streak matches the palette. */
        if (style === "comet") {
          const cx = s.left + s.width / 2, cy = s.top + s.height / 2;
          const tint = document.documentElement.getAttribute("data-btn") === "v2" ? "#EA983E" : "#1A733E";
          for (let k = 1; k <= 5; k++) {
            const size = 16 - k * 1.6;
            const dot = document.createElement("div");
            dot.style.cssText =
              "position:fixed;z-index:199;pointer-events:none;border-radius:50%;left:" +
              (cx - size / 2) + "px;top:" + (cy - size / 2) + "px;width:" + size +
              "px;height:" + size + "px;background:" + tint + ";";
            document.body.appendChild(dot);
            const da = dot.animate(
              [
                { transform: "translate(0,0) scale(1)", opacity: 0.55 - k * 0.08, offset: 0 },
                { transform: "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(0.2)", opacity: 0, offset: 1 },
              ],
              { duration: flightMs, delay: k * 26, easing: "cubic-bezier(0.4,0,0.7,1)", fill: "forwards" },
            );
            da.onfinish = () => dot.remove();
            setTimeout(() => dot.remove(), flightMs + k * 26 + 500);
          }
        }

        const anim = ghost.animate(frames, {
          duration: flightMs, easing: "linear", fill: "forwards",
        });
        anim.onfinish = finish;
      };

      setTimeout(throwIt, pickupMs);
      // Belt and braces: if the tab is backgrounded the animation may never
      // fire onfinish, and a stranded ghost would sit over the page forever.
      setTimeout(finish, pickupMs + flightMs + 700);
    });
  }

  /* The visible cart button for the current breakpoint. Both exist in the
     DOM at all times; only one is laid out. */
  function visibleCartButton() {
    return (
      [...document.querySelectorAll('[data-open="cart"]')].find(
        (b) => b.getBoundingClientRect().width > 0,
      ) || null
    );
  }

  function visibleAccountTarget() {
    return (
      [...document.querySelectorAll("[data-fav-target], [data-account-link]")].find(
        (b) => b.getBoundingClientRect().width > 0,
      ) || null
    );
  }

  /*
   * Empty cart.
   *
   * Was a bare centred <p> reading "سلتك فارغة." — a dead end with nothing to
   * look at and nowhere to go, in a container otherwise sized for a list.
   * Built to the SAME shape as the favourites empty state (glyph, heading,
   * one supporting line, one CTA) and reusing its exact CTA label, so the two
   * empty states in this build read as one idea rather than two designs.
   *
   * It renders in three places — the drawer, the cart page and (since the
   * checkout summary started reading the store) the checkout aside — so it is
   * built to survive a ~340px column: nothing here has a fixed width.
   */
  function cartEmptyHTML() {
    return (
      '<div class="cart-empty flex flex-col items-center gap-2 px-4 py-12 text-center">' +
      '<span class="cart-empty__badge place-items-center grid bg-cream mb-1 rounded-full text-cta size-16">' +
      '<span class="w-8 h-8">' + ICON.cart + "</span>" +
      "</span>" +
      '<p class="font-bold text-ink text-lg">' + esc(t("سلتك فارغة")) + "</p>" +
      '<p class="max-w-[30ch] text-muted text-sm leading-6">' +
      esc(t("المنتجات اللي تضيفها هتظهر هنا.")) + "</p>" +
      '<a href="shop.html" class="btn-elevate flex justify-center items-center bg-cta hover:bg-cta-hover mt-3 px-6 rounded-full min-h-11 font-semibold text-white text-sm transition-colors">' +
      esc(t("تصفح المنتجات")) + "</a>" +
      "</div>"
    );
  }

  /* The JAAD price sticker (Figma 9946:16778) as markup — the deep-green badge
     with the lime offset shadow and the asymmetric corners, split EGP / whole /
     .dec. It is the site's ONE price treatment (product cards, the bundle list,
     the upsell rail and components.price_sticker all draw it), and the cart was
     the one place still printing a plain bold figure — a lime chip in the drawer
     and unstyled text in the checkout summary (Ahmed, 2026-08-23). Same badge
     everywhere a price shows.

     Split into `stickerParts` + wrapper because renderCart updates a line total
     IN PLACE on every quantity change: writing `textContent` onto a composed
     badge would flatten it back to a bare string on the first press. Rows carry
     `data-price-sticker`, and paintLineTotal below repaints the parts instead. */
  function stickerParts(price, egpCls, wholeCls) {
    const v = Number(price) || 0;
    const whole = Math.floor(v);
    const dec = String(Math.round((v - whole) * 100)).padStart(2, "0");
    return (
      '<span class="' + egpCls + ' leading-[1.4]">EGP</span>' +
      '<span class="' + wholeCls + ' leading-none">' + whole + "</span>" +
      '<span class="' + egpCls + ' leading-[1.4]">.' + dec + "</span>"
    );
  }
  /* `sm` matches components.price_sticker("sm") — the size the cart rows, the
     bundle list and the compact upsell card all use. */
  const STICKER_SM = {
    egp: "text-[11px]",
    whole: "text-[16px]",
    box: "bg-greenDeep shadow-[2px_3px_0px_#98CA55] px-1.5 rounded-tl-[14px] rounded-br-[14px]",
  };
  /* `md` matches components.price_sticker("md") — the size the product CARD
     uses. Added so the JS-rendered card stops drawing its own (Ahmed,
     2026-08-24): it had an 18px "EGP" against the component's 15px, the same
     3px disagreement the Python card had. */
  const STICKER_MD = {
    egp: "text-[15px]",
    whole: "text-[24px]",
    box: "bg-greenDeep shadow-[3px_5px_0px_#98CA55] px-2 rounded-tl-[20px] rounded-br-[20px]",
  };
  function priceStickerHTML(price, attrs) {
    return (
      '<span ' + (attrs || "") + ' data-price-sticker class="inline-flex items-end gap-0.5 shrink-0 ' +
      STICKER_SM.box + ' font-bold text-white latin">' +
      stickerParts(price, STICKER_SM.egp, STICKER_SM.whole) +
      "</span>"
    );
  }
  /* One writer for a line's money, whichever shape the row uses. */
  function paintLineTotal(el, value) {
    if (!el) return;
    if (el.hasAttribute("data-price-sticker")) {
      el.innerHTML = stickerParts(value, STICKER_SM.egp, STICKER_SM.whole);
    } else {
      el.textContent = egp(value);
    }
  }

  function cartLineHTML(it) {
    /* On checkout/payment the order is LOCKED (Ahmed, 2026-08-02): no stepper,
       no remove, and a COMPACT row. The shopper has already decided what they
       are buying, so the summary is a receipt to confirm, not an editor to be
       distracted by. Everywhere else — the cart page and the drawer — the full
       editable row below stands. renderCart's in-place update only touches
       [data-line-total] and [data-line-qty], both present here, so the keyed
       reconcile works for either shape. */
    if (isCheckout()) {
      return `
      <div class="flex items-center gap-3 py-2.5 border-divider border-b last:border-b-0" data-cart-line data-id="${esc(String(it.id))}">
        <img src="${esc(it.image)}" alt="${esc(it.name)}" class="cart-thumb bg-cream shrink-0 rounded-lg w-12 h-12" loading="lazy" />
        <div class="flex flex-col flex-1 min-w-0">
          <p class="font-semibold text-ink text-sm line-clamp-1">${esc(it.name)}</p>
          <!-- Pack weight beside the count, separated by a middot: on the
               locked summary the row is a receipt, and "250 g · Qty 2" is the
               line a shopper checks against what they meant to buy. -->
          <p class="text-muted text-xs">${weightOf(it.id) ? esc(weightOf(it.id)) + " · " : ""}${esc(t("العدد"))}: <span class="latin" data-line-qty>${it.qty}</span></p>
        </div>
        ${priceStickerHTML(it.price * it.qty, "data-line-total")}
      </div>`;
    }
    return `
      <div class="flex items-stretch gap-3 py-4 border-divider border-b last:border-b-0" data-cart-line data-id="${esc(String(it.id))}">
        <!-- A SQUARE tile (Ahmed, 2026-08-23). It used to stretch to the row's
             height, which made it a tall rectangle — and a square product photo
             contained inside a tall rectangle leaves a cream band above and
             below it, which is exactly the "border around the product" being
             removed here. A square tile plus .cart-thumb (contain, no padding)
             and the photograph fills it edge to edge.

             The SIZE is responsive on purpose. Widening it everywhere would
             take 24px straight out of the text column, and at 320 that column
             is the tightest thing on the page — the stepper row needs 138px
             inside 141px (DESIGN-NOTES section 7), so 24px less would
             reintroduce exactly the overflow the flex-wrap below exists to
             prevent. 96px from the sm breakpoint up, where the space actually
             exists; 72px at 320, where it does not. -->
        <img src="${esc(it.image)}" alt="${esc(it.name)}" class="cart-thumb bg-cream shrink-0 rounded-lg w-[72px] h-[72px] sm:w-24 sm:h-24" />
        <!-- justify-between, so the three rows distribute across whatever
             height the line has instead of bunching at the top and leaving a
             gap under the stepper — the misalignment Ahmed flagged. -->
        <div class="flex flex-col flex-1 justify-between gap-1 min-w-0">
          <div class="flex justify-between items-start gap-2">
            <p class="flex-1 min-w-0 font-semibold text-ink text-sm line-clamp-2">${esc(it.name)}</p>
            ${priceStickerHTML(it.price * it.qty, "data-line-total")}
          </div>
          <p class="mt-1 text-muted text-xs">${weightOf(it.id) ? esc(weightOf(it.id)) + " · " : ""}${esc(t("العدد"))}: <span class="latin" data-line-qty>${it.qty}</span></p>
          <!-- gap-1 until sm: at 320 the stepper (122) + حذف (24) + gap (8)
               came to 154 inside a 141px column, overflowing the row by 13px.
               The tighter gap brings it to 138. The baseline sweep missed
               this because it happened to run against an emptied cart, so no
               line ever rendered.

               flex-wrap because that budget is language-dependent and was
               only ever balanced against the Arabic. "Remove" is about 21px
               wider than "حذف", which put the row 7px over the same 141px
               column in English at 320 — the identical failure, one
               translation later. Wrapping is the fix that does not need
               re-balancing for the next language: the row stays on one line
               wherever it fits (375 and up, both languages) and drops the
               button below the stepper only where it genuinely cannot. -->
          <div class="flex flex-wrap justify-between items-center gap-2 mt-2">
            <!-- The CANONICAL counter, not a cousin of it (Ahmed, 2026-08-23:
                 "I want the same counter used in the rest of the site"). This
                 row had drifted: no white fill, a bare - with no ring of its
                 own, a light 14px number and 32px buttons. Every other counter
                 on the site - the product page (components.qty_stepper) and the
                 product cards that adopted it - is a white pill with a 4px
                 inset, a hairline-ringed - circle, a bold number and a bg-cta +
                 circle. The sizes here match the CARD rendering of it
                 (size-10 on phones, size-8 from sm) because this is the same
                 kind of compact row, and the 44px phone target is the audited
                 floor. The old 32px was affordable only while the separate
                 حذف link ate the row's width; that link is long gone. -->
            <!-- data-cart-stepper is a STYLING hook only (styles.css pins the
                 − … + axis to LTR so it does not mirror in Arabic). The click
                 handling is delegated off [data-cart-step] on the buttons, so
                 this attribute deliberately does not match [data-stepper],
                 which initStepper would bind a second, conflicting handler to. -->
            <div data-cart-stepper class="inline-flex items-center gap-1 bg-white p-1 border border-divider rounded-full">
              <!-- At quantity 1 the − becomes a trash can and removing is what
                   it does (Ahmed, 2026-07-26). The behaviour was already this:
                   the handler removes the line when the step would take it
                   below 1. Only the glyph lied, showing "one fewer" for a press
                   that emptied the row.

                   This replaced a separate حذف text link, which is a real win
                   beyond the tidying: that link was a 24px-wide target on every
                   cart line (DESIGN-NOTES §7), and its width was what pushed
                   the row over its 320px budget and blocked the stepper being
                   grown to 44px. One control instead of two, and the budget
                   back.

                   Both glyphs ship and are toggled, rather than the innerHTML
                   being rewritten: the rows are keyed-reconciled and keep their
                   DOM nodes, so swapping markup under a live row would discard
                   whatever the icon was doing mid-transition. -->
              <button type="button" data-cart-step="-1" class="place-items-center grid border border-divider hover:bg-cream rounded-full size-10 sm:size-8 text-ink shrink-0 transition-colors" aria-label="إنقاص" data-line-dec>
                <span class="w-5 h-5 sm:w-4 sm:h-4" data-line-dec-minus>${ICON.minus}</span>
                <span class="w-5 h-5 sm:w-4 sm:h-4 text-muted" data-line-dec-trash hidden>${ICON.trash}</span>
              </button>
              <span class="min-w-[1.5ch] font-bold text-ink text-center latin" data-line-qty-num>${it.qty}</span>
              <button type="button" data-cart-step="1" class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full size-10 sm:size-8 text-white shrink-0 transition-colors" aria-label="زيادة"><span class="w-5 h-5 sm:w-4 sm:h-4">${ICON.plus}</span></button>
          </div>
        </div>
      </div>`;
  }

  /* ---------------------------------------------------------------
     Per-card quantity stepper

     Once a product is in the cart, its card swaps the add button for a
     −/n/+ control, so the second unit is one tap away instead of a re-add
     that gives no feedback. State comes from the same place as everything
     else — the card's `data-id` against the store — so every card for the
     same product on the page (rail + grid + upsell) stays in step, and the
     control survives a reload with no extra persistence.

     Driven off `cart:change`, so a change made in the drawer repaints the
     cards and vice versa.
     --------------------------------------------------------------- */
  function syncCardSteppers(scope) {
    (scope || document).querySelectorAll("[data-card-stepper]").forEach((stepper) => {
      const card = stepper.closest("[data-product]");
      if (!card) return;
      // Sibling lookup, not a card-wide query: on the product page the
      // outer [data-product] host also contains the related-products rail,
      // whose cards have add buttons of their own.
      const addBtn = stepper.parentElement.querySelector("[data-add-to-cart]");
      const it = Cart.find(card.dataset.id);
      stepper.hidden = !it;
      if (addBtn) addBtn.hidden = !!it;
      const num = stepper.querySelector("[data-card-qty]");
      if (it && num && num.textContent !== String(it.qty)) {
        // Rolls in the direction the quantity moved — see rollTo above.
        rollTo(num, it.qty, it.qty > (parseInt(num.textContent, 10) || 0) ? 1 : -1);
      }
    });
  }

  /* ---------------------------------------------------------------
     Checkout option rows, and the two pickers behind them.

     `setOptMeta(key, text, resolved)` is the ONE writer of a row's status
     text. A row is either prompting for a choice it still needs ("اختر الفرع",
     painted as a call to action) or showing the answer. Keeping both states in
     one function is what stops a confirmed branch name from being repainted as
     a prompt by some later handler.
     --------------------------------------------------------------- */
  function setOptMeta(key, text, resolved) {
    document.querySelectorAll('[data-opt-meta="' + key + '"]').forEach((el) => {
      el.textContent = text;
      el.classList.toggle("is-prompt", !resolved);
      el.classList.toggle("is-resolved", !!resolved);
    });
  }

  function optMetaText(key) {
    const el = document.querySelector('[data-opt-meta="' + key + '"]');
    return el ? el.textContent.trim() : "";
  }

  function optMetaResolved(key) {
    const el = document.querySelector('[data-opt-meta="' + key + '"]');
    return !!el && el.classList.contains("is-resolved");
  }

  /* Store picker ---------------------------------------------------
     Reads the governorate/branch tree baked into checkout.html at build time
     (see build/pages/checkout.py). Parsed once, lazily, on first open — the
     payload is only needed if the shopper actually picks up in store, and
     parsing 316 branches on every checkout load to serve the minority who do
     is work most visits never use. */
  let storeTree = null;
  function loadStoreTree() {
    if (storeTree) return storeTree;
    const tag = document.querySelector("[data-store-tree]");
    if (!tag) return (storeTree = []);
    try {
      storeTree = JSON.parse(tag.textContent) || [];
    } catch (err) {
      storeTree = [];
    }
    return storeTree;
  }

  let pickedStore = null;

  function renderStoreList(govIndex) {
    const list = document.querySelector("[data-store-list]");
    const confirm = document.querySelector("[data-store-confirm]");
    if (!list) return;
    const tree = loadStoreTree();
    const group = tree[govIndex];
    const branches = (group && group.branches) || [];
    pickedStore = null;
    if (confirm) confirm.disabled = true;

    if (!branches.length) {
      // Says what happened rather than rendering nothing — an empty box reads
      // as a broken picker, which is the same failure the search modal's empty
      // state exists to avoid.
      list.innerHTML =
        '<p class="py-6 text-muted text-sm text-center">' +
        esc(t("لا توجد فروع في هذه المحافظة")) +
        "</p>";
      return;
    }
    list.innerHTML = branches
      .map(
        (b, i) => `
        <button type="button" data-store-pick="${i}"
                class="store-option flex flex-col items-start gap-0.5 bg-white p-3 border border-divider rounded-xl w-full text-start transition-colors">
          <span class="font-semibold text-ink text-sm">${esc(b.t)}</span>
          ${b.a ? `<span class="text-muted text-xs leading-5">${esc(b.a)}</span>` : ""}
        </button>`,
      )
      .join("");
  }

  function initStorePicker() {
    const gov = document.querySelector("[data-store-gov]");
    if (!gov || gov.dataset.ready === "true") return;
    gov.dataset.ready = "true";
    const tree = loadStoreTree();
    gov.innerHTML = tree
      .map((g, i) => `<option value="${i}">${esc(g.gov)}</option>`)
      .join("");
    renderStoreList(0);
    gov.addEventListener("change", () => renderStoreList(+gov.value || 0));
  }

  /* Schedule picker ------------------------------------------------
     Slots are in-house placeholder — the client publishes no delivery windows
     anywhere, so these are plausible rather than real (DESIGN-NOTES). The DAYS
     are real and computed from the device clock at open time. */
  /* Per language, for the same reason as the day names: these are picked by
     INDEX and pasted into the row's status text, so a single Arabic array left
     English mode showing "Tuesday 28 July · 12:00 م - 2:00 م" — half a
     sentence in each language. Kept as parallel arrays rather than formatted
     from numbers because ص/م do not map onto AM/PM by a rule worth writing for
     six fixed windows. */
  const SCHED_SLOTS_BY_LANG = {
    ar: [
      "10:00 ص - 12:00 م",
      "12:00 م - 2:00 م",
      "2:00 م - 4:00 م",
      "4:00 م - 6:00 م",
      "6:00 م - 8:00 م",
      "8:00 م - 10:00 م",
    ],
    en: [
      "10:00 AM - 12:00 PM",
      "12:00 PM - 2:00 PM",
      "2:00 PM - 4:00 PM",
      "4:00 PM - 6:00 PM",
      "6:00 PM - 8:00 PM",
      "8:00 PM - 10:00 PM",
    ],
  };
  const schedSlots = () => SCHED_SLOTS_BY_LANG[currentLang()] || SCHED_SLOTS_BY_LANG.ar;
  /* Day and month names per language. These CANNOT go through t(): the strings
     are assembled at runtime from the device clock, so there is no fixed
     Arabic phrase for the dictionary to key on — "الإثنين 27 يوليو" only
     exists on one day of one year. Shipping only the Arabic set left the
     English chips reading "Today, الإثنين 27 يوليو", which is how this was
     caught.

     Deliberately NOT Intl.DateTimeFormat: it resolves against the BROWSER's
     locale, not the site's language toggle, so a visitor on an English OS
     reading the Arabic site would get English day names inside Arabic copy.
     The site's own language has to win. */
  const DAY_NAMES = {
    ar: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
    en: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  };
  const MONTH_NAMES = {
    ar: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
         "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"],
    en: ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
  };

  let pickedDay = null;
  let pickedSlot = null;
  // Survives a gift toggle so a chosen branch is not lost to an unrelated
  // switch — see the restore in the gift handler.
  let savedPickupMeta = "";

  function schedDays() {
    const out = [];
    const lang = currentLang();
    const days = DAY_NAMES[lang] || DAY_NAMES.ar;
    const months = MONTH_NAMES[lang] || MONTH_NAMES.ar;
    const now = new Date();
    for (let i = 0; i < 7; i++) {
      const d = new Date(now.getFullYear(), now.getMonth(), now.getDate() + i);
      out.push({
        label: i === 0
          ? t("اليوم")
          : days[d.getDay()] + " " + d.getDate() + " " + months[d.getMonth()],
        key: d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(),
      });
    }
    return out;
  }

  /* Day-strip arrows.

     All the arithmetic is done on the ABSOLUTE scroll offset, because RTL
     reports `scrollLeft` as negative in this engine — the same trap that broke
     the product carousels (HANDOFF §4.1) and that `getPos()` there exists to
     paper over. Working in absolute terms means one set of comparisons for
     both directions; only the sign applied to the final scroll differs.

     `dir` is LOGICAL (+1 = further into the strip), so the arrows mean the
     same thing in Arabic and English and the glyphs mirror via rtl:scale-flip. */
  const schedPos = (el) => Math.abs(el.scrollLeft);
  const schedMax = (el) => Math.max(0, el.scrollWidth - el.clientWidth);

  function syncSchedArrows() {
    const strip = document.querySelector("[data-sched-days]");
    if (!strip) return;
    const pos = schedPos(strip);
    const max = schedMax(strip);
    // 2px tolerance: a scrolled strip settles a fraction short of its own
    // maximum, and an arrow that stays lit at the end reads as broken.
    document.querySelectorAll("[data-sched-nav]").forEach((btn) => {
      const dir = +btn.dataset.schedNav;
      const atEnd = dir > 0 ? pos >= max - 2 : pos <= 2;
      btn.disabled = max === 0 || atEnd;
      btn.classList.toggle("is-disabled", btn.disabled);
    });
  }

  function scrollSchedDays(dir) {
    const strip = document.querySelector("[data-sched-days]");
    if (!strip) return;
    const chip = strip.querySelector("[data-sched-day]");
    // Two chips per press — enough to feel like progress, small enough that
    // nothing is skipped past unseen. Falls back to half the strip if the
    // chips have not been measured yet.
    const step = chip
      ? (chip.getBoundingClientRect().width + 8) * 2
      : strip.clientWidth / 2;
    const rtl = document.documentElement.getAttribute("dir") === "rtl";
    strip.scrollBy({ left: (rtl ? -1 : 1) * dir * step, behavior: "smooth" });
  }

  function renderSchedule() {
    const daysBox = document.querySelector("[data-sched-days]");
    const slotsBox = document.querySelector("[data-sched-slots]");
    const confirm = document.querySelector("[data-sched-confirm]");
    if (!daysBox || !slotsBox) return;
    const days = schedDays();
    if (pickedDay === null) pickedDay = 0;
    daysBox.innerHTML = days
      .map(
        (d, i) => `
        <button type="button" data-sched-day="${i}"
                class="sched-chip shrink-0 px-4 py-2 border rounded-full font-semibold text-sm whitespace-nowrap transition-colors${i === pickedDay ? " is-active" : ""}">${esc(d.label)}</button>`,
      )
      .join("");
    slotsBox.innerHTML = schedSlots().map(
      (s, i) => `
        <button type="button" data-sched-slot="${i}"
                class="sched-chip px-3 py-2 border rounded-xl text-sm transition-colors${i === pickedSlot ? " is-active" : ""}">${esc(s)}</button>`,
    ).join("");
    if (confirm) confirm.disabled = pickedSlot === null;

    /* Arrow state is measured AFTER the chips exist, and again on the next
       frame. While the modal is still hidden every width reports 0, so a
       measurement taken at render time concludes the strip does not overflow
       and greys both arrows out permanently — the blueprint calls this out and
       it is the one thing that makes this control look broken on first open. */
    syncSchedArrows();
    requestAnimationFrame(syncSchedArrows);
    if (!daysBox.dataset.navReady) {
      daysBox.dataset.navReady = "1";
      daysBox.addEventListener("scroll", syncSchedArrows, { passive: true });
    }
  }

  /* ---------------------------------------------------------------
     Product-page buy block — the CTA label and the cart-bound stepper.

     Same contract as syncCardSteppers: state is read from the store by the
     host's `data-id`, never held here, so a change made in the drawer, on a
     card, or in another tab's restored cart repaints this block too, and a
     reload restores it with no extra persistence.

     The label is two spans toggled on `hidden`, not one span whose text is
     rewritten, because translateDocument() keys off exact strings and stashes
     the original text node in a WeakMap. Rewriting textContent under it would
     either lose the English on the next language switch or restore the wrong
     Arabic on the way back.
     --------------------------------------------------------------- */
  function syncBuyBlock(scope) {
    (scope || document).querySelectorAll("[data-cart-bound]").forEach((stepper) => {
      const host = stepper.closest("[data-product]");
      if (!host) return;
      const line = Cart.find(host.dataset.id);
      const qty = line ? line.qty : 0;

      /* The DIGIT floors at 1; the STATE does not (Ahmed, 2026-07-26). A
         product page opens on someone who has not decided anything yet, and a
         0 there reads as out of stock — so it rests at 1 even with an empty
         basket. The real quantity still drives everything else below, which is
         what keeps the floor from becoming a lie. */
      const qtyEl = stepper.querySelector("[data-qty]");
      const shown = Math.max(1, qty);
      if (qtyEl) {
        rollTo(qtyEl, shown, shown >= (parseInt(qtyEl.textContent, 10) || 0) ? 1 : -1);
      }

      /* ...and the − button is what tells the two apart, since "1, not in the
         basket" and "1, in the basket" are now drawn with the same digit:

             not in basket   disabled + dimmed, minus glyph
             1 in basket     live, trash glyph
             2+ in basket    live, minus glyph

         So the first + leaves the digit at 1 and still visibly answers the
         press — the − lights up, the ghost flies, the badge ticks. */
      const dec = stepper.querySelector("[data-line-dec]");
      if (dec) {
        dec.disabled = qty === 0;
        dec.classList.toggle("opacity-40", qty === 0);
        syncLineDecrement(stepper, qty);
      }
    });
  }

  /* ---------------------------------------------------------------
     Sticky buy bar (product page)

     A re-CTA that appears once the real buy block has scrolled ABOVE the
     viewport: fixed to the bottom on mobile, and parked under the sticky nav
     at the top on desktop. It owns NO state — its −/＋ and CTA forward to the
     real cart-bound stepper and buy button, and its title/price/quantity
     mirror them, so there is exactly one writer of the cart (the existing
     delegated handlers).

     Show/hide keys off `boundingClientRect.top < 0`, not plain
     `!isIntersecting`: on mobile the buy block starts BELOW the fold, and a bar
     that appeared before the shopper had even reached the product would be
     noise. It shows only after the block has left past the TOP.
     --------------------------------------------------------------- */
  function initStickyBuyBar() {
    const bar = document.querySelector("[data-sticky-buybar]");
    if (!bar) return;
    const buyBlock = document.querySelector("[data-buy-block]");
    const host = buyBlock && buyBlock.closest("[data-product]");
    if (!buyBlock || !host) return;

    const mainStepper = host.querySelector("[data-cart-bound]");
    const mainBuy = host.querySelector("[data-buy-cta]");
    const mainPrice = host.querySelector("[data-price-display]");
    const mainQty = mainStepper && mainStepper.querySelector("[data-qty]");
    const barPrice = bar.querySelector("[data-sticky-price]");
    const barQty = bar.querySelector("[data-sticky-qty]");

    // Mirror the real controls' text. Idempotent, so it can run on any signal
    // that might have moved either number.
    const mirror = () => {
      if (barPrice && mainPrice) barPrice.textContent = mainPrice.textContent;
      if (barQty && mainQty) barQty.textContent = mainQty.textContent;
    };

    // Forward, don't duplicate: the bar drives the real controls so the cart
    // keeps a single writer. The +/− mirror the stepper; the CTA mirrors the
    // real buy button, which opens the side cart once the quantity is set.
    bar.addEventListener("click", (e) => {
      const step = e.target.closest("[data-sticky-step]");
      if (step) {
        if (mainStepper) {
          const real = mainStepper.querySelector(
            '[data-step="' + step.getAttribute("data-sticky-step") + '"]',
          );
          if (real) real.click();
        }
        return;
      }
      if (e.target.closest("[data-sticky-buy]") && mainBuy) mainBuy.click();
    });

    // A size chip fires no cart:change but does repoint the price, and the
    // quantity rolls its own text node — so watch the nodes themselves rather
    // than only the store.
    if (window.MutationObserver) {
      const mo = new MutationObserver(mirror);
      const opts = { childList: true, characterData: true, subtree: true };
      if (mainPrice) mo.observe(mainPrice, opts);
      if (mainQty) mo.observe(mainQty, opts);
    }
    document.addEventListener("cart:change", mirror);
    mirror();

    // Visible only once the block has left past the top edge.
    if (window.IntersectionObserver) {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((en) => {
            const past = !en.isIntersecting && en.boundingClientRect.top < 0;
            bar.classList.toggle("is-visible", past);
            bar.setAttribute("aria-hidden", past ? "false" : "true");
            // Lets styles.css drop the floating search/cart pill below the bar
            // on desktop, where the two share the top edge (see .buybar-shown).
            document.documentElement.classList.toggle("buybar-shown", past);
          });
        },
        { threshold: 0 },
      );
      io.observe(buyBlock);
    }
  }

  /* ---------------------------------------------------------------
     Points discount (the "خصم المبلغ" banner on cart and checkout)

     Stored, not held in a variable: the shopper applies it on the cart page
     and expects checkout to remember. The amount comes off the banner's own
     data attribute at click time; nothing here knows what a point is worth.
     Demo state like the points balance itself — see DESIGN-NOTES.
     --------------------------------------------------------------- */
  const WALLET_KEY = "jaad:walletApplied";
  const walletApplied = () => Number(localStorage.getItem(WALLET_KEY)) || 0;

  /* Wallet balance = a base PLUS everything transferred in (Ahmed, 2026-08-04):
     redeemed loyalty points AND activated vouchers both land here, so the wallet
     is the single balance the whole account reflects. Every wallet display
     ([data-wallet-amount], the toggle's data-wallet-balance) reads the total.
     BASE_WALLET mirrors components.WALLET_BALANCE; POINTS_BASE mirrors
     _account.CUSTOMER["points"]. Demo state — no live endpoint (DESIGN-NOTES). */
  const BASE_WALLET = 1200;
  const POINTS_BASE = 3200;
  const POINTS_PER_EGP = 10; // 10 points -> EGP 1
  const POINTS_TIERS = [["فضية", 0], ["ذهبية", 2000], ["بلاتينية", 4000]];
  const PT_SPENT_KEY = "jaad:pointsSpent";
  const VOUCHERS_KEY = "jaad:vouchersWallet";
  const V_USED_KEY = "jaad:vouchersUsed";
  // Vouchers a shopper added by code (Ahmed, 2026-08-05): each is stored as
  // {id,label,validity,value} and lands in the AVAILABLE list — it is NOT
  // credited to the wallet until the shopper activates it, exactly like the
  // seeded vouchers. Kept apart from V_USED_KEY (which records activations of
  // either kind) so a reload re-renders the ones still waiting to be activated.
  const V_ADDED_KEY = "jaad:vouchersAdded";
  const VOUCHERS_TOTAL = 3; // mirrors _account.VOUCHERS length
  const vouchersUsed = () => { try { return JSON.parse(localStorage.getItem(V_USED_KEY) || "[]"); } catch (e) { return []; } };
  const vouchersAdded = () => { try { return JSON.parse(localStorage.getItem(V_ADDED_KEY) || "[]"); } catch (e) { return []; } };
  const numKey = (k) => { try { return Number(localStorage.getItem(k)) || 0; } catch (e) { return 0; } };
  const pointsSpent = () => numKey(PT_SPENT_KEY);
  const pointsRemaining = () => Math.max(0, POINTS_BASE - pointsSpent());
  const vouchersCredit = () => numKey(VOUCHERS_KEY);
  function walletBonus() {
    return Math.round(pointsSpent() / POINTS_PER_EGP) + vouchersCredit();
  }
  /* Count a wallet display from its current value up to `to`, with a soft scale
     "pop" (Ahmed, 2026-08-04) — so activating a voucher or redeeming points is
     felt, not just shown. Smooth ease-out on the number, a CSS bounce on the
     box; skipped under reduced motion. */
  function walletCountUp(el, from, to) {
    if (reduceMotion() || from === to) { el.textContent = "EGP " + to; return; }
    const dur = 900, t0 = performance.now();
    const ease = (p) => 1 - Math.pow(1 - p, 3);
    el.classList.remove("wallet-pop");
    void el.offsetWidth;
    el.classList.add("wallet-pop");
    const step = (now) => {
      const p = Math.min(1, (now - t0) / dur);
      el.textContent = "EGP " + Math.round(from + (to - from) * ease(p));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
    // rAF is throttled/paused in a hidden or backgrounded tab, so it may never
    // reach the last frame; a timer (which still fires) guarantees the final
    // value and cleanup regardless. Worst case: the number jumps, never sticks.
    setTimeout(() => { el.textContent = "EGP " + to; el.classList.remove("wallet-pop"); }, dur + 120);
  }

  /* The "money just landed in your wallet" beat (Ahmed, 2026-08-05). On top of
     the count-up, three layered cues so a credit is unmissable:
       - the wallet CARD glows and lifts (a green ring pulse), so the eye is
         pulled to the whole balance panel, not just the digits;
       - a "+EGP N" chip rises off the balance and fades, naming the amount that
         arrived;
       - the celebrate() burst already used on the cart wallet toggle.
     All are decoration: each is guarded by reduceMotion() and Element.animate,
     and the number itself is always set correctly by walletCountUp regardless. */
  function walletCreditFX(el, delta) {
    if (!el || delta <= 0 || reduceMotion()) return;
    const card = el.closest("[data-wallet-card]");
    if (card) {
      card.classList.remove("wallet-card-glow");
      void card.offsetWidth;
      card.classList.add("wallet-card-glow");
      setTimeout(() => card.classList.remove("wallet-card-glow"), 1400);
    }
    if (el.animate) {
      const r = el.getBoundingClientRect();
      const chip = document.createElement("div");
      chip.className = "wallet-delta-chip";
      chip.textContent = "+EGP " + delta;
      chip.style.left = r.left + r.width / 2 + "px";
      chip.style.top = r.top + "px";
      document.body.appendChild(chip);
      chip.animate(
        [
          { transform: "translate(-50%, 0) scale(0.8)", opacity: 0 },
          { transform: "translate(-50%, -12px) scale(1)", opacity: 1, offset: 0.25 },
          { transform: "translate(-50%, -44px) scale(1)", opacity: 0 },
        ],
        { duration: 1200, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" },
      ).onfinish = () => chip.remove();
    }
    celebrate(el);
  }

  function syncWalletBalance(animate) {
    const total = BASE_WALLET + walletBonus();
    document.querySelectorAll("[data-wallet-amount]").forEach((el) => {
      const cur = parseInt((el.textContent || "").replace(/[^\d]/g, ""), 10) || 0;
      if (animate && cur !== total) {
        walletCountUp(el, cur, total);
        if (total > cur) walletCreditFX(el, total - cur);
      } else {
        el.textContent = "EGP " + total;
      }
    });
    document.querySelectorAll("[data-wallet-toggle]").forEach((el) => (el.dataset.walletBalance = String(total)));
  }

  /* Promo codes. DISCOUNT10 is not invented — it is the code the site's own
     announcement bar advertises at the top of every page ("خصم 10% لما تستخدم
     برومو كود DISCOUNT10"), so the bar and the checkout now agree. Keep them
     in sync: a promo bar advertising a code the checkout rejects is worse than
     no bar. Anything else here would be inventing an offer on the client's
     behalf, which is the line this project holds elsewhere too. */
  // Gifting is chosen on checkout but enforced on payment, so it is stored
  // rather than held in a variable — see the gift handler.
  const GIFT_KEY = "jaad:gift";
  const isGiftOrder = () => localStorage.getItem(GIFT_KEY) === "1";

  const PROMO_CODES = { DISCOUNT10: { type: "percent", value: 10 } };
  const PROMO_KEY = "jaad:promo";
  const promoCode = () => (localStorage.getItem(PROMO_KEY) || "").toUpperCase();

  /* Computed from the subtotal every time rather than stored as an amount:
     a percentage banked as EGP would go stale the moment the basket changed,
     and would keep discounting a line the shopper had already removed. */
  function promoDiscount(sub) {
    const rule = PROMO_CODES[promoCode()];
    if (!rule) return 0;
    return rule.type === "percent"
      ? Math.round(sub * rule.value) / 100
      : Math.min(rule.value, sub);
  }

  /* Applying a code. Success and failure both SAY something — an Apply button
     that silently does nothing on a typo is indistinguishable from a broken
     one, which is how the old dead button read for its whole life. */
  function applyPromo(wrap) {
    // Scope to the field that was used — the drawer and the cart page each own
    // a [data-promo], so a bare document.querySelector would read (and message)
    // whichever happens to sit first in the DOM rather than the one clicked.
    wrap = wrap || document.querySelector("[data-promo]");
    const input = wrap && wrap.querySelector("[data-promo-input]");
    const msg = wrap && wrap.querySelector("[data-promo-msg]");
    if (!input) return;
    const code = input.value.trim().toUpperCase();
    if (!code) return;
    const ok = !!PROMO_CODES[code];
    if (ok) {
      localStorage.setItem(PROMO_KEY, code);
      renderCart();
      celebrate(wrap);
    } else {
      localStorage.removeItem(PROMO_KEY);
      renderCart();
    }
    if (msg) {
      msg.hidden = false;
      msg.textContent = ok
        ? t("تم تطبيق الكود") + " " + code
        : t("كود غير صالح");
      /* text-heading, not text-lime: this line is 12px copy telling the
         shopper their code worked, and #8ACC3E is 1.9:1 on white (Ahmed,
         2026-08-23). Its failure twin, text-error, is legible — the good news
         should not be the half nobody can read. */
      msg.classList.toggle("text-heading", ok);
      msg.classList.toggle("text-error", !ok);
    }
  }

  /* Promo field state (Ahmed, 2026-08-02): trigger -> input box -> applied
     chip. Called from renderCart, so it is correct on load, after apply/remove,
     and across cart -> checkout. When no valid code is stored it only reveals
     the trigger if the input box is not currently open, so a change elsewhere
     (adding an item) never collapses a code the shopper is mid-typing. */
  function syncPromoUI() {
    const code = promoCode();
    const applied = !!PROMO_CODES[code];
    document.querySelectorAll("[data-promo]").forEach((wrap) => {
      const open = wrap.querySelector("[data-promo-open]");
      const box = wrap.querySelector("[data-promo-box]");
      const appliedEl = wrap.querySelector("[data-promo-applied]");
      const codeEl = wrap.querySelector("[data-promo-applied-code]");
      if (applied) {
        if (open) open.hidden = true;
        if (box) box.hidden = true;
        if (appliedEl) appliedEl.hidden = false;
        if (codeEl) codeEl.textContent = code;
      } else {
        if (appliedEl) appliedEl.hidden = true;
        const boxOpen = box && !box.hidden;
        if (open) open.hidden = !!boxOpen;
      }
    });
  }

  /* Rules a gift order imposes, applied on ARRIVAL as well as on toggle.
     Checkout restores the switch itself; payment.html has no switch at all and
     only ever sees the stored flag, which is the whole reason it is stored.

     Both blocked rows follow the same contract as the pickup row: dimmed, not
     removed, with the reason in place of the control, and the selection handed
     to a sibling if the blocked one was chosen — a disabled row left checked
     is a form the shopper cannot submit and cannot fix. */
  function syncGiftRules() {
    const on = isGiftOrder();

    const giftSwitch = document.querySelector("[data-gift-switch]");
    if (giftSwitch && giftSwitch.checked !== on) {
      giftSwitch.checked = on;
      giftSwitch.dispatchEvent(new Event("change", { bubbles: true }));
      return; // the change handler does the rest, including this row's rules
    }

    const cod = document.querySelector("[data-cod-option]");
    if (cod) {
      cod.classList.toggle("option-blocked", on);
      const input = cod.querySelector("input[type=radio]");
      if (input) {
        input.disabled = on;
        if (on && input.checked) {
          const fallback = document.querySelector(
            'input[name="' + input.name + '"]:not([value="cod"])',
          );
          /* `change` does not fire for a programmatic .checked write, and the
             card form's reveal listens for exactly that — without the dispatch,
             switching a COD order to a gift would move the selection to the card
             row and leave the card fields folded shut under it. */
          if (fallback) {
            fallback.checked = true;
            fallback.dispatchEvent(new Event("change", { bubbles: true }));
          }
        }
      }
    }
  }

  function syncWalletUI() {
    const d = walletApplied();
    /* The switch is the state, so it is set rather than asked. This also
       covers the load path: arriving at checkout with the wallet already on
       from the cart page has to paint the switch on, and a checkbox does not
       remember anything across a navigation by itself. */
    document.querySelectorAll("[data-wallet-switch]").forEach((input) => {
      if (input.checked !== !!d) input.checked = !!d;
    });
    /* The card's caption follows the state: a spent balance must not keep
       being offered as available.

       `invisible`, not `hidden`. The two copies are stacked in one grid cell
       (see wallet_toggle in components.py) so the card keeps the height of its
       tallest state — toggling them in and out of flow instead collapsed the
       block on press and shunted the whole order summary up under the cursor. */
    document
      .querySelectorAll("[data-wallet-idle]")
      .forEach((el) => el.classList.toggle("invisible", !!d));
    document
      .querySelectorAll("[data-wallet-used]")
      .forEach((el) => el.classList.toggle("invisible", !d));
    /* Deliberately no totals work here. The checkout summary used to be
       static build-time markup with its own data-base-total, so this function
       carried a second, parallel set of totals hooks. It now carries the cart
       page's hooks instead: renderCart owns every figure on both pages, and
       every caller of this function already calls it. One renderer to keep
       correct rather than two to keep agreeing. */
  }

  /* The decrement button's two meanings. At 2+ it subtracts; at 1 the next
     press empties the row, so it says so — trash glyph, error ink, and an
     accessible name that matches, because a screen-reader user hearing
     "decrease" would have no warning at all that the row is about to go. */
  function syncLineDecrement(row, qty) {
    if (!row) return;
    const btn = row.querySelector("[data-line-dec]");
    if (!btn) return;
    /* Exactly 1, not <= 1. At 0 the button is disabled and there is nothing to
       delete, so a trash can there promises an action that cannot happen; the
       product page's stepper sits at 0 whenever the product is out of the
       basket, which is most of the time. Cart rows never reach 0 — the line is
       gone by then — so this reads the same on both. */
    const removes = qty === 1;
    const minus = btn.querySelector("[data-line-dec-minus]");
    const trash = btn.querySelector("[data-line-dec-trash]");
    if (minus) minus.hidden = removes;
    if (trash) trash.hidden = !removes;
    btn.setAttribute("aria-label", removes ? t("حذف") : t("إنقاص"));
  }

  function renderCart() {
    const items = Cart.items();
    const sub = Cart.subtotal();
    const empty = items.length === 0;
    // Capped at the order's own worth — a 100 EGP wallet against a 60 EGP
    // basket discounts 60, it does not owe the shopper money.
    /* THE money math, in one place and in this order:
         afterPromo = max(0, subtotal + delivery − promo)
         walletUsed = min(wallet, afterPromo)     ← capped at the bill
         total      = afterPromo − walletUsed
       Promo resolves first because it is a discount ON the order; the wallet is
       a payment against whatever is left. Reversing them would let a wallet
       cover the pre-discount figure and hand back the difference as change. */
    // Free delivery at/above FREE_SHIP; below it the flat fee applies.
    const deliveryFee = empty ? 0 : sub >= FREE_SHIP ? 0 : DELIVERY_FEE;
    const gross = empty ? 0 : sub + deliveryFee;
    const promo = empty ? 0 : Math.min(promoDiscount(sub), gross);
    const afterPromo = Math.max(0, gross - promo);
    const walletUsed = empty ? 0 : Math.min(walletApplied(), afterPromo);

    /* Badge — every cart button on the page.
       While a ghost is mid-flight the badge is held at its old value, so the
       number ticks up at the moment the item lands rather than before it has
       left. State is still the truth; only the display waits. */
    if (!badgeHold) syncCartBadges();

    // The card stepper is the thing being pressed, so it is NOT held back
    // with the badge — its number has to answer the tap immediately. The
    // product page's buy block is the same case for the same reason.
    syncCardSteppers();
    syncBuyBlock();

    /*
     * Keyed reconcile rather than innerHTML replacement. Blowing the list away
     * on every change would destroy nodes mid-transition and drop focus, which
     * makes row-level micro-interactions impossible to build on top. Rows that
     * survive a change keep their DOM node; only genuinely new or gone rows are
     * created or detached.
     */
    document.querySelectorAll("[data-cart-lines]").forEach((host) => {
      // Drop the server-rendered rows the first time the store paints.
      host.querySelectorAll("[data-cart-static]").forEach((el) => el.remove());
      let emptyMsg = host.querySelector("[data-cart-empty]");
      if (empty && !emptyMsg) {
        emptyMsg = document.createElement("div");
        emptyMsg.setAttribute("data-cart-empty", "");
        emptyMsg.innerHTML = cartEmptyHTML();
        host.appendChild(emptyMsg);
      } else if (!empty && emptyMsg) {
        emptyMsg.remove();
      }

      const seen = {};
      items.forEach((it, i) => {
        seen[it.id] = true;
        let row = host.querySelector('[data-cart-line][data-id="' + CSS.escape(String(it.id)) + '"]');
        if (!row) {
          const tmp = document.createElement("div");
          tmp.innerHTML = cartLineHTML(it);
          row = tmp.firstElementChild;
          host.appendChild(row);
        } else {
          // Update in place so the node — and anything animating it — survives.
          const price = row.querySelector("[data-line-total]");
          const qtyTxt = row.querySelector("[data-line-qty]");
          const qtyNum = row.querySelector("[data-line-qty-num]");
          paintLineTotal(price, it.price * it.qty);
          if (qtyTxt) qtyTxt.textContent = it.qty;
          if (qtyNum) {
            rollTo(qtyNum, it.qty, it.qty > (parseInt(qtyNum.textContent, 10) || 0) ? 1 : -1);
          }
        }
        /* Runs for BOTH branches — a freshly created row starts at whatever
           quantity it was added with, which is routinely 1, so painting this
           only on the update path would ship every new line with a minus that
           removes. */
        syncLineDecrement(row, it.qty);
        // Keep DOM order in step with state order.
        if (host.children[i] !== row) host.insertBefore(row, host.children[i] || null);
      });

      host.querySelectorAll("[data-cart-line]").forEach((row) => {
        if (!seen[row.dataset.id]) row.remove();
      });
    });

    /* Totals + checkout gating, drawer and cart page alike. */
    document.querySelectorAll("[data-cart-subtotal]").forEach((el) => (el.textContent = egp(sub)));
    /* The drawer does NOT show or apply the wallet (Ahmed, 2026-08-04): its
       total is the real order cost (after promo, before wallet). The wallet is
       spent on the cart/checkout pages, whose total keeps subtracting it. */
    document.querySelectorAll("[data-cart-total]").forEach((el) => {
      const inDrawer = el.closest('[data-drawer="cart"]');
      el.textContent = egp(Math.max(0, inDrawer ? afterPromo : afterPromo - walletUsed));
    });
    document.querySelectorAll("[data-cart-discount-row]").forEach((el) => (el.hidden = !walletUsed));
    document.querySelectorAll("[data-cart-discount]").forEach((el) => (el.textContent = "− " + egp(walletUsed)));
    document.querySelectorAll("[data-cart-promo-row]").forEach((el) => (el.hidden = !promo));
    document.querySelectorAll("[data-cart-promo-discount]").forEach((el) => (el.textContent = "− " + egp(promo)));
    /* An EMPTY basket is the only thing that still blocks checkout. */
    document.querySelectorAll("[data-cart-checkout]").forEach((el) => {
      const blocked = empty;
      el.classList.toggle("pointer-events-none", blocked);
      el.classList.toggle("opacity-50", blocked);
      el.setAttribute("aria-disabled", blocked ? "true" : "false");
    });

    /* Delivery fee — a data hook now, not static build-time text, so free
       delivery can zero it live. Reads "مجاني" in green once earned. */
    document.querySelectorAll("[data-cart-delivery]").forEach((el) => {
      const free = !empty && deliveryFee === 0;
      el.textContent = free ? t("مجاني") : egp(deliveryFee);
      // Same swap as the promo message above — "FREE" in 1.9:1 lime was the
      // least readable word in the summary.
      el.classList.toggle("text-heading", free);
      el.classList.toggle("font-bold", free);
    });
    /* "Add X more for free delivery" progress bar. Hidden on an empty basket;
       fills toward FREE_SHIP and flips to the success message once reached. */
    const toFree = Math.max(0, FREE_SHIP - sub);
    document.querySelectorAll("[data-freeship]").forEach((el) => (el.hidden = empty));
    /* The fill is LIGHT green throughout (Ahmed, 2026-08-23). It used to paint
       in `bg-cta` — the same near-black brand green as the primary buttons —
       which made a progress bar read with the weight of a CTA and, on the cream
       track, as a hard dark slab. The completed state no longer needs its own
       colour either: the caption right above it already flips to the 🎉 line. */
    document.querySelectorAll("[data-freeship-fill]").forEach((el) => {
      el.style.width = (empty ? 0 : Math.min(100, (sub / FREE_SHIP) * 100)) + "%";
    });
    document.querySelectorAll("[data-freeship-msg]").forEach((el) => {
      el.innerHTML =
        toFree > 0
          ? esc(t("أضف")) +
            ' <span class="font-bold latin">' + egp(toFree) + "</span> " +
            esc(t("لتحصل على شحن مجاني"))
          : "🎉 " + esc(t("مبروك! توصيل طلبك مجاني"));
    });
    syncPromoUI();
  }

  /*
   * Throw a product's image into the cart button and tick the badge when it
   * lands. Returns whether a flight actually started, because the caller has
   * to know: the badge is held from BEFORE the mutation until the landing, so
   * a hold with no flight to release it would freeze the number forever.
   */
  /* opts.onLand fires when the ghost arrives — or immediately when there is
     no flight to wait for (no source, no cart button on screen, or reduced
     motion). Callers that open something on arrival need it to run in EVERY
     one of those cases, or the drawer silently never opens for a shopper who
     has reduced motion turned on. It is called before the badgeHold guard
     below for the same reason: that guard is about which flight repaints the
     badge, and has nothing to do with this caller's follow-up. */
  /* The flight source is meant to be the product PHOTO. On a product card
     that is simply the card's own first <img>. But on the single-product
     page the buy controls (the cart-bound stepper and اشتري الان) live in the
     DETAILS column — a [data-product] host whose first <img> is a spec icon
     (the 3D leaf/bolt/shield PNGs in trust_row_3d), not the product — while
     the real photo is the gallery's [data-gallery-main] over in the media
     column. Prefer that when it exists so the PRODUCT flies to the cart, not
     the leaf icon (Ahmed, 2026-07-30). Rails on the product page keep using
     their own card image (the card-step path passes it directly and does not
     call this), so a companion product still flies from its own card. */
  function productFlightImg(scope) {
    return (
      document.querySelector("[data-gallery-main]") ||
      (scope && scope.querySelector("img")) ||
      null
    );
  }

  /* Adding to the cart no longer FLIES anything (Ahmed, 2026-08-23: "remove
     it and just animate the number in the floating cart").
     
     What is left is the landing, played immediately: the badge rolls to its new
     number, the button takes a small squash and the glyph pulses. That was
     always the part carrying the message — the flight was a way of pointing at
     it, and pointing costs ~600ms during which the shopper cannot press the
     button again without the animation stacking.

     `sourceEl` and `opts.from` are still accepted so the ~dozen call sites need
     no change, and `flyTo` itself is left in place: the product-page story ride
     still uses it, and it is the obvious thing to call again if the flight is
     ever wanted back.

     badgeHold is what deferred the badge repaint until a flight landed. With
     nothing in the air there is nothing to defer, so it stays at 0 and the
     ordinary `if (!badgeHold) syncCartBadges()` path just runs. */
  function throwToCart(sourceEl, opts) {
    const target = visibleCartButton();
    const onLand = opts && opts.onLand;
    if (onLand) onLand();
    if (!target || reduceMotion()) return false;
    // The badge rolls, so it is not ALSO pulsed — a pulse started a frame later
    // would take over the transform and cut the roll off mid-slide. The button
    // takes the catch instead.
    syncCartBadges();
    squash(target);
    const glyph = target.querySelector("[data-cart-glyph]");
    if (glyph) pulse(glyph);
    return true;
  }

  /* The bundle total has to answer the checkboxes. It was baked at build
     time, so unticking a companion left the figure claiming a price for
     something you had just declined to buy. */
  function syncBundleTotal() {
    document.querySelectorAll("[data-bundle]").forEach((box) => {
      const out = box.querySelector("[data-bundle-total]");
      if (!out) return;
      let sum = Number(box.dataset.bundleBase) || 0;
      box.querySelectorAll("[data-bundle-item]").forEach((row) => {
        const check = row.querySelector("[data-bundle-check]");
        if (check && !check.checked) return;
        sum += Number(row.dataset.price) || 0;
      });
      out.textContent = egp(sum);
    });
  }

  function initCartUI() {
    Cart.init();
    document.addEventListener("cart:change", renderCart);
    renderCart();
    syncBundleTotal();
    document.addEventListener("change", (e) => {
      if (e.target.closest("[data-bundle-check]")) syncBundleTotal();

      /* Wallet switch. `change`, not `click`: the control is a checkbox inside
         a <label>, so a click on the label fires click TWICE (once for the
         label, once for the forwarded activation) but change exactly once.
         Reading e.target.checked also means the keyboard path (space) works
         without a second handler. */
      /* Gift order. Three things follow the switch, and they have to move
         together or the form contradicts itself. */
      const giftSwitch = e.target.closest("[data-gift-switch]");
      if (giftSwitch) {
        const on = giftSwitch.checked;
        const panel = document.querySelector("[data-gift-panel]");

        /* Persisted, because the rule it enforces lives on the NEXT page. The
           gift card promises "الدفع عند الاستلام غير متاح لطلبات الهدايا", and
           cash on delivery is chosen on payment.html — so the flag has to
           survive the navigation or the promise is decoration. */
        if (on) localStorage.setItem(GIFT_KEY, "1");
        else localStorage.removeItem(GIFT_KEY);

        /* `required` is added and removed with the toggle, never authored into
           the markup. A required field inside the collapsed panel makes the
           browser refuse to submit and point its validation bubble at an
           element with no height — the shopper gets a blocked form and nothing
           to look at. */
        if (panel) {
          panel.querySelectorAll("input").forEach((input) => {
            if (on) input.setAttribute("required", "");
            else input.removeAttribute("required");
          });
          /* aria-hidden follows the collapse so a screen reader does not walk
             into fields that are visually gone. */
          panel.setAttribute("aria-hidden", on ? "false" : "true");
        }

        /* Pickup contradicts gifting — the recipient is the point — so it is
           blocked rather than merely discouraged. If it was already the
           selection, hand the choice back to delivery: leaving a dimmed,
           unclickable option checked would strand the form in a state the
           shopper cannot get out of. */
        const pickupBox = document.querySelector("[data-pickup-option]");
        if (pickupBox) {
          /* One class does the whole visual change: dimming, blocking the
             pointer, and swapping the radio dot for the reason (styles.css).
             Nothing here shows or hides the note itself, so the two can never
             disagree about which is on screen. */
          pickupBox.classList.toggle("option-blocked", on);

          /* The chosen branch is SAVED and restored, not recomputed. Turning
             gifting on and off again used to be enough to lose it: the row's
             meta would come back as the generic "اختر الفرع" prompt and the
             shopper would have to re-pick a store they had already chosen. */
          if (on) {
            if (optMetaResolved("pickup")) savedPickupMeta = optMetaText("pickup");
          } else if (savedPickupMeta) {
            setOptMeta("pickup", savedPickupMeta, true);
          }

          const pickupInput = pickupBox.querySelector("input[type=radio]");
          if (on && pickupInput && pickupInput.checked) {
            const fallback = document.querySelector(
              'input[name="' + pickupInput.name + '"]:not([value="pickup"])',
            );
            if (fallback) {
              fallback.checked = true;
              toast("الاستلام من المتجر غير متاح لطلبات الهدايا");
            }
          }
          if (pickupInput) pickupInput.disabled = on;
        }
        return;
      }

      const walletSwitch = e.target.closest("[data-wallet-switch]");
      if (walletSwitch) {
        const card = walletSwitch.closest("[data-wallet-toggle]");
        const balance = Number(card && card.dataset.walletBalance) || 0;
        if (walletSwitch.checked && balance > 0) {
          localStorage.setItem(WALLET_KEY, String(balance));
          /* renderCart caps the figure at the bill, so quote what was actually
             taken off rather than the whole balance — telling someone with a
             EGP 90 basket that EGP 1,200 came off is wrong twice over. */
          renderCart();
          syncWalletUI();
          const used = Math.min(balance, Cart.subtotal() + DELIVERY_FEE);
          toast(t("تم خصم") + " " + egp(used) + " " + t("من الإجمالي"), "spend");
          celebrate(card);
        } else {
          localStorage.removeItem(WALLET_KEY);
          renderCart();
          syncWalletUI();
          toast("تم إلغاء خصم المحفظة", "info");
        }
        return;
      }
    });
    // A discount applied on a previous page (cart -> checkout) must paint on
    // arrival, not wait for the first click.
    syncWalletUI();
    syncGiftRules();

    /* Enter inside a promo input applies it — the field is not a <form> (it can
       sit inside the checkout's place-order form, and a nested form would submit
       the order), so the submit gesture is wired by hand. Scoped to the field
       that holds focus, like the Apply button. */
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Enter") return;
      const input = e.target.closest("[data-promo-input]");
      if (!input) return;
      e.preventDefault();
      applyPromo(input.closest("[data-promo]"));
    });

    document.addEventListener("click", (e) => {

      /* Promo — open the field, then apply. Both live here rather than in the
         component so the cart page and checkout share one implementation. */
      const promoOpen = e.target.closest("[data-promo-open]");
      if (promoOpen) {
        const wrap = promoOpen.closest("[data-promo]");
        const box = wrap && wrap.querySelector("[data-promo-box]");
        if (box) {
          box.hidden = false;
          promoOpen.hidden = true;
          const input = box.querySelector("[data-promo-input]");
          if (input) input.focus();
        }
        return;
      }

      const promoApply = e.target.closest("[data-promo-apply]");
      if (promoApply) {
        applyPromo(promoApply.closest("[data-promo]"));
        return;
      }

      /* Remove/cancel an applied code — back to the trigger state. Resets EVERY
         field, not just the one clicked: one code is stored globally, so the
         drawer and the page both have to fall back to their trigger. */
      if (e.target.closest("[data-promo-remove]")) {
        localStorage.removeItem(PROMO_KEY);
        document.querySelectorAll("[data-promo]").forEach((wrap) => {
          const box = wrap.querySelector("[data-promo-box]");
          const input = wrap.querySelector("[data-promo-input]");
          const msg = wrap.querySelector("[data-promo-msg]");
          if (box) box.hidden = true;
          if (input) input.value = "";
          if (msg) {
            msg.hidden = true;
            msg.textContent = "";
          }
        });
        renderCart();
        toast(t("تم إلغاء الكود"));
        return;
      }

      /* An option row that owns a picker opens it on selection, so choosing
         "pick up in store" and choosing WHICH store are one gesture. Not
         `return`-ing: the row is a <label>, and the radio still has to receive
         the click that selects it. */
      const opensRow = e.target.closest("[data-opens]");
      if (opensRow) {
        const key = opensRow.getAttribute("data-opens");
        if (key === "storepicker") initStorePicker();
        if (key === "schedule") renderSchedule();
        openOverlay(key);
        /* Re-measure once the modal is actually on screen. Everything inside a
           hidden overlay has zero width, so the arrows sized during the render
           above would conclude there is nothing to scroll. */
        if (key === "schedule") setTimeout(syncSchedArrows, 60);
      }

      const storePick = e.target.closest("[data-store-pick]");
      if (storePick) {
        const list = storePick.closest("[data-store-list]");
        list.querySelectorAll("[data-store-pick]").forEach((b) => b.classList.remove("is-active"));
        storePick.classList.add("is-active");
        const gov = document.querySelector("[data-store-gov]");
        const tree = loadStoreTree();
        const group = tree[(gov && +gov.value) || 0];
        pickedStore = group && group.branches[+storePick.dataset.storePick];
        const confirm = document.querySelector("[data-store-confirm]");
        if (confirm) confirm.disabled = !pickedStore;
        return;
      }

      if (e.target.closest("[data-store-confirm]")) {
        if (pickedStore) {
          setOptMeta("pickup", pickedStore.t, true);
          closeOverlay();
        }
        return;
      }

      const schedNav = e.target.closest("[data-sched-nav]");
      if (schedNav) {
        scrollSchedDays(+schedNav.dataset.schedNav);
        return;
      }

      const schedDay = e.target.closest("[data-sched-day]");
      if (schedDay) {
        pickedDay = +schedDay.dataset.schedDay;
        // Changing the day clears the slot: slot 3 on Tuesday is not slot 3 on
        // Wednesday, and silently carrying the index over would confirm a time
        // the shopper never looked at.
        pickedSlot = null;
        renderSchedule();
        return;
      }

      const schedSlot = e.target.closest("[data-sched-slot]");
      if (schedSlot) {
        pickedSlot = +schedSlot.dataset.schedSlot;
        renderSchedule();
        return;
      }

      if (e.target.closest("[data-sched-confirm]")) {
        if (pickedSlot !== null) {
          const days = schedDays();
          setOptMeta("later", days[pickedDay].label + " · " + schedSlots()[pickedSlot], true);
          closeOverlay();
        }
        return;
      }

      /* Product-page buy CTA. Two states on one button — see the block
         comment in build/pages/product.py for the flow it replaces.

         Already in the cart: this is "عرض السلة", so just open the summary.
         Adding nothing is the point; the stepper is how you change quantity
         now, and a CTA that silently re-added would fight it.

         Not in the cart: add the stepper's quantity, then open the summary
         WHEN THE GHOST LANDS. Opening immediately would slide the drawer over
         the top of the flight it was supposed to complete — the item would
         appear to be thrown at a panel that was already covering the target.
         onLand also fires when there is no flight at all (reduced motion, or
         the cart button off-screen), so the drawer opens either way. */
      const buyCta = e.target.closest("[data-buy-cta]");
      if (buyCta) {
        const product = productFrom(buyCta);
        if (!product) return;
        /* Already in the basket — the stepper put it there — so this is purely
           "carry on", and the summary is what carries on. */
        if (Cart.find(product.id)) {
          openOverlay("cart");
          return;
        }
        /* Not in the basket. "Buy now" that buys nothing would be a dead
           button, so add one and open the summary when it lands. */
        const scope = buyCta.closest("[data-product]") || document;
        const img = productFlightImg(scope);
        throwToCart(img, {
          card: true,
          tag: "+1",
          onLand: () => openOverlay("cart"),
        });
        Cart.add(product, 1);
        toast("تمت الإضافة إلى السلة", "cart");
        return;
      }

      /* Cart-bound stepper (product page). This is the add control: there is
         no separate "add to cart" press any more, so + on a product that is
         not in the basket is what puts it there, and every press after that
         moves the same line. − at 1 removes it and the counter returns to 0.

         Every + throws a ghost to the cart, exactly like the card stepper —
         with no add button left, this flight is the only motion confirming
         that a press reached the basket. Cart.setQty removes below 1 by
         itself, so there is no separate branch for the trash state. */
      const boundStep = e.target.closest("[data-cart-bound] [data-step]");
      if (boundStep) {
        const delta = parseInt(boundStep.getAttribute("data-step"), 10);
        const product = productFrom(boundStep);
        if (!product) return;
        const line = Cart.find(product.id);
        const scope = boundStep.closest("[data-product]");

        if (delta > 0) {
          throwToCart(productFlightImg(scope), {
            card: true,
            quick: true,
            tag: "+1",
          });
        }
        if (!line) {
          if (delta > 0) Cart.add(product, 1);
          return; // at 0 a − has nothing to take away
        }
        const next = line.qty + delta;
        Cart.setQty(product.id, next);
        if (next < 1) toast("تمت الإزالة من السلة", "info");
        return; // syncBuyBlock repaints the digit off the store
      }

      const add = e.target.closest("[data-add-to-cart]");
      if (add) {
        const product = productFrom(add);
        if (!product) return;
        // Respect a quantity stepper sitting next to the button (product page).
        const scope = add.closest("[data-product]") || document;
        const qtyEl = scope.querySelector("[data-stepper] [data-qty]");

        /* Send the product image to the cart, and hold the badge at its old
           number until it lands. The mutation itself is not delayed — the
           store updates now, only the badge waits, so nothing can desync.
           The hold has to start BEFORE the mutation, or Cart.add's
           `cart:change` repaints the badge on the way past. */
        const img = scope.querySelector && scope.querySelector("img");
        const qty = qtyEl ? parseInt(qtyEl.textContent, 10) : 1;
        throwToCart(img, { card: true, tag: "+" + qty });

        Cart.add(product, qty);
        toast("تمت الإضافة إلى السلة", "cart");
        return;
      }

      /* "أضف الجميع الى السلة" — the frequently-bought-together block.
         Adds this product plus every companion still ticked, in one go and
         with one flight, rather than three separate ghosts racing each
         other. Nothing ticked still adds the product being viewed, which is
         what the total says it will do. */
      const bundleAdd = e.target.closest("[data-bundle-add]");
      if (bundleAdd) {
        const box = bundleAdd.closest("[data-bundle]");
        if (!box) return;
        const picks = [];
        const base = productFrom(box);
        if (base) picks.push(base);
        box.querySelectorAll("[data-bundle-item]").forEach((row) => {
          const check = row.querySelector("[data-bundle-check]");
          if (check && !check.checked) return;
          const prod = productFrom(row);
          if (prod) picks.push(prod);
        });
        if (!picks.length) return;
        const img = box.querySelector("[data-bundle-item] img") || box.querySelector("img");
        throwToCart(img, { card: true, tag: "+" + picks.length });
        picks.forEach((prod) => Cart.add(prod, 1));
        toast(picks.length + " " + t("منتجات أُضيفت إلى السلة"));
        return;
      }

      /* Card stepper. Every increment throws another one across the page —
         the reward for pressing + is the same little flight, not a number
         that quietly changes. Stepping below 1 drops the line, which puts
         the add button back. */
      const cardStep = e.target.closest("[data-card-step]");
      if (cardStep) {
        const product = productFrom(cardStep);
        if (!product) return;
        const card = cardStep.closest("[data-product]");
        const delta = parseInt(cardStep.dataset.cardStep, 10);
        const it = Cart.find(product.id);
        const next = (it ? it.qty : 0) + delta;

        if (next < 1) {
          Cart.remove(product.id);
          toast("تمت الإزالة من السلة", "info");
          return;
        }
        if (delta > 0) throwToCart(card && card.querySelector("img"), { card: true, quick: true, tag: "+1" });
        if (it) Cart.setQty(product.id, next);
        else Cart.add(product, 1);

        pulse(cardStep);
        // The quantity itself is NOT pulsed here any more: syncCardSteppers
        // rolls it directionally on the same tick, and a pulse started after
        // the roll would win the transform and cancel it mid-slide.
        return;
      }

      /* Cart line stepper. Cart.setQty removes the line by itself below 1, so
         the trash state of the − button needs no separate branch — it is the
         same press, and the store already did the right thing with it. The
         toast is here because removal is now one tap from a quantity of 1,
         where it used to need the separate حذف link: it names what went, so an
         accidental press is recoverable knowledge rather than a row that
         vanished. */
      const step = e.target.closest("[data-cart-step]");
      if (step) {
        const line = step.closest("[data-cart-line]");
        const it = Cart.find(line.dataset.id);
        if (!it) return;
        const next = it.qty + parseInt(step.dataset.cartStep, 10);
        Cart.setQty(it.id, next);
        if (next < 1) toast("تمت الإزالة من السلة", "info");
        return;
      }
    });
  }

  /* ---------------------------------------------------------------
     Favourites UI

     Two jobs: reflect saved state onto every heart button on the page, and
     drive the favourites account page.

     The heart's filled/outline state is expressed purely through
     `aria-pressed` — the accessible state and the visual state are the same
     attribute, so they cannot drift. styles.css does the icon swap off that
     selector. Note it does NOT use the `hidden` attribute: `[hidden]` is
     already forced with `!important` in styles.css, which would make the
     state impossible to override back on. See CLAUDE.md.
     --------------------------------------------------------------- */
  function syncFavButtons(scope) {
    (scope || document).querySelectorAll("[data-fav-toggle]").forEach((btn) => {
      const product = productFrom(btn);
      if (!product) return;
      const on = Favs.has(product.id);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.setAttribute("aria-label", t(on ? "إزالة من المفضلة" : "أضف إلى المفضلة"));
    });
  }

  /*
   * The favourites page ships every catalogue card in the DOM, hidden, and
   * this reveals the saved ones — the same "filter what is already rendered"
   * approach the listing chips use, so the card markup still comes from
   * components.py alone rather than being duplicated in JS, and it works
   * from file:// with no fetch.
   */
  function renderFavsPage() {
    const grid = document.querySelector("[data-favs-grid]");
    if (!grid) return;
    let shown = 0;
    grid.querySelectorAll("[data-product]").forEach((card) => {
      const on = Favs.has(card.dataset.id);
      card.hidden = !on;
      if (on) shown++;
    });
    const empty = document.querySelector("[data-favs-empty]");
    if (empty) empty.hidden = shown > 0;
    grid.hidden = shown === 0;
    const countEl = document.querySelector("[data-favs-count]");
    if (countEl) countEl.textContent = String(shown);
  }

  /* ---------------------------------------------------------------
     Demo auth UI — the sign-in form, and the chrome that reflects it.
     --------------------------------------------------------------- */
  function initAuthUI() {
    Auth.init();

    // Return-destination from ?next= — only a same-site .html filename is
    // honoured, never an absolute URL from the query string (open-redirect).
    const nextParam = () => {
      try {
        return new URLSearchParams(location.search).get("next") || "";
      } catch (e) {
        return "";
      }
    };
    const safeNext = (n) => (/^[a-z0-9_-]+\.html$/i.test(String(n || "")) ? n : "");

    const paintAccountLinks = () => {
      const authed = Auth.isAuthed();
      const u = Auth.user();
      document.querySelectorAll("[data-account-link]").forEach((el) => {
        el.setAttribute("href", pageHref(authed ? "/my-account" : "/login"));
        const label = el.querySelector("[data-account-label]");
        if (label) {
          label.textContent = authed
            ? currentLang() === "en"
              ? u.nameEn
              : u.name
            : t("الحساب");
        }
      });
      document.querySelectorAll("[data-authed-only]").forEach((el) => {
        el.hidden = !authed;
      });
      document.querySelectorAll("[data-anon-only]").forEach((el) => {
        el.hidden = authed;
      });
      // Email-verify banner — only for a signed-in user whose email is
      // EXPLICITLY unverified (a freshly registered account). Undefined counts
      // as verified, so an older demo session never surfaces it.
      document.querySelectorAll("[data-email-unverified]").forEach((el) => {
        el.hidden = !(authed && u && u.emailVerified === false);
      });
      // The verify page shows the mobile the OTP was "sent" to.
      const p = Auth.pending();
      document.querySelectorAll("[data-otp-mobile]").forEach((el) => {
        el.textContent = (p && p.mobile) || "—";
      });
    };

    document.addEventListener("auth:change", paintAccountLinks);
    paintAccountLinks();

    // Passwordless LOGIN — a mobile number, then hand off to the OTP page.
    document.querySelectorAll("[data-login-form]").forEach((form) => {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const mobile = (form.querySelector('[name="mobile"]') || {}).value || "";
        if (String(mobile).replace(/\D/g, "").length < 6) {
          toast(t("من فضلك أدخل رقم موبايل صحيح"), "error");
          return;
        }
        Auth.startLogin(mobile, safeNext(nextParam()));
        window.location.href = pageHref("/verify");
      });
    });

    // REGISTER — capture the details, then hand off to the same OTP page.
    document.querySelectorAll("[data-register-form]").forEach((form) => {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const val = (n) => (form.querySelector('[name="' + n + '"]') || {}).value || "";
        const mobile = val("phone") || val("mobile");
        if (String(mobile).replace(/\D/g, "").length < 6) {
          toast(t("من فضلك أدخل رقم موبايل صحيح"), "error");
          return;
        }
        Auth.startRegister(
          {
            firstName: val("first-name"),
            lastName: val("last-name"),
            mobile: mobile,
            email: val("email"),
          },
          safeNext(nextParam()),
        );
        window.location.href = pageHref("/verify");
      });
    });

    // OTP verify page.
    const otpForm = document.querySelector("[data-otp-form]");
    if (otpForm) {
      // No pending flow means there is nothing to verify — bounce to sign in.
      if (!Auth.pending()) {
        window.location.href = pageHref("/login");
        return;
      }
      const boxes = [...otpForm.querySelectorAll("[data-otp-box]")];
      const readCode = () => boxes.map((b) => b.value).join("").trim();
      // Single-digit boxes with auto-advance and backspace between them.
      boxes.forEach((box, i) => {
        box.addEventListener("input", () => {
          box.value = box.value.replace(/\D/g, "").slice(-1);
          box.classList.toggle("is-filled", !!box.value);
          if (box.value && i < boxes.length - 1) boxes[i + 1].focus();
        });
        box.addEventListener("keydown", (ev) => {
          if (ev.key === "Backspace" && !box.value && i > 0) boxes[i - 1].focus();
        });
      });
      const msg = otpForm.querySelector("[data-otp-msg]");
      otpForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const res = Auth.verifyOtp(readCode());
        if (res.ok) {
          if (msg) msg.hidden = true;
          // Flip the button to a "verified" state before the redirect so the
          // shopper sees the success, not an instant page swap (Ahmed).
          const submitBtn = otpForm.querySelector("[data-otp-submit]");
          if (submitBtn) {
            submitBtn.textContent = "✓ " + t("تم التحقق");
            submitBtn.disabled = true;
            submitBtn.classList.add("opacity-90", "pointer-events-none");
          }
          toast(t("تم تسجيل الدخول بنجاح"));
          const dest = safeNext(res.next);
          setTimeout(() => {
            window.location.href = dest || pageHref("/my-account");
          }, 1100);
        } else if (msg) {
          msg.textContent = t("رمز التحقق غير صحيح، حاول مرة أخرى");
          msg.hidden = false;
        } else {
          toast(t("رمز التحقق غير صحيح، حاول مرة أخرى"), "error");
        }
      });
      // Resend with a cooldown (Ahmed, 2026-08-04): after a "send" the button
      // disables and counts down the seconds left before another send is
      // allowed; it re-enables at zero. The cooldown also runs on load, since a
      // code was just sent arriving here.
      const RESEND_COOLDOWN = 30;
      const resendBtn = otpForm.querySelector("[data-resend-otp]");
      if (resendBtn) {
        /* Capture the ARABIC source string, and run it through t() at every
           write (Ahmed, 2026-08-23). initAuthUI runs before applyLangToContent
           in boot(), so this reads the markup's Arabic — which is exactly what
           we want as a translation KEY, and exactly what we must not print. The
           old code cached the raw label and wrote it straight back when the
           cooldown expired, so an English visitor watched the button count down
           in English and then flip to "إعادة إرسال الرمز". */
        const baseKey = resendBtn.textContent.trim();
        let resendTimer = null;
        const cooldown = (secs) => {
          let left = secs;
          resendBtn.disabled = true;
          resendBtn.classList.add("opacity-50", "pointer-events-none");
          const paint = () => {
            if (left <= 0) {
              clearInterval(resendTimer);
              resendTimer = null;
              resendBtn.disabled = false;
              resendBtn.classList.remove("opacity-50", "pointer-events-none");
              resendBtn.textContent = t(baseKey);
              return;
            }
            resendBtn.textContent =
              t("إعادة الإرسال خلال") +
              ' ' + left + ' ' + t("ثانية");
            left -= 1;
          };
          paint();
          resendTimer = setInterval(paint, 1000);
        };
        resendBtn.addEventListener("click", () => {
          if (resendBtn.disabled) return;
          toast(t("تم إرسال رمز جديد"));
          cooldown(RESEND_COOLDOWN);
        });
        cooldown(RESEND_COOLDOWN);
      }
    }

    /* Verify-email — the dashboard banner AND the profile page's email row
       (Ahmed, 2026-08-23). Auth.verifyEmail() only returns true when there was
       genuinely an unverified email to flip, so the row is repainted
       unconditionally: on the profile page the demo identity carries no
       emailVerified flag at all, and the row would otherwise sit on "غير مؤكد"
       forever no matter how many times the button was pressed. */
    const paintEmailRow = () => {
      document.querySelectorAll("[data-email-row]").forEach((row) => {
        const verified = !(Auth.user() && Auth.user().emailVerified === false);
        row.querySelectorAll("[data-email-state]").forEach((el) => {
          el.hidden = (el.dataset.emailState === "verified") !== verified;
        });
      });
    };
    document.addEventListener("auth:change", paintEmailRow);

    document.querySelectorAll("[data-verify-email]").forEach((btn) => {
      btn.addEventListener("click", () => {
        Auth.verifyEmail();
        const row = btn.closest("[data-email-row]");
        if (row) {
          row.querySelectorAll("[data-email-state]").forEach((el) => {
            el.hidden = el.dataset.emailState !== "verified";
          });
        }
        toast(t("تم تأكيد بريدك الإلكتروني بنجاح"));
      });
    });

    document.querySelectorAll("[data-logout]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        Auth.logout();
        toast(t("تم تسجيل الخروج"));
        setTimeout(() => (window.location.href = pageHref("/")), 600);
      });
    });
  }

  /* ---------------------------------------------------------------
     "شاهدت هذا مؤخراً" — the recently-viewed rail on the product page.

     Renders the SAME card shape as `product_card()` in components.py
     (`.product-card`, `.product-card__frame`, `[data-card-stepper]` and all)
     so it drops straight into the existing add-to-cart delegation and
     `syncCardSteppers()` with no card-specific wiring. It only omits the
     sale strike-through and the "peek" zoom badge, because a stored view —
     unlike a card built from catalog.json — never carries `regular`/`sale`.
     --------------------------------------------------------------- */
  /* The scene shot for a product id.
   *
   * Recently-viewed entries are whatever `data-image` said when the product was
   * viewed, and until 2026-08-24 the product page put the WHITE CUT-OUT there
   * while recentCardHTML treated the stored path as the scene. The result was a
   * rail where anything the shopper had actually visited rendered as a pale
   * cut-out in scenes mode, while the seeded entries looked right.
   *
   * The page records the scene now, but entries already in localStorage still
   * hold the old path, so this heals them on read rather than waiting for the
   * shopper to re-visit each product: a stored path under products/ is the
   * cut-out, and every one of the 26 SKUs has products-styled/<id>.jpg. */
  function sceneFor(id, stored) {
    if (stored && stored.indexOf("products-styled/") !== -1) return stored;
    return "images/jaad/products-styled/" + String(id) + ".jpg";
  }

  function recentCardHTML(p, compact) {
    const id = esc(String(p.id));
    const name = esc(p.name || "");
    const price = Number(p.price) || 0;
    const whole = Math.floor(price);
    const dec = String(Math.round((price - whole) * 100)).padStart(2, "0");
    // Mirrors components.product_widget() (Figma 9946:16778): bordered square,
    // green sticker price badge with a lime offset shadow, circular cart button.
    // `compact` shrinks it for the cart-drawer upsell (Ahmed, 2026-08-18) while
    // keeping the exact same design language as the homepage card.
    const c = compact === true;
    const width = c ? "w-[152px]" : "w-[258px]";
    const btnPos = c ? "right-3 -bottom-4" : "right-4 -bottom-5";
    const btnSize = c ? "size-9" : "size-10";
    const cartIco = c ? "w-5 h-5" : "w-[22px] h-[22px]";
    const stepH = c ? "h-9" : "h-10";
    // Phone-first counter sizing + badge clearance, matching product_widget()
    // in components.py (Ahmed, 2026-08-19): the +/- targets grow to size-10 on
    // phones (compact stays small from sm up), and the text block takes extra
    // top padding so the straddling counter clears the price badge. Keep the
    // two in step — the cards must read as ONE control site-wide.
    const stepBtn = c ? "size-10 sm:size-7" : "size-10 sm:size-8";
    const stepIco = "w-5 h-5 sm:w-4 sm:h-4";
    const pad = c ? "gap-2 p-2 pt-8 sm:pt-2" : "gap-3 p-3 pt-9 sm:pt-3";
    /* The badge comes from the shared sticker constants — sm for the compact
       drawer card, md for the full one — rather than five separate size
       ternaries that had drifted 3px off the component. */
    const stick = c ? STICKER_SM : STICKER_MD;
    const titleCls = c ? "text-sm line-clamp-2 min-h-[2.5em]" : "text-lg";
    return `
      <article class="product-widget${c ? " product-widget--sm" : ""} carousel-slide ${width} shrink-0 snap-start"
               data-product data-id="${id}" data-name="${name}" data-price="${price}" data-image="${esc(p.image || "")}">
        <div class="relative">
          <a href="product-${id}.html" class="block relative bg-white border border-[#C1C3C6] rounded-2xl aspect-square overflow-hidden">
            <img src="${esc(imgFor(sceneFor(id, p.image), PLAIN_BY_ID[id]))}" data-img-scene="${esc(sceneFor(id, p.image))}" data-img-plain="${esc(PLAIN_BY_ID[id] || p.image || "")}" alt="${name}" class="w-full h-full object-cover" loading="lazy" />
          </a>
          <div class="${btnPos} z-10 absolute">
            <button type="button" data-add-to-cart aria-label="Add to cart"
                    class="btn-elevate place-items-center grid bg-cta hover:bg-cta-hover shadow-custom4 rounded-full ${btnSize} text-white transition-colors">
              <span class="${cartIco}">${ICON.cart}</span>
            </button>
            <div data-card-stepper hidden class="items-center gap-1 bg-white shadow-custom4 p-1 border border-divider rounded-full flex">
              <button type="button" data-card-step="-1" aria-label="Decrease" class="place-items-center grid border border-divider hover:bg-cream rounded-full ${stepBtn} text-ink shrink-0 transition-colors"><span class="${stepIco}">${ICON.minus}</span></button>
              <span data-card-qty class="min-w-[1.5ch] font-bold text-ink text-center latin">1</span>
              <button type="button" data-card-step="1" aria-label="Increase" class="place-items-center grid bg-cta hover:bg-cta-hover rounded-full ${stepBtn} text-white shrink-0 transition-colors"><span class="${stepIco}">${ICON.plus}</span></button>
            </div>
          </div>
        </div>
        <div class="product-widget__body flex flex-col ${pad}">
          <span class="items-end gap-0.5 self-start inline-flex ${stick.box} font-bold text-white latin">
            <span class="${stick.egp} leading-[1.4]">EGP</span>
            <span class="${stick.whole} leading-[1.2]">${whole}</span>
            <span class="${stick.egp} leading-[1.4]">.${dec}</span>
          </span>
          <div class="flex flex-col gap-0.5">
            <h3 class="font-semibold text-black ${titleCls} leading-snug">
              <a href="product-${id}.html" data-product-title class="hover:text-heading transition-colors">${name}</a>
            </h3>
            ${weightOf(id) ? `<span class="text-muted ${c ? "text-xs" : "text-sm"} latin" data-product-weight>${esc(weightOf(id))}</span>` : ""}
          </div>
        </div>
      </article>`;
  }

  // The rail must show at least this many on EVERY product page (Ahmed,
  // 2026-07-30) — an empty "previously seen" strip on a first visit read as
  // broken. Genuine history leads; when there is less of it than this we top
  // up from a real-product pool so the section is never sparse. Display-only:
  // the padding is NOT written back into the Recent store, so it never
  // masquerades as something the shopper actually viewed once they browse.
  const RECENT_MIN = 4;
  const RECENT_FALLBACK = FAVS_SEED; // real catalogue products, {id,name,price,image}

  function initRecentlyViewed() {
    Recent.init();

    document.querySelectorAll("[data-recently-viewed]").forEach((section) => {
      const track = section.querySelector("[data-recent-track]");
      if (!track) return;
      const excludeId = section.dataset.excludeId;
      const items = Recent.exclude(excludeId);
      const min = Number(section.dataset.recentMin) || RECENT_MIN;

      // Pad up to `min` with fallback products, skipping the current
      // product and anything already in the list (dedupe by id).
      if (items.length < min) {
        const have = new Set(items.map((x) => String(x.id)));
        have.add(String(excludeId));
        for (const p of RECENT_FALLBACK) {
          if (items.length >= min) break;
          if (have.has(String(p.id))) continue;
          items.push(p);
          have.add(String(p.id));
        }
      }

      if (!items.length) return; // only if the pool itself is empty
      track.innerHTML = items.map((x) => recentCardHTML(x)).join("");
      section.hidden = false;
      syncCardSteppers(section);
    });

    // Record the CURRENT product as viewed AFTER rendering the rail above,
    // so a product never lists itself the first time its own page loads.
    const host = document.querySelector("[data-record-view]");
    const product = host && productFrom(host);
    if (product) Recent.add(product);
  }

  function initFavsUI() {
    Favs.init();

    const refresh = () => {
      syncFavButtons();
      renderFavsPage();
      // Keep every wishlist-count pill in step with the store — the account
      // sidebar shows one on ALL its pages, not just the favourites page that
      // renderFavsPage runs on (Ahmed, 2026-08-04).
      const n = String(Favs.count());
      document
        .querySelectorAll("[data-favs-count]")
        .forEach((el) => (el.textContent = n));
    };
    document.addEventListener("favs:change", refresh);
    refresh();

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-fav-toggle]");
      if (!btn) return;
      const product = productFrom(btn);
      if (!product) return;

      const wasOn = Favs.has(product.id);
      const on = Favs.toggle(product);
      toast(on ? "تمت الإضافة إلى المفضلة" : "تمت الإزالة من المفضلة");

      // The heart itself always reacts, so the control feels alive even where
      // there is nowhere to fly to (the phone masthead has no account icon).
      pulse(btn);
      if (!on || wasOn) return;

      const target = visibleAccountTarget();
      if (!target) return;
      // A filled heart in the brand red-pink, not a clone of the button — the
      // button is an outline at rest, and an outline reads as nothing at 16px.
      const heartGhost =
        '<span style="display:grid;place-items:center;width:100%;height:100%;color:#e0245e">' +
        '<svg viewBox="0 0 24 24" fill="currentColor" style="width:100%;height:100%">' +
        '<path d="M12 20.5s-7.5-4.6-7.5-9.6a4.4 4.4 0 0 1 7.5-3.1 4.4 4.4 0 0 1 7.5 3.1c0 5-7.5 9.6-7.5 9.6Z"/>' +
        "</svg></span>";
      flyTo(btn, target, heartGhost).then(() => {
        pulse(target);
      });
    });
  }

  /* ---------------------------------------------------------------
     Products mega-panel (desktop)
     --------------------------------------------------------------- */
  /* Flash-sale countdown (Figma node 9943:16452). No real sale window exists,
     so this is a rolling 2-day demo deadline — it always shows a live, plausible
     countdown and resets cleanly. Updates Days/Hours/Mins (no seconds in the
     design), so a 20s tick keeps the minutes honest without churn. */
  function initFlashCountdown() {
    /* querySelectorAll, not querySelector (Ahmed, 2026-08-25). The promo now
       renders TWICE — once in the desktop utility bar, once in the phone's own
       strip — and only one of the two is ever visible, so a single-element
       lookup had a 50/50 chance of driving the hidden one and leaving the
       visible clock frozen at 00:00:00. */
    const bars = [...document.querySelectorAll("[data-flash-sale]")];
    if (!bars.length) return;
    bars.forEach((b) => { if (b._flashTimer) clearInterval(b._flashTimer); });
    const CYCLE = 2 * 24 * 60 * 60 * 1000;
    const set = (k, v) => {
      const txt = String(v).padStart(2, "0");
      bars.forEach((b) => {
        const el = b.querySelector(`[data-flash="${k}"]`);
        if (el) el.textContent = txt;
      });
    };
    const tick = () => {
      const now = Date.now();
      let rem = Math.max(0, Math.ceil(now / CYCLE) * CYCLE - now);
      const d = Math.floor(rem / 86400000);
      rem -= d * 86400000;
      const h = Math.floor(rem / 3600000);
      rem -= h * 3600000;
      const m = Math.floor(rem / 60000);
      set("days", d);
      set("hours", h);
      set("mins", m);
    };
    tick();
    const timer = setInterval(tick, 20000);
    bars.forEach((b) => { b._flashTimer = timer; });
  }

  /* Proximity scatter: a leaf only moves when the cursor passes NEAR it — it is
     shoved away from the pointer, like brushing leaves aside. The push is
     PERSISTENT: displacement accumulates and the leaf STAYS where it was pushed
     (it never springs back), capped so leaves don't fly off. Base positions are
     cached in document coords (scroll-aware). rAF-throttled.

     Touch / no-hover devices have no cursor, so there the SAME leaves are driven
     by SCROLL instead (see the touch branch below): scrolling down blows them
     UP, scrolling up blows them DOWN, reusing the identical CSS-eased
     --wx/--wy/--wr offsets and per-section fence — it reads as the same wind.
     Held still under prefers-reduced-motion. NOTE: none of this is gated by the
     data-btn / data-img / data-fly runtime toggles — the leaves animate in every
     combination of those states. */
  function initLeafWind() {
    // Reduced motion is the ONLY hard stop: leaves hold still and neither the
    // cursor nor the scroll wiring is attached. (The data-btn / data-img /
    // data-fly toggles are never consulted here, so they cannot disable this.)
    if (
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    )
      return;
    const leaves = Array.prototype.slice.call(
      document.querySelectorAll("[data-leaf]"),
    );
    if (!leaves.length) return;
    const R = 150; // influence radius (px) — only leaves within this react
    const STEP = 30; // how hard each pass shoves a nearby leaf
    const BOUNCE = 0.5; // rebound off a boundary (0 = stick, 1 = full reflect)
    leaves.forEach((el, i) => {
      el._ax = 0;
      el._ay = 0;
      el._ar = 0;
      // Per-leaf scroll-wind response — deterministic (index-based) so a gust
      // moves the field with a little lead/lag instead of as one rigid block.
      el._ky = 0.7 + ((i * 7) % 5) * 0.16; // vertical parallax gain
      el._kx = (((i * 5) % 3) - 1) * 0.22; // slight lateral sway
      el._kr = (((i * 3) % 5) - 2) * 0.05; // gentle roll
    });
    const cacheBase = () => {
      leaves.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (!r.width) {
          el._bx = null; // hidden (below md)
          return;
        }
        el._bx = r.left + window.scrollX + r.width / 2 - el._ax;
        el._by = r.top + window.scrollY + r.height / 2 - el._ay;
        el._hw = r.width / 2;
        el._hh = r.height / 2;
        // The leaf's own section is the fence: it can be shoved around inside
        // it (full width ≈ the screen) but never out of it.
        const sec = el.closest("section, footer");
        const s = sec ? sec.getBoundingClientRect() : null;
        el._secL = s ? s.left + window.scrollX : -1e6;
        el._secR = s ? s.right + window.scrollX : 1e6;
        el._secT = s ? s.top + window.scrollY : -1e6;
        el._secB = s ? s.bottom + window.scrollY : 1e6;
      });
    };
    cacheBase();
    window.addEventListener("load", cacheBase);
    window.addEventListener("resize", cacheBase, { passive: true });
    if (document.fonts && document.fonts.ready)
      document.fonts.ready.then(cacheBase);
    // Keep a coordinate inside [min,max]; if it overshoots, rebound inward.
    const reflect = (p, min, max) => {
      if (max <= min) return (min + max) / 2;
      if (p < min) return min + (min - p) * BOUNCE;
      if (p > max) return max - (p - max) * BOUNCE;
      return p;
    };

    // Touch / no-hover / sub-md viewports have no cursor, so SCROLL is the wind.
    // We never read layout in here (every base is already cached), so it can't
    // thrash; the rAF only runs while a gust is still settling.
    const touch =
      window.matchMedia &&
      (window.matchMedia("(hover: none)").matches ||
        window.matchMedia("(pointer: coarse)").matches ||
        window.innerWidth < 768);
    if (touch) {
      let sraf = null;
      let lastY = window.pageYOffset || window.scrollY || 0;
      let pending = 0; // scroll delta accumulated since the last frame
      let w = 0; // current wind displacement (px); decays back toward 0
      const GAIN = 0.35; // fraction of each scroll delta that becomes wind
      const FRICTION = 0.9; // per-frame decay so leaves settle once scrolling stops
      const WMAX = 70; // cap so a fast fling can't blow leaves off
      const frame = () => {
        sraf = null;
        // Scroll DOWN (pending > 0) blows leaves UP → negative wind; scrolling
        // up flips the sign. The accumulator then eases back toward rest.
        w -= pending * GAIN;
        pending = 0;
        if (w > WMAX) w = WMAX;
        else if (w < -WMAX) w = -WMAX;
        w *= FRICTION;
        if (Math.abs(w) < 0.15) w = 0;
        leaves.forEach((el) => {
          if (el._bx == null) return; // hidden (display:none below md) — skip
          // Same fence as the cursor path: the shove is clamped inside the
          // leaf's own section so it never drifts out.
          el._ax =
            reflect(el._bx + w * el._kx, el._secL + el._hw, el._secR - el._hw) -
            el._bx;
          el._ay =
            reflect(el._by + w * el._ky, el._secT + el._hh, el._secB - el._hh) -
            el._by;
          el._ar = Math.max(-42, Math.min(42, w * el._kr));
          el.style.setProperty("--wx", el._ax.toFixed(1) + "px");
          el.style.setProperty("--wy", el._ay.toFixed(1) + "px");
          el.style.setProperty("--wr", el._ar.toFixed(1) + "deg");
        });
        // Keep animating until the gust has fully died down.
        if (w !== 0 && !sraf) sraf = requestAnimationFrame(frame);
      };
      window.addEventListener(
        "scroll",
        () => {
          const y = window.pageYOffset || window.scrollY || 0;
          pending += y - lastY;
          lastY = y;
          if (!sraf) sraf = requestAnimationFrame(frame);
        },
        { passive: true },
      );
      return;
    }

    // Hover devices (desktop): the CURSOR is the wind. Unchanged behaviour.
    let raf = null,
      mx = -1e5,
      my = -1e5;
    const apply = () => {
      raf = null;
      leaves.forEach((el) => {
        if (el._bx == null) return;
        // Distance from the leaf's CURRENT (already-scattered) spot to the
        // pointer — once shoved away it sits farther off, so the same cursor
        // spot won't keep shoving it.
        const dx = el._bx + el._ax - mx;
        const dy = el._by + el._ay - my;
        const dist = Math.hypot(dx, dy);
        if (dist >= R) return; // outside — keep the offset, never spring back
        const f = 1 - dist / R;
        const inv = dist > 0.01 ? 1 / dist : 0;
        // Proposed new position, then fenced to the section (bounces at edges).
        const px = reflect(
          el._bx + el._ax + dx * inv * STEP * f,
          el._secL + el._hw,
          el._secR - el._hw,
        );
        const py = reflect(
          el._by + el._ay + dy * inv * STEP * f,
          el._secT + el._hh,
          el._secB - el._hh,
        );
        el._ax = px - el._bx;
        el._ay = py - el._by;
        el._ar = Math.max(-42, Math.min(42, el._ar + dx * inv * 5 * f));
        el.style.setProperty("--wx", el._ax.toFixed(1) + "px");
        el.style.setProperty("--wy", el._ay.toFixed(1) + "px");
        el.style.setProperty("--wr", el._ar.toFixed(1) + "deg");
      });
    };
    window.addEventListener(
      "mousemove",
      (e) => {
        mx = e.clientX + window.scrollX;
        my = e.clientY + window.scrollY;
        if (!raf) raf = requestAnimationFrame(apply);
      },
      { passive: true },
    );
  }

  function initMegaMenu() {
    const toggle = document.querySelector("[data-megamenu-toggle]");
    const panel = document.getElementById("mega-panel");
    if (!toggle || !panel) return;
    const caret = toggle.querySelector("[data-megamenu-caret]");
    const cats = [...panel.querySelectorAll("[data-mega-cat]")];
    const subs = [...panel.querySelectorAll("[data-mega-sub]")];

    /* The caret flip is a class, not an inline transform, so it eases with the
       shared `.chevron` rule rather than snapping. */
    const setOpen = (open) => {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (caret) caret.classList.toggle("chevron--open", open);
    };

    const activate = (idx) => {
      idx = String(idx);
      cats.forEach((b) => (b.dataset.active = b.dataset.megaCat === idx));
      subs.forEach((u) => (u.hidden = u.dataset.megaSub !== idx));
    };

    /* Hover-intent — the fix for "travelling to the left". Crossing sibling
       rows to reach the stage must not swap the panel, so a switch is delayed
       and each fresh mouseenter cancels the pending one: only the row the
       pointer SETTLES on — the last entered before it dives into the stage —
       actually wins. ~110ms is under the notice threshold for a deliberate
       hover yet long enough to skip rows merely brushed in transit. The pending
       switch is deliberately NOT cancelled when the pointer leaves a row toward
       the stage (a fast dive would otherwise drop the category being aimed at)
       — only when it leaves the whole panel. Keyboard focus activates at once. */
    let timer = null;
    const clearPending = () => {
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }
    };
    cats.forEach((b) => {
      const idx = b.dataset.megaCat;
      b.addEventListener("mouseenter", () => {
        clearPending();
        timer = setTimeout(() => activate(idx), 110);
      });
      b.addEventListener("focus", () => {
        clearPending();
        activate(idx);
      });
      // A row is a link: click navigates to the category — no activate() here.
    });
    panel.addEventListener("mouseleave", clearPending);

    // Up/Down move between rail rows for parity with hover.
    panel.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
      const i = cats.indexOf(document.activeElement);
      if (i === -1) return;
      e.preventDefault();
      const next = e.key === "ArrowDown" ? i + 1 : i - 1;
      cats[(next + cats.length) % cats.length].focus();
    });

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen(panel.hidden);
    });
    document.addEventListener("click", (e) => {
      if (!panel.hidden && !panel.contains(e.target) && !toggle.contains(e.target))
        setOpen(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !panel.hidden) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  function initListing(scope) {
    const grid = scope.querySelector("[data-product-grid]");
    const chips = [...scope.querySelectorAll("[data-filter]")];
    if (!grid || !chips.length) return;

    const cards = [...grid.children];
    cards.forEach((c, i) => (c.dataset.order = i)); // "الأكثر مبيعاً" = as published
    const countEl = scope.querySelector("[data-result-count]");
    const emptyEl = scope.querySelector("[data-empty-state]");
    const select = scope.querySelector("[data-listing] select, select");

    const setChip = (el, on) => {
      el.classList.remove(...(on ? CHIP_OFF : CHIP_ON));
      el.classList.add(...(on ? CHIP_ON : CHIP_OFF));
      el.setAttribute("aria-current", on ? "true" : "false");
    };

    function apply(slug, sort) {
      const visible = cards.filter((c) => {
        const show = slug === "all" || c.dataset.cat === slug;
        c.hidden = !show;
        return show;
      });
      if (sort && sort !== "popular") {
        const dir = sort === "price-desc" ? -1 : 1;
        const key = sort === "newest" ? "id" : "price";
        visible.sort((a, b) =>
          sort === "newest"
            ? Number(b.dataset.id) - Number(a.dataset.id)
            : dir * (Number(a.dataset.price) - Number(b.dataset.price))
        );
      } else {
        visible.sort((a, b) => Number(a.dataset.order) - Number(b.dataset.order));
      }
      visible.forEach((c) => grid.appendChild(c));
      if (countEl) countEl.textContent = visible.length;
      if (emptyEl) emptyEl.hidden = visible.length > 0;
      chips.forEach((c) => setChip(c, c.dataset.filter === slug));
    }

    let current = "all";
    chips.forEach((c) =>
      c.addEventListener("click", (ev) => {
        ev.preventDefault();
        current = c.dataset.filter;
        apply(current, select ? select.value : "popular");
        history.replaceState(null, "", "#" + current);
      })
    );
    if (select) {
      select.addEventListener("change", () => apply(current, select.value));
    }

    const readHash = () => {
      const h = (location.hash || "").replace("#", "");
      return h && chips.some((c) => c.dataset.filter === h) ? h : null;
    };

    // Arriving from the nav at shop.html#<slug> while already on shop.html is
    // a hash change, not a load — without this the page would sit unfiltered.
    window.addEventListener("hashchange", () => {
      const h = readHash();
      if (!h) return;
      current = h;
      apply(current, select ? select.value : "popular");
    });

    current = readHash() || "all";
    apply(current, select ? select.value : "popular");
  }

  /* ---------------------------------------------------------------
     Custom sort dropdown (desktop)

     A native <select> stays the source of truth, the mobile control (the OS
     picker beats a popover on a phone) and the no-JS fallback — see
     sort_select() in components.py. On desktop this hides it and drives a
     styled listbox that writes the choice straight back to the select and
     fires `change`, so initListing's sort wiring is untouched.

     The option labels are rendered at build time in Arabic, so
     translateDocument() — which runs BEFORE kInit on a language switch — keeps
     both the native <option>s and these rows translated. We only re-sync the
     trigger's own label text, on every kInit, from the already-translated row.
     --------------------------------------------------------------- */
  /* ---------------------------------------------------------------
     Dropdown (design system) — replaces the native <select> popup
     (Ahmed, 2026-08-23)

     Progressive enhancement rather than a component every caller has to adopt:
     this upgrades any `select.select-control` in place, so the checkout's city
     / district / area, the profile form and the address modal's selects — which
     scripts.js writes at runtime, long after any build step — are all covered
     without a single call site changing, and any future one is covered the day
     it is written.

     The native <select> is kept, not replaced. It is what submits, what
     `required` validates against, what external code reads and writes, and what
     a no-JS visit gets. Everything here is a skin over it: picking a row writes
     the value back and fires `change`, so nothing downstream can tell the
     difference.

     Motion and structure follow the reference Ahmed supplied; the timings live
     in styles.css (.dd) next to the rest of the field styling.
     --------------------------------------------------------------- */
  const DD_CHECK = '<span class="dd__opt-check" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m5 13 4 4L19 7" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>';
  const DD_CHEV = '<span class="dd__chev" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>';

  function upgradeSelect(select) {
    if (select.dataset.ddReady) return;
    select.dataset.ddReady = "1";

    const box = document.createElement("div");
    box.className = "dd";
    box.setAttribute("data-dd", "");
    box.setAttribute("data-state", "closed");
    select.parentNode.insertBefore(box, select);
    box.appendChild(select);
    select.classList.add("dd__native");
    // The listbox below replaces it in the a11y tree; leaving both exposed
    // would announce every field twice.
    select.setAttribute("aria-hidden", "true");
    select.tabIndex = -1;

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "dd__trigger";
    trigger.setAttribute("aria-haspopup", "listbox");
    trigger.setAttribute("aria-expanded", "false");
    // Point the trigger at the same <label for=…> the select had, so clicking
    // the label still opens the control and the accessible name survives.
    const lbl = select.id ? document.querySelector('label[for="' + CSS.escape(select.id) + '"]') : null;
    if (lbl) {
      if (!lbl.id) lbl.id = "ddl-" + Math.abs(hashStr(select.id || select.name || "dd")).toString(36);
      trigger.setAttribute("aria-labelledby", lbl.id);
    } else if (select.getAttribute("aria-label")) {
      trigger.setAttribute("aria-label", select.getAttribute("aria-label"));
    }
    trigger.innerHTML = '<span class="dd__value"></span>' + DD_CHEV;

    const pop = document.createElement("ul");
    pop.className = "dd__pop";
    pop.setAttribute("role", "listbox");
    pop.tabIndex = -1;

    // The travelling hover fill. One element for the whole list; setActive
    // moves it. Kept out of buildRows so it survives the list being rebuilt.
    const marker = document.createElement("span");
    marker.className = "dd__marker";
    marker.setAttribute("aria-hidden", "true");

    box.appendChild(trigger);
    box.appendChild(pop);

    let rows = [];

    // Built from the <option>s every time, because several of these selects are
    // REPOPULATED at runtime (picking a governorate rewrites the area list), and
    // a list built once would keep offering the previous city's districts.
    function buildRows() {
      pop.innerHTML = "";
      pop.appendChild(marker);
      rows = [...select.options].map((opt, i) => {
        const li = document.createElement("li");
        li.className = "dd__opt";
        li.setAttribute("role", "option");
        li.dataset.value = opt.value;
        // The stagger is CAPPED. The reference staggers four items, where 30ms
        // apart is a cascade; the governorate list is 28 long, where it would
        // be a 0.8s crawl and the last rows would still be arriving after the
        // shopper had started reading. Past the ninth row they all land
        // together, which still reads as one cascade because the rows below the
        // fold are scrolled to, not watched.
        li.style.setProperty("--i", Math.min(i, 8));
        li.innerHTML = DD_CHECK + '<span class="dd__opt-text"></span>';
        li.querySelector(".dd__opt-text").textContent = opt.textContent;
        pop.appendChild(li);
        return li;
      });
      sync();
    }

    function sync() {
      const opt = select.options[select.selectedIndex] || select.options[0];
      const val = trigger.querySelector(".dd__value");
      val.textContent = opt ? opt.textContent : "";
      // An empty value is the "اختر" placeholder, which is a prompt and should
      // not be painted as if something had been chosen.
      val.classList.toggle("is-placeholder", !opt || opt.value === "");
      rows.forEach((li) =>
        li.setAttribute("aria-selected", li.dataset.value === select.value ? "true" : "false"));
    }

    const isOpen = () => box.getAttribute("data-state") === "open";

    function onOutside(e) { if (!box.contains(e.target)) close(false); }

    function open() {
      if (isOpen()) return;
      box.setAttribute("data-state", "open");
      trigger.setAttribute("aria-expanded", "true");
      document.addEventListener("pointerdown", onOutside, true);
      const sel = rows.find((li) => li.getAttribute("aria-selected") === "true") || rows[0];
      setActive(sel || null);
      if (sel) sel.scrollIntoView({ block: "nearest" });
    }
    function close(focusTrigger) {
      if (!isOpen()) return;
      box.setAttribute("data-state", "closed");
      trigger.setAttribute("aria-expanded", "false");
      document.removeEventListener("pointerdown", onOutside, true);
      setActive(null);
      if (focusTrigger) trigger.focus();
    }
    function setActive(li) {
      rows.forEach((r) => r.classList.toggle("is-active", r === li));
      if (!li) { marker.style.opacity = "0"; return; }
      // The FIRST placement must not animate: with the marker parked at the top
      // of the list at height 0, sliding into place would look like the fill
      // dropping in from the panel's edge every time the menu opens. Only the
      // moves BETWEEN rows are the effect that was asked for, so the first one
      // is applied with transitions off and they are restored a frame later.
      const first = marker.style.opacity !== "1";
      if (first) marker.style.transition = "none";
      marker.style.setProperty("--y", li.offsetTop + "px");
      marker.style.height = li.offsetHeight + "px";
      marker.style.opacity = "1";
      if (first) { void marker.offsetWidth; marker.style.transition = ""; }
    }
    function choose(li) {
      if (!li) return;
      if (select.value !== li.dataset.value) {
        select.value = li.dataset.value;
        // Bubbling, because the address modal listens on an ancestor to
        // repopulate the next select down.
        select.dispatchEvent(new Event("change", { bubbles: true }));
      }
      sync();
      close(true);
    }

    trigger.addEventListener("click", () => (isOpen() ? close(false) : open()));
    pop.addEventListener("click", (e) => {
      const li = e.target.closest(".dd__opt");
      if (li) choose(li);
    });
    pop.addEventListener("mousemove", (e) => {
      const li = e.target.closest(".dd__opt");
      if (li) setActive(li);
    });
    // Leaving the list sends the fill back to whatever is actually selected,
    // rather than stranding it on the last row the pointer crossed.
    pop.addEventListener("mouseleave", () => {
      if (!isOpen()) return;
      setActive(rows.find((li) => li.getAttribute("aria-selected") === "true") || null);
    });

    // Keyboard: the control is a button, so it owns the keys while closed too.
    box.addEventListener("keydown", (e) => {
      const k = e.key;
      if (!isOpen()) {
        if (k === "ArrowDown" || k === "ArrowUp" || k === "Enter" || k === " ") {
          e.preventDefault();
          open();
        }
        return;
      }
      const active = rows.find((r) => r.classList.contains("is-active"));
      const at = rows.indexOf(active);
      if (k === "Escape") { e.preventDefault(); close(true); }
      else if (k === "ArrowDown") { e.preventDefault(); setActive(rows[Math.min(rows.length - 1, at + 1)] || rows[0]); scrollActive(); }
      else if (k === "ArrowUp") { e.preventDefault(); setActive(rows[Math.max(0, at - 1)] || rows[0]); scrollActive(); }
      else if (k === "Home") { e.preventDefault(); setActive(rows[0]); scrollActive(); }
      else if (k === "End") { e.preventDefault(); setActive(rows[rows.length - 1]); scrollActive(); }
      else if (k === "Enter" || k === " ") { e.preventDefault(); choose(active); }
      else if (k === "Tab") close(false);
    });
    function scrollActive() {
      const a = rows.find((r) => r.classList.contains("is-active"));
      if (a) a.scrollIntoView({ block: "nearest" });
    }

    // Someone else writing to the select — the address modal repopulating it,
    // a saved address being applied, a form reset — has to move the skin too.
    select.addEventListener("change", sync);
    try {
      new MutationObserver(buildRows).observe(select, { childList: true });
    } catch (err) { /* option list simply stays as first built */ }

    buildRows();
  }

  function hashStr(str) {
    let h = 0;
    for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) | 0;
    return h;
  }

  /* Idempotent and safe to re-run: upgradeSelect no-ops on anything it has
     already done, so this is called again after any markup that ships its own
     selects is injected. */
  function initDropdowns(scope) {
    (scope || document).querySelectorAll("select.select-control").forEach(upgradeSelect);
  }

  function initFancySelect(scope) {
    scope.querySelectorAll("[data-fancy-select]").forEach((box) => {
      const select = box.querySelector("select");
      const fallback = box.querySelector("[data-fancy-fallback]");
      const ui = box.querySelector("[data-fancy-ui]");
      const trigger = box.querySelector("[data-fancy-trigger]");
      const pop = box.querySelector("[data-fancy-pop]");
      const label = box.querySelector("[data-fancy-label]");
      const items = [...box.querySelectorAll("[data-fancy-opt]")];
      if (!select || !ui || !trigger || !pop || !label || !items.length) return;

      // Trigger label + selected marks, read from the (already translated)
      // rows. Runs on every kInit, so a language switch and a pick made through
      // the native mobile control both land here.
      // Size the native select to its CURRENT value's text (Ahmed, 2026-08-02).
      // A native <select> is otherwise as wide as its LONGEST option, so on
      // mobile — where the native control is what shows — the chevron sat after
      // the width of "السعر: من الأعلى" even while "الأكثر مبيعاً" was picked,
      // leaving a gap. Measuring the selected option lets the field hug its word
      // with the chevron a fixed gap away, on the phone as on desktop.
      const sizeNative = () => {
        const opt = select.options[select.selectedIndex];
        if (!opt) return;
        const cs = getComputedStyle(select);
        const probe = document.createElement("span");
        probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap";
        probe.style.fontSize = cs.fontSize;
        probe.style.fontFamily = cs.fontFamily;
        probe.style.fontWeight = cs.fontWeight;
        probe.textContent = opt.text;
        document.body.appendChild(probe);
        select.style.width = Math.ceil(probe.getBoundingClientRect().width) + 2 + "px";
        probe.remove();
      };
      const sync = () => {
        const active =
          items.find((li) => li.dataset.value === select.value) || items[0];
        label.textContent = active.querySelector("[data-opt-text]").textContent;
        items.forEach((li) =>
          li.setAttribute("aria-selected", li === active ? "true" : "false"),
        );
        sizeNative();
      };

      // Same capped stagger as the design-system dropdown.
      items.forEach((li, i) => li.style.setProperty("--i", Math.min(i, 8)));

      if (box.dataset.fancyReady) {
        sync();
        return;
      }
      box.dataset.fancyReady = "1";

      // Reveal the custom UI on desktop only; drop the native select from the
      // a11y tree there (this listbox replaces it) but keep it functional.
      fallback.classList.add("xl:hidden");
      ui.classList.add("xl:block");
      select.setAttribute("aria-hidden", "true");
      select.tabIndex = -1;
      // Re-hug the native select on every pick (including the mobile OS picker),
      // and once now on init.
      select.addEventListener("change", sizeNative);
      sizeNative();

      // State lives on the BOX as data-state, not as `hidden` on the popup, so
      // the panel keeps its box while it fades out — the same reason the design
      // system dropdown does it (see .dd in styles.css). `hidden` is removed
      // once here; from then on visibility is the CSS's business.
      pop.classList.remove("hidden");
      box.setAttribute("data-state", "closed");
      const isOpen = () => box.getAttribute("data-state") === "open";
      function onOutside(e) {
        if (!box.contains(e.target)) close(false);
      }
      const open = () => {
        box.setAttribute("data-state", "open");
        trigger.setAttribute("aria-expanded", "true");
        (
          items.find((li) => li.getAttribute("aria-selected") === "true") ||
          items[0]
        ).focus();
        document.addEventListener("pointerdown", onOutside, true);
      };
      const close = (focusTrigger) => {
        box.setAttribute("data-state", "closed");
        trigger.setAttribute("aria-expanded", "false");
        document.removeEventListener("pointerdown", onOutside, true);
        if (focusTrigger) trigger.focus();
      };
      const choose = (li) => {
        if (select.value !== li.dataset.value) {
          select.value = li.dataset.value;
          select.dispatchEvent(new Event("change", { bubbles: true }));
        }
        sync();
        close(true);
      };

      trigger.addEventListener("click", () =>
        isOpen() ? close(false) : open(),
      );
      trigger.addEventListener("keydown", (e) => {
        if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open();
        }
      });
      items.forEach((li, i) => {
        li.tabIndex = -1;
        li.addEventListener("click", () => choose(li));
        li.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            choose(li);
          } else if (e.key === "ArrowDown") {
            e.preventDefault();
            (items[i + 1] || items[0]).focus();
          } else if (e.key === "ArrowUp") {
            e.preventDefault();
            (items[i - 1] || items[items.length - 1]).focus();
          } else if (e.key === "Escape") {
            e.preventDefault();
            close(true);
          } else if (e.key === "Tab") {
            close(false);
          }
        });
      });

      select.addEventListener("change", sync);
      sync();
    });
  }

  /* ---------------------------------------------------------------
     Order notes, referral copy, addresses

     Three controls that shipped as dead markup and now do what they say
     (Ahmed pressed all three, 2026-07-22). Same store discipline as the
     cart: localStorage state, render as a pure function of it.
     --------------------------------------------------------------- */
  const NOTE_KEY = "jaad:orderNote";

  /* Order note, with real states now (Ahmed, 2026-08-02): an EDIT view
     (textarea + save) and an APPLIED view (the saved note, with edit / remove).
     syncNoteUI swaps between them off the stored note, so a saved note comes
     back on reload already applied rather than as a filled-in textarea. */
  function readNote() {
    try {
      return (localStorage.getItem(NOTE_KEY) || "").trim();
    } catch (e) {
      return "";
    }
  }
  /* Three resting states now (Ahmed, 2026-08-04): the TRIGGER
     ([data-note-open]) when there is no note, the FILLED field
     ([data-note-view]) when there is, and the EDITOR ([data-note-edit]) which
     is only ever shown transiently by a click — never by sync — so this resets
     to whichever resting state the stored note implies. */
  function syncNoteUI() {
    const note = readNote();
    document.querySelectorAll("[data-note]").forEach((wrap) => {
      // Read-only note (payment step, Ahmed 2026-08-04): a note carried over
      // from checkout is shown but NOT editable/removable. Hide the whole block
      // when there is no note.
      if (wrap.hasAttribute("data-note-readonly")) {
        wrap.hidden = !note;
        const roText = wrap.querySelector("[data-note-text]");
        if (note && roText) roText.textContent = note;
        return;
      }
      const open = wrap.querySelector("[data-note-open]");
      const edit = wrap.querySelector("[data-note-edit]");
      const view = wrap.querySelector("[data-note-view]");
      const text = wrap.querySelector("[data-note-text]");
      const ta = wrap.querySelector("[data-order-note]");
      if (note) {
        if (text) text.textContent = note;
        if (open) open.hidden = true;
        if (edit) edit.hidden = true;
        if (view) view.hidden = false;
      } else {
        if (open) open.hidden = false;
        if (edit) edit.hidden = true;
        if (view) view.hidden = true;
        if (ta) ta.value = "";
      }
    });
  }

  function initOrderNotes() {
    syncNoteUI();

    // Reveal the editor for one wrap, prefilled and focused.
    const openEditor = (wrap, prefill) => {
      const open = wrap.querySelector("[data-note-open]");
      const edit = wrap.querySelector("[data-note-edit]");
      const view = wrap.querySelector("[data-note-view]");
      const ta = wrap.querySelector("[data-order-note]");
      if (open) open.hidden = true;
      if (view) view.hidden = true;
      if (edit) edit.hidden = false;
      if (ta) {
        ta.value = prefill || "";
        ta.focus();
      }
    };

    document.addEventListener("click", (e) => {
      // Open the editor — from the trigger (empty) or by clicking a filled note
      // (prefilled). Both read the stored note, which is "" before one exists.
      const opener = e.target.closest("[data-note-open], [data-note-edit-btn]");
      if (opener) {
        openEditor(opener.closest("[data-note]") || document, readNote());
        return;
      }
      // Cancel — drop back to the resting state (filled note if stored, else the
      // trigger). Storage is untouched, so an in-progress edit is discarded.
      if (e.target.closest("[data-note-cancel]")) {
        syncNoteUI();
        return;
      }
      const save = e.target.closest("[data-order-note-save]");
      if (save) {
        const wrap = save.closest("[data-note]") || document;
        const ta = wrap.querySelector("[data-order-note]");
        if (!ta) return;
        const note = ta.value.trim();
        try {
          if (note) localStorage.setItem(NOTE_KEY, note);
          else localStorage.removeItem(NOTE_KEY);
        } catch (err) {
          /* ignore */
        }
        syncNoteUI();
        toast(note ? "تمت إضافة ملاحظتك على الطلب" : "تمت إزالة الملاحظات");
        pulse(save);
        return;
      }
      // Remove an applied note.
      if (e.target.closest("[data-note-remove]")) {
        try {
          localStorage.removeItem(NOTE_KEY);
        } catch (err) {
          /* ignore */
        }
        syncNoteUI();
        toast("تمت إزالة الملاحظات");
        return;
      }
    });
  }

  function initReferralCopy() {
    /* navigator.clipboard.writeText rejects in more places than you would
       think (unfocused document, older WebViews), so a hidden-textarea
       execCommand copy backs it up — and the copied state must only ever
       paint when one of the two actually took. */
    function copyText(text) {
      const legacy = () => {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
        document.body.appendChild(ta);
        ta.select();
        let ok = false;
        try {
          ok = document.execCommand("copy");
        } catch (err) {
          ok = false;
        }
        ta.remove();
        return ok;
      };
      /* writeText does not merely reject in awkward contexts — with a
         pending permission decision it can simply never settle, which left
         the button frozen on neither branch. So it races a short timer:
         whoever finishes first wins, and the timer path still sits inside
         the click's transient user activation, which execCommand needs. */
      return new Promise((resolve, reject) => {
        let settled = false;
        const win = () => {
          if (!settled) {
            settled = true;
            resolve();
          }
        };
        const viaLegacy = () => {
          if (settled) return;
          if (legacy()) win();
          else {
            settled = true;
            reject(new Error("copy failed"));
          }
        };
        if (navigator.clipboard) {
          navigator.clipboard.writeText(text).then(win, viaLegacy);
          setTimeout(viaLegacy, 350);
        } else {
          viaLegacy();
        }
      });
    }

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-copy-ref]");
      if (!btn || btn.dataset.copied) return;
      const link = (btn.closest("div") || document).querySelector("[data-ref-link]");
      const text = link ? link.textContent.trim() : "";
      if (!text) return;
      copyText(text).then(
        () => {
          /* The copied state lives on the button itself — a toast alone is
             off in the corner, and the question being answered is "did THIS
             button work". Reverts after a beat so it can be used again. */
          btn.dataset.copied = "true";
          const old = btn.textContent;
          btn.textContent = t("تم النسخ ✓");
          btn.classList.add("pointer-events-none");
          setTimeout(() => {
            btn.textContent = old;
            btn.classList.remove("pointer-events-none");
            delete btn.dataset.copied;
          }, 2600);
        },
        () => toast("تعذر النسخ — انسخ الرابط يدوياً", "error"),
      );
    });
  }

  /* ---------------------------------------------------------------
     Loyalty points redeem + vouchers (Ahmed, 2026-08-04). All demo, no live
     endpoint (DESIGN-NOTES §1). Redeeming points AND activating vouchers both
     add EGP to the wallet (walletBonus/syncWalletBalance above). The points
     balance, its progress bar and the tier ladder update live.
     --------------------------------------------------------------- */
  const nfEn = (n) => Number(n).toLocaleString("en-US");
  function tierInfo(pts) {
    let idx = 0;
    for (let i = 0; i < POINTS_TIERS.length; i++) if (pts >= POINTS_TIERS[i][1]) idx = i;
    const cur = POINTS_TIERS[idx], nxt = POINTS_TIERS[idx + 1] || null;
    let pct = 100, toNext = 0;
    if (nxt) { const span = nxt[1] - cur[1]; pct = Math.max(0, Math.min(100, Math.round(((pts - cur[1]) / span) * 100))); toNext = Math.max(0, nxt[1] - pts); }
    return { idx: idx, nxt: nxt, pct: pct, toNext: toNext };
  }
  function syncPointsUI() {
    const rem = pointsRemaining();
    const ti = tierInfo(rem);
    document.querySelectorAll("[data-points-balance]").forEach((el) => (el.textContent = nfEn(rem)));
    document.querySelectorAll("[data-points-badge]").forEach((el) => (el.textContent = nfEn(rem)));
    document.querySelectorAll("[data-points-progress]").forEach((el) => (el.style.width = ti.pct + "%"));
    document.querySelectorAll("[data-points-tonext]").forEach((el) => {
      el.innerHTML = ti.nxt
        ? '<span class="latin">' + nfEn(ti.toNext) + "</span> " + esc(t("نقطة للوصول لعضوية")) + " " + esc(ti.nxt[0])
        : esc(t("وصلت لأعلى مستوى عضوية")) + " 🎉";
    });
    document.querySelectorAll("[data-tier-cards]").forEach((wrap) => {
      wrap.querySelectorAll("[data-tier]").forEach((c) => {
        if (Number(c.dataset.tier) === ti.idx) c.setAttribute("data-current", "");
        else c.removeAttribute("data-current");
      });
    });
  }
  function initPointsRedeem() {
    syncPointsUI();
    const modal = document.querySelector('[data-sheet="pointsRedeem"]');
    if (!modal) return;
    const input = modal.querySelector("[data-redeem-input]");
    const egpEl = modal.querySelector("[data-redeem-egp]");
    const availEl = modal.querySelector("[data-redeem-available]");
    const msg = modal.querySelector("[data-redeem-msg]");
    const clampVal = () => {
      let v = Math.floor(Number(input && input.value) || 0);
      if (v < 0) v = 0;
      if (v > pointsRemaining()) v = pointsRemaining();
      return v;
    };
    const paint = () => {
      const v = clampVal();
      if (egpEl) egpEl.textContent = "EGP " + Math.round(v / POINTS_PER_EGP);
      if (msg) msg.hidden = true;
    };
    document.querySelectorAll('[data-open="pointsRedeem"]').forEach((b) =>
      b.addEventListener("click", () => {
        if (availEl) availEl.textContent = nfEn(pointsRemaining());
        if (input) { input.max = String(pointsRemaining()); input.value = String(Math.min(pointsRemaining(), 500)); }
        paint();
      }));
    if (input) input.addEventListener("input", paint);
    const allBtn = modal.querySelector("[data-redeem-all]");
    if (allBtn) allBtn.addEventListener("click", () => { if (input) input.value = String(pointsRemaining()); paint(); });
    const confirm = modal.querySelector("[data-redeem-confirm]");
    if (confirm) confirm.addEventListener("click", () => {
      const v = clampVal();
      if (v < POINTS_PER_EGP) {
        if (msg) { msg.textContent = t("أقل عدد للاستبدال هو") + " " + POINTS_PER_EGP + " " + t("نقاط"); msg.hidden = false; }
        return;
      }
      try { localStorage.setItem(PT_SPENT_KEY, String(pointsSpent() + v)); } catch (e) { /* ignore */ }
      syncPointsUI();
      syncWalletBalance(true);
      closeOverlay();
      toast(t("تم تحويل") + " " + nfEn(v) + " " + t("نقطة إلى محفظتك"), "wallet");
    });
  }
  function syncVouchersCount() {
    // Sidebar badge on EVERY account page reads the same remaining count, so an
    // activation (or a newly added code) on the vouchers page shows up in the
    // nav everywhere. Counted from localStorage, not the DOM, because the list
    // only exists on the vouchers page: seeded vouchers still waiting +
    // code-added vouchers still waiting, each minus the ones already activated.
    const used = vouchersUsed();
    const staticUsed = used.filter((id) => String(id).indexOf("added-") !== 0).length;
    const staticRemain = Math.max(0, VOUCHERS_TOTAL - staticUsed);
    const addedRemain = vouchersAdded().filter((v) => used.indexOf(v.id) < 0).length;
    const remain = staticRemain + addedRemain;
    document.querySelectorAll("[data-vouchers-count]").forEach((el) => (el.textContent = remain));
    const empty = document.querySelector("[data-vouchers-empty]");
    if (empty) {
      const list = document.querySelector("[data-vouchers-list]");
      empty.hidden = !list || list.querySelectorAll("[data-voucher]").length > 0;
    }
  }
  /* Voucher history ("القسائم السابقة") — activated vouchers are logged here so
     they show as USED under the static expired ones, and survive reload (Ahmed,
     2026-08-04). */
  const V_HIST_KEY = "jaad:vouchersHistory";
  const AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
  const fmtDateAr = (d) => d.getDate() + " " + AR_MONTHS[d.getMonth()] + " " + d.getFullYear();
  const vouchersHistory = () => { try { return JSON.parse(localStorage.getItem(V_HIST_KEY) || "[]"); } catch (e) { return []; } };
  function voucherHistRow(label, dateStr) {
    return '<div class="flex items-center gap-3 bg-white/70 p-4 border border-divider rounded-2xl">'
      + '<img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-11 h-11 object-contain shrink-0 opacity-60 grayscale" />'
      + '<div class="flex flex-col flex-1 min-w-0"><span class="font-bold text-muted text-sm">' + esc(label) + '</span>'
      + '<span class="text-muted text-xs">' + esc(t("تم الاستخدام")) + ' ' + esc(dateStr) + '</span></div>'
      + '<span class="inline-flex items-center bg-mint px-2.5 py-1 rounded-full font-semibold text-ink-800 text-xs shrink-0">' + esc(t("مستخدمة")) + '</span></div>';
  }
  function renderVoucherHistory() {
    const host = document.querySelector("[data-vouchers-history-dynamic]");
    if (!host) return;
    host.innerHTML = vouchersHistory().slice().reverse().map((h) => voucherHistRow(h.label, h.date)).join("");
  }
  function addVoucherHistory(label, value) {
    try {
      const h = vouchersHistory();
      h.push({ label: label, value: value, date: fmtDateAr(new Date()) });
      localStorage.setItem(V_HIST_KEY, JSON.stringify(h));
    } catch (e) { /* ignore */ }
    renderVoucherHistory();
  }
  // Markup for an available-voucher card, matching the seeded ones the vouchers
  // page renders (build/pages/my_account_vouchers.py) so a code-added voucher is
  // indistinguishable from a seeded one — same activate (+) control, same hooks.
  const V_PLUS = '<svg viewBox="0 0 24 24" fill="none" class="w-full h-full"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
  function voucherCardHTML(v) {
    return '<div data-voucher data-voucher-id="' + esc(v.id) + '" class="flex items-center gap-3 bg-white shadow-custom4 p-4 rounded-2xl">'
      + '<img src="images/jaad/icons/discount-tag-3d.png" alt="" class="w-11 h-11 object-contain shrink-0" />'
      + '<div class="flex flex-col flex-1 min-w-0"><span class="font-bold text-cta text-sm">' + esc(v.label) + '</span>'
      + '<span class="text-muted text-xs">' + esc(v.validity) + '</span></div>'
      + '<button type="button" data-voucher-activate data-value="' + esc(String(v.value)) + '" data-label="' + esc(v.label) + '" aria-label="' + esc("تفعيل " + v.label) + '" '
      + 'class="place-items-center grid bg-cream hover:bg-cta hover:text-white border border-divider rounded-full size-10 text-cta shrink-0 transition-colors"><span class="w-4 h-4">' + V_PLUS + '</span></button>'
      + '</div>';
  }
  function initVouchers() {
    renderVoucherHistory();
    const list = document.querySelector("[data-vouchers-list]");
    const used = vouchersUsed();
    // Drop already-activated seeded cards on load so they can't be claimed twice
    // (the wallet credit is persisted separately in VOUCHERS_KEY).
    document.querySelectorAll("[data-voucher]").forEach((v) => {
      if (used.indexOf(v.dataset.voucherId) >= 0) v.remove();
    });
    // Re-render code-added vouchers that are still waiting to be activated,
    // newest first — they live in the available list exactly like seeded ones.
    if (list) vouchersAdded().forEach((v) => {
      if (used.indexOf(v.id) >= 0) return;
      if (list.querySelector('[data-voucher-id="' + v.id + '"]')) return;
      list.insertAdjacentHTML("afterbegin", voucherCardHTML(v));
    });
    syncVouchersCount();

    // Add a voucher BY CODE — it joins the AVAILABLE list with its value and an
    // expiry, and is NOT credited to the wallet here (Ahmed, 2026-08-05): the
    // shopper still chooses to activate it, the same two-step the seeded
    // vouchers already use. The value is read off the code's trailing digits
    // (JAAD150 -> 150), else a default; expiry is 90 days out. Demo — there is
    // no live voucher endpoint (DESIGN-NOTES §1).
    const addForm = document.querySelector("[data-voucher-add-form]");
    if (addForm) addForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const code = ((addForm.querySelector('[name="code"]') || {}).value || "").trim();
      if (!code) return;
      const m = code.match(/(\d{2,4})/);
      const value = m ? Number(m[1]) : 50;
      const exp = new Date(); exp.setDate(exp.getDate() + 90);
      const v = {
        id: "added-" + Date.now(),
        label: t("خصم") + " " + value + " " + t("جنيه"),
        validity: t("صالحة حتى") + " " + fmtDateAr(exp),
        value: value,
      };
      try {
        const arr = vouchersAdded(); arr.push(v);
        localStorage.setItem(V_ADDED_KEY, JSON.stringify(arr));
      } catch (e2) { /* ignore */ }
      if (list) list.insertAdjacentHTML("afterbegin", voucherCardHTML(v));
      addForm.reset();
      syncVouchersCount();
      closeOverlay();
      toast(t("تمت إضافة القسيمة إلى قائمتك"), "success");
    });

    // Activate (+) — DELEGATED on the list so code-added cards (built after load)
    // work the same as the seeded ones. Opens the confirm sheet with the value.
    let pending = null;
    if (list) list.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-voucher-activate]");
      if (!btn) return;
      pending = btn.closest("[data-voucher]");
      const val = Number(btn.dataset.value) || 0;
      const sheet = document.querySelector('[data-sheet="voucherActivate"]');
      if (sheet) {
        sheet.dataset.value = String(val);
        const vEl = sheet.querySelector("[data-voucher-activate-value]");
        if (vEl) vEl.textContent = "EGP " + val;
      }
      openOverlay("voucherActivate");
    });
    const vConfirm = document.querySelector("[data-voucher-activate-confirm]");
    if (vConfirm && list) vConfirm.addEventListener("click", () => {
      const sheet = document.querySelector('[data-sheet="voucherActivate"]');
      const val = Number(sheet && sheet.dataset.value) || 0;
      const id = pending && pending.dataset.voucherId;
      try {
        localStorage.setItem(VOUCHERS_KEY, String(vouchersCredit() + val));
        if (id) { const u = vouchersUsed(); u.push(id); localStorage.setItem(V_USED_KEY, JSON.stringify(u)); }
      } catch (e) { /* ignore */ }
      const label = (pending && pending.querySelector("[data-voucher-activate]") && pending.querySelector("[data-voucher-activate]").dataset.label) || t("قسيمة خصم");
      if (pending) pending.remove();
      pending = null;
      addVoucherHistory(label, val);
      syncVouchersCount();
      closeOverlay();
      syncWalletBalance(true);
      toast(t("تم تفعيل القسيمة وإضافتها لمحفظتك"), "wallet");
    });
  }

  /* Order detail drawer (Ahmed, 2026-08-02): the whole order row opens a shared
     side-drawer and reveals that order's pre-rendered panel, so several orders
     can be viewed in turn without leaving the list. Buttons carrying
     data-order-open (the dashboard's tracker/detail) fire the same path
     natively; the keydown covers the <tr role="button"> rows. */
  function initOrders() {
    const drawer = document.querySelector('[data-drawer="order"]');
    if (!drawer) return;
    function open(id) {
      drawer.querySelectorAll("[data-order-panel]").forEach((panel) => {
        panel.hidden = panel.getAttribute("data-order-id") !== id;
      });
      const body = drawer.querySelector("[data-order-panels]");
      if (body) body.scrollTop = 0;
      openOverlay("order");
    }
    document.addEventListener("click", (e) => {
      const row = e.target.closest("[data-order-open]");
      if (!row) return;
      open(row.getAttribute("data-order-open"));
    });
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Enter" && e.key !== " ") return;
      const row = e.target.closest("tr[data-order-open]");
      if (!row) return;
      e.preventDefault();
      open(row.getAttribute("data-order-open"));
    });
  }

  /* Re-order — add a past order's whole item list back to the cart in one
     press, then open the cart drawer. Items ride on hidden [data-reorder-item]
     payloads next to the button, keyed by the catalogue id so the store dedupes
     against existing lines rather than creating a second one. */
  function initReorder() {
    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-reorder]");
      if (!btn) return;
      const card = btn.closest("[data-reorder-card]") || document;
      let n = 0;
      card.querySelectorAll("[data-reorder-item]").forEach((it) => {
        const qty = Number(it.dataset.qty) || 1;
        Cart.add(
          {
            id: it.dataset.id,
            name: it.dataset.name,
            price: Number(it.dataset.price) || 0,
            image: it.dataset.image,
          },
          qty,
        );
        n += qty;
      });
      if (n) {
        toast("تمت إضافة منتجات الطلب إلى السلة");
        openOverlay("cart");
      }
    });
  }

  /*
   * Addresses — the same contract as the cart and favourites stores: seeded
   * from the page's two demo addresses, persisted under jaad:addresses,
   * and the grid re-rendered from state on every change. Exactly one address
   * is the DEFAULT at all times: setting a new default clears the old one,
   * deleting the default promotes the first survivor.
   *
   * The stored flag is still called `main` — renaming a persisted key would
   * silently orphan every address already saved in a shopper's browser. Only
   * the WORD in the UI changed (Ahmed, 2026-08-23): "default" is what this
   * actually means — the address a new order starts with — where "main"
   * suggested a hierarchy of addresses that does not exist.
   */
  const ADDR_KEY = "jaad:addresses";
  const ADDR_SEED = [
    { id: "a-home", label: "المنزل", line1: "شقة 3 - 220 شارع الحرية - الدور الأول", line2: "مصر الجديدة، القاهرة", main: true },
    { id: "a-work", label: "العمل", line1: "مبنى 12 - شارع التسعين الشمالي", line2: "التجمع الخامس، القاهرة", main: false },
  ];

  function addrAll() {
    try {
      const v = JSON.parse(localStorage.getItem(ADDR_KEY));
      if (Array.isArray(v)) return v;
    } catch (e) {
      /* fall through to seed */
    }
    return ADDR_SEED.map((a) => Object.assign({}, a));
  }

  function addrWrite(list) {
    if (list.length && !list.some((a) => a.main)) list[0].main = true;
    try {
      localStorage.setItem(ADDR_KEY, JSON.stringify(list));
    } catch (e) {
      /* ignore */
    }
    renderAddresses();
  }

  /* One card. The "default address" state is a SWITCH now (Ahmed, 2026-08-23),
     not the read-only cream pill it used to be: the pill told you which address
     was the default and gave you no way to change it — the only route was to
     open Edit, find a checkbox in the form and save. Setting your default is a
     one-tap decision, so it is one tap.

     The switch is the same `[data-switch] + .switch` control the wallet and
     gift toggles use, so it inherits their painted states and keyboard support.
     The default's own switch is `disabled`: turning it OFF would leave the list
     with no default at all, and the honest answer to "what happens then" is
     "you pick a different one instead", which is exactly what the other cards'
     switches are for. */
  function addressCardHTML(a) {
    return `
      <div class="flex flex-col gap-4 bg-white shadow-custom4 p-6 rounded-[20px]" data-address-card data-id="${esc(a.id)}">
        <div class="flex justify-between items-center gap-3">
          <h3 class="font-bold text-ink text-base">${esc(t(a.label))}</h3>
        </div>
        <!-- t() on the stored VALUES, not just the chrome (Ahmed, 2026-08-23).
             The seed is Arabic, the grid re-renders from the store on every
             change, and the translation pass has long since finished by then —
             so an English visitor who touched any address (and, now that the
             default is a toggle, that is a one-tap action) watched the two demo
             addresses flip back into Arabic. Anything the shopper typed
             themselves simply has no dictionary entry and passes through
             unchanged, which is the correct behaviour for a real address. -->
        <div class="flex flex-col gap-1 text-muted text-sm">
          <span>${esc(t(a.line1))}</span><span>${esc(t(a.line2))}</span>
        </div>
        <label class="flex justify-between items-center gap-3 mt-auto pt-4 border-divider border-t ${a.main ? "" : "cursor-pointer"}">
          <span class="font-semibold ${a.main ? "text-ink" : "text-muted"} text-sm">${esc(t("العنوان الافتراضي"))}</span>
          <input type="checkbox" data-switch data-address-default class="sr-only"${a.main ? " checked disabled" : ""} />
          <span class="switch shrink-0" aria-hidden="true"><span class="switch__knob"></span></span>
        </label>
        <div class="flex gap-2">
          <button type="button" data-address-edit class="hover:bg-cream px-4 py-1.5 border border-divider rounded-full font-semibold text-ink text-xs transition-colors">${esc(t("تعديل"))}</button>
          <button type="button" data-address-remove class="px-4 py-1.5 font-semibold text-error text-xs">${esc(t("حذف"))}</button>
        </div>
      </div>`;
  }

  function renderAddresses() {
    const grid = document.querySelector("[data-addresses-grid]");
    if (!grid) return;
    const list = addrAll();
    grid.innerHTML = list.length
      ? list.map(addressCardHTML).join("")
      : `<p class="col-span-full py-8 text-muted text-sm">${esc(t("لا توجد عناوين محفوظة بعد."))}</p>`;
  }

  function openAddressForm(addr) {
    const form = document.querySelector("[data-address-form]");
    if (!form) return;
    form.dataset.addressId = addr ? addr.id : "";
    form.elements.label.value = addr ? addr.label : "";
    form.elements.line1.value = addr ? addr.line1 : "";
    form.elements.line2.value = addr ? addr.line2 : "";
    form.elements.main.checked = addr ? !!addr.main : false;
    // The default address cannot demote itself — there would be no default
    // left. Pick a different card's switch instead.
    form.elements.main.disabled = !!(addr && addr.main);
    const title = document.querySelector("[data-address-form-title]");
    if (title) title.textContent = addr ? t("تعديل العنوان") : t("اضف عنوان");
    openOverlay("address");
    setTimeout(() => form.elements.label.focus(), 80);
  }

  function initAddresses() {
    if (!document.querySelector("[data-addresses-grid]")) return;
    renderAddresses();

    /* The default switch. `change`, not the click delegation below — a label
       wrapping a checkbox fires click twice (once for the label, once for the
       input it forwards to), and a click handler would toggle the state and
       then toggle it straight back. */
    document.addEventListener("change", (e) => {
      const sw = e.target.closest("[data-address-default]");
      if (!sw) return;
      const host = sw.closest("[data-address-card]");
      if (!host) return;
      const list = addrAll();
      list.forEach((a) => (a.main = a.id === host.dataset.id));
      addrWrite(list);
      toast(t("تم تعيين العنوان الافتراضي"));
    });

    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-address-add]")) {
        openAddressForm(null);
        return;
      }
      const card = e.target.closest("[data-address-card]");
      if (!card) return;
      const list = addrAll();
      const addr = list.find((a) => a.id === card.dataset.id);
      if (!addr) return;
      if (e.target.closest("[data-address-edit]")) {
        openAddressForm(addr);
      } else if (e.target.closest("[data-address-remove]")) {
        addrWrite(list.filter((a) => a.id !== addr.id));
        toast(t("تم حذف العنوان"));
      }
    });

    document.addEventListener("submit", (e) => {
      const form = e.target.closest("[data-address-form]");
      if (!form) return;
      e.preventDefault();
      const list = addrAll();
      const id = form.dataset.addressId;
      const entry = {
        id: id || "a-" + Date.now(),
        label: form.elements.label.value.trim(),
        line1: form.elements.line1.value.trim(),
        line2: form.elements.line2.value.trim(),
        main: form.elements.main.checked,
      };
      if (!entry.label || !entry.line1 || !entry.line2) return;
      if (entry.main) list.forEach((a) => (a.main = false));
      const at = list.findIndex((a) => a.id === id);
      if (at >= 0) list[at] = Object.assign({}, list[at], entry);
      else list.push(entry);
      addrWrite(list);
      closeOverlay();
      toast(t(id ? "تم تعديل العنوان" : "تمت إضافة العنوان"));
    });
  }

  /* Category cards fan their two cutouts apart on hover (desktop). Touch has no
     hover, so on (hover: none) reveal the SAME motion by SCROLL: when a card
     reaches the vertical centre of the viewport it gets .in-view and the
     group-[.in-view] variants fire (Ahmed, 2026-08-19). The root is a thin band
     at the viewport centre (top/bottom margins pulled in ~45%), so a card is
     "active" only while it sits centred — exactly the phone behaviour asked for. */
  function initCategoryReveal(scope) {
    const cards = [...scope.querySelectorAll("[data-cat-card]")];
    if (!cards.length || !("IntersectionObserver" in window)) return;
    // Trigger on any device WITHOUT real hover OR any phone-width viewport — a
    // narrowed desktop that shows the mobile 1-col layout has no fan-apart hover
    // either, so it should scroll-reveal too (comma = OR in a media query list).
    const noHover = window.matchMedia("(hover: none), (pointer: coarse), (max-width: 767px)");
    let io = null;
    const enable = () => {
      if (io) return;
      io = new IntersectionObserver(
        (entries) =>
          entries.forEach((e) => e.target.classList.toggle("in-view", e.isIntersecting)),
        // A generous centre band (middle ~30% of the viewport) so a card lights up
        // as it scrolls through the middle of the screen, not only dead-centre.
        { rootMargin: "-35% 0px -35% 0px", threshold: 0 },
      );
      cards.forEach((c) => io.observe(c));
    };
    const disable = () => {
      if (!io) return;
      io.disconnect();
      io = null;
      cards.forEach((c) => c.classList.remove("in-view"));
    };
    const apply = () => (noHover.matches ? enable() : disable());
    apply();
    if (noHover.addEventListener) noHover.addEventListener("change", apply);
    else if (noHover.addListener) noHover.addListener(apply);
  }

  window.kInit = function (scope) {
    scope = scope || document;
    scope.querySelectorAll(".carousel").forEach(initCarousel);
    scope.querySelectorAll("[data-drag-scroll]").forEach(initDragScroll);
    initAccordions(scope);
    initTabs(scope);
    initGallery(scope);
    initSteppers(scope);
    initSizeAndPrice(scope);
    initDemoForms(scope);
    initPasswordReveals(scope);
    initListing(scope);
    initFancySelect(scope);
    initDropdowns(scope);
    initReveal(scope);
    initCategoryReveal(scope);
  };

  /* ---------------------------------------------------------------
     Boot
     --------------------------------------------------------------- */
  /* Runtime A/B for the button style (Ahmed, 2026-08-18): a fixed switch at the
     bottom that flips every primary CTA between V1 (green pill) and V2 (orange,
     16px) and remembers the choice in localStorage. Pure CSS does the repaint
     via html[data-btn] (see styles.css). */
  /* Pick the right product image for the current toggle mode. Used by the JS
     card builder so dynamically-rendered cards are born in the correct mode. */
  function imgFor(scene, plain) {
    scene = scene || "";
    plain = plain || scene;
    return document.documentElement.getAttribute("data-img") === "plain" ? plain : scene;
  }

  /* Swap every product image between its in-scene shot and its white-background
     original. Static (Python) cards + the gallery are swapped here; dynamic
     cards are born correct via imgFor(), and this also catches any already on
     the page. The gallery plate flips fill: cut-outs sit contained, scenes
     cover the plate edge-to-edge. */
  function applyImgStyle(mode) {
    mode = mode === "plain" ? "plain" : "scene";
    document.querySelectorAll("img[data-img-scene]").forEach((im) => {
      const scene = im.getAttribute("data-img-scene") || "";
      const plain = im.getAttribute("data-img-plain") || scene;
      const next = mode === "plain" ? plain : scene;
      if (next && im.getAttribute("src") !== next) im.setAttribute("src", next);
    });
    document.querySelectorAll("[data-gallery-main]").forEach((im) => {
      const plate = im.closest("[data-gallery-plate]");
      if (plate) plate.setAttribute("data-fill", mode === "plain" ? "contain" : "cover");
    });
    // Let the scroll story recompute when the mode flips into/out of white.
    document.dispatchEvent(new CustomEvent("jaad:img", { detail: mode }));
  }

  /* White-mode scroll story (product page). A pinned, scroll-scrubbed stage:
     the packshot locks to centre and drifts subtly on X/Y with a small 2D tilt
     (it is a flat image, so no 3D tumble) while the benefit panels reveal one
     at a time, alternating sides and overlapping the image; the FAQ accordions
     follow below. Inert unless the story markup is present AND the image toggle
     is in white mode. Reduced-motion falls back to a static, un-pinned stack. */
  function initProductStory() {
    const story = document.querySelector("[data-story]");
    if (!story) return;
    const stage = story.querySelector("[data-story-stage]");
    const img = story.querySelector("[data-story-img]");
    const panels = [...story.querySelectorAll("[data-story-panel]")];
    const galleryImg = document.querySelector("[data-gallery-main]");
    const galleryPlate = galleryImg ? galleryImg.closest("[data-gallery-plate]") : null;
    const detach = (on) => { if (galleryPlate) galleryPlate.classList.toggle("story-detached", on); };
    const faqSection = document.querySelector("[data-story-faq]");
    if (!stage || !img || !panels.length) return;
    const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
    const lerp = (a, b, t) => a + (b - a) * t;

    if (reduceMotion()) {
      // No scrub: drop the fixed overlay into normal flow as a static stack.
      story.style.height = "auto";
      stage.style.cssText += ";position:static;opacity:1;pointer-events:auto;display:flex;flex-direction:column;align-items:center;gap:24px;padding:24px 16px;";
      img.style.cssText += ";position:static;transform:none;left:auto;top:auto;width:min(80vw,420px);height:auto;";
      panels.forEach((panel) => {
        panel.style.cssText += ";position:static;opacity:1;transform:none;left:auto;right:auto;width:min(90vw,340px);";
      });
      return;
    }

    /* FLIP: S = the gallery image's rect projected to scroll 0 (the flight
       START); E = the centred, large rect (the flight END). The clone is laid
       out AT E and a transform maps it back onto S while flying, so it literally
       lifts off the gallery and eases to centre as one continuous scroll. */
    // The story uses a transparent CUTOUT so the flying product is isolated over
    // the page (no white box over the copy). Point the gallery at the SAME cutout
    // in white mode, so the image that detaches is the one already on screen.
    const CUTOUT = story.getAttribute("data-cutout") || img.getAttribute("src");
    img.src = CUTOUT;
    if (galleryImg) {
      galleryImg.setAttribute("data-img-plain", CUTOUT);
      if (document.documentElement.getAttribute("data-img") === "plain") galleryImg.src = CUTOUT;
    }

    // Leaves that drift OUT of the packshot during the hold (Ahmed, 2026-08-19,
    // for both option A choices). Purely decorative; created once, positioned
    // each frame off the image centre and the hold progress `g`.
    const LEAF_SVG =
      '<svg viewBox="0 0 24 24" fill="currentColor" class="w-full h-full">' +
      '<path d="M6.05 8.05c-2.73 2.73-2.73 7.15-.02 9.88 1.47-3.4 4.09-6.24 ' +
      '7.36-7.93-2.77 2.34-4.71 5.61-5.39 9.32 2.6 1.23 5.8.78 7.95-1.37C19.43 ' +
      '14.47 20 4 20 4S9.53 4.57 6.05 8.05z"/></svg>';
    const LEAF_N = 12;
    const leaves = [];
    for (let i = 0; i < LEAF_N; i++) {
      const s = document.createElement("span");
      s.className = "product-story__leaf";
      s.setAttribute("aria-hidden", "true");
      s.innerHTML = LEAF_SVG;
      stage.appendChild(s);
      leaves.push(s);
    }

    let S = null, E = null, fitOff = 0;
    function measure() {
      const ar = img.naturalWidth && img.naturalHeight ? img.naturalHeight / img.naturalWidth : 1.2;
      if (galleryImg) {
        const r = galleryImg.getBoundingClientRect();
        // Fit the aspect INSIDE the gallery box (object-contain) so the clone
        // starts EXACTLY on the displayed packshot — no size jump on detach.
        let fw, fh;
        if (ar > r.height / r.width) { fh = r.height; fw = fh / ar; }
        else { fw = r.width; fh = fw * ar; }
        // Vertical letterbox offset of the fitted packshot inside its gallery box.
        // The clone must ride at box-top + this, not the box top, or it jumps up
        // by this much the instant it takes over from the real (sticky) gallery.
        fitOff = (r.height - fh) / 2;
        S = { left: r.left + (r.width - fw) / 2, top: r.top + (r.height - fh) / 2 + window.scrollY, width: fw, height: fh };
      } else {
        S = { left: window.innerWidth * 0.2, top: 120, width: window.innerWidth * 0.6, height: window.innerHeight * 0.5 };
      }
      let ew = Math.min(window.innerWidth * 0.72, 500);
      let eh = ew * ar;
      const maxh = window.innerHeight * 0.76;
      if (eh > maxh) { eh = maxh; ew = eh / ar; }
      E = { left: (window.innerWidth - ew) / 2, top: (window.innerHeight - eh) / 2, width: ew, height: eh };
      img.style.left = E.left + "px";
      img.style.top = E.top + "px";
      img.style.width = E.width + "px";
      img.style.height = E.height + "px";
    }

    // Where the ridden packshot pins on screen while the rest of the right
    // column scrolls past beneath it. Below the sticky nav (60) AND the sticky
    // buy bar, so the riding product never tucks behind either.
    const PIN_TOP = 132;
    const easeInOut = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

    let ticking = false;
    function frame() {
      ticking = false;
      if (document.documentElement.getAttribute("data-img") !== "plain") {
        stage.style.opacity = "0";
        if (galleryImg) galleryImg.style.opacity = "";
        detach(false);
        return;
      }
      if (!E) measure();
      const y = window.scrollY;
      const D1 = Math.max(1, story.offsetTop);     // top of the story section = where the right column ends
      const D2 = Math.max(1, story.offsetHeight);  // story spacer height (the flight + reveal live in here)

      if (y > D1 + D2) {                            // past the whole story: released
        stage.style.opacity = "0";
        if (galleryImg) galleryImg.style.opacity = "0";
        return;
      }

      // ===================== MOBILE (Ahmed, 2026-08-19 v3) =====================
      // On a phone the desktop RIDE/FLIP doesn't fit: the pinned packshot riding
      // behind the copy was cramped and unreadable. Instead the story stays fully
      // HIDDEN while the product content scrolls, then — only once the content
      // ends (y >= D1) — the white packshot animates IN at screen centre (fade +
      // rise + slight scale), the four benefits reveal, leaves stream, and the
      // whole overlay releases up as the FAQ rises. No ride, no over/under-content
      // overlap; it plays in its own white spacer on top.
      if (window.matchMedia("(max-width: 640px)").matches) {
        if (y < D1) {                               // still in the content: nothing overlaid
          stage.style.opacity = "0";
          if (galleryImg) galleryImg.style.opacity = "";
          detach(false);
          return;
        }
        if (galleryImg) galleryImg.style.opacity = "0";
        stage.style.opacity = "1";
        detach(false);
        img.src = CUTOUT;
        img.style.left = E.left + "px";
        img.style.top = E.top + "px";
        img.style.width = E.width + "px";
        img.style.height = E.height + "px";
        img.style.transformOrigin = "center center";

        const g = clamp01((y - D1) / D2);
        const INTRO = 0.14;                          // fraction spent easing the packshot in
        const t = clamp01(g / INTRO);
        const ease = easeInOut(t);
        const OUTRO_AT = 0.80, OUTRO_LEN = 0.15;
        const outro = clamp01((g - OUTRO_AT) / OUTRO_LEN);
        const sc = lerp(0.86, 1, ease);
        const ty = lerp(30, 0, ease);
        const drift = t >= 1 ? 5 * Math.sin(g * Math.PI * 2) : 0;
        img.style.opacity = (ease * (1 - outro)).toFixed(3);
        img.style.transform =
          "translateY(" + (ty + drift).toFixed(1) + "px) scale(" + sc.toFixed(3) + ")";

        const first = 0.16, step = 0.11, fade = 0.08;
        panels.forEach((panel, i) => {
          const st = first + i * step;
          const a = (g >= st) ? clamp01((g - st) / fade) : 0;
          panel.style.opacity = (a * (1 - outro)).toFixed(3);
          panel.style.transform = "translateY(" + ((1 - a) * 20).toFixed(1) + "px)";
        });

        const cx = E.left + E.width / 2, cy = E.top + E.height / 2;
        leaves.forEach((leaf, i) => {
          const ang = i * 2.39996;
          const startI = 0.16 + (i % 5) * 0.04;
          const p = clamp01((g - startI) / 0.5);
          const dist = lerp(18, 150 + (i % 4) * 34, p);   // tighter spread than desktop
          const lx = cx + Math.cos(ang) * dist - 11;
          const ly = cy + Math.sin(ang) * dist - 40 * p - 11;
          const lrot = p * 200 * (i % 2 ? 1 : -1);
          const op = Math.sin(clamp01(p) * Math.PI) * (1 - outro);
          leaf.style.transform =
            "translate(" + lx.toFixed(1) + "px," + ly.toFixed(1) + "px) rotate(" + lrot.toFixed(1) + "deg)";
          leaf.style.opacity = op.toFixed(3);
        });

        const faqTopM = faqSection ? faqSection.getBoundingClientRect().top : Infinity;
        const releaseTyM = Math.min(0, faqTopM - window.innerHeight * 1.05);
        stage.style.transform = "translateY(" + releaseTyM.toFixed(1) + "px)";
        return;
      }

      // ===================== RIDE (Ahmed, 2026-08-19 v2) =====================
      // Content-first, but the package no longer just scrolls away: it RIDES.
      // While the taller right column (gallery + "قد يعجبك أيضاً") scrolls, the
      // packshot pins under the nav and travels down WITH you. The real gallery
      // stays live at the top of the page; the fixed clone takes over exactly at
      // the pin line (seamless, same spot) and holds there until the column ends.
      // The flight STARTS the moment the (pinned) gallery's bottom lines up with
      // the bottom of the taller right column — the content has run out beneath
      // the packshot (Ahmed, 2026-08-19: same instant the border fades) — and
      // eases to centre over the scroll left until the story spacer (D1). No
      // pinned dead-hold in between: from that alignment on, every scrolled px
      // moves the package a little closer to centre.
      const FLY_START = D1 - PIN_TOP - S.height;
      if (y < FLY_START) {
        // Read the REAL gallery box each frame so the clone can take over on the
        // exact same pixels (the box is CSS-sticky at PIN_TOP; a computed y-based
        // guess drifted from it and caused a visible "switch in place" jump).
        const gr = galleryImg ? galleryImg.getBoundingClientRect() : null;
        const boxTop = gr ? gr.top : (S.top - y);   // gallery box top on screen
        if (boxTop > PIN_TOP) {                     // gallery still scrolling in & interactive
          stage.style.opacity = "0";
          if (galleryImg) galleryImg.style.opacity = "";
          detach(false);                            // outer plate border ON
          return;
        }
        // Pinned: the package RIDES. The clone sits on the LIVE fitted packshot —
        // box top plus the object-contain letterbox offset — so the hand-off from
        // the real gallery is pixel-identical. The gallery's CSS sticky RELEASES
        // once its bottom hits the grid bottom (before FLY_START), so boxTop keeps
        // climbing off-screen after that; the clone must NOT follow it up — it
        // clamps to the pin line and HOLDS there until the flight, or the
        // detach-to-centre starts from an off-screen package and reads as a
        // fade-in at centre instead of a travel.
        if (galleryImg) galleryImg.style.opacity = "0";
        stage.style.opacity = "1";
        stage.style.transform = "none";
        detach(false);                              // border ON until the flight starts
        img.src = galleryImg ? (galleryImg.currentSrc || galleryImg.src || CUTOUT) : CUTOUT;
        img.style.left = (gr ? gr.left + (gr.width - S.width) / 2 : S.left) + "px";
        img.style.top = (Math.max(boxTop, PIN_TOP) + fitOff) + "px";
        img.style.width = S.width + "px";
        img.style.height = S.height + "px";
        img.style.opacity = "1";
        img.style.transform = "none";
        panels.forEach((panel) => { panel.style.opacity = "0"; });
        leaves.forEach((leaf) => { leaf.style.opacity = "0"; });
        return;
      }

      // ================= DETACH → FLY TO CENTRE → HOLD =================
      // The content beneath the packshot has run out (y >= FLY_START). It
      // DETACHES and travels to screen-centre as one continuous motion (a FLIP
      // that maps the centred END rect back onto the pinned rect and eases to
      // identity), arriving as the story spacer takes the screen (y = D1); it
      // then holds while the four benefits reveal and the leaves stream out.
      if (galleryImg) galleryImg.style.opacity = "0";
      stage.style.opacity = "1";
      detach(true);                                 // outer plate border FADES OUT as it detaches
      img.src = CUTOUT;
      img.style.transformOrigin = "top left";       // FLIP math needs top-left (mobile sets centre)
      img.style.left = E.left + "px";
      img.style.top = E.top + "px";
      img.style.width = E.width + "px";
      img.style.height = E.height + "px";

      const g = clamp01((y - D1) / D2);
      // Flight progress: 0 at FLY_START (border fade + lift-off, one instant) →
      // 1 at D1. One eased travel across that whole stretch — it starts moving
      // the moment it detaches (Ahmed, 2026-08-19: no pinned wait, no late fly).
      const t = clamp01((y - FLY_START) / Math.max(1, D1 - FLY_START));
      const ease = easeInOut(t);
      const OUTRO_AT = 0.80, OUTRO_LEN = 0.15;
      const outro = clamp01((g - OUTRO_AT) / OUTRO_LEN);

      // FLIP: pinned rect P (left S.left, top PIN_TOP + letterbox offset, size S)
      // → centred rect E. The +fitOff matches where the ride left the packshot,
      // so detach continues from the exact same spot (no jump).
      const dx = lerp(S.left - E.left, 0, ease);
      const dy = lerp(PIN_TOP + fitOff - E.top, 0, ease);
      const sc = lerp(S.width / E.width, 1, ease);
      const drift = t >= 1 ? 6 * Math.sin(g * Math.PI * 2) : 0;  // gentle drift once arrived
      img.style.opacity = (1 - outro).toFixed(3);
      img.style.transform =
        "translate(" + (dx + drift).toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + sc.toFixed(3) + ")";

      const first = 0.16, step = 0.11, fade = 0.08;
      panels.forEach((panel, i) => {
        const st = first + i * step;
        const a = (g >= st) ? clamp01((g - st) / fade) : 0;
        panel.style.opacity = (a * (1 - outro)).toFixed(3);
        panel.style.transform = "translateY(" + ((1 - a) * 20).toFixed(1) + "px)";
      });

      // Leaves stream out from BEHIND the packshot (z-index in styles.css) once it
      // has arrived, thinning out with the outro. Emitted from the image centre
      // along fixed angles (golden-angle spread) so they never clump.
      const cx = E.left + E.width / 2, cy = E.top + E.height / 2;
      leaves.forEach((leaf, i) => {
        const ang = i * 2.39996;                      // golden angle, radians
        const startI = 0.16 + (i % 5) * 0.04;
        const p = clamp01((g - startI) / 0.5);
        const dist = lerp(20, 205 + (i % 4) * 42, p);
        const lx = cx + Math.cos(ang) * dist - 11;
        const ly = cy + Math.sin(ang) * dist - 46 * p - 11;
        const lrot = p * 200 * (i % 2 ? 1 : -1);
        const op = Math.sin(clamp01(p) * Math.PI) * (1 - outro);
        leaf.style.transform =
          "translate(" + lx.toFixed(1) + "px," + ly.toFixed(1) + "px) rotate(" + lrot.toFixed(1) + "deg)";
        leaf.style.opacity = op.toFixed(3);
      });

      // The story does NOT vanish at the end — the whole overlay scrolls UP with
      // the page (1:1) as the FAQ rises in from below, so it stays fully visible
      // and just leaves past the top while the FAQ takes its place. No overlap,
      // no disappearing act.
      const faqTop = faqSection ? faqSection.getBoundingClientRect().top : Infinity;
      const releaseTy = Math.min(0, faqTop - window.innerHeight * 1.05);
      stage.style.transform = "translateY(" + releaseTy.toFixed(1) + "px)";
      stage.style.opacity = "1";
    }

    function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", () => { measure(); schedule(); }, { passive: true });
    document.addEventListener("jaad:img", () => { measure(); schedule(); });
    measure();
    frame();
  }

  /* ---------------------------------------------------------------
     About — "From nature to you" scroll journey (Ahmed, 2026-08-20)

     Sibling to initProductStory, deliberately a different mechanic: there a
     packshot flies to centre and holds; here one circular window stays put and
     the product worlds travel THROUGH it as the chapter copy cross-fades.

     Scroll-scrubbed off the section's own spacer, so it is fully reversible and
     never animates on a timer. The JS does the minimum: pick the current
     chapter index, set a 0..1 progress for the ring, and drive a short "burst"
     around each hand-off that throws the leaves out. Everything visual lives in
     styles.css, so a chapter with no JS still renders (chapter 0 is marked
     current at build time).

     Inert without [data-about-journey], and a full no-op under reduced motion,
     where the CSS already un-pins the section into a readable stack.
     --------------------------------------------------------------- */
  function initAboutJourney() {
    const section = document.querySelector("[data-about-journey]");
    if (!section) return;
    if (reduceMotion()) return;          // CSS renders the static stack

    const imgs = [...section.querySelectorAll("[data-journey-img]")];
    const chapters = [...section.querySelectorAll("[data-journey-chapter]")];
    const nodes = [...section.querySelectorAll("[data-journey-node]")];
    const leaves = [...section.querySelectorAll("[data-journey-leaf]")];
    const ring = section.querySelector("[data-journey-progress]");
    const media = section.querySelector("[data-journey-media]");
    const n = chapters.length;
    if (!n || imgs.length !== n) return;

    const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
    let current = -1;
    let target = 0;
    let shown = 0;
    let raf = 0;

    // The same damped chase the timeline below uses (see initAboutTimeline for
    // the full reasoning): the target tracks scroll exactly, the drawn value
    // eases toward it, and the few frames of lag are what read as weight rather
    // than as a value being dragged by the wheel. Both sections on this page
    // move on the one rule, so the page has a single feel instead of two.
    // Lower is heavier: each frame closes this much of the remaining distance,
    // so 0.06 lags further behind the wheel and settles more slowly than 0.085
    // did (Ahmed, 2026-08-23: "make the scroll ease a little"). This is the one
    // number to turn if the page feels floaty or snappy - both sections read it,
    // so they stay in step with each other whatever it is set to.
    const EASE = 0.06;
    const SNAP = 0.0004;

    function readTarget() {
      const rect = section.getBoundingClientRect();
      const span = Math.max(1, section.offsetHeight - window.innerHeight);
      // 0 when the section's top reaches the viewport top, 1 at its end.
      target = clamp01(-rect.top / span);
      kick();
    }
    function tick() {
      raf = 0;
      const diff = target - shown;
      if (Math.abs(diff) < SNAP) shown = target;
      else shown += diff * EASE;
      paint(shown);
      if (shown !== target) kick();
    }
    function kick() { if (!raf) raf = requestAnimationFrame(tick); }

    function paint(g) {

      // Which chapter owns this scroll position. The last chapter keeps the
      // stage through the run-out rather than blanking at exactly g === 1.
      const idx = Math.min(n - 1, Math.floor(g * n));
      if (idx !== current) {
        current = idx;
        imgs.forEach((el, i) => el.classList.toggle("is-current", i === idx));
        chapters.forEach((el, i) => el.classList.toggle("is-current", i === idx));
        nodes.forEach((el, i) => el.classList.toggle("is-current", i === idx));
      }

      if (ring) ring.style.setProperty("--p", g.toFixed(3));

      // Leaf burst: peaks at each chapter boundary and decays quickly, so the
      // leaves throw out on the hand-off instead of drifting the whole time.
      const local = g * n - idx;                 // 0..1 within the chapter
      const burst = Math.max(0, 1 - local / 0.34);
      // A scrub can also run backwards; the burst is symmetrical either way.
      const val = burst.toFixed(3);
      leaves.forEach((leaf) => leaf.style.setProperty("--burst", val));

      // The window breathes very slightly across its own chapter, so the
      // sequence never looks frozen between hand-offs.
      if (media) media.style.transform = "scale(" + (1 + local * 0.03).toFixed(4) + ")";
    }

    window.addEventListener("scroll", readTarget, { passive: true });
    window.addEventListener("resize", readTarget, { passive: true });
    // Land on the real value for the first paint rather than easing up from
    // zero — a page opened part-way down should not animate itself in.
    readTarget();
    shown = target;
    paint(shown);
  }

  /* ---------------------------------------------------------------
     About — the timeline vector ("الطريق إلى جاد", Ahmed, 2026-08-23)

     Draws the meandering path in as the section scrolls, rides a dot on the
     drawn end, and wakes each milestone as the line reaches its node.

     The scrub window is deliberately NOT the section's own box. A timeline is
     read top to bottom while it crosses the screen, so progress runs from "the
     section's top has just reached the bottom of the viewport" to "its bottom
     has just left the top" — the whole time any part of it is on screen. Using
     the section box alone would finish the drawing while the last milestone was
     still below the fold.

     The head dot is placed through the SVG's own screen CTM rather than by
     arithmetic on the viewBox: `preserveAspectRatio="none"` scales x and y by
     different factors, and the CTM already carries both, so the browser does
     the mapping and there is nothing here to drift out of step with the CSS.

     Inert without [data-about-timeline], and a full no-op under reduced motion,
     where the CSS hands over a drawn line and visible rows.
     --------------------------------------------------------------- */
  function initAboutTimeline() {
    const section = document.querySelector("[data-about-timeline]");
    if (!section) return;
    if (reduceMotion()) return;          // CSS renders the drawn, static version

    const path = section.querySelector("[data-time-path]");
    const head = section.querySelector("[data-time-head]");
    const rows = [...section.querySelectorAll("[data-time-row]")];
    if (!path || !rows.length) return;

    const body = section.querySelector(".about-time__body") || section;
    const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
    let len = 0;
    let target = 0;   // where the scroll says we are
    let shown = 0;    // where the drawing actually is, chasing it
    let raf = 0;

    // Re-author the path in PIXEL space and match the viewBox to it 1:1.
    //
    // The server-rendered path is in a 100-wide, 100-per-row viewBox stretched
    // over the band with preserveAspectRatio="none". That renders correctly and
    // is the right thing to ship for a no-JS visit, but it cannot be DASHED
    // correctly: `vector-effect: non-scaling-stroke` moves the stroke — dash
    // pattern included — into screen space, while getTotalLength() stays in
    // user units. The two disagree by whatever the stretch factor is, so a dash
    // array of "the path's length" repeats several times down the band and the
    // line paints in stripes instead of drawing in once.
    //
    // Making the viewBox the band's own pixel box removes the disagreement at
    // the source: one user unit is one pixel, the stretch factor is 1, and the
    // measured length is the drawn length. It also means the node maths is the
    // same on both sides — a row is H/n tall here and in the CSS grid.
    // How far the line swings away from the straight run between two nodes, as
    // a fraction of the band's width. Big on purpose (Ahmed, 2026-08-23): the
    // reference's paths leave one point, sweep most of the way across, and come
    // back to the next.
    const SWING = 0.34;
    // Never let the curve reach the band's edge - a line that touches it reads
    // as a mistake rather than a flourish. Proportional rather than a flat
    // 24px: on the phone's 64px gutter a fixed inset ate most of the room the
    // swing had to work in and flattened the line to nearly straight.
    const edgeFor = (w) => Math.min(24, w * 0.12);

    // The path is a CATMULL-ROM SPLINE through a list of points, converted to
    // cubic beziers, rather than a hand-placed curve per pair of nodes.
    //
    // The reason is the corner (Ahmed, 2026-08-23: "I don't want a sharp
    // angle"). The old version ran a straight vertical lead-in down to the
    // first node and then left it with both control points off to one side,
    // i.e. arriving vertically and departing horizontally — a 90° corner at
    // exactly the most visible node on the page. Node-to-node happened to be
    // smooth, because the lobe flipped sign and left the two control points
    // collinear through the node, but that was luck rather than a property.
    //
    // A Catmull-Rom spline has the property instead of getting lucky: each
    // point's tangent is set from its NEIGHBOURS, so every join is C1
    // continuous by construction — including the first and the last. Nothing in
    // here can produce a corner.
    //
    // The wander comes from the point list, not from bent controls: between
    // each pair of nodes a MIDPOINT is pushed far out to alternating sides, and
    // the spline flows through it. Pushed far enough the curve overshoots into
    // the long, looping sweep the reference has.
    // Where the node dots actually ARE, measured from the DOM rather than
    // recomputed from a copy of the layout maths. The dots are placed by CSS
    // and move between breakpoints (a narrow gutter on phones, alternating
    // 44px either side of centre from md); measuring them means the line cannot
    // drift out of register with them at any width, and it is why RTL needs no
    // special case here.
    function nodePoints(box) {
      return rows.map((row) => {
        const d = row.querySelector(".about-time__dot").getBoundingClientRect();
        return { x: d.left + d.width / 2 - box.left, y: d.top + d.height / 2 - box.top };
      });
    }

    function splinePath(pts) {
      // Duplicate the ends so the first and last segments have neighbours to
      // take their tangent from.
      const p = [pts[0]].concat(pts, [pts[pts.length - 1]]);
      const cmds = ["M" + r(pts[0].x) + " " + r(pts[0].y)];
      for (let i = 1; i < p.length - 2; i++) {
        const p0 = p[i - 1], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2];
        // The /6 is the standard Catmull-Rom to bezier conversion; it is what
        // makes the curve pass THROUGH every point rather than near it.
        const c1x = p1.x + (p2.x - p0.x) / 6, c1y = p1.y + (p2.y - p0.y) / 6;
        const c2x = p2.x - (p3.x - p1.x) / 6, c2y = p2.y - (p3.y - p1.y) / 6;
        cmds.push("C" + r(c1x) + " " + r(c1y) + ", " + r(c2x) + " " + r(c2y) + ", " + r(p2.x) + " " + r(p2.y));
      }
      return cmds;
    }
    const r = (v) => Math.round(v * 10) / 10;

    // The point list: an entry point above the first node, then every node with
    // a swung midpoint between consecutive ones, then an exit below the last.
    // The entry and exit are offset sideways too — a lead-in that came straight
    // down would give the first node a vertical tangent and put the corner back.
    function pointsFor(nodes, w, h) {
      const edge = edgeFor(w);
      const clampX = (v) => (v < edge ? edge : v > w - edge ? w - edge : v);
      const first = nodes[0];
      const last = nodes[nodes.length - 1];
      const pts = [{ x: clampX(first.x + w * SWING * 0.5), y: -h * 0.04 }];
      for (let i = 0; i < nodes.length; i++) {
        pts.push(nodes[i]);
        if (i < nodes.length - 1) {
          const b = nodes[i + 1];
          const lobe = (i % 2 === 0 ? 1 : -1) * w * SWING;
          pts.push({ x: clampX((nodes[i].x + b.x) / 2 + lobe), y: (nodes[i].y + b.y) / 2 });
        }
      }
      /* The run-out used to leave sideways and finish BELOW the box, where it
         was clipped away — the line simply stopped at the last milestone and
         the head blinked out (Ahmed, 2026-08-25: "I want that circle to not
         fade out at the end"). It now swings once more and lands centred on
         the bottom edge, inside the tail spacer, which puts the head directly
         over the middle stat card. Two points rather than one so the spline
         still has a wander to flow through instead of straightening early. */
      pts.push({ x: clampX((last.x + w / 2) / 2 - w * SWING * 0.28), y: last.y + (h - last.y) * 0.45 });
      pts.push({ x: w / 2, y: h - 4 });
      return pts;
    }

    // Where each node lands in that list: entry, then node, midpoint, node, …
    // so node i is at index 1 + 2i. The command that ENDS at list index k is
    // cmds[k] (cmds[0] is the M), so the prefix through node i is the first
    // 2 + 2i commands.
    const nodeCmdCount = (i) => 2 + 2 * i;

    // How far along the path each node sits, as a fraction of the whole. Not
    // (i + 0.5) / n: the path carries a lead-in from the top edge down to the
    // first node and a run-out from the last one to the bottom, and each swung
    // segment is far longer than the vertical distance it covers. Guessing
    // would light the milestones out of step with the line that is supposed to
    // be reaching them, which is the one thing this section has to get right.
    //
    // A detached <path> is enough to measure a prefix — it never enters the
    // document.
    let nodeAt = [];
    function measureNodes(cmds, total) {
      const probe = document.createElementNS("http://www.w3.org/2000/svg", "path");
      nodeAt = rows.map((_row, i) => {
        probe.setAttribute("d", cmds.slice(0, nodeCmdCount(i)).join(" "));
        return probe.getTotalLength() / total;
      });
    }

    function measure() {
      const svg = path.ownerSVGElement;
      const box = svg.getBoundingClientRect();
      const w = Math.max(1, Math.round(box.width));
      const h = Math.max(1, Math.round(box.height));
      const cmds = splinePath(pointsFor(nodePoints(box), w, h));
      const d = cmds.join(" ");
      svg.setAttribute("viewBox", "0 0 " + w + " " + h);
      svg.querySelectorAll("path").forEach((el) => el.setAttribute("d", d));
      len = path.getTotalLength();
      path.style.setProperty("--len", len);
      measureNodes(cmds, len);
    }

    const nodeFrac = (i) =>
      (nodeAt[i] === undefined ? (i + 0.5) / rows.length : nodeAt[i]);

    /* The stats row is the line's destination. It fires ONCE, from the drawing
       progress rather than from an IntersectionObserver, so the cards answer
       when the head actually arrives rather than when they happen to be 40% on
       screen — which, scrolling quickly, was usually well before the line got
       anywhere near them. */
    const statsRow = document.querySelector("[data-about-stats]");
    let statsHit = false;
    function hitStats() {
      if (statsHit || !statsRow) return;
      statsHit = true;
      statsRow.classList.add("is-hit");
      runStatCountUp(statsRow);
    }

    /* MOBILE progress, derived from where the ROWS are rather than from the
       section's box.
       
       The previous attempt drove the two separately: the line still drew off
       the section's scroll position while the cards woke off their own
       position in the viewport. They inevitably drifted, and the visible result
       was a card appearing before the line had reached its circle (Ahmed,
       2026-08-24).
       
       So on mobile the progress is BUILT from the rows: it returns exactly the
       node fraction of the last row to pass the trigger, plus however far the
       next row has travelled toward it. The line's head therefore sits on the
       last lit circle by construction, and because the reveal test below is
       once again simply `d >= nodeFrac(i)`, a card cannot light before the line
       arrives — the two read the same number. */
    function mobileTarget() {
      const vh = window.innerHeight;
      // Measured on the row's CENTRE, not its top — and that distinction is the
      // whole thing. A node sits at its row's vertical centre, so triggering on
      // the row's TOP crossing the screen put the line's head half a card
      // LOWER than the trigger, i.e. at or past the bottom edge: the line was
      // technically drawing but every inch of its travel happened below the
      // fold (Ahmed, 2026-08-24: "I can't see the line traveling, it is way in
      // the bottom"). Keyed to the centre, the lit node lands at 0.55 of the
      // viewport — just above the middle, where it is plainly in view and the
      // stretch between two nodes draws across the screen as you scroll.
      const trigger = vh * 0.55;
      const mids = rows.map((r) => {
        const b = r.getBoundingClientRect();
        return b.top + b.height / 2;
      });
      const rowH = Math.max(1, rows[0].getBoundingClientRect().height);
      let last = -1;
      for (let i = 0; i < rows.length; i++) if (mids[i] < trigger) last = i;
      // Approaching the first node.
      if (last < 0) return nodeFrac(0) * clamp01((trigger + rowH - mids[0]) / rowH);
      // Past the last one: run the tail out to 1.
      if (last >= rows.length - 1) {
        const t = clamp01((trigger - mids[last]) / rowH);
        return nodeFrac(last) + (1 - nodeFrac(last)) * t;
      }
      const t = clamp01((trigger + rowH - mids[last + 1]) / rowH);
      return nodeFrac(last) + (nodeFrac(last + 1) - nodeFrac(last)) * t;
    }

    // Scroll position -> the raw progress the page is actually at.
    function readTarget() {
      if (window.innerWidth < 768) {
        target = clamp01(mobileTarget());
        kick();
        return;
      }
      const rect = body.getBoundingClientRect();
      const vh = window.innerHeight;
      // Span: from first-touch at the bottom edge to last-exit past the top.
      const span = Math.max(1, rect.height + vh);
      const p = clamp01((vh - rect.top) / span);
      // A short lead-in and run-out, so the line is not already drawing before
      // the heading is on screen and is fully drawn a little before the section
      // leaves — the last milestone should be readable while its dot is lit.
      target = clamp01((p - 0.12) / 0.66);
      kick();
    }

    // The drawn progress CHASES the scrolled progress rather than equalling it
    // (Ahmed, 2026-08-23: "smoother slightly slower ... like the framer site").
    //
    // Scrubbing an animation directly off scrollTop makes it exactly as smooth
    // as the input, and a wheel or a trackpad flick is not smooth - it arrives
    // in jumps, so the line jumps with it. Framer's scroll-linked animations do
    // not do that because they run the value through a spring: the target moves
    // instantly, the rendered value eases toward it over a few frames, and the
    // small lag is what reads as weight.
    //
    // This is that, as a critically-damped chase: each frame closes EASE of the
    // remaining distance, so it converges quickly without overshoot. Lower is
    // heavier and slower. It also means the animation keeps running for a few
    // frames AFTER the scroll stops, which is exactly the settle the reference
    // has and a direct scrub cannot.
    // Lower is heavier: each frame closes this much of the remaining distance,
    // so 0.06 lags further behind the wheel and settles more slowly than 0.085
    // did (Ahmed, 2026-08-23: "make the scroll ease a little"). This is the one
    // number to turn if the page feels floaty or snappy - both sections read it,
    // so they stay in step with each other whatever it is set to.
    const EASE = 0.06;
    const SNAP = 0.0004;   // close enough to land on, rather than chase forever

    function tick() {
      raf = 0;
      const diff = target - shown;
      if (Math.abs(diff) < SNAP) shown = target;
      else shown += diff * EASE;
      paint(shown);
      if (shown !== target) kick();
    }
    function kick() { if (!raf) raf = requestAnimationFrame(tick); }

    function paint(d) {
      path.style.setProperty("--draw", (1 - d).toFixed(4));

      rows.forEach((row, i) => {
        // ONE test on both breakpoints: the line arrives, the card follows.
        // What differs is where `d` comes from — see mobileTarget() — not how a
        // row decides it has been reached.
        row.classList.toggle("is-reached", d >= nodeFrac(i));
      });

      if (d >= 0.995) hitStats();

      if (head) {
        /* Only d <= 0 hides it now. It used to hide at d >= 1 as well, which
           is what made the head vanish exactly when it reached the end of its
           travel; the point is clamped to the path's length instead, so it
           parks on the final point and stays there. */
        if (d <= 0) {
          head.classList.remove("is-on");
        } else {
          const pt = path.getPointAtLength(len * Math.min(d, 1));
          const m = path.getScreenCTM();
          if (m) {
            const sp = new DOMPoint(pt.x, pt.y).matrixTransform(m);
            const host = body.getBoundingClientRect();
            head.style.left = (sp.x - host.left) + "px";
            head.style.top = (sp.y - host.top) + "px";
            head.classList.add("is-on");
          }
        }
      }
    }

    measure();
    window.addEventListener("scroll", readTarget, { passive: true });
    window.addEventListener("resize", () => { measure(); readTarget(); }, { passive: true });
    // Land on the real value for the first paint rather than easing up from
    // zero on load — a page opened part-way down should not animate itself in.
    readTarget();
    shown = target;
    paint(shown);
  }

  /* Contact hero parallax (Ahmed, 2026-08-25).

     The PHOTOGRAPH moves, the body does not — the body is ordinary document
     flow travelling at scroll speed, and the separation between the two is the
     whole effect. Rate is 0.28, i.e. the image drifts down at just over a
     quarter of the page's speed.

     Travel is bounded by the image's own overhang: it is 128% of the frame and
     starts 14% above it, so 14% of the frame height is available in either
     direction. Clamping to that is what guarantees no gap ever opens at an
     edge, whatever the viewport does. */
  function initContactParallax() {
    const img = document.querySelector("[data-contact-parallax]");
    if (!img) return;
    const hero = img.closest("[data-contact-hero]");
    if (!hero || reduceMotion()) return;
    let ticking = false;
    function frame() {
      ticking = false;
      const rect = hero.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;   // off screen: nothing to do
      const limit = rect.height * 0.14;
      const shift = Math.max(-limit, Math.min(limit, -rect.top * 0.28));
      img.style.transform = "translate3d(0," + shift.toFixed(1) + "px,0)";
    }
    function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule, { passive: true });
    frame();
  }

  /* The hero badge's ring turns with the scroll (Ahmed, 2026-08-25).

     Driven off scrollY rather than the badge's own position, so it keeps
     turning for the whole first screenful instead of stopping the moment the
     hero leaves — the badge is still on screen while the hero exits, and a ring
     that freezes mid-word looks broken. 0.12 deg per pixel is roughly one full
     turn per three screens: present, not a fidget spinner. */
  function initHeroBadge() {
    const badge = document.querySelector("[data-hero-badge]");
    if (!badge) return;
    const ring = badge.querySelector(".hero-badge__ring");
    if (!ring || reduceMotion()) return;
    let ticking = false;
    function frame() {
      ticking = false;
      ring.style.setProperty("--badge-spin", (window.scrollY * 0.12).toFixed(2) + "deg");
    }
    function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener("scroll", schedule, { passive: true });
    frame();
  }

  /* Slow parallax on the About hero art. Same guards as the journey: opt-out
     under reduced motion, no-op when the element is absent. */
  function initAboutParallax() {
    const img = document.querySelector("[data-about-parallax]");
    if (!img || reduceMotion()) return;
    const frame_ = img.parentElement;
    let ticking = false;
    function frame() {
      ticking = false;
      const r = frame_.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;   // off-screen
      // -1 (entering from below) .. 1 (leaving past the top)
      const p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
      img.style.transform = "translateY(" + (p * -26).toFixed(1) + "px) scale(1.12)";
    }
    function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule, { passive: true });
    frame();
  }

  /* Count-up for the About stats: runs once when each tile scrolls into view.
     Preserves whatever suffix/format the built value carries ("26", "100%"),
     so the markup stays the source of truth for what the number says. */
  /* The count itself, callable. Guarded by a flag per tile so the timeline can
     fire it without having to know whether it already ran. */
  function runStatCountUp(scope) {
    const tiles = [...(scope || document).querySelectorAll("[data-stat] [data-stat-value]")];
    tiles.forEach((el) => {
      if (el._counted) return;
      el._counted = true;
      const raw = el.getAttribute("data-stat-value") || el.textContent;
      const target = parseFloat(raw);
      if (!isFinite(target)) { el.textContent = raw; return; }
      const suffix = String(raw).replace(/^[\d.,]+/, "");
      const start = performance.now();
      const DUR = 900;
      (function step(now) {
        const t = Math.min(1, (now - start) / DUR);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (t < 1) requestAnimationFrame(step);
        else el.textContent = raw;
      })(start);
    });
  }

  function initStatCountUp() {
    const tiles = [...document.querySelectorAll("[data-stat] [data-stat-value]")];
    if (!tiles.length) return;
    if (reduceMotion() || !("IntersectionObserver" in window)) return;  // built values stand
    /* When the timeline is on the page it OWNS the trigger — the numbers run
       as the line's head reaches the cards. Leaving this observer attached as
       well would race it and usually win, which is the behaviour being
       replaced. */
    if (document.querySelector("[data-about-timeline]")) return;

    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        runStatCountUp(entry.target.closest("[data-stat]") || entry.target);
      });
    }, { threshold: 0.4 });
    tiles.forEach((el) => io.observe(el));
  }

  /* ---------------------------------------------------------------
     Blog post ?post=<slug> swap (Ahmed, 2026-08-20)

     The fork ships ONE static blog.html — there is no per-post routing and no
     CMS behind it. The index links each card as `blog.html?post=<slug>` and
     every post's copy is inlined in a #post-data JSON block, so clicking the
     third card reads the third post instead of always landing on the first.
     Falls back to the server-rendered first post when the slug is missing or
     unknown, so a bare blog.html (and any crawler) still sees a real article.
     --------------------------------------------------------------- */
  function initBlogPost() {
    const article = document.querySelector("[data-post-article]");
    const dataEl = document.getElementById("post-data");
    if (!article || !dataEl) return;
    const slug = new URLSearchParams(location.search).get("post");
    if (!slug) return;                        // bare blog.html: keep the built-in post
    let posts;
    try { posts = JSON.parse(dataEl.textContent); } catch (_e) { return; }
    const p = posts && posts[slug];
    if (!p) return;                           // unknown slug: leave the fallback post

    const set = (sel, html) => {
      const el = article.querySelector(sel);
      if (el) el.innerHTML = html;
    };
    set("[data-post-title]", esc(p.title));
    set("[data-post-meta]", esc(p.meta));
    set("[data-post-excerpt]", esc(p.excerpt));
    set("[data-post-tags]", (p.tags || []).map((t) =>
      '<span class="inline-flex items-center px-3 py-1 border border-heading ' +
      'rounded-full font-medium text-heading text-xs">' + esc(t) + "</span>").join(""));
    set("[data-post-body]", (p.body || []).map((par) =>
      '<p class="text-bodyInk text-base xl:text-lg leading-[1.9]">' + esc(par) + "</p>").join(""));
    set("[data-post-tips]", (p.tips || []).map((t) => "<li>" + esc(t) + "</li>").join(""));
    const img = article.querySelector("[data-post-image]");
    if (img && p.image) { img.src = p.image; img.alt = p.title || ""; }
    if (p.title) document.title = p.title + " | JAAD";
    // (The breadcrumb used to be updated here too. Breadcrumbs were removed
    // site-wide on 2026-08-20, so there is no trail left to keep in step.)
  }

  /* ---------------------------------------------------------------
     Icon concept swap (Ahmed, 2026-08-19; narrowed 2026-08-23)
     The Green/Orange toggle swaps the four PRODUCT-BENEFIT icons for a
     different metaphor per slot - leaf->select, bolt->cup, shield->serve,
     delivery->parcel - so the idea changes, not just the styling.

     It used to swap the fourteen account and tracker icons too, each to its
     own `*-3d--alt.png`. That pairing existed because the old set came in two
     rendered concepts; the clay set replacing it is ONE concept for the whole
     site ("clay all"), so there is no second version of a wallet or a map pin
     to swap to and those mappings are gone with the files. Both sides of the
     four that remain are clay, so the toggle changes the metaphor without
     changing the material.

     A MutationObserver re-applies to icons injected after load (drawer,
     recent rail).
     --------------------------------------------------------------- */
  const ICON_ALT = {
    "images/jaad/icons/spec-leaf.png": "images/jaad/icons/spec-select.png",
    "images/jaad/icons/spec-bolt.png": "images/jaad/icons/spec-cup.png",
    "images/jaad/icons/spec-shield.png": "images/jaad/icons/spec-serve.png",
    "images/jaad/icons/spec-delivery.png": "images/jaad/icons/spec-parcel.png",
  };
  const ICON_BASE = {};
  Object.keys(ICON_ALT).forEach((k) => { ICON_BASE[ICON_ALT[k]] = k; });
  function iconBaseOf(src) {
    if (!src) return null;
    if (ICON_ALT[src]) return src;         // already a base
    if (ICON_BASE[src]) return ICON_BASE[src]; // an alt → its base
    return null;
  }
  function applyIconConceptTo(img) {
    let base = img.getAttribute("data-icon-base");
    if (!base) {
      base = iconBaseOf(img.getAttribute("src"));
      if (!base) return;
      img.setAttribute("data-icon-base", base);
    }
    const want = document.documentElement.getAttribute("data-btn") === "v2" ? ICON_ALT[base] : base;
    if (img.getAttribute("src") !== want) img.setAttribute("src", want);
  }
  function applyIconConcepts(root) {
    (root || document).querySelectorAll("img").forEach(applyIconConceptTo);
  }
  function initIconConcepts() {
    applyIconConcepts();
    try {
      const obs = new MutationObserver((muts) => {
        muts.forEach((m) => m.addedNodes && m.addedNodes.forEach((n) => {
          if (n.nodeType !== 1) return;
          if (n.tagName === "IMG") applyIconConceptTo(n);
          else if (n.querySelectorAll) n.querySelectorAll("img").forEach(applyIconConceptTo);
        }));
      });
      obs.observe(document.body, { childList: true, subtree: true });
    } catch (e) { /* observer unsupported — toggle still swaps existing icons */ }
  }

  function initBtnStyleSwitch() {
    const BKEY = "jaad:btnstyle", IKEY = "jaad:imgstyle", FKEY = "jaad:flystyle";
    let btn = "v1", img = "scene", fly = "arc";
    try { btn = localStorage.getItem(BKEY) || "v1"; } catch (e) { /* ignore */ }
    try { img = localStorage.getItem(IKEY) || "scene"; } catch (e) { /* ignore */ }
    // Fly-to-cart is fixed to "drop" (Ahmed, 2026-08-19): its toggle row is
    // removed from the panel below, but the arc/comet code stays in place so the
    // toggle can be restored by re-adding the row. FKEY is left defined for that.
    fly = "drop";
    document.documentElement.setAttribute("data-btn", btn);
    document.documentElement.setAttribute("data-img", img);
    document.documentElement.setAttribute("data-fly", fly);
    applyImgStyle(img);
    if (document.querySelector("[data-btn-switch]")) return;
    const CKEY = "jaad:uiswitch-collapsed";
    let collapsed = false;
    try { collapsed = localStorage.getItem(CKEY) === "1"; } catch (e) { /* ignore */ }
    const el = document.createElement("div");
    el.className = "btnswitch" + (collapsed ? " is-collapsed" : "");
    el.setAttribute("data-btn-switch", "");
    el.innerHTML =
      // Collapsible header: click the whole bar to fold the panel down to just
      // this handle, so the dev toggles never sit over the design being reviewed.
      '<button type="button" class="btnswitch__head" data-btnswitch-collapse aria-expanded="' + (collapsed ? "false" : "true") + '">' +
        '<span class="btnswitch__title">UI controls</span>' +
        '<span class="btnswitch__chev" aria-hidden="true">▾</span>' +
      '</button>' +
      '<div class="btnswitch__body">' +
        '<div class="btnswitch__row">' +
          '<span class="btnswitch__lbl">Button style</span>' +
          '<div class="btnswitch__seg">' +
            '<button type="button" data-btn-v="v1"><span class="btnswitch__dot" style="background:#00451C"></span>Green</button>' +
            '<button type="button" data-btn-v="v2"><span class="btnswitch__dot" style="background:#EA983E"></span>Orange</button>' +
            '<button type="button" data-btn-v="v3"><span class="btnswitch__dot" style="background:#4A790C"></span>Moss</button>' +
          '</div>' +
        '</div>' +
        '<div class="btnswitch__row">' +
          '<span class="btnswitch__lbl">Product images</span>' +
          '<div class="btnswitch__seg">' +
            '<button type="button" data-img-v="scene"><span class="btnswitch__dot" style="background:#EA983E"></span>Scenes</button>' +
            '<button type="button" data-img-v="plain"><span class="btnswitch__dot" style="background:#fff;box-shadow:inset 0 0 0 1px #C1C3C6"></span>White</button>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(el);
    const paint = () => {
      el.querySelectorAll("[data-btn-v]").forEach((b) =>
        b.setAttribute("aria-pressed", b.getAttribute("data-btn-v") === btn ? "true" : "false"));
      el.querySelectorAll("[data-img-v]").forEach((b) =>
        b.setAttribute("aria-pressed", b.getAttribute("data-img-v") === img ? "true" : "false"));
      el.querySelectorAll("[data-fly-v]").forEach((b) =>
        b.setAttribute("aria-pressed", b.getAttribute("data-fly-v") === fly ? "true" : "false"));
    };
    paint();
    el.addEventListener("click", (e) => {
      const collapse = e.target.closest("[data-btnswitch-collapse]");
      if (collapse) {
        const nowCollapsed = el.classList.toggle("is-collapsed");
        collapse.setAttribute("aria-expanded", nowCollapsed ? "false" : "true");
        try { localStorage.setItem(CKEY, nowCollapsed ? "1" : "0"); } catch (err) { /* ignore */ }
        return;
      }
      const bb = e.target.closest("[data-btn-v]");
      if (bb) {
        btn = bb.getAttribute("data-btn-v");
        document.documentElement.setAttribute("data-btn", btn);
        try { localStorage.setItem(BKEY, btn); } catch (err) { /* ignore */ }
        applyIconConcepts();   // swap every 3D icon to the chosen concept
        paint();
        return;
      }
      const ib = e.target.closest("[data-img-v]");
      if (ib) {
        img = ib.getAttribute("data-img-v");
        document.documentElement.setAttribute("data-img", img);
        try { localStorage.setItem(IKEY, img); } catch (err) { /* ignore */ }
        applyImgStyle(img);
        paint();
        return;
      }
      const fb = e.target.closest("[data-fly-v]");
      if (fb) {
        fly = fb.getAttribute("data-fly-v");
        document.documentElement.setAttribute("data-fly", fly);
        try { localStorage.setItem(FKEY, fly); } catch (err) { /* ignore */ }
        paint();
      }
    });
  }

  /* ---------------------------------------------------------------
     Payment method — reveal the card form, and format what is typed into it

     ⚠️ PROTOTYPE. These fields are a mock-up of a gateway screen; the real
     one has to be the provider's hosted fields or iframe, so a card number
     never lands in a Jaad-served input. See build/pages/payment.py's module
     docstring. Nothing here validates, transmits or stores anything — it only
     spaces the digits so the field is readable while the flow is reviewed.

     The reveal is driven off the radios rather than CSS `:has()` so it also
     fires for syncGiftRules(), which can move the selection off a blocked row
     programmatically — a `change` event the radios do not emit on their own,
     hence the explicit call at the end.
     --------------------------------------------------------------- */
  function initPaymentMethod() {
    const box = document.querySelector("[data-card-fields]");
    if (!box) return;
    const radios = [...document.querySelectorAll('input[name="payment-method"]')];

    function sync() {
      const picked = radios.find((r) => r.checked);
      const isCard = !!picked && picked.value === "card";
      box.hidden = !isCard;
      // A hidden fieldset must not be submitted or tabbed into.
      box.querySelectorAll("input").forEach((i) => (i.disabled = !isCard));
    }
    radios.forEach((r) => r.addEventListener("change", sync));

    /* Group the number in fours as it is typed. The caret is put back at the
       end rather than preserved mid-string: this runs on `input`, and a naive
       reformat otherwise throws the caret to position 0 on every keystroke. */
    const num = box.querySelector("[data-card-number]");
    if (num) {
      num.addEventListener("input", () => {
        const digits = num.value.replace(/\D/g, "").slice(0, 16);
        num.value = digits.replace(/(.{4})/g, "$1 ").trim();
      });
    }
    /* MM/YY — the slash is inserted, never typed. */
    const exp = box.querySelector("[data-card-expiry]");
    if (exp) {
      exp.addEventListener("input", () => {
        const digits = exp.value.replace(/\D/g, "").slice(0, 4);
        exp.value = digits.length > 2 ? digits.slice(0, 2) + "/" + digits.slice(2) : digits;
      });
    }
    const cvv = box.querySelector("#card-cvv");
    if (cvv) {
      cvv.addEventListener("input", () => {
        cvv.value = cvv.value.replace(/\D/g, "").slice(0, 4);
      });
    }
    sync();
  }

  /* ---------------------------------------------------------------
     Order-placed celebration (thank-you page)

     `celebrate()` above is the small twelve-dot beat that marks a discount on
     a cart. Placing an order is the one genuinely big moment in the whole
     flow, and the page marked it with a green tick and nothing else (Ahmed,
     2026-08-23) — so this is the larger sibling: a short confetti fall across
     the width of the page, plus a pop on the tick itself.

     Deliberately still restrained, and it obeys the same three rules as every
     other bit of motion here:
       * it runs ONCE, on arrival, and never again — no loop to sit under
         someone reading their order number;
       * it is `position: fixed` under a `pointer-events: none` wrapper, so no
         ancestor's overflow clips it and nothing it drops can swallow a click;
       * reduced motion (or a browser without Element.animate) skips it
         entirely. The tick and the "تم تقديم طلبك بنجاح" line are the real
         confirmation; this only dresses them.
     --------------------------------------------------------------- */
  function initOrderCelebration() {
    const host = document.querySelector("[data-order-celebrate]");
    if (!host) return;
    const badge = host.querySelector("[data-order-check]");
    if (badge) pulse(badge);
    if (reduceMotion() || !document.body.animate) return;

    const wrap = document.createElement("div");
    wrap.setAttribute("aria-hidden", "true");
    wrap.style.cssText =
      "position:fixed;inset:0;z-index:60;pointer-events:none;overflow:hidden";
    // Brand greens + the lime and cream that already carry "good news" here.
    const colors = ["#006328", "#618F2B", "#8ACC3E", "#98CA55", "#EA983E", "#FDF8F1"];
    const N = 44;
    for (let i = 0; i < N; i++) {
      const bit = document.createElement("span");
      const round = i % 3 === 0;
      const w = round ? 8 : 6 + Math.random() * 5;
      const h = round ? 8 : 10 + Math.random() * 6;
      bit.style.cssText =
        "position:absolute;top:-24px;left:" + (Math.random() * 100).toFixed(2) + "%;" +
        "width:" + w.toFixed(1) + "px;height:" + h.toFixed(1) + "px;" +
        "border-radius:" + (round ? "9999px" : "2px") + ";" +
        "background:" + colors[i % colors.length] + ";opacity:0";
      wrap.appendChild(bit);
      const drift = (Math.random() - 0.5) * 220;
      const spin = 360 + Math.random() * 720;
      bit.animate(
        [
          { transform: "translate3d(0,0,0) rotate(0deg)", opacity: 0 },
          { transform: "translate3d(" + drift * 0.3 + "px, 12vh, 0) rotate(" + spin * 0.25 + "deg)", opacity: 1, offset: 0.12 },
          { transform: "translate3d(" + drift + "px, 104vh, 0) rotate(" + spin + "deg)", opacity: 1, offset: 0.92 },
          { transform: "translate3d(" + drift + "px, 112vh, 0) rotate(" + spin + "deg)", opacity: 0 },
        ],
        {
          duration: 2600 + Math.random() * 1400,
          delay: Math.random() * 700,
          easing: "cubic-bezier(0.25, 0.6, 0.45, 1)",
          fill: "forwards",
        },
      );
    }
    document.body.appendChild(wrap);
    // Longest possible piece (delay + duration) plus a little slack.
    setTimeout(() => wrap.remove(), 5000);
  }

  /* ---------------------------------------------------------------
     Order tracker — the demo cycle

     ⚠️ REVIEW BEHAVIOUR, not product behaviour. A real tracker moves when the
     order moves; this one walks the four stages on a timer so the whole
     progression can be seen without placing four orders (Ahmed, 2026-08-23:
     "make it go through the 4 states as a test"). It only runs on trackers
     built with `demo=True` — see DEMO_TRACKER in build/pages/_account.py, which
     is the one switch to flip when real order state arrives.

     It repaints CLASSES and CUSTOM PROPERTIES on the existing nodes rather than
     re-rendering the tracker: every node already ships its check badge and the
     courier already ships on every tracker, precisely so a stage change is a
     class toggle and nothing animating is thrown away mid-transition.

     The percentage formulas mirror `_ride_style()` in _account.py. They are
     four lines of arithmetic in two places, which is worth one comment each
     rather than a runtime round-trip; if the stage count ever stops being four,
     both read it from the node count.
     --------------------------------------------------------------- */
  const RIDE_DEMO_MS = 3200;   // per stage
  const RIDE_HOLD_MS = 4200;   // longer pause on "delivered" before looping

  function paintOrderRide(root, step) {
    const nodes = [...root.querySelectorAll(".order-ride__node")];
    const n = nodes.length;
    if (!n) return;
    const last = n - 1;
    const at = Math.max(0, Math.min(step, last));
    const delivered = at >= last;

    nodes.forEach((node, i) => {
      const done = i < at || (delivered && i === last);
      const now = i === at && !delivered;
      node.classList.toggle("is-done", done);
      node.classList.toggle("is-now", now);
      node.classList.toggle("is-todo", !done && !now);
    });

    root.classList.toggle("is-delivered", delivered);
    // The courier rides one leg only: "in transit" -> "delivered".
    root.classList.toggle("is-transit", at === last - 1);
    root.style.setProperty("--fillto", ((last ? at / last : 0) * 100).toFixed(3) + "%");
    root.dataset.rideStep = String(at);
  }

  function initOrderRideDemo() {
    const rides = [...document.querySelectorAll("[data-ride-demo]")];
    if (!rides.length) return;
    // One timer for all of them, so several trackers on a page (the dashboard
    // card and the order drawer) stay in step instead of drifting apart.
    let step = parseInt(rides[0].dataset.rideStep, 10);
    if (!isFinite(step)) step = 0;
    const last = (rides[0].querySelectorAll(".order-ride__node").length || 4) - 1;

    const tick = () => {
      step = step >= last ? 0 : step + 1;
      rides.forEach((r) => paintOrderRide(r, step));
      window.setTimeout(tick, step >= last ? RIDE_HOLD_MS : RIDE_DEMO_MS);
    };
    window.setTimeout(tick, RIDE_DEMO_MS);
  }

  function boot() {
    initBtnStyleSwitch();
    const header = document.getElementById("site-header");
    const footer = document.getElementById("site-footer");
    if (header) header.innerHTML = headerHTML();
    if (footer) footer.innerHTML = footerHTML();

    const overlays = document.createElement("div");
    overlays.id = "site-overlays";
    overlays.innerHTML = overlaysHTML();
    document.body.appendChild(overlays);

    initDelegation();
    initStickyNav();
    initMegaMenu();
    initFlashCountdown();
    initSearch();
    initLangSwitcher();
    initCartUI();
    syncWalletBalance();
    initAuthUI();
    initFavsUI();
    // Reads/writes localStorage only — no fetch — so it can safely run
    // before applyLangToContent() and window.kInit() below, which need the
    // rail's cards (if any) already in the DOM to translate and reveal them.
    initRecentlyViewed();
    initLeafWind();
    initOrderNotes();
    initReferralCopy();
    initAddresses();
    initPointsRedeem();
    initVouchers();
    initOrders();
    initReorder();
    // No-op off the payment page (guards on [data-card-fields]).
    initPaymentMethod();
    // Must run after the chrome is in the DOM and after initFavsUI, so the
    // dictionary pass sees every string on the page. Without this call a
    // stored English preference only styled the chrome.
    applyLangToContent();
    window.kInit(document);
    // Once per page, after the buy block and its host are in the DOM. Guards
    // itself off [data-sticky-buybar], so it is a no-op everywhere but product.
    initStickyBuyBar();

    // White-mode scroll story — guards off [data-story], so it is a no-op
    // everywhere but the story product page.
    initProductStory();

    // Blog post ?post=<slug> swap — no-op off the post page.
    initBlogPost();

    // Confetti on arrival at the thank-you page; no-op everywhere else
    // (guards on [data-order-celebrate]).
    initOrderCelebration();

    // Demo-only: walk the order tracker through its four stages. No-op
    // wherever no tracker carries [data-ride-demo].
    initOrderRideDemo();

    // About page: pinned scroll journey, hero parallax, stat count-up. Each
    // guards off its own markup, so all three are no-ops elsewhere.
    initAboutJourney();
    initHeroBadge();
    initContactParallax();
    initAboutTimeline();
    initAboutParallax();
    initStatCountUp();

    // Swap every 3D icon to the concept that matches the current toggle, and
    // keep watching for icons injected later (drawer, recent rail).
    initIconConcepts();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
