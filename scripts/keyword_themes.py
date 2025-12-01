import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_per_bank(input_path, output_path, top_k=20):
    df = pd.read_csv(input_path)

    all_theme_rows = []

    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]

        texts = bank_df['review'].dropna().astype(str).tolist()
        if not texts:
            continue

        vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)  # unigrams + bigrams
        )
        X = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()

        # average tf-idf score per term
        scores = X.mean(axis=0).A1
        term_scores = list(zip(feature_names, scores))
        term_scores.sort(key=lambda x: x[1], reverse=True)

        top_terms = term_scores[:top_k]

        # simple manual grouping into broad themes
        ui_keywords = []
        performance_keywords = []
        access_keywords = []
        other_keywords = []

        for term, score in top_terms:
            low = term.lower()
            if any(w in low for w in ["ui", "interface", "design", "layout", "screen"]):
                ui_keywords.append(term)
            elif any(w in low for w in ["slow", "fast", "speed", "loading", "transfer"]):
                performance_keywords.append(term)
            elif any(w in low for w in ["login", "password", "account", "access"]):
                access_keywords.append(term)
            else:
                other_keywords.append(term)

        all_theme_rows.append({
            "bank": bank,
            "ui_experience_keywords": ", ".join(ui_keywords[:10]),
            "performance_keywords": ", ".join(performance_keywords[:10]),
            "access_account_keywords": ", ".join(access_keywords[:10]),
            "other_keywords": ", ".join(other_keywords[:10])
        })

    themes_df = pd.DataFrame(all_theme_rows)
    themes_df.to_csv(output_path, index=False)
    print(f"Saved themes summary to {output_path}")
    print(themes_df)

if __name__ == "__main__":
    extract_keywords_per_bank(
        "data/reviews_with_sentiment.csv",
        "data/bank_themes_summary.csv",
        top_k=40
    )
