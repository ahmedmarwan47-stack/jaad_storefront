/*
 * tailwind.config.js — JAAD design system.
 *
 * Forked from the Abu Auf build (same architecture: build-time Tailwind CLI,
 * scanning generated HTML + scripts.js + build/**​/*.py). Structural tokens
 * (screens, container, shadows, radii, type scale) are carried over verbatim
 * from Abu Auf as a starting point — they are NOT yet verified against Jaad's
 * own Figma variables (no `get_variable_defs` pass has been run on the Jaad
 * file). Treat the type scale and shadow/radius values as provisional until
 * checked against Jaad's Figma.
 *
 * COLOR TOKENS below are re-pointed to Jaad's brand manual (2026), which is
 * authoritative for exactly five values:
 *   #006328  primary dark green   — chrome, CTAs, brand surfaces
 *   #8ACC3E  lime                 — badges, success, secondary accent
 *   #F7931E  orange               — sale/highlight ONLY (locked decision:
 *                                    "green-led, orange sparingly")
 *   #FDF8F1  cream                — backgrounds, soft sections
 *   #000000 / #FFFFFF             — black / white
 * Every other shade below (the 50–900 ramps, hover/dark variants,
 * accessibility tokens) is COMPUTED from those five anchors — tint/shade
 * interpolation plus WCAG 2.1 contrast checks, not hand-picked, not a Figma
 * variable (Jaad has none exported yet). Recomputation script + contrast
 * checks were run 2026-08-17; see git history for the derivation if these
 * ever need to be redone against a future Figma variables export.
 *
 * CONTRAST FINDING — white text on the orange token fails WCAG AA (2.3:1).
 * Any orange surface (badges, sale chips, the orange CTA block) MUST use
 * dark/black text, never white. Black-on-orange clears 9.15:1.
 *
 * CONTENT SCANNING — same rule as Abu Auf: Tailwind only emits a class it can
 * SEE as a literal string. Three sources matter and all three must stay
 * listed:
 *   1. static-export/*.html   the generated pages
 *   2. static-export/scripts.js  header, footer, cart, search, overlays —
 *      all injected at runtime from template literals in this file
 *   3. build/**​/*.py         the source of that markup
 * Never build a class name by concatenation — the scanner cannot see it.
 *
 * FONTS: Almarai (Arabic, Google Fonts) replaces Baloo Bhaijaan 2. Aeonik
 * (Latin, licensed — self-hosted from build/tailwind/fonts/) replaces Inter.
 *
 * RTL: same as Abu Auf — logical-property utilities (ms/me/ps/pe/start/end),
 * no plugin required.
 *
 * ─────────────────────────────────────────────────────────────────────────
 * JAAD TOKEN MAP (brand manual 2026)
 *
 * CANONICAL brand tokens — prefer these in all NEW markup:
 *   primary        #006328  primary green (full 50–900 scale; DEFAULT/600)
 *   primary.hover  #00451C   ·  primary.900 #003616 (deepest)
 *   cta            #00451C  dark-green CTA button, hover #006328
 *   lime           #8ACC3E  secondary accent / success / badges
 *   orange         #F7931E  sale/highlight ONLY — DARK text (white fails, 2.3:1)
 *   highlight      #EA983E  warm orange accent variant
 *   cream          #FDF8F1  backgrounds / soft sections
 *   ink            #003616 / #00451C  deepest greens (text on cream, chrome)
 *   divider        #D9D9D9  hairlines / separators
 *
 * RADIUS scale (named): pill (9999px) · card (16px) · panel (20px).
 * SHADOW scale: function-named tokens under boxShadow (cart-*, custom*, …).
 *
 * LEGACY Abu-Auf names are KEPT as ALIASES — they are still referenced across
 * the generated markup, scripts.js and build/**​/*.py, so deleting them breaks
 * the build. Each is tagged inline `// legacy Abu-Auf alias -> JAAD <name>`
 * and resolves to a canonical value above; NO legacy value has been changed.
 * A future pass can rename usages to the canonical tokens, then drop the
 * aliases. Notable mappings:
 *   accent.yellow / accent.green -> lime      interaction.base        -> cream
 *   beige / neutral.cream        -> cream      neutral.divider         -> divider
 *   interaction.primary          -> cta        neutral.secondary       -> gray
 *   primaryColor/primaryDark/…   -> primary/ink   offWhite/lightBlue/…  -> cream
 * ─────────────────────────────────────────────────────────────────────────
 */
