"""
Phase 4 — Clean and enrich review data.

Reads fact_reviews from MySQL, enriches with:
  - Normalized review date (YYYY-MM)
  - Detected language (langdetect, ISO codes)
  - Inferred audience region (from language)
  - VADER sentiment scores and label

Outputs:
  - data_processed/reviews_enriched.csv
  - Updated columns in fact_reviews (MySQL)

Run with: anaconda3 python scripts/06_clean_enrich.py
"""

import os
import math
import pymysql
import pandas as pd
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
from langdetect import DetectorFactory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Fix langdetect randomness — same text always produces same result
DetectorFactory.seed = 0

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST", "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", 3306)),
    "user":     os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "audience_to_stage"),
    "charset":  "utf8mb4",
}

OUTPUT_PATH = "data_processed/reviews_enriched.csv"

# Region mapping: ISO 639-1 language code → audience region
REGION_MAP = {
    "en": "Western",
    "fr": "Western",
    "de": "Western",
    "it": "Western",
    "nl": "Western",
    "pt": "Western",
    "es": "Latin",
    "ru": "CIS",
    "uk": "CIS",
    "kk": "CIS",
    "ar": "MENA",
    "fa": "MENA",
    "tr": "MENA",
    "hi": "South_Asia",
    "ur": "South_Asia",
    "bn": "South_Asia",
}

# =============================================================================
# STEP 1 — Load from MySQL
# =============================================================================

