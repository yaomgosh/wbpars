#!/usr/bin/env python3
"""Collect product links while user scrolls manually in regular browser.

Usage:
  python collect_product_links_manual.py --url https://www.wildberries.ru/catalog/zhenshchinam/odezhda
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def is_product_url(url: str) -> bool:
    if not url:
        return False
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        return False
    path = p.path.lower()
    return ("/catalog/" in path and "detail.aspx" in path) or ("/product/" in path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manual scroll link collector")
    parser.add_argument("--url", required=True, help="Category/search URL to open")
    parser.add_argument("--marketplace", default="wildberries")
    parser.add_argument("--output", default=Path("input/product_urls_collected.csv"), type=Path)
    parser.add_argument("--seconds", type=int, default=180, help="How long to collect links")
    parser.add_argument("--channel", default="chrome", help="Browser channel, e.g. chrome")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    links: set[str] = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel=args.channel)
        context = browser.new_context()
        page = context.new_page()

        print("Open category page and scroll manually in the opened browser window...")
        page.goto(args.url, wait_until="domcontentloaded")

        started = time.time()
        while time.time() - started < args.seconds:
            anchors = page.locator("a[href]")
            for idx in range(min(anchors.count(), 3000)):
                href = anchors.nth(idx).get_attribute("href")
                if href and href.startswith("/"):
                    href = f"{urlparse(args.url).scheme}://{urlparse(args.url).netloc}{href}"
                if href and is_product_url(href):
                    links.add(href.split("#", 1)[0])
            print(f"\rCollected product links: {len(links)}", end="")
            time.sleep(1.5)

        print()
        context.close()
        browser.close()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["marketplace", "product_url"])
        for link in sorted(links):
            writer.writerow([args.marketplace, link])

    print(f"Saved {len(links)} links to {args.output}")


if __name__ == "__main__":
    main()
