import pandas as pd

def preprocess_reviews(input_path, output_path):
    df = pd.read_csv(input_path)

    # Remove duplicates based on review text + bank
    df = df.drop_duplicates(subset=['review', 'bank'])

    # Drop rows with missing review or rating
    df = df.dropna(subset=['review', 'rating'])

    # Normalize date to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # Drop rows where date could not be parsed
    df = df.dropna(subset=['date'])

    # Keep only required columns
    df = df[['review', 'rating', 'date', 'bank', 'source']]

    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")
    print(df.head())
    print(df.shape)

if __name__ == "__main__":
    preprocess_reviews("data/raw_reviews.csv", "data/clean_reviews.csv")
