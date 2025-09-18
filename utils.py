import spacy
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



def clean_headline(text):
    parts = text.split("\n")
    if len(parts) >= 3:
        return "\n".join(parts[2:]).strip()
    else:
        return text.strip()


def scrape_google_finance_news(save_path="financial_news.json"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service("d:\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=options)

    driver.get("https://www.google.com/finance")
    time.sleep(5)

    # Scroll down to make sure content loads
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

    news_data = []

    try:
        # Locate the "Today's Financial News" section
        section = driver.find_element(By.CSS_SELECTOR, 'section[aria-labelledby="news-title"]')
        articles = section.find_elements(By.CSS_SELECTOR, 'div[data-article-source-name]')

        for article in articles:
            try:
                link_tag = article.find_element(By.CSS_SELECTOR, 'a')
                headline = link_tag.text.strip()
                source = article.get_attribute('data-article-source-name')

                if headline:
                    news_data.append({
                        "headline": clean_headline(headline),
                        "source": source
                    })

            except Exception as inner_error:
                print("⚠️ Skipping one article due to error:", inner_error)

    except Exception as e:
        print("❌ Error while scraping:", e)

    driver.quit()

    # ✅ Save to JSON
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(news_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Scraped {len(news_data)} headlines and saved to '{save_path}'")
    except Exception as json_error:
        print("❌ Failed to save JSON file:", json_error)

    return news_data


def clean_headline(text):
    parts = text.split("\n")
    if len(parts) >= 3:
        return "\n".join(parts[2:]).strip()
    else:
        return text.strip()


def preprocess_text(headlines):
    nlp = spacy.load("en_core_web_sm")
    cleaned = []
    for text in headlines:
        doc = nlp(text.lower())
        tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and token.is_alpha
        ]
        cleaned.append(" ".join(tokens))
    print("✅ Text preprocessed")
    return cleaned

# def scrape_headlines(url="https://finance.yahoo.com/"):
#     response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Yahoo Finance headlines are inside <h3> tags
#     headlines = [h.get_text() for h in soup.find_all("h3")]
#     return headlines[:10]  # take first 10 for demo