"""Utility: restore reviews_raw.csv from MySQL (run once if CSV is lost)."""
import pymysql, os, pandas as pd
from dotenv import load_dotenv
load_dotenv()
conn = pymysql.connect(
    host=os.getenv("MYSQL_HOST"), port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"), charset="utf8mb4"
)
with conn.cursor() as cur:
    cur.execute("""
        SELECT v.venue_key AS venue, r.reviewer, r.location,
               r.review_date AS date, r.trip_type, r.rating,
               r.review_text, r.source_status, r.source
        FROM fact_reviews r
        JOIN dim_venue v ON r.id_venue = v.id_venue
        ORDER BY r.id_review
    """)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
conn.close()
df = pd.DataFrame(rows, columns=cols)
df.to_csv("data_raw/tripadvisor/reviews_raw.csv", index=False, encoding="utf-8")
print(f"Restored {len(df)} rows to reviews_raw.csv")
print(df["venue"].value_counts().to_string())
