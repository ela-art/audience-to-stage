"""
Phase 3 — Build MySQL database and load CSVs into star schema.

Creates:
  - database: audience_to_stage
  - tables:   dim_venue, fact_reviews, tourism_stats

Loads:
  - data_manual/competition_profiles.csv  → dim_venue
  - data_raw/tripadvisor/reviews_raw.csv  → fact_reviews (venue key resolved to id_venue)
  - data_raw/tourism/dubai_visitor_stats.csv → tourism_stats

Run with: anaconda3 python scripts/05_build_database.py
"""

import os
import math
import pymysql
import pandas as pd
from dotenv import load_dotenv

# =============================================================================
# CONFIG
# =============================================================================

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST", "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", 3306)),
    "user":     os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "charset":  "utf8mb4",
}
DB_NAME = os.getenv("MYSQL_DATABASE", "audience_to_stage")

CSV_VENUES   = "data_manual/competition_profiles.csv"
CSV_REVIEWS  = "data_raw/tripadvisor/reviews_raw.csv"
CSV_TOURISM  = "data_raw/tourism/dubai_visitor_stats.csv"


# =============================================================================
# HELPERS
# =============================================================================

def none_if_nan(value):
    """Convert NaN / float nan to None so pymysql sends SQL NULL."""
    if value is None:
        return None
    try:
        if math.isnan(float(value)):
            return None
    except (TypeError, ValueError):
        pass
    return value


def connect_no_db():
    """Open a connection without selecting a database (needed to CREATE it)."""
    return pymysql.connect(**DB_CONFIG)


def connect_db():
    """Open a connection with the target database selected."""
    return pymysql.connect(**DB_CONFIG, database=DB_NAME)


# =============================================================================
# SETUP
# =============================================================================

def create_database(cursor):
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    print(f"[OK] Database '{DB_NAME}' ready.")


