"""
Blog copy — JAAD's Media Center.

PLACEHOLDER: written in-house in JAAD's voice and product categories. The live
blog is client-rendered, so its copy is not scrapable — swap these for the
client's real posts before launch. See DESIGN-NOTES.md.

Rewritten English-first (Ahmed, 2026-08-20) to match the homepage, which is the
reference for the redesign. The previous set was inherited from the Abu Auf
fork: Arabic-only copy pointing at Abu Auf's own numbered image files
(`1-2.webp`, `big.webp`, …) that do not exist in this repo, so every blog card
rendered a broken image.

Each post: (slug, image, [tags], meta, title, excerpt, body paragraphs, tips).
The first three share the homepage's article art; the rest reuse it in rotation
until the client's real post photography lands.
"""

POSTS = [
    {
        "slug": "turkish-coffee-tradition",
        "image": "images/jaad/site/article-1.jpg",
        "tags": ["Coffee", "Wellness"],
        "meta": "July 15, 2026 — 5 min read",
        "title": "The Art of Turkish Coffee: A Tradition Worth Preserving",
        "excerpt": "Discover the centuries-old craft behind authentic Turkish coffee, from selecting the finest beans to the perfect brew technique.",
        "body": [
            "Turkish coffee is one of the oldest brewing methods still in daily use, and it "
            "survives for a reason: nothing else gives you the same intensity in such a small "
            "cup. The beans are ground finer than for any other method — closer to powder than "
            "to sand — and brewed slowly in a cezve until the foam rises.",
            "The grind is where most people go wrong. Too coarse and the coffee is thin and "
            "watery; too fine and it turns bitter and muddy. We grind our Turkish blends to "
            "order in small batches so the coffee reaches you at the right texture, with the "
            "aromatic oils still intact.",
            "Heat matters just as much. Bring the cezve up slowly over low heat and pull it "
            "off the moment the foam climbs the neck — never let it boil over. Pour the foam "
            "into the cup first, then the rest, and give it a minute to settle before the "
            "first sip.",
        ],
        "tips": [
            "Grind fine and brew within days for the fullest aroma",
            "Use cold, fresh water — one cup measured in the cup you'll drink from",
            "Never let it boil; pull the cezve the moment the foam rises",
        ],
    },
    {
        "slug": "mediterranean-nuts",
        "image": "images/jaad/site/article-2.jpg",
        "tags": ["Nutrition", "Nuts"],
        "meta": "June 28, 2026 — 4 min read",
        "title": "Why Mediterranean Nuts Are the World's Best Kept Secret",
        "excerpt": "From the groves of the Mediterranean come the finest walnuts and almonds, packed with nutrients and unmatched flavor.",
        "body": [
            "Mediterranean growing conditions — long dry summers, mineral-rich soil and cool "
            "nights — concentrate flavor in a way irrigated industrial groves cannot match. "
            "The nuts come out denser, sweeter and far higher in natural oils.",
            "Nutritionally they are among the best snacks available: a small daily handful is "
            "linked to better heart health and cholesterol levels, thanks to unsaturated fats, "
            "fiber and plant protein. The trick is portion, not restriction.",
            "Roasting is where quality is won or lost. High-temperature industrial roasting "
            "strips heat-sensitive vitamins and flattens flavor, so we roast in small batches "
            "at measured temperatures that preserve both the nutritional value and the taste.",
        ],
        "tips": [
            "Start small — a handful a day is plenty",
            "Mix almonds, cashews and walnuts to vary the nutrients you get",
            "Store in a sealed jar away from heat and light",
        ],
    },
    {
        "slug": "essential-spice-blends",
        "image": "images/jaad/site/article-3.jpg",
        "tags": ["Spices", "Recipes"],
        "meta": "June 10, 2026 — 6 min read",
        "title": "Spice Up Your Kitchen: 5 Essential Blends Every Home Cook Needs",
        "excerpt": "Transform your everyday cooking with these aromatic spice blends sourced from the world's finest growing regions.",
        "body": [
            "Most home kitchens are over-stocked with single spices that go stale and "
            "under-stocked with the few blends that actually carry a dish. Five well-chosen "
            "blends will take you further than thirty jars you open twice a year.",
            "Freshness is the whole game with spices. Ground spice starts losing its volatile "
            "oils immediately, which is why a jar that has sat open for a year tastes like "
            "dust. Buy smaller quantities more often and you will taste the difference in "
            "every dish.",
            "Store them properly and they will hold: airtight, out of direct light, and never "
            "above the stove — the one place almost everyone keeps them, and the fastest way "
            "to cook the aroma out of a jar before you ever use it.",
        ],
        "tips": [
            "Buy small and often rather than in bulk",
            "Keep jars away from the stove — heat kills aroma fastest",
            "Toast whole spices briefly before grinding to wake them up",
        ],
    },
    {
        "slug": "coffee-roast-guide",
        "image": "images/jaad/site/article-1.jpg",
        "tags": ["Coffee", "Guide"],
        "meta": "May 22, 2026 — 6 min read",
        "title": "Light, Medium or Dark: Choosing Your Coffee Roast",
        "excerpt": "Every roast level has its own character. Learn what separates them and find the one that suits your taste.",
        "body": [
            "Roast level is the single biggest lever on how your coffee tastes — bigger than "
            "origin for most drinkers. Light roasts keep more of the bean's original acidity "
            "and fruit; dark roasts trade that for body, chocolate and a rounder finish.",
            "Medium sits where most people are happiest: enough sweetness and body to drink "
            "black, enough clarity to still taste where the coffee came from. It is also the "
            "most forgiving of small brewing mistakes.",
            "There is no better or worse here, only fit. Match the roast to how you drink: "
            "lighter for filter and pour-over, medium for Turkish and espresso, darker if you "
            "take your coffee with milk and want it to cut through.",
        ],
        "tips": [
            "Drinking it black? Start with a medium roast",
            "Adding milk? A darker roast holds up better",
            "Buy whole bean and grind fresh whenever you can",
        ],
    },
    {
        "slug": "healthy-snack-box",
        "image": "images/jaad/site/article-2.jpg",
        "tags": ["Nutrition", "Family"],
        "meta": "May 3, 2026 — 4 min read",
        "title": "Building a Snack Box That Kids Actually Finish",
        "excerpt": "A mix of nuts, dried fruit and simple staples that balances real nutrition against what children will genuinely eat.",
        "body": [
            "The gap between a healthy snack box and an eaten snack box is where most good "
            "intentions die. The fix is not stricter rules — it is variety, texture and a "
            "little sweetness in the same box as the good stuff.",
            "Build around three slots: something crunchy (nuts or seeds), something sweet "
            "(dates or dried fruit) and something plain to reset the palate. Rotate within "
            "each slot week to week so the box never becomes predictable.",
            "Prep matters more than the shopping list. Portion into small containers once a "
            "week rather than every morning, and everything stays fresh while the daily "
            "decision disappears entirely.",
        ],
        "tips": [
            "Portion once a week, not every morning",
            "Pair a sweet item with a plain one in the same box",
            "Rotate the mix weekly so it never gets boring",
        ],
    },
    {
        "slug": "homemade-granola",
        "image": "images/jaad/site/article-3.jpg",
        "tags": ["Recipes", "Breakfast"],
        "meta": "April 18, 2026 — 8 min read",
        "title": "Homemade Granola with Nuts and Honey",
        "excerpt": "A simple recipe you can make at home that keeps for a full week — ideal for fast breakfasts.",
        "body": [
            "Shop-bought granola is usually far sweeter than it needs to be. Making it at home "
            "takes about forty minutes, costs less per portion, and lets you decide exactly "
            "how much honey goes in.",
            "The base is oats, roughly chopped nuts and a little salt. Honey and oil bind it; "
            "the ratio between them decides whether you get loose granola or proper clusters. "
            "More honey, more clustering — but bake it lower and slower or the sugar burns.",
            "Add dried fruit only after baking, never before. Fruit that goes into the oven "
            "comes out hard and bitter, which is the most common reason a first attempt at "
            "granola disappoints.",
        ],
        "tips": [
            "Bake low and slow — 150°C, stirring once",
            "Stir in dried fruit after baking, never before",
            "Cool completely before jarring or it turns soft",
        ],
    },
]
