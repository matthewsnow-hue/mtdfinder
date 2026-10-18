# MTD Finder
Independent guide to Making Tax Digital for Income Tax software for UK sole traders and landlords. Run by Matthew Snow trading as Sno Automations.

- `data/products.json`: software data scraped from HMRC's finder (https://www.tax.service.gov.uk/find-making-tax-digital-income-tax-software/). The daily routine refreshes this file.
- `tools/build.py`: regenerates all HTML, sitemap.xml, robots.txt and llms.txt. Run `python3 tools/build.py`.
- Hosted on GitHub Pages. TODO: custom domain mtdfinder.co.uk, Stripe link, newsletter backend, confirm contact email.
- `assets/count.js`: self-hosted GoatCounter script (ISC). Version, SHA-256 and update steps: `docs/goatcounter.md`.
