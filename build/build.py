#!/usr/bin/env python3
"""
Build the Jaad static export.

    python3 build/build.py            # build every page
    python3 build/build.py home shop  # build only these

Each module in build/pages/ exposes SLUG (output filename) and build() ->
HTML string. Shared markup lives in build/components.py, shared data access in
build/catalog.py — edit either and every page picks the change up on the next
run. Runtime chrome (header, footer, overlays) and design tokens live in
static-export/scripts.js and tw-config.js and need no rebuild at all.
"""
import importlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORT = os.path.join(ROOT, "static-export")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "pages"))

# Page modules, in build order.
PAGES = [
    # commerce
    "home", "shop", "shop_category", "product", "cart", "checkout", "payment", "thank_you",
    # auth
    "login", "register", "verify", "forget_password", "reset_password",
    # account
    "my_account", "my_account_orders", "my_account_order",
    "my_account_favorites", "my_account_addresses", "my_account_wallet",
    "my_account_vouchers", "my_account_point", "my_account_profile",
    # content
    "about", "contact_us", "faqs", "blogs", "blog",
    "rewards",
    # "export" dropped (Ahmed, 2026-08-17): that page was explicitly
    # "scraped verbatim" from Abu Auf's real live export page — every
    # string and image on it was their content, not Jaad's. Nothing links
    # to it anymore (removed from nav/home already); the file is still in
    # build/pages/export.py if a real Jaad export program ever needs it.
    # legal
    "privacy_policy", "terms_conditions", "return_policy",
    # misc
    "store_closed",
]


def check_assets(name, html):
    """Fail loudly on a reference to a file that isn't in the export."""
    missing = []
    for src in set(re.findall(r'(?:src|srcset|href)="([^"]+)"', html)):
        if src.startswith(("http", "data:", "#", "mailto:", "tel:")):
            continue
        # A URL fragment or query is not part of the file path — shop.html#slug
        # is a link to shop.html (the nav uses exactly this form to open the
        # listing pre-filtered by category). Resolve the file part alone, or the
        # whole "file.html#slug" string is read as a filename that never exists.
        path = src.split("#", 1)[0].split("?", 1)[0]
        if not path or path.endswith((".html", ".css", ".js")):
            continue
        if not os.path.exists(os.path.join(EXPORT, path)):
            missing.append(path)
    for m in sorted(missing):
        print(f"    ! missing asset: {m}")
    return len(missing)


def build_tailwind(partial=False):
    """
    Compile static-export/tailwind.css from the markup we just wrote.

    Runs LAST on purpose: Tailwind only emits classes it can see, and the
    pages it scans are the ones this script has just generated. Run it first
    and a class added this build would be missing from the stylesheet until
    someone happened to build twice.

    Returns truthy on failure, and the caller makes that a non-zero exit. A
    silent skip is the one outcome to avoid — the CSS would simply be stale,
    every newly-added utility would do nothing, and the page would look
    subtly wrong with no error anywhere. That is the same class of silent
    failure as the missing-asset check this build already guards against.
    """
    if partial:
        # A single-page rebuild scans the whole site anyway, so this is safe
        # to skip; say so rather than implying the CSS is current.
        print("\n  tailwind: skipped (partial build) — run `npm run css`")
        return 0

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(os.path.join(root, "node_modules", "tailwindcss")):
        print("\n  ! tailwind: node_modules/tailwindcss missing — run `npm install`")
        return 1
    try:
        res = subprocess.run(
            ["npm", "run", "--silent", "css"],
            cwd=root, capture_output=True, text=True, timeout=180,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"\n  ! tailwind: could not run npm ({exc})")
        return 1
    if res.returncode != 0:
        print("\n  ! tailwind build FAILED:")
        for line in (res.stderr or res.stdout).strip().splitlines()[-8:]:
            print("      " + line)
        return 1
    css_path = os.path.join(root, "static-export", "tailwind.css")
    size = os.path.getsize(css_path) if os.path.exists(css_path) else 0
    if size < 5000:
        print(f"\n  ! tailwind: output implausibly small ({size} bytes)")
        return 1
    print(f"\n  tailwind.css {size:>28,} bytes   ok")
    return 0


