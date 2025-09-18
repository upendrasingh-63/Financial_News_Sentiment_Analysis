from transformers import pipeline

def analyze_sentiment(cleaned_headlines):
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    results = sentiment_pipeline(cleaned_headlines)
    return results
