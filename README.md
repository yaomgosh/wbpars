# Compliant Marketplace Lead Research Tool

Python tool for researching **publicly visible** marketplace seller leads in clothing/accessories categories.

## Compliance guardrails

This MVP is intentionally constrained:

- Uses only publicly visible pages and fields.
- Does **not** bypass login/captcha/rate limits/anti-bot systems.
- Does **not** collect private personal data.
- Does **not** send automated messages.
- Detects likely access blocks and logs blocked pages into SQLite (`blocked_pages`).

## Stack

- Python 3.11+
- Playwright
- pandas
- SQLite
- CSV export

## Project files

- `lead_research.py` – main crawler/extractor/exporter.
- `input/example_search_urls.csv` – example input format.
- `output/leads.db` – generated SQLite DB (after run).
- `output/sellers.csv` – generated deduplicated sellers export (after run).

## Input format

CSV with required columns:

- `marketplace`
- `search_url`

Example:

```csv
marketplace,search_url
example_marketplace,https://example.com/search?q=clothing
example_marketplace,https://example.com/search?q=accessories
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

```bash
python lead_research.py \
  --input input/example_search_urls.csv \
  --output output/sellers.csv \
  --db output/leads.db \
  --headless
```

Optional tuning:

- `--max-products-per-search` (default: `50`)
- `--max-scrolls` (default: `8`)
- `--scroll-pause-sec` (default: `1.4`)
- `--page-pause-sec` (default: `1.2`)

## Output columns (CSV)

Extracted columns:

- `marketplace`
- `sample_product_title`
- `sample_product_url`
- `sample_price`
- `sample_rating`
- `sample_reviews_count`
- `brand`
- `seller_shop_name`
- `seller_profile_url`
- `public_legal_entity_or_inn`
- `products_seen`

Manual enrichment columns (empty, for human workflow):

- `contact_source`
- `contact`
- `outreach_status`
- `creative_opportunity`
- `lead_score`

## Notes

- Selectors are intentionally generic to support MVP experimentation across marketplaces.
- Some marketplaces may require per-site selector tuning.
- If a site displays anti-bot/captcha/access-block text, the tool logs the page and skips it.