def check_runtime_js():
    """
    Catch backticks inside the HTML comments in scripts.js.

    Nearly all of that file's markup lives in template literals, so a stray
    backtick in a comment silently ENDS the string and turns the rest of the
    markup into expressions. The failure is brutal and non-obvious: the whole
    header renders empty, and because it throws inside a function called
    during boot, nothing reaches the console unless you go looking.

    This has bitten twice — once on `px-4 xl:px-20`, once on `.mega-cat`.
    `node --check` does NOT catch it: the result is still valid JavaScript,
    just not the JavaScript anyone meant. Hence a build-time check.
    """
    path = os.path.join(EXPORT, "scripts.js")
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as f:
        src = f.read()
    bad = []
    for m in re.finditer(r"<!--.*?-->", src, re.S):
        if "`" in m.group(0):
            bad.append((src[:m.start()].count("\n") + 1, m.group(0)[:60].replace("\n", " ")))
    for line, snippet in bad:
        print(f"    ! backtick inside an HTML comment at scripts.js:{line} -> {snippet}...")
    return len(bad)


def main(only=None):
    targets = [p for p in PAGES if not only or p in only]
    if only:
        unknown = set(only) - set(PAGES)
        if unknown:
            print(f"unknown page(s): {', '.join(sorted(unknown))}")
            return 1

    # The English dictionary, BEFORE the pages: every page links i18n-en.js, so
    # generating it first means check_assets() below is validating a file that
    # actually exists on this run rather than one left over from the last.
    # Regenerated unconditionally, for the same reason the Tailwind build is —
    # a dictionary that can go stale against the markup is a dictionary that
    # silently stops translating the strings you just changed.
    import i18n
    i18n_text, i18n_tpl, i18n_bytes = i18n.write()
    print(f"  {'i18n-en.js':<28} {i18n_bytes:>8,} bytes   "
          f"{i18n_text} text, {i18n_tpl} templates")

    total_missing = 0
    extra_pages = 0
    for name in targets:
        mod = importlib.import_module(name)
        html = mod.build()
        dest = os.path.join(EXPORT, mod.SLUG)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        missing = check_assets(name, html)
        total_missing += missing
        status = "ok" if not missing else f"{missing} missing asset(s)"
        print(f"  {mod.SLUG:<28} {len(html):>8,} bytes   {status}")

        # A module may fan out into one page per data record (product.py:
        # product-<id>.html for each catalogue product). Same asset check per
        # page, one summary line — 99 rows of ok teach nothing.
        if hasattr(mod, "build_many"):
            fan_bytes = fan_missing = fanned = 0
            for slug, page_html in mod.build_many():
                with open(os.path.join(EXPORT, slug), "w", encoding="utf-8") as f:
                    f.write(page_html)
                fan_missing += check_assets(slug, page_html)
                fan_bytes += len(page_html)
                fanned += 1
            total_missing += fan_missing
            extra_pages += fanned
            status = "ok" if not fan_missing else f"{fan_missing} missing asset(s)"
            print(f"  {name} x {fanned:<22} {fan_bytes:>8,} bytes   {status}")

    bad_js = check_runtime_js()
    css_failed = build_tailwind(partial=bool(only))

    print(f"\nbuilt {len(targets)} page(s)"
          + (f" + {extra_pages} fanned-out page(s)" if extra_pages else "")
          + (f"; {total_missing} broken asset reference(s)" if total_missing else "")
          + (f"; {bad_js} template-literal hazard(s) in scripts.js" if bad_js else "")
          + ("; TAILWIND CSS NOT REBUILT" if css_failed else ""))
    return 1 if (total_missing or bad_js or css_failed) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or None))
