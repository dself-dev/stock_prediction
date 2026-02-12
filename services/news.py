# services/news.py
from __future__ import annotations

from typing import List, TypedDict, Optional, Dict, Any
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright, Page, Browser


class Article(TypedDict):
    rank: int
    headline: str
    url: str
    published_iso: Optional[str]
    published_text: Optional[str]
    tickers: str
    body: str


class NewsResult(TypedDict):
    ticker: str
    count: int
    saved_to: str
    items: List[Article]


def scrape_yahoo_news(
    ticker: str,
    *,
    limit: int = 5,
    headless: bool = True,
    slow_mo: int = 500,
) -> NewsResult:
    """
    Exact behavior from the working script, packaged as a function for FastAPI.

    Steps:
      1) open Yahoo Finance search
      2) search by ticker
      3) wait for "Recent News: {TICKER}"
      4) collect cards under that header
      5) visit top N, extract fields, save CSV at the same path as the script
    """
    t = ticker.strip().upper()
    articles: List[Article] = []

    with sync_playwright() as pw:
        browser: Browser = pw.firefox.launch(headless=headless, slow_mo=slow_mo)
        page: Page = browser.new_page()

        # search
        page.goto("https://finance.yahoo.com/search", wait_until="domcontentloaded")
        page.get_by_placeholder("Search for news, tickers or companies").fill(t)
        page.get_by_role("button", name="Search").click()

        # anchor: "Recent News: {TICKER}"
        header = f"Recent News: {t}"
        page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)

        # cards under that header
        cards_sel = f"section[role='article'][data-testid='storyitem']:below(h3:has-text('{header}'))"
        page.wait_for_selector(cards_sel, timeout=15000)
        cards = page.locator(cards_sel)

        # clamp to available
        count = min(limit, max(0, cards.count()))

        # scrape each article and save rows
        for i in range(count):
            link = cards.nth(i).locator("a.subtle-link.titles, a.subtle-link").first
            href = link.get_attribute("href")
            if not href:
                continue

            page.goto(href, wait_until="domcontentloaded")

            # headline
            title = (page.locator("h1").first.text_content() or "").strip()

            # published time
            time_el = page.locator("time.byline-attr-meta-time").first
            if time_el.count():
                published_iso = time_el.get_attribute("datetime")
                published_text = (time_el.text_content() or "").strip()
            else:
                published_iso = None
                published_text = None

            # body
            paras = page.locator("div.caas-body p").all_text_contents()
            if not paras:
                paras = page.locator("article p").all_text_contents()
            body = "\n".join(p.strip() for p in paras if p and p.strip())

            # tickers carousel (optional)
            tick_syms = page.locator("section.ticker-list a[data-testid='ticker-container'] .symbol").all_text_contents()
            tickers_in_article = ",".join(s.strip() for s in tick_syms) if tick_syms else ""

            articles.append(Article(
                search_ticker=t,  # kept original semantics in saved CSV via DataFrame columns
                rank=i + 1,
                headline=title,
                url=page.url,
                published_iso=published_iso,
                published_text=published_text,
                tickers=tickers_in_article,
                body=body,
            ))  # type: ignore[typeddict-item]

            # re-anchor for next card
            page.go_back(wait_until="domcontentloaded")
            page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)
            page.wait_for_selector(cards_sel, timeout=15000)

        browser.close()

    # write CSV at the same path the script used
    outpath = Path(rf"C:\Users\dself\OneDrive\Market_data\scraped_news\news_{t}.csv")
    # keep original column order/keys by constructing DataFrame from dicts
    df = pd.DataFrame(articles)
    df.to_csv(outpath, index=False)

    return NewsResult(
        ticker=t,
        count=len(articles),
        saved_to=str(outpath),
        items=articles,
    )
if __name__ == "__main__":
    t = input("Enter ticker: ").strip().upper()
    result = scrape_yahoo_news(t, limit=3, headless=False, slow_mo=500)
    print("Scraped", result["count"], "articles for", result["ticker"])
    print("CSV saved to:", result["saved_to"])
