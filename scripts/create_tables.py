import psycopg2

def create_tables():
    conn = psycopg2.connect(
        dbname="bank_reviews",
        user="postgres",
        password="8417",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(100) UNIQUE,
            app_name VARCHAR(200)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER,
            review_date DATE,
            sentiment_label VARCHAR(20),
            sentiment_score REAL,
            source VARCHAR(50)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Created tables banks and reviews")

if __name__ == "__main__":
    create_tables()
