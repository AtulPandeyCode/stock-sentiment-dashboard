import os
from transformers import pipeline


def load_finbert():
    print("Loading FinBERT model...")

    local_path = "./finbert_model"

    if os.path.exists(local_path):
        print("Found local model, loading from disk...")
        model_source = local_path
    else:
        print("No local model found, downloading from HuggingFace...")
        model_source = "ProsusAI/finbert"

    finbert = pipeline(
        task="text-classification",
        model=model_source,
        top_k=None
    )
    print("FinBERT loaded successfully.")
    return finbert


def analyze_sentiment(headlines, finbert):
    results = []
    for headline in headlines:
        if not headline or len(str(headline).strip()) < 5:
            continue
        try:
            text = str(headline)[:512]
            output = finbert(text)
            scores = {item["label"]: item["score"] for item in output[0]}
            best_label = max(scores, key=scores.get).lower()
            best_score = scores[max(scores, key=scores.get)]
            results.append({
                "text": headline,
                "label": best_label,
                "score": round(best_score, 4),
                "all_scores": scores
            })
        except Exception as e:
            print("Error analyzing headline: " + str(e))
            continue
    return results


def compute_overall_score(results):
    if not results:
        return 0.0
    score_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
    weighted_scores = [
        score_map.get(r["label"], 0.0) * r["score"]
        for r in results
    ]
    return round(sum(weighted_scores) / len(weighted_scores), 4)


def get_sentiment_label(overall_score):
    if overall_score > 0.15:
        return "Bullish 🟢"
    elif overall_score < -0.15:
        return "Bearish 🔴"
    else:
        return "Neutral ⚪"