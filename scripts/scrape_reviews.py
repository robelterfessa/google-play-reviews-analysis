from google_play_scraper import reviews
import pandas as pd

def scrape_bank_reviews(app_id, bank_name, num_reviews=400):
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        count=num_reviews,
        filter_score_with=None
    )

    df = pd.DataFrame(result)
    df = df[['content', 'score', 'at']]
    df = df.rename(columns={'content': 'review', 'score': 'rating', 'at': 'date'})
    df['bank'] = bank_name
    df['source'] = 'google_play'
    return df

if __name__ == "__main__":
    # put your real app IDs here
    cbe_app_id = "com.combanketh.mobilebanking"
    boa_app_id = "com.boa.boaMobileBanking"
    dashen_app_id = "com.dashen.dashensuperapp"

    cbe_reviews = scrape_bank_reviews(cbe_app_id, "CBE")
    boa_reviews = scrape_bank_reviews(boa_app_id, "BOA")
    dashen_reviews = scrape_bank_reviews(dashen_app_id, "Dashen")

    all_reviews = pd.concat([cbe_reviews, boa_reviews, dashen_reviews], ignore_index=True)

    print(all_reviews.head())
    print(all_reviews['bank'].value_counts())
    all_reviews.to_csv("data/raw_reviews.csv", index=False)
    print("Saved raw reviews to data/raw_reviews.csv")