def load_reviews(conn):
    """Load fact_reviews joined with dim_venue for venue_key context."""
    sql = """
        SELECT
            r.id_review,
            r.id_venue,
            v.venue_key,
            r.reviewer,
            r.location,
            r.review_date,
            r.trip_type,
            r.rating,
            r.review_text,
            r.source_status,
            r.source
        FROM fact_reviews r
        JOIN dim_venue v ON r.id_venue = v.id_venue
        ORDER BY r.id_review;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    print(f"[OK] Loaded {len(df)} reviews from MySQL.")
    return df


# =============================================================================
# STEP 2 — Normalize dates
# =============================================================================

MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}

def normalize_date(raw):
    """'Feb 2026' → '2026-02'. Returns None if unparseable."""
    if not raw or (isinstance(raw, float) and math.isnan(raw)):
        return None
    raw = str(raw).strip()
    parts = raw.split()
    if len(parts) != 2:
        return None
    month_str, year_str = parts
    month_num = MONTH_MAP.get(month_str[:3].lower())
    if not month_num:
        return None
    try:
        year = int(year_str)
    except ValueError:
        return None
    return f"{year}-{month_num}"

def enrich_dates(df):
    df["review_date_norm"] = df["review_date"].apply(normalize_date)
    nulls = df["review_date_norm"].isna().sum()
    print(f"[OK] Dates normalized. Unparseable: {nulls}/{len(df)}")
    return df


# =============================================================================
# STEP 3 — Detect language
# =============================================================================

def detect_language(text):
    """Returns ISO 639-1 language code or 'unknown'."""
    if not text or not isinstance(text, str) or len(text.strip()) < 10:
        return "unknown"
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def enrich_language(df):
    df["detected_language"] = df["review_text"].apply(detect_language)
    unknown = (df["detected_language"] == "unknown").sum()
    print(f"[OK] Language detected. Unknown: {unknown}/{len(df)}")
    return df


# =============================================================================
# STEP 4 — Infer audience region
# =============================================================================

def infer_region(lang_code):
    return REGION_MAP.get(lang_code, "Other")

def enrich_region(df):
    df["audience_region"] = df["detected_language"].apply(infer_region)
    print(f"[OK] Audience region inferred.")
    return df


# =============================================================================
# STEP 5 — VADER sentiment
# =============================================================================

def enrich_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()

    def analyze(text):
        if not text or not isinstance(text, str):
            return {"pos": None, "neg": None, "neu": None, "compound": None}
        scores = analyzer.polarity_scores(text)
        return {
            "pos":      round(scores["pos"], 4),
            "neg":      round(scores["neg"], 4),
            "neu":      round(scores["neu"], 4),
            "compound": round(scores["compound"], 4),
        }

    def label(compound):
        if compound is None:
            return "unknown"
        if compound >= 0.05:
            return "positive"
        if compound <= -0.05:
            return "negative"
        return "neutral"

    scores_df = df["review_text"].apply(analyze).apply(pd.Series)
    scores_df.columns = ["sentiment_pos", "sentiment_neg", "sentiment_neu", "sentiment_compound"]

    df = pd.concat([df, scores_df], axis=1)
    df["sentiment_label"] = df["sentiment_compound"].apply(label)

    print(f"[OK] VADER sentiment analysis complete.")
    return df


# =============================================================================
# STEP 6 — Save CSV + update MySQL
# =============================================================================

def save_csv(df):
    os.makedirs("data_processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"[OK] Saved enriched CSV -> {OUTPUT_PATH} ({len(df)} rows)")


def alter_table(cursor):
    """Add new columns to fact_reviews if they don't already exist."""
    new_cols = [
        ("review_date_norm",   "VARCHAR(7)"),
        ("detected_language",  "VARCHAR(10)"),
        ("audience_region",    "VARCHAR(30)"),
        ("sentiment_pos",      "FLOAT"),
        ("sentiment_neg",      "FLOAT"),
        ("sentiment_neu",      "FLOAT"),
        ("sentiment_compound", "FLOAT"),
        ("sentiment_label",    "VARCHAR(10)"),
    ]
    # MySQL doesn't support IF NOT EXISTS on ALTER TABLE — check information_schema
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'fact_reviews';
    """)
    existing = {row[0] for row in cursor.fetchall()}

    for col_name, col_type in new_cols:
        if col_name not in existing:
            cursor.execute(f"ALTER TABLE fact_reviews ADD COLUMN `{col_name}` {col_type};")
            print(f"  [ALTER] Added column: {col_name} ({col_type})")
        else:
            print(f"  [SKIP]  Column already exists: {col_name}")


def update_mysql(conn, df):
    """Update each row in fact_reviews with the enriched values."""
    sql = """
        UPDATE fact_reviews SET
            review_date_norm   = %s,
            detected_language  = %s,
            audience_region    = %s,
            sentiment_pos      = %s,
            sentiment_neg      = %s,
            sentiment_neu      = %s,
            sentiment_compound = %s,
            sentiment_label    = %s
        WHERE id_review = %s;
    """

    def val(x):
        """Convert NaN/None to None for pymysql."""
        if x is None:
            return None
        try:
            if isinstance(x, float) and math.isnan(x):
                return None
        except (TypeError, ValueError):
            pass
        return x

    updated = 0
    with conn.cursor() as cur:
        alter_table(cur)
        conn.commit()

        for _, row in df.iterrows():
            cur.execute(sql, (
                val(row["review_date_norm"]),
                val(row["detected_language"]),
                val(row["audience_region"]),
                val(row["sentiment_pos"]),
                val(row["sentiment_neg"]),
                val(row["sentiment_neu"]),
                val(row["sentiment_compound"]),
                val(row["sentiment_label"]),
                int(row["id_review"]),
            ))
            updated += 1

        conn.commit()

    print(f"[OK] Updated {updated} rows in fact_reviews (MySQL).")


# =============================================================================
# STEP 7 — Summary
# =============================================================================

def print_summary(df):
    print("\n" + "=" * 60)
    print("ENRICHMENT SUMMARY")
    print("=" * 60)

    print("\n--- Language distribution ---")
    lang_counts = df["detected_language"].value_counts()
    for lang, count in lang_counts.items():
        print(f"  {lang:<10} {count:>4} reviews")

    print("\n--- Audience region distribution ---")
    region_counts = df["audience_region"].value_counts()
    for region, count in region_counts.items():
        print(f"  {region:<15} {count:>4} reviews")

    print("\n--- Sentiment by venue ---")
    pivot = (
        df.groupby(["venue_key", "sentiment_label"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["positive", "neutral", "negative"], fill_value=0)
    )
    print(pivot.to_string())

    print("\n--- Average compound sentiment by venue ---")
    avg_sentiment = (
        df.groupby("venue_key")["sentiment_compound"]
        .mean()
        .round(3)
        .sort_values(ascending=False)
    )
    for venue, score in avg_sentiment.items():
        print(f"  {venue:<20} {score:>+.3f}")

    print("=" * 60)


# =============================================================================
# MAIN
# =============================================================================

def run():
    print("=" * 60)
    print("Phase 4 -- Clean and enrich reviews")
    print("=" * 60)

    conn = pymysql.connect(**DB_CONFIG)

    try:
        # Step 1: load
        df = load_reviews(conn)

        # Step 2: normalize dates
        df = enrich_dates(df)

        # Step 3: detect language
        df = enrich_language(df)

        # Step 4: infer region
        df = enrich_region(df)

        # Step 5: sentiment
        df = enrich_sentiment(df)

        # Step 6: save
        save_csv(df)
        update_mysql(conn, df)

        # Step 7: summary
        print_summary(df)

    finally:
        conn.close()


if __name__ == "__main__":
    run()
