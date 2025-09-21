# # services/news.py
# from __future__ import annotations

# from typing import List, TypedDict, Optional, Dict, Any
# from pathlib import Path
# import pandas as pd
# from playwright.sync_api import sync_playwright, Page, Browser

# # I added this import so I can run sentiment analysis on the headlines + body text
# from nltk.sentiment.vader import SentimentIntensityAnalyzer


# class Article(TypedDict):
#     rank: int
#     headline: str
#     url: str
#     published_iso: Optional[str]
#     published_text: Optional[str]
#     tickers: str
#     body: str


# class NewsResult(TypedDict):
#     ticker: str
#     count: int
#     saved_to: str
#     items: List[Article]


# def scrape_yahoo_news(
#     ticker: str,
#     *,
#     limit: int = 5,
#     headless: bool = True,
#     slow_mo: int = 500,
# ) -> NewsResult:
#     """
#     Exact behavior from the working script, packaged as a function for FastAPI.

#     Steps:
#       1) open Yahoo Finance search
#       2) search by ticker
#       3) wait for "Recent News: {TICKER}"
#       4) collect cards under that header
#       5) visit top N, extract fields, save CSV at the same path as the script
#     """
#     t = ticker.strip().upper()
#     articles: List[Article] = []

#     with sync_playwright() as pw:
#         browser: Browser = pw.firefox.launch(headless=headless, slow_mo=slow_mo)
#         page: Page = browser.new_page()

#         # I go to the Yahoo Finance search page and type in the ticker
#         page.goto("https://finance.yahoo.com/search", wait_until="domcontentloaded")
#         page.get_by_placeholder("Search for news, tickers or companies").fill(t)
#         page.get_by_role("button", name="Search").click()

#         # anchor: "Recent News: {TICKER}"
#         header = f"Recent News: {t}"
#         page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)

#         # I grab the cards listed under that header
#         cards_sel = f"section[role='article'][data-testid='storyitem']:below(h3:has-text('{header}'))"
#         page.wait_for_selector(cards_sel, timeout=15000)
#         cards = page.locator(cards_sel)

#         # clamp to available
#         count = min(limit, max(0, cards.count()))

#         # scrape each article and save rows
#         for i in range(count):
#             link = cards.nth(i).locator("a.subtle-link.titles, a.subtle-link").first
#             href = link.get_attribute("href")
#             if not href:
#                 continue

#             page.goto(href, wait_until="domcontentloaded")

#             # headline
#             title = (page.locator("h1").first.text_content() or "").strip()

#             # published time
#             time_el = page.locator("time.byline-attr-meta-time").first
#             if time_el.count():
#                 published_iso = time_el.get_attribute("datetime")
#                 published_text = (time_el.text_content() or "").strip()
#             else:
#                 published_iso = None
#                 published_text = None

#             # body
#             paras = page.locator("div.caas-body p").all_text_contents()
#             if not paras:
#                 paras = page.locator("article p").all_text_contents()
#             body = "\n".join(p.strip() for p in paras if p and p.strip())

#             # tickers carousel (optional)
#             tick_syms = page.locator("section.ticker-list a[data-testid='ticker-container'] .symbol").all_text_contents()
#             tickers_in_article = ",".join(s.strip() for s in tick_syms) if tick_syms else ""

#             articles.append(Article(
#                 search_ticker=t,  # I keep this so I know what ticker I searched
#                 rank=i + 1,
#                 headline=title,
#                 url=page.url,
#                 published_iso=published_iso,
#                 published_text=published_text,
#                 tickers=tickers_in_article,
#                 body=body,
#             ))  # type: ignore[typeddict-item]

#             # I return back to the news list so I can grab the next card
#             page.go_back(wait_until="domcontentloaded")
#             page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)
#             page.wait_for_selector(cards_sel, timeout=15000)

#         browser.close()

#     # I write the scraped results to CSV just like before
#     outpath = Path(rf"C:\Users\dself\OneDrive\Market_data\scraped_news\news_{t}.csv")
#     df = pd.DataFrame(articles)
#     df.to_csv(outpath, index=False)

#     return NewsResult(
#         ticker=t,
#         count=len(articles),
#         saved_to=str(outpath),
#         items=articles,
#     )


# def score_with_vader(csv_path: str) -> float:
#     """
#     After I scrape and save the news, I call this function to score
#     the headlines + bodies using VADER and return the average compound score.
#     """
#     df = pd.read_csv(csv_path)
#     if df.empty:
#         return 0.0

