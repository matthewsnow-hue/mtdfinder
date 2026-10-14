# MTD Finder design notes (14 Oct 2026)

How we studied them: HTML/CSS fetched and 1440px headless screenshots taken. Aramco's page didn't load headlessly and Lando Norris only gave HTML, so those notes are partial.

| Reference | Fonts | Palette | Layout / hero | Nav / motion / buttons | Why it feels premium |
|---|---|---|---|---|---|
| Pumpkin House (site-phi-six-43) | Marcellus display + Instrument Sans | Muted teal, warm wood | Full-bleed photo hero | Minimal overlay nav | One strong image, very little text |
| Master Charters | Cormorant Garamond + Albert Sans | Deep navy #0b1a26, white, one green CTA | Left-aligned large serif headline on a dark photo | Small caps eyebrow with rule, glassy CTA panel | Serif plus restraint, a single action |
| Operant Automations | Instrument Serif + Bricolage Grotesque | Dark olive, sand #ebe6da, copper #d9a277 | Split hero with wordmark on rules | Rectangular outline buttons | Earthy restrained palette, hairline rules |
| Populon | Cormorant Garamond (+ mono labels) | Cream paper, ink, one burgundy accent | Centred serif headline, italic accent word | Tiny letter-spaced caps nav, square caps CTA | Editorial calm, lots of whitespace, one accent |
| Epiminds | Instrument Serif + Satoshi / Instrument Sans | Near-black #06040a, white | Loader then dark hero | Heavy scroll-driven motion | Serif/sans pairing on black |
| Lando Norris | Custom "Brier" | Black #101400 + neon #d2ff00 | Big imagery, bold type | Rich WebGL motion | One loud signature colour, confident scale |
| Aramco CBA | (not captured) | n/a | n/a | n/a | n/a |
| Edwin Le | Custom grotesk | Black, white, purple #5b0080 | Centred greeting with typed text and a wave graphic | Hamburger nav, typing animation | Personality through motion, very sparse |
| Exergy3 | Custom sans | Forest #082e29, mint #edf6f0, orange #ff7500 | Rounded framed full-bleed photo | Floating pill nav | Framed media, soft radii, pill nav |
| Superwhisper | Flow Circular | Near-white #fafafa, greys | Centred two-line headline over a dark gradient | Pill buttons, small trust line | Short copy, big contrast |

## Takeaways applied to MTD Finder
- **Type:** Instrument Serif (display, with italic accent words) plus Instrument Sans (UI and body). Tiny letter-spaced caps for eyebrows and nav (Populon, Master Charters).
- **Palette:** cream paper #f8f4ec, ink navy #0e1b26, one accent of deep forest green #1f5b47 (trust and money). A dark navy panel for the checker (Master Charters). No gradients or neon: it's a tax tool, so it should feel calm.
- **Layout:** centred editorial hero with hairline rules. Floating pill nav (Exergy3). A 1200px grid with generous whitespace.
- **Motion:** subtle reveals only, with prefers-reduced-motion respected. No loaders and no WebGL, to stay fast.
- **Buttons:** square-ish, small caps labels (Populon), or ink pills.
- **Directory UX:** sticky filter sidebar on desktop and a collapsible filter drawer on mobile, instant search, result count, clear-all, and uniform spec rows on every card so they compare at a glance. Compare up to 3 products side by side.
