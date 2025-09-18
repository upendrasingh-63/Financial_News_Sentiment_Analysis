from pymongo import MongoClient

def store_in_mongodb(headlines, sentiments):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["financial_news"]
    collection = db["headlines"]

    for text, sentiment in zip(headlines, sentiments):
        collection.insert_one({
            "headline": text,
            "label": sentiment["label"],
            "score": float(sentiment["score"])
        })

    print("✅ Data stored in MongoDB")
