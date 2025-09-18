from utils import scrape_headlines, preprocess_text
from sentiment import analyze_sentiment
from db import store_in_mongodb
import json

def main():
    try:
        print("🔍 Scraping financial headlines...")
        headlines = scrape_headlines()
        if not headlines:
            raise ValueError("No headlines found. Check scraping logic or website structure.")
        print("Headlines:", headlines)
        
        with open("headlines.json", "w", encoding="utf-8") as f:
            news_data=json.load(f)
            
        new_data = [clean_headline(article["headline"]) for article in news_data]

        print("\n🧹 Preprocessing...")
        cleaned = preprocess_text(headlines)    
        if not cleaned:
            raise ValueError("Preprocessing failed. No valid text to analyze.")

        print("\n📊 Running sentiment analysis...")
        sentiments = analyze_sentiment(cleaned)
        if not sentiments:
            raise RuntimeError("Sentiment analysis returned no results.")

        for h, s in zip(headlines, sentiments):
            print(f"{h} --> {s['label']} ({s['score']:.2f})")

        print("\n💾 Saving results to MongoDB...")
        store_in_mongodb(headlines, sentiments)

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        print("✅ Program finished (with or without errors).")


if __name__ == "__main__":
    main()
