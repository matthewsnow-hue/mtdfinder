# GoatCounter (visitor statistics)

Dashboard: https://mtdfinder.goatcounter.com · endpoint `https://mtdfinder.goatcounter.com/count` · approved by Matthew (A-019).

## Self-hosted count.js
`assets/count.js` is a verbatim copy of GoatCounter's script with a 6-line comment header added on top. Self-hosting is supported upstream (https://www.goatcounter.com/help/countjs-host); the `/count` endpoint is guaranteed to stay compatible. We self-host so the script isn't lost when `gc.zgo.at` is blocked.

| | |
|---|---|
| Source | https://gc.zgo.at/count.js (Last-Modified Tue, 28 Jul 2026 21:08:19 GMT) |
| Fetched | 2026-10-19 |
| Upstream version | identical to github.com/arp242/goatcounter `public/count.js` at master commit 478f026eb9 (2026-04-07), newer than release v2.7.0 (count.js has no version string of its own) |
| SHA-256 (upstream bytes, i.e. `tail -n +7 assets/count.js`) | `792b7abd26c1fb6ae62906833e09a301251e2641816e69e4f95aba518f3fe3f0` |
| Licence | ISC (count.js only; the rest of GoatCounter is EUPL 1.2). The upstream ISC notice is kept in the file header. |

Check: `tail -n +7 assets/count.js | sha256sum`.
Update: re-download, replace everything below the header, update the header and this table, rebuild.
Snippet (in `tools/build.py`, `GOATCOUNTER`): `<script data-goatcounter="https://mtdfinder.goatcounter.com/count" async src="/assets/count.js"></script>`

Note: count.js marks headless/WebDriver browsers as bots (`b=150..153`), and GoatCounter drops those hits, so automated test loads don't show on the dashboard.
