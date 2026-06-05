"""
Phase 5 — Export CSVs for Tableau.

Reads from MySQL audience_to_stage and writes 4 analysis-ready CSVs
to data/tableau_exports/.

Run with: anaconda3 python scripts/07_export_tableau.py
"""

import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST", "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", 3306)),
    "user":     os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root1234"),
    "database": os.getenv("MYSQL_DATABASE", "audience_to_stage"),
    "charset":  "utf8mb4",
}

OUTPUT_DIR = "data/tableau_exports"

# ---------------------------------------------------------------------------
# Queries — corrected to match real schema:
#   id_venue (not venue_id), sentiment_compound (not sentiment_score),
#   review_date_norm is already VARCHAR 'YYYY-MM' (no DATE_FORMAT needed),
#   tourism_stats has year + visitor_count by country (no stat_date / hotel_occupancy_rate)
# ---------------------------------------------------------------------------

QUERIES = {
    "sentiment_over_time.csv": """
        SELECT
            v.venue_name,
            r.review_date_norm          AS month,
            AVG(r.sentiment_compound)   AS avg_sentiment,
            AVG(r.rating)               AS avg_rating,
            COUNT(*)                    AS review_count
        FROM fact_reviews r
        JOIN dim_venue v ON r.id_venue = v.id_venue
        WHERE r.review_date_norm IS NOT NULL
        GROUP BY v.venue_name, r.review_date_norm
        ORDER BY v.venue_name, month;
    """,

    "rating_distribution.csv": """
        SELECT
            v.venue_name,
            r.rating,
            COUNT(*) AS count
        FROM fact_reviews r
        JOIN dim_venue v ON r.id_venue = v.id_venue
        GROUP BY v.venue_name, r.rating
        ORDER BY v.venue_name, r.rating;
    """,

    # tourism_stats is annual by country — aggregate to total visitors per year
    # then join on the year portion of review_date_norm
    "reviews_vs_tourism.csv": """
        SELECT
            r.review_date_norm                      AS month,
            v.venue_name,
            COUNT(*)                                AS review_count,
            AVG(r.sentiment_compound)               AS avg_sentiment,
            AVG(r.rating)                           AS avg_rating,
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
        ORDER BY month, v.venue_name;
    """,

    "competition_profiles.csv": """
        SELECT
            venue_name, venue_type, format,
            visual_register, cultural_barriers, sensory_intensity,
            music_style, audience_profile, conflict_resilience,
            estilo_show, estilo_movimiento, registro_corporal,
            relacion_publico, carga_erotica, referente_cultural,
            nivel_habilidad, paleta_vestuario, diseno_vestuario,
            estilo_musical, ticket_price_usd, tripadvisor_rating,
            tripadvisor_reviews, years_active, producer, artistic_director
        FROM dim_venue;
    """,
}


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = pymysql.connect(**DB_CONFIG)
    print("=" * 55)
    print("Phase 5 -- Tableau CSV exports")
    print("=" * 55)

    try:
        with conn.cursor() as cur:
            for filename, sql in QUERIES.items():
                cur.execute(sql)
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
                df = pd.DataFrame(rows, columns=cols)

                out_path = os.path.join(OUTPUT_DIR, filename)
                df.to_csv(out_path, index=False, encoding="utf-8")
                print(f"  {filename:<35} {len(df):>4} rows -> {out_path}")

    finally:
        conn.close()

    print("=" * 55)
    print("Done.")


if __name__ == "__main__":
    run()
