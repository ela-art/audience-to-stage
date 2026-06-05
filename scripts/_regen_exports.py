"""Regenerate reviews_vs_tourism.csv and create correlation_tourism_sentiment.csv."""
import pymysql, pandas as pd, os

conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234',
                       database='audience_to_stage', charset='utf8mb4')

OUT = "data/tableau_exports"
os.makedirs(OUT, exist_ok=True)

def run_query(sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
    return pd.DataFrame(rows, columns=cols)

# --- 1. reviews_vs_tourism.csv (monthly, with 2024 now populated) ---
df1 = run_query("""
    SELECT
        r.review_date_norm                          AS month,
        v.venue_name,
        COUNT(*)                                    AS review_count,
        ROUND(AVG(r.sentiment_compound), 4)         AS avg_sentiment,
        CAST(ROUND(AVG(r.rating), 0) AS UNSIGNED)   AS avg_rating,
        t.total_visitors
    FROM fact_reviews r
    JOIN dim_venue v ON r.id_venue = v.id_venue
    LEFT JOIN (
        SELECT year, SUM(visitor_count) AS total_visitors
        FROM tourism_stats
        GROUP BY year
    ) t ON CAST(LEFT(r.review_date_norm, 4) AS UNSIGNED) = t.year
    WHERE r.review_date_norm IS NOT NULL
    GROUP BY r.review_date_norm, v.venue_name, t.total_visitors
    ORDER BY month, v.venue_name
""")
df1.to_csv(f"{OUT}/reviews_vs_tourism.csv", sep=";", decimal=",", index=False, encoding="utf-8")
nulls = df1["total_visitors"].isna().sum()
print(f"reviews_vs_tourism.csv   {len(df1):>3} rows | NULLs en total_visitors: {nulls}")
print(df1.head(3).to_string(index=False))
print()

# --- 2. correlation_tourism_sentiment.csv (annual, one row per year+venue) ---
# For scatter: visitors (X) vs avg_sentiment (Y), colored by venue
df2 = run_query("""
    SELECT
        LEFT(r.review_date_norm, 4)                 AS year,
        v.venue_name,
        COUNT(*)                                    AS review_count,
        ROUND(AVG(r.sentiment_compound), 4)         AS avg_sentiment,
        CAST(ROUND(AVG(r.rating), 0) AS UNSIGNED)   AS avg_rating,
        t.total_visitors
    FROM fact_reviews r
    JOIN dim_venue v ON r.id_venue = v.id_venue
    LEFT JOIN (
        SELECT year, SUM(visitor_count) AS total_visitors
        FROM tourism_stats
        GROUP BY year
    ) t ON CAST(LEFT(r.review_date_norm, 4) AS UNSIGNED) = t.year
    WHERE r.review_date_norm IS NOT NULL
    GROUP BY LEFT(r.review_date_norm, 4), v.venue_name, t.total_visitors
    ORDER BY year, v.venue_name
""")
df2.to_csv(f"{OUT}/correlation_tourism_sentiment.csv", sep=";", decimal=",", index=False, encoding="utf-8")
nulls2 = df2["total_visitors"].isna().sum()
print(f"correlation_tourism_sentiment.csv  {len(df2):>3} rows | NULLs en total_visitors: {nulls2}")
print(df2.to_string(index=False))

conn.close()
