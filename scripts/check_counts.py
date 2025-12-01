import pandas as pd

df = pd.read_csv("data/clean_reviews.csv")
print(df['bank'].value_counts())
print("Total rows:", df.shape[0])
