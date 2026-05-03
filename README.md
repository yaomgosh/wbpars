# Compliant Marketplace Lead Research Tool

Tool for collecting publicly visible marketplace seller leads.

## Guardrails
- Public pages only.
- No bypass of login/captcha/rate limits/anti-bot protection.
- No private personal data collection.
- No automated messaging.
- If blocked, page is logged into `blocked_pages`.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

If Playwright Chromium download is unstable, run with installed Chrome channel:
```bash
python lead_research.py --channel chrome ...
```

## Mode A — Search mode (auto-discovery)
Input columns: `marketplace,search_url`

```bash
python lead_research.py \
  --input input/example_search_urls.csv \
  --output output/sellers.csv \
  --db output/leads.db \
  --headless
```

## Mode B — Product URL mode (recommended)
Input columns: `marketplace,product_url`

```bash
python lead_research.py \
  --product-urls-file input/product_urls_template.csv \
  --output output/sellers.csv \
  --db output/leads.db \
  --channel chrome
```

## Mode C — Manual scroll collector (you scroll, script saves product links)
1. Open category URL in regular Chrome via helper script.
2. Scroll manually for 2–5 minutes.
3. Script saves discovered product links to CSV.

```bash
python collect_product_links_manual.py \
  --url "https://www.wildberries.ru/catalog/zhenshchinam/odezhda" \
  --marketplace wildberries \
  --output input/product_urls_collected.csv \
  --seconds 180 \
  --channel chrome
```

Then process collected links:
```bash
python lead_research.py \
  --product-urls-file input/product_urls_collected.csv \
  --output output/sellers.csv \
  --db output/leads.db \
  --channel chrome
```

## Output
- `output/leads.db` (SQLite tables: `products`, `blocked_pages`)
- `output/sellers.csv` (dedup sellers + manual columns)

Manual columns:
- `contact_source`
- `contact`
- `outreach_status`
- `creative_opportunity`
- `lead_score`
