import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

def add_sentiment(input_path, output_path):
    df = pd.read_csv(input_path)

    sia = SentimentIntensityAnalyzer()

    # calculate sentiment scores
    scores = df['review'].astype(str).apply(sia.polarity_scores)
    df['sentiment_score'] = scores.apply(lambda x: x['compound'])

    def label_from_score(s):
        if s >= 0.05:
            return 'positive'
        elif s <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    df['sentiment_label'] = df['sentiment_score'].apply(label_from_score)

    df.to_csv(output_path, index=False)
    print(f"Saved sentiment data to {output_path}")
    print(df[['review', 'sentiment_label', 'sentiment_score']].head())
    print(df['sentiment_label'].value_counts())

if __name__ == "__main__":
    add_sentiment("data/clean_reviews.csv", "data/reviews_with_sentiment.csv")