#     sid = SentimentIntensityAnalyzer()
#     scores = []

#     for _, row in df.iterrows():
#         text = f"{row['headline']} {row['body']}"
#         s = sid.polarity_scores(str(text))
#         scores.append(s["compound"])

#     return sum(scores) / len(scores) if scores else 0.0


# if __name__ == "__main__":
#     # I let the user enter the ticker here for testing
#     t = input("Enter ticker: ").strip().upper()
#     result = scrape_yahoo_news(t, limit=3, headless=False, slow_mo=500)
#     print("Scraped", result["count"], "articles for", result["ticker"])
#     print("CSV saved to:", result["saved_to"])

#     # right after scraping, I score sentiment on the same CSV
#     avg_sent = score_with_vader(result["saved_to"])
#     print(f"Average sentiment score for {t}: {avg_sent:.3f}")
# services/news.py
from __future__ import annotations

from typing import List, TypedDict, Optional
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright, Page, Browser

# I added this import so I can run sentiment analysis on the headlines + body text
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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
    I scrape Yahoo Finance news for the given ticker and save the results to CSV.
    """
    t = ticker.strip().upper()
    articles: List[Article] = []

    with sync_playwright() as pw:
        browser: Browser = pw.firefox.launch(headless=headless, slow_mo=slow_mo)
        page: Page = browser.new_page()

        # I go to the Yahoo Finance search page and type in the ticker
        page.goto("https://finance.yahoo.com/search", wait_until="domcontentloaded")
        page.get_by_placeholder("Search for news, tickers or companies").fill(t)
        page.get_by_role("button", name="Search").click()

        # anchor: "Recent News: {TICKER}"
        header = f"Recent News: {t}"
        page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)

        # I grab the cards listed under that header
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
                search_ticker=t,
                rank=i + 1,
                headline=title,
                url=page.url,
                published_iso=published_iso,
                published_text=published_text,
                tickers=tickers_in_article,
                body=body,
            ))  # type: ignore[typeddict-item]

            # I return back to the news list so I can grab the next card
            page.go_back(wait_until="domcontentloaded")
            page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)
            page.wait_for_selector(cards_sel, timeout=15000)

        browser.close()

    # I write the scraped results to CSV just like before
    outpath = Path(rf"C:\Users\dself\OneDrive\Market_data\scraped_news\news_{t}.csv")
    df = pd.DataFrame(articles)
    df.to_csv(outpath, index=False)

    return NewsResult(
        ticker=t,
        count=len(articles),
        saved_to=str(outpath),
        items=articles,
    )


def score_with_vader(csv_path: str) -> dict:
    """
    I run VADER sentiment on scraped news and also check for
    bullish/bearish keywords. Returns average score + label.
    """
    df = pd.read_csv(csv_path)
    if df.empty:
        return {"avg_sentiment": 0.0, "label": "neutral"}

    sid = SentimentIntensityAnalyzer()
    scores = []

    # I keep a small keyword dictionary to adjust signals
    bullish_words = ["beat", "growth", "record", "profit", "deal", "partnership", "upgrade", "strong"]
    bearish_words = ["miss", "loss", "downgrade", "layoff", "scandal", "investigation", "lawsuit", "weak"]

    signal = 0  # -1 = bearish, 0 = neutral, +1 = bullish

    for _, row in df.iterrows():
        text = f"{row['headline']} {row['body']}".lower()
        s = sid.polarity_scores(str(text))
        scores.append(s["compound"])

        # keyword checks
        if any(word in text for word in bullish_words):
            signal += 1
        if any(word in text for word in bearish_words):
            signal -= 1

    avg_score = sum(scores) / len(scores) if scores else 0.0

    # final label based on avg_score + keywords
    if avg_score > 0.2 or signal > 0:
        label = "positive"
    elif avg_score < -0.2 or signal < 0:
        label = "negative"
    else:
        label = "neutral"

    return {"avg_sentiment": avg_score, "label": label}


if __name__ == "__main__":
    # I let the user enter the ticker here for testing
    t = input("Enter ticker: ").strip().upper()
    result = scrape_yahoo_news(t, limit=3, headless=False, slow_mo=500)
    print("Scraped", result["count"], "articles for", result["ticker"])
    print("CSV saved to:", result["saved_to"])

    # right after scraping, I score sentiment on the same CSV
    sentiment_result = score_with_vader(result["saved_to"])
    print(f"Average sentiment score for {t}: {sentiment_result['avg_sentiment']:.3f} → {sentiment_result['label'].upper()}")
