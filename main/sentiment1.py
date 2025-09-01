# from playwright.sync_api import sync_playwright

# pw = sync_playwright().start()
# browser = pw.firefox.launch(headless=False, slow_mo=500)
# page = browser.new_page()

# ticker = input("enter ticker: ").strip().upper()

# # search
# page.goto("https://finance.yahoo.com/search", wait_until="domcontentloaded")
# page.get_by_placeholder("Search for news, tickers or companies").fill(ticker)
# page.get_by_role("button", name="Search").click()

# # anchor to "Recent News: {TICKER}"
# header = f"Recent News: {ticker}"
# page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)

# # cards under that header
# cards_sel = f"section[role='article'][data-testid='storyitem']:below(h3:has-text('{header}'))"
# page.wait_for_selector(cards_sel, timeout=15000)
# cards = page.locator(cards_sel)

# # list first 5
# count = min(5, cards.count())
# for i in range(count):
#     card = cards.nth(i)
#     link = card.locator("a.subtle-link.titles, a.subtle-link").first
#     href = link.get_attribute("href")
#     h3 = card.locator("h3").first
#     headline = h3.text_content() if h3.count() else (
#         link.get_attribute("aria-label") or link.get_attribute("title") or ""
#     )
#     print(f"{i+1}. {headline}\n   {href}")

# # open each sequentially by navigating to href (no popup/click issues)
# for i in range(count):
#     href = cards.nth(i).locator("a.subtle-link.titles, a.subtle-link").first.get_attribute("href")
#     if not href:
#         continue
#     page.goto(href, wait_until="domcontentloaded")
#     print(f"Opened {i+1}: {page.title()} -> {page.url}")
#     page.go_back(wait_until="domcontentloaded")
#     page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)
#     page.wait_for_selector(cards_sel, timeout=15000)

# browser.close()
# pw.stop()

from playwright.sync_api import sync_playwright
import pandas as pd

pw = sync_playwright().start()
browser = pw.firefox.launch(headless=False, slow_mo=500)
page = browser.new_page()

ticker = input("enter ticker: ").strip().upper()

# search
page.goto("https://finance.yahoo.com/search", wait_until="domcontentloaded")
page.get_by_placeholder("Search for news, tickers or companies").fill(ticker)
page.get_by_role("button", name="Search").click()

# anchor to "Recent News: {TICKER}"
header = f"Recent News: {ticker}"
page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)

# cards under that header
cards_sel = f"section[role='article'][data-testid='storyitem']:below(h3:has-text('{header}'))"
page.wait_for_selector(cards_sel, timeout=15000)
cards = page.locator(cards_sel)

# (optional) list first 5 found
count = min(5, cards.count())
for i in range(count):
    card = cards.nth(i)
    link = card.locator("a.subtle-link.titles, a.subtle-link").first
    href = link.get_attribute("href")
    h3 = card.locator("h3").first
    headline = h3.text_content() if h3.count() else (
        link.get_attribute("aria-label") or link.get_attribute("title") or ""
    )
    print(f"{i+1}. {headline}\n   {href}")

# scrape each article and save to CSV
articles = []
for i in range(count):
    link = cards.nth(i).locator("a.subtle-link.titles, a.subtle-link").first
    href = link.get_attribute("href")
    if not href:
        continue

    page.goto(href, wait_until="domcontentloaded")

    # headline on article page
    title = (page.locator("h1").first.text_content() or "").strip()

    # published time
    time_el = page.locator("time.byline-attr-meta-time").first
    if time_el.count():
        published_iso = time_el.get_attribute("datetime")
        published_text = (time_el.text_content() or "").strip()
    else:
        published_iso = None
        published_text = None

    # body text (Yahoo hosted articles use caas-body)
    paras = page.locator("div.caas-body p").all_text_contents()
    if not paras:
        paras = page.locator("article p").all_text_contents()
    body = "\n".join(p.strip() for p in paras if p and p.strip())

    # tickers in the carousel (if present)
    tick_syms = page.locator("section.ticker-list a[data-testid='ticker-container'] .symbol").all_text_contents()
    tickers_in_article = ",".join(s.strip() for s in tick_syms) if tick_syms else ""

    articles.append({
        "search_ticker": ticker,
        "rank": i + 1,
        "headline": title,
        "url": page.url,
        "published_iso": published_iso,
        "published_text": published_text,
        "tickers": tickers_in_article,
        "body": body,
    })

    # go back to the results and re-anchor
    page.go_back(wait_until="domcontentloaded")
    page.wait_for_selector(f"h3:has-text('{header}')", timeout=15000)
    page.wait_for_selector(cards_sel, timeout=15000)

# write CSV so we can scrape this-----will come back to organize in dataframe so we can save to db
df = pd.DataFrame(articles)
outfile = fr"C:\Users\dself\OneDrive\Market_data\scraped_news\news_{ticker}.csv"

df.to_csv(outfile, index=False)
print(f"Saved {len(df)} rows to {outfile}")

browser.close()
pw.stop()
