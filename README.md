# Jaad storefront

A static storefront. Plain HTML/CSS/JS with no framework and no server — a
small Python script generates the pages, and Tailwind compiles the stylesheet.
The built site is what ships; `static-export/` is committed, so a clone can be
opened and served without building anything first.

## Running it on your own machine

You need **Python 3** and **Node 18+**. Check with `python3 --version` and
`node --version`; both come pre-installed on macOS except Node, which you can
get from [nodejs.org](https://nodejs.org) or `brew install node`.

```bash
git clone https://github.com/ahmedmarwan47-stack/jaad_storefront.git
cd jaad_storefront

npm install                  # once, and again only if package.json changes
python3 build/build.py       # generate the pages + compile tailwind.css
python3 build/serve.py       # serve on http://localhost:8000
```

Open **http://localhost:8000**. Ctrl-C stops the server.

The port is always 8000 and never moves. The server sends `Cache-Control:
no-store` on every response, so a plain refresh always shows the current
build — you never need a hard reload or a private window.

On Windows use `python` instead of `python3`.

## Making a change

Where things live:

| You want to change | Edit | Then |
|---|---|---|
| One page's content or layout | `build/pages/<page>.py` | `python3 build/build.py` |
| Markup shared by many pages (buttons, form fields, product cards) | `build/components.py` | `python3 build/build.py` |
| Header, footer, cart drawer, menus, overlays, the chat dock | `static-export/scripts.js` | just refresh\* |
| Hand-written CSS (animations, drawers, components) | `static-export/styles.css` | just refresh |
| Colours, fonts, spacing tokens | `tailwind.config.js` | `python3 build/build.py` |
| Product data | `static-export/data/catalog.json` | `python3 build/build.py` |

\* `scripts.js` and `styles.css` are served as-is, so a refresh is enough —
**unless** your edit introduces a Tailwind class that wasn't already used
somewhere on the site. Tailwind only emits classes it can see, so a brand-new
one needs `npm run css` (or a full `python3 build/build.py`) before it does
anything. If a change "does nothing", this is almost always why.

You can leave `build/serve.py` running the whole time — rebuild in a second
terminal and refresh the browser.

### Build output

`build.py` prints a line per page and fails loudly rather than silently:

- `! missing asset:` — a page links a file that isn't in `static-export/`.
- `TAILWIND CSS NOT REBUILT` — the stylesheet is stale; the site will look
  subtly wrong with no other error.
- a backtick inside an HTML comment in `scripts.js` — this silently ends the
  surrounding template literal and renders the whole header empty, so it is
  checked for at build time.

A non-zero exit means one of the above. Don't deploy on it.

To rebuild a single page while iterating: `python3 build/build.py register`
(Tailwind is skipped on a partial build — run `npm run css` before deploying).

## Deploying

The live site is the **`gh-pages`** branch, which is a copy of `static-export/`
at its root, published at
<https://ahmedmarwan47-stack.github.io/jaad_storefront/>.

Push your work to a branch, and it can be deployed from there. Deploying is a
separate step from merging: `gh-pages` holds the built site, `main` holds the
source.
