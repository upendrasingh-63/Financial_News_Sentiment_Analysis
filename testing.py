# from utils import preprocess_text, scrape_headlines

# headlines=scrape_headlines()
# print("Headlines:", headlines)

from utils import scrape_google_finance_news

headlines = scrape_google_finance_news()
print("Headlines:", headlines)