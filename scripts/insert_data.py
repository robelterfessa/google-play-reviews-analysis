import psycopg2
import pandas as pd

def insert_data(csv_path):
    df = pd.read_csv(csv_path)

    conn = psycopg2.connect(
        dbname="bank_reviews",
        user="postgres",
        password="8417",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()

    # 1) Insert banks and build name -> id map
    bank_names = df['bank'].unique()
    bank_id_map = {}

    for name in bank_names:
        cur.execute(
            "INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING RETURNING bank_id;",
            (name, None)
        )
        row = cur.fetchone()
        if row is not None:
            bank_id_map[name] = row[0]
        else:
            cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s;", (name,))
            bank_id_map[name] = cur.fetchone()[0]

    conn.commit()

    # 2) Insert reviews
    for _, row in df.iterrows():
        bank_id = bank_id_map.get(row['bank'])
        cur.execute(
            """
            INSERT INTO reviews
            (bank_id, review_text, rating, review_date,
             sentiment_label, sentiment_score, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                bank_id,
                row['review'],
                int(row['rating']),
                row['date'],
                row.get('sentiment_label'),
                float(row.get('sentiment_score')) if not pd.isna(row.get('sentiment_score')) else None,
                row['source'],
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Inserted reviews into database")

if __name__ == "__main__":
    insert_data("data/reviews_with_sentiment.csv")