def create_tables(cursor):
    # DROP + CREATE ensures schema is always current when columns change
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("DROP TABLE IF EXISTS fact_reviews;")
    cursor.execute("DROP TABLE IF EXISTS dim_venue;")
    cursor.execute("DROP TABLE IF EXISTS tourism_stats;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    cursor.execute("""
        CREATE TABLE dim_venue (
            id_venue            INT AUTO_INCREMENT PRIMARY KEY,
            venue_key           VARCHAR(50),
            show_name           VARCHAR(100),
            venue_type          VARCHAR(50),
            format              VARCHAR(50),
            location_district   VARCHAR(100),
            years_active        INT,
            ticket_price_usd    FLOAT,
            tripadvisor_reviews INT,
            tripadvisor_rating  FLOAT,
            visual_register     INT,
            cultural_barriers   INT,
            sensory_intensity   INT,
            music_style         VARCHAR(100),
            audience_profile    VARCHAR(100),
            conflict_resilience VARCHAR(20),
            producer            VARCHAR(150),
            artistic_director   VARCHAR(100),
            estilo_show         VARCHAR(50),
            estilo_movimiento   VARCHAR(200),
            registro_corporal   VARCHAR(100),
            relacion_publico    VARCHAR(50),
            carga_erotica       VARCHAR(50),
            referente_cultural  VARCHAR(200),
            nivel_habilidad     VARCHAR(50),
            paleta_vestuario    VARCHAR(200),
            diseno_vestuario    VARCHAR(200),
            estilo_musical      VARCHAR(200)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_reviews (
            id_review    INT AUTO_INCREMENT PRIMARY KEY,
            id_venue     INT,
            reviewer     VARCHAR(100),
            location     VARCHAR(100),
            review_date  VARCHAR(50),
            trip_type    VARCHAR(50),
            rating       INT,
            review_text  TEXT,
            source_status VARCHAR(20),
            source       VARCHAR(50),
            FOREIGN KEY (id_venue) REFERENCES dim_venue(id_venue)
        ) ENGINE=InnoDB;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tourism_stats (
            id_stat       INT AUTO_INCREMENT PRIMARY KEY,
            year          INT,
            country       VARCHAR(100),
            region        VARCHAR(100),
            visitor_count FLOAT,
            percentage    VARCHAR(10),
            granularity   VARCHAR(20),
            source        VARCHAR(100)
        ) ENGINE=InnoDB;
    """)

    print("[OK] Tables dim_venue, fact_reviews, tourism_stats ready.")


# =============================================================================
# LOADERS
# =============================================================================

def load_dim_venue(cursor):
    """Load competition_profiles.csv → dim_venue."""
    df = pd.read_csv(CSV_VENUES, encoding="utf-8")

    sql = """
        INSERT INTO dim_venue (
            venue_key, show_name, venue_type, format,
            location_district, years_active, ticket_price_usd,
            tripadvisor_reviews, tripadvisor_rating,
            visual_register, cultural_barriers, sensory_intensity,
            music_style, audience_profile, conflict_resilience,
            producer, artistic_director,
            estilo_show, estilo_movimiento, registro_corporal,
            relacion_publico, carga_erotica, referente_cultural,
            nivel_habilidad, paleta_vestuario, diseno_vestuario,
            estilo_musical
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s
        )
    """

    rows = 0
    for _, row in df.iterrows():
        cursor.execute(sql, (
            none_if_nan(row.get("venue_key")),
            none_if_nan(row.get("show_name")),
            none_if_nan(row.get("venue_type")),
            none_if_nan(row.get("format")),
            none_if_nan(row.get("location_district")),
            none_if_nan(row.get("years_active")),
            none_if_nan(row.get("ticket_price_usd")),
            none_if_nan(row.get("tripadvisor_reviews")),
            none_if_nan(row.get("tripadvisor_rating")),
            none_if_nan(row.get("visual_register")),
            none_if_nan(row.get("cultural_barriers")),
            none_if_nan(row.get("sensory_intensity")),
            none_if_nan(row.get("music_style")),
            none_if_nan(row.get("audience_profile")),
            none_if_nan(row.get("conflict_resilience")),
            none_if_nan(row.get("producer")),
            none_if_nan(row.get("artistic_director")),
            none_if_nan(row.get("estilo_show")),
            none_if_nan(row.get("estilo_movimiento")),
            none_if_nan(row.get("registro_corporal")),
            none_if_nan(row.get("relacion_publico")),
            none_if_nan(row.get("carga_erotica")),
            none_if_nan(row.get("referente_cultural")),
            none_if_nan(row.get("nivel_habilidad")),
            none_if_nan(row.get("paleta_vestuario")),
            none_if_nan(row.get("diseno_vestuario")),
            none_if_nan(row.get("estilo_musical")),
        ))
        rows += 1

    return rows


def load_fact_reviews(cursor):
    """Load reviews_raw.csv → fact_reviews, resolving venue_key → id_venue."""
    df = pd.read_csv(CSV_REVIEWS, encoding="utf-8")

    # Build lookup: venue_key → id_venue from what we just inserted
    cursor.execute("SELECT id_venue, venue_key FROM dim_venue;")
    venue_map = {row[1]: row[0] for row in cursor.fetchall()}

    sql = """
        INSERT INTO fact_reviews (
            id_venue, reviewer, location, review_date,
            trip_type, rating, review_text, source_status, source
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    rows = 0
    skipped = 0
    for _, row in df.iterrows():
        venue_key = none_if_nan(row.get("venue"))
        id_venue  = venue_map.get(venue_key)

        if id_venue is None:
            # venue_key not found in dim_venue — log and skip
            skipped += 1
            print(f"  [WARN] Unknown venue_key '{venue_key}' in reviews — row skipped.")
            continue

        cursor.execute(sql, (
            id_venue,
            none_if_nan(row.get("reviewer")),
            none_if_nan(row.get("location")),
            none_if_nan(row.get("date")),       # CSV column is 'date'
            none_if_nan(row.get("trip_type")),
            none_if_nan(row.get("rating")),
            none_if_nan(row.get("review_text")),
            none_if_nan(row.get("source_status")),
            none_if_nan(row.get("source")),
        ))
        rows += 1

    if skipped:
        print(f"  [INFO] {skipped} review(s) skipped (venue_key not in dim_venue).")

    return rows


def load_tourism_stats(cursor):
    """Load dubai_visitor_stats.csv → tourism_stats."""
    df = pd.read_csv(CSV_TOURISM, encoding="utf-8")

    if df.empty:
        print("  [INFO] tourism CSV is empty — no rows to insert. Manual entry needed.")
        return 0

    # Flexible column mapping: the PDF extractor creates varied column names
    # Expected columns (from 02_extract_tourism.py): year, month, nationality,
    # visitor_count, granularity, source_page — but may differ if extracted from tables.
    col_map = {
        "nationality": "country",
        "source_page": "source",
    }
    df = df.rename(columns=col_map)

    # Ensure expected columns exist (fill with None if missing)
    for col in ["year", "country", "region", "visitor_count", "percentage", "granularity", "source"]:
        if col not in df.columns:
            df[col] = None

    sql = """
        INSERT INTO tourism_stats (
            year, country, region, visitor_count,
            percentage, granularity, source
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    rows = 0
    for _, row in df.iterrows():
        cursor.execute(sql, (
            none_if_nan(row.get("year")),
            none_if_nan(row.get("country")),
            none_if_nan(row.get("region")),
            none_if_nan(row.get("visitor_count")),
            none_if_nan(row.get("percentage")),
            none_if_nan(row.get("granularity")),
            none_if_nan(str(row.get("source")) if row.get("source") is not None else None),
        ))
        rows += 1

    return rows


# =============================================================================
# MAIN
# =============================================================================

def run():
    print("=" * 60)
    print("Phase 3 — Building MySQL database")
    print("=" * 60)

    # --- Step 1: create database ---
    try:
        conn = connect_no_db()
        with conn.cursor() as cur:
            create_database(cur)
        conn.commit()
        conn.close()
    except pymysql.Error as e:
        print(f"[ERROR] Could not connect or create database: {e}")
        raise

    # --- Step 2: create tables ---
    try:
        conn = connect_db()
        with conn.cursor() as cur:
            create_tables(cur)
        conn.commit()
    except pymysql.Error as e:
        print(f"[ERROR] Could not create tables: {e}")
        conn.close()
        raise

    # --- Step 3: load data ---
    try:
        with conn.cursor() as cur:
            print("\nLoading dim_venue...")
            n_venues = load_dim_venue(cur)
            conn.commit()
            print(f"  -> {n_venues} rows inserted into dim_venue.")

            print("\nLoading fact_reviews...")
            n_reviews = load_fact_reviews(cur)
            conn.commit()
            print(f"  -> {n_reviews} rows inserted into fact_reviews.")

            print("\nLoading tourism_stats...")
            n_stats = load_tourism_stats(cur)
            conn.commit()
            print(f"  -> {n_stats} rows inserted into tourism_stats.")

    except FileNotFoundError as e:
        print(f"[ERROR] CSV file not found: {e}")
        raise
    except pymysql.Error as e:
        print(f"[ERROR] Database error during load: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

    # --- Summary ---
    print("\n" + "=" * 60)
    print("LOAD COMPLETE")
    print(f"  dim_venue      : {n_venues} rows")
    print(f"  fact_reviews   : {n_reviews} rows")
    print(f"  tourism_stats  : {n_stats} rows")
    print("=" * 60)


if __name__ == "__main__":
    run()