module.exports = {
  content: [
    "./static-export/**/*.html",
    "./static-export/scripts.js",
    "./build/**/*.py",
  ],
  theme: {
    screens: {
      xs: "414px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
    container: {
      screens: {
        sm: "100%",
        md: "100%",
        lg: "1024px",
        xl: "1280px",
      },
    },
    extend: {
      fontFamily: {
        // Arabic-first: the default sans IS the Arabic face.
        sans: ["Almarai", "system-ui", "sans-serif"],
        arabic: ["Almarai", "sans-serif"],
        latin: ["Aeonik", "system-ui", "sans-serif"],
        Aeonik: ["Aeonik", "system-ui", "sans-serif"],
        // Back-compat aliases so any page not yet rebuilt still renders in-brand.
        Inter: ["Aeonik", "system-ui", "sans-serif"],
        DM_Sans: ["Almarai", "sans-serif"],
        Caveat: ["Almarai", "sans-serif"],
      },
      animation: {
        customBounce: "customBounce 3s ease-in-out infinite",
        "spin-slow": "spin 3s linear infinite",
        slideDown: "slideDown 0.35s ease-out forwards",
      },
      keyframes: {
        slideDown: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(0)" },
        },
        customBounce: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10%)" },
        },
      },
      colors: {
        /* ============================================================
         * JAAD CANONICAL TOKENS (brand manual 2026) — clean names.
         * Authoritative brand colors; prefer these in NEW markup. The
         * legacy Abu-Auf names further down alias INTO these values.
         * ============================================================ */
        cream: "#FDF8F1", // JAAD cream — page/section backgrounds
        orange: "#F7931E", // JAAD orange — sale/highlight ONLY, DARK text
        highlight: "#EA983E", // JAAD highlight — warm orange accent variant
        divider: "#D9D9D9", // JAAD divider — hairlines / separators
        ink: {
          // JAAD ink — deepest greens for text on cream & chrome.
          DEFAULT: "#003616", // = primary.900
          800: "#00451C", // = primary.800 / cta
        },

        /* ---- FIGMA-AUTHORITATIVE tokens (Ahmed, 2026-08-20) --------------
         * Pulled from the Jaad Figma via `get_variable_defs` — these are the
         * REAL design variables, unlike the ramps above, which this config
         * COMPUTED from the printed brand manual before the Figma file was
         * available. Where the two disagree, Figma wins.
         *
         * `heading` (#29612F) is the one that matters: Figma's Primary/Dark
         * Green, used for headings, the hero CTA, the header bar and section
         * titles. The homepage/product/blog pages already use it as a literal;
         * the older inner pages still use ink #003616 for the same job, which
         * is the site's one remaining visual split. New markup: use these.
         * ----------------------------------------------------------------- */
        heading: "#29612F", // Figma Primary/Dark Green — headings, section titles
        limeFigma: "#98CA55", // Figma Primary/Green — badges, chips, top strip
        greenDeep: "#006328", // second, deeper green — price badge, add-to-cart

        /* ---- JAAD core brand ------------------------------------------- */
        // Primary/Green — masthead, brand surfaces, section bands.
        // DEFAULT/600 = the manual's exact #006328.
        primary: {
          DEFAULT: "#006328",
          light: "#FDF8F1",
          hover: "#00451C",
          50: "#F0F6F2",
          100: "#DBE9E1",
          200: "#B2D0BE",
          300: "#85B498",
          400: "#4C9268",
          500: "#1A733E",
          600: "#006328",
          700: "#005422",
          800: "#00451C",
          900: "#003616",
        },
        // Interaction/Primary CTA — buttons. Hover resolves LIGHTER (same
        // pattern as Abu Auf): DEFAULT is the deep shade, hover eases toward
        // the manual's exact primary.
        // JAAD cta (CANONICAL) — dark-green button, hover eases to primary.
        // Kept name; legacy Abu-Auf markup also references it. values: ink/cream.
        cta: { DEFAULT: "#00451C", hover: "#006328", light: "#FDF8F1" },
        // Accent — orange, per the locked "green-led, orange sparingly"
        // decision. Reserve for sale/highlight pops only. TEXT ON ORANGE
        // MUST BE DARK — white fails contrast here (2.3:1).
        accent: {
          DEFAULT: "#F7931E",
          orange: "#F7931E",
          error: "#A8200D",
          // Repurposed "accent green" bucket -> lime, Jaad's actual second
          // brand color (Abu Auf used a distinct yellow here; Jaad has none).
          green: "#8ACC3E", // legacy Abu-Auf alias -> JAAD lime
          // `accent-yellow` is Abu Auf's general highlight class (price
          // badges, points balance, small tags — 21 call sites in the
          // inherited markup, NOT sale-specific). Re-pointed at lime rather
          // than orange: orange is reserved for sale/highlight pops only
          // (locked decision), and painting 21 everyday UI elements orange
          // would break that. Lime already clears 10.79:1 with dark text.
          yellow: "#8ACC3E", // legacy Abu-Auf alias -> JAAD lime
          50: "#FFF9F2",
          100: "#FEF0E0",
          200: "#FDDFBC",
          300: "#FBCB93",
          400: "#F9B362",
          500: "#F89E34",
          600: "#F7931E",
          700: "#D27D1A",
          800: "#AD6715",
          900: "#885110",
        },
        // Primary/Beige — hero and soft section backgrounds. Jaad's manual
        // specifies one cream tone (not a separate beige+cream pair like Abu
        // Auf) — both `beige` and `neutral.cream` below point at it until a
        // distinct wash value is specified.
        beige: {
          // legacy Abu-Auf alias -> JAAD cream
          DEFAULT: "#FDF8F1",
          50: "#FFFFFE",
          100: "#FFFEFD",
          200: "#FEFDFB",
          300: "#FEFCF8",
          400: "#FEFAF5",
          500: "#FDF9F2",
          600: "#FDF8F1",
          700: "#D7D3CD",
          800: "#B1AEA9",
          900: "#8B8885",
        },
        // Lime — badges, success states, secondary accent. Black text on
        // lime clears 10.79:1; this bucket is safe for dark text at any shade.
        lime: {
          DEFAULT: "#8ACC3E",
          50: "#F8FCF3",
          100: "#EFF8E4",
          200: "#DCF0C5",
          300: "#C7E7A2",
          400: "#ADDB78",
          500: "#96D151",
          600: "#8ACC3E",
          700: "#75AD35",
          800: "#618F2B",
          900: "#4C7022",
        },

        /* ---- Shared system tokens ---------------------------------------
           Generic UI grays/dividers — not brand hues, carried over from Abu
           Auf as-is; they were already neutral, not tuned to its palette. */
        interaction: {
          primary: "#00451C", // legacy Abu-Auf alias -> JAAD cta / ink
          hover: "#006328", // legacy Abu-Auf alias -> JAAD primary
          tertiary: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
          "tertiary-hover": "#E9ECE1",
          base: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
          divider: "#D9D9D9", // legacy Abu-Auf alias -> JAAD divider
          outline: "#868685",
          disabled: "#C6C6C6",
          "secondary-text": "#5F5F5F",
        },
        neutral: {
          black: "#000000",
          white: "#FFFFFF",
          beige: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
          cream: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
          divider: "#D9D9D9", // legacy Abu-Auf alias -> JAAD divider
          outline: "#868685",
          disabled: "#C6C6C6",
          // Same contrast fix as Abu Auf (#777777 failed 4.5:1 on white/beige) —
          // this token is a gray-on-light-surface fix, independent of brand hue.
          secondary: "#5F5F5F", // legacy Abu-Auf alias -> JAAD gray (neutral, not brand)
          50: "#f9f9f9",
          100: "#f3f3f3",
          200: "#e5e5e5",
          300: "#d7d7d7",
          400: "#c9c9c9",
          500: "#bbbbbb",
          600: "#868685",
          700: "#777777",
          800: "#5a5a5a",
          900: "#3d3d3d",
        },
        gray: {
          100: "#f3f3f3",
          200: "#e5e5e5",
          300: "#D6D7D9",
          400: "#c9c9c9",
          500: "#bbbbbb",
          550: "#6E727B",
          600: "#868685",
          700: "#787878",
        },
        // Secondary green ramp (Abu Auf kept a parallel "green" bucket
        // aliasing its own primary shades — mirrored here on Jaad's primary).
        // legacy Abu-Auf alias -> JAAD primary
        green: {
          100: "#DBE9E1",
          200: "#B2D0BE",
          300: "#85B498",
          400: "#4C9268",
          500: "#1A733E",
          600: "#006328",
          700: "#005422",
          800: "#00451C",
          900: "#003616",
        },

        /* ---- Egypt flag (locale switcher) -------------------------------
           Not a brand color — the literal Egyptian flag palette, unchanged. */
        flag: {
          white: "#FFFFFF",
          green: "#005B13",
          black: "#000000",
          amber: "#CC9500",
          red: "#F0263C",
        },

        /* ---- Accessibility tokens ----------------------------------------
           Flat names on purpose (see Abu Auf's note on nested-hyphen keys).
           Verified against WCAG 2.1 AA by computed contrast ratio, 2026-08-17. */
        // Light text legible on the dark green footer/#006328 surfaces — lime
        // tinted 25% toward white clears 4.54:1 (plain lime is ~3.4:1, fails).
        onDarkGreen: "#A7D96E",
        // Muted text on a BLACK bar — carried over from Abu Auf's fix
        // (#949494, 6.92:1); generic gray-on-black, not brand-tuned.
        onBlack: "#949494",
        // Text on cream needs no separate muted token — primary green itself
        // clears 7.06:1 on #FDF8F1, unlike Abu Auf's beige which needed one.
        onBeigeMuted: "#006328",

        /* ---- Semantic / legacy aliases ----------------------------------
           Kept for any markup not yet rebuilt against the new token names.
           Every name below is a legacy Abu-Auf alias -> a JAAD canonical
           value (mapping noted inline). No value changed; rename later. */
        success: "#618F2B", // legacy Abu-Auf alias -> JAAD lime.800
        border: { light: "#D6D7D9" }, // legacy Abu-Auf alias -> gray.300 (neutral)
        primaryDark: "#00451C", // legacy Abu-Auf alias -> JAAD ink.800 / cta
        primaryExtraDark: "#003616", // legacy Abu-Auf alias -> JAAD ink
        primaryColor: "#006328", // legacy Abu-Auf alias -> JAAD primary
        primaryLight: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
        offWhite: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
        // Sale/discount badge — Jaad's rule reserves orange for exactly this,
        // unlike Abu Auf's generic red. Badge TEXT must be dark (see note above).
        cardbadgecolor: "#F7931E", // legacy Abu-Auf alias -> JAAD orange
        bordercolor: "#868685", // legacy Abu-Auf alias -> neutral.outline
        black900: "#00000090", // legacy Abu-Auf alias -> black @ 56% (overlay)
        textSecondary: "#2C3340", // legacy Abu-Auf alias -> neutral (slate text)
        primaryText: "#969696", // legacy Abu-Auf alias -> neutral (muted text)
        secondaryText: "#757575", // legacy Abu-Auf alias -> neutral (muted text)
        blackText: "#2b2525", // legacy Abu-Auf alias -> neutral (near-black text)
        customGray: "#EAEBEC", // legacy Abu-Auf alias -> neutral (light gray)
        customGrayMedium: "#979BA0", // legacy Abu-Auf alias -> neutral (mid gray)
        ctaBackground: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
        dividerText: "#C1C3C6", // legacy Abu-Auf alias -> divider (muted)
        lightBlue: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
        backgroundLocationBar: "#FDF8F1", // legacy Abu-Auf alias -> JAAD cream
      },
      /* ---- JAAD shadow scale (named tokens) --------------------------
         Function-named elevations carried over from Abu Auf; the green-tinted
         cart-* shadows already read as JAAD (rgba/#hex based on primary green).
         Kept as-is — no values changed. */
      boxShadow: {
        "cart-utility-box": "0px 0px 2px 1px #00000014",
        custom2: "0px 2px 3px rgba(0, 69, 28, 0.2)",
        custom3: "0px 0px 8px rgba(0, 0, 0, 0.16)",
        custom4: "0px 0px 6px rgba(0, 0, 0, 0.1)",
        "custom-5": "0px 2px 6px 0px #00000014",
        "cart-overview": "0px -2px 12px 0px #0063281f",
        "cart-btn": "0px 5px 10px 0px #0063284d",
        defaultSwitcher:
          "0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)",
        "location-btn": "0px 1px 2px rgba(0, 0, 0, 0.05)",
        "search-btn": "0px 1px 2px rgba(0, 0, 0, 0.05)",
      },
      scale: { flip: "-1" },
      borderRadius: {
        DEFAULT: "0.25rem",
        sm: "0.125rem",
        md: "0.375rem",
        lg: "0.5rem",
        xl: "0.75rem",
        "2xl": "22px",
        "3xl": "32px",
        full: "9999px",
        custom: "10px",
        /* ---- JAAD radius scale (brand manual 2026) ------------------- */
        pill: "9999px", // JAAD radius — pill / fully rounded (buttons, chips)
        card: "16px", // JAAD radius — 16px (cards, inputs, 16px button variant)
        panel: "20px", // JAAD radius — 20px (panels, larger surfaces)
      },
      /*
       * Type scale — carried over from Abu Auf's Figma-derived ramp as a
       * starting point. NOT yet verified against Jaad's own Figma variables.
       */
      fontSize: {
        "2xs": ["10px", "16px"],
        xs: ["12px", "18px"],
        sm: ["14px", "20px"],
        base: ["16px", "22px"],
        lg: ["18px", "26px"],
        xl: ["20px", "28px"],
        "2xl": ["24px", "36px"],
        "3xl": ["32px", "42px"],
        "4xl": ["36px", "48px"],
        "5xl": ["48px", "64px"],
        "6xl": ["60px", "72px"],
        "7xl": ["96px", "112px"],
      },
    },
  },
};
