# google-play-reviews-analysis

Solution to week-2 challenges of Kaim Ai mastery challenge

## Data Collection Summary

- Target: 400+ reviews per bank (1,200 total).
- Actual collected:
  - CBE: 326 reviews
  - BOA: 350 reviews
  - Dashen: 336 reviews
- Reason: Google Play store returned fewer reviews than the target during scraping.

The rest of the analysis uses all available cleaned reviews from `data/clean_reviews.csv`.

## Sentiment and Themes (Task 2)

- Sentiment: VADER (NLTK) used to compute `sentiment_score` (compound) and `sentiment_label` (positive/neutral/negative) for each review, saved in `data/reviews_with_sentiment.csv`.[attached_file:1]
- Themes: TF-IDF used per bank to extract top keywords, manually grouped into themes: UI/experience, performance, access/account, and other, saved in `data/bank_themes_summary.csv`.[attached_file:1]

## Task 3: PostgreSQL Storage

- Database: `bank_reviews` in PostgreSQL.
- Tables created with `scripts/create_tables.py`:
  - `banks(bank_id, bank_name, app_name)`
  - `reviews(review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)`.[attached_file:1]
- Data inserted from `data/reviews_with_sentiment.csv` using `scripts/insert_data.py`.[attached_file:1]
- Verification (pgAdmin Query Tool):
  - `SELECT COUNT(*) FROM reviews;` → <1012>.
  - `SELECT bank_name, COUNT(*) ...` → per‑bank counts.
