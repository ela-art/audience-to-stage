"""
Phase 6 — Statistical correlation analysis.

Tests the core hypothesis: does annual tourism volume correlate with
audience sentiment and satisfaction scores across Dubai entertainment venues?

Methods:
  - Pearson r  : linear correlation (assumes normal distribution)
  - Spearman r : rank-based correlation (non-parametric, robust to small samples)

Output:
  - Console report with correlation coefficients, p-values, and interpretation
  - data/tableau_exports/correlation_stats.csv

Run with: anaconda3 python scripts/09_correlation_analysis.py
"""

import os
import pymysql
import pandas as pd
from scipy import stats
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

OUTPUT_PATH = "data/tableau_exports/correlation_stats.csv"

ALPHA = 0.05  # significance threshold


def load_data(conn):
    """Annual aggregates per venue joined with tourism totals."""
    sql = """
        SELECT
            LEFT(r.review_date_norm, 4)                 AS year,
            v.venue_name,
            COUNT(*)                                    AS review_count,
            ROUND(AVG(r.sentiment_compound), 4)         AS avg_sentiment,
            ROUND(AVG(r.rating), 4)                     AS avg_rating,
            ROUND(STDDEV(r.rating), 4)                  AS stddev_rating,
            t.total_visitors
        FROM fact_reviews r
        JOIN dim_venue v ON r.id_venue = v.id_venue
        LEFT JOIN (
            SELECT year, SUM(visitor_count) AS total_visitors
            FROM tourism_stats
            GROUP BY year
        ) t ON CAST(LEFT(r.review_date_norm, 4) AS UNSIGNED) = t.year
        WHERE r.review_date_norm IS NOT NULL
          AND t.total_visitors IS NOT NULL
        GROUP BY LEFT(r.review_date_norm, 4), v.venue_name, t.total_visitors
        ORDER BY year, v.venue_name
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    df["year"]           = df["year"].astype(int)
    df["total_visitors"] = df["total_visitors"].astype(float)
    df["avg_sentiment"]  = df["avg_sentiment"].astype(float)
    df["avg_rating"]     = df["avg_rating"].astype(float)
    df["stddev_rating"]  = df["stddev_rating"].astype(float)
    df["review_count"]   = df["review_count"].astype(int)
    return df


def run_correlation(x, y, label_x, label_y, df_label="all venues"):
    """Run Pearson and Spearman, print results, return dict."""
    if len(x) < 3:
        print(f"  [SKIP] {label_y} — too few data points (n={len(x)})")
        return None

    p_r, p_pval = stats.pearsonr(x, y)
    s_r, s_pval = stats.spearmanr(x, y)

    def sig(pval):
        if pval < 0.01:  return "** (p<0.01)"
        if pval < 0.05:  return "*  (p<0.05)"
        if pval < 0.10:  return ".  (p<0.10)"
        return "   (not significant)"

    def strength(r):
        r = abs(r)
        if r >= 0.7: return "strong"
        if r >= 0.4: return "moderate"
        if r >= 0.2: return "weak"
        return "negligible"

    print(f"\n  {label_x} vs {label_y} [{df_label}] (n={len(x)})")
    print(f"    Pearson  r={p_r:+.3f}  p={p_pval:.4f} {sig(p_pval)}  [{strength(p_r)}]")
    print(f"    Spearman r={s_r:+.3f}  p={s_pval:.4f} {sig(s_pval)}  [{strength(s_r)}]")

    return {
        "comparison": f"{label_x} vs {label_y}",
        "scope": df_label,
        "n": len(x),
        "pearson_r": round(p_r, 4),
        "pearson_p": round(p_pval, 4),
        "pearson_sig": sig(p_pval).strip(),
        "spearman_r": round(s_r, 4),
        "spearman_p": round(s_pval, 4),
        "spearman_sig": sig(s_pval).strip(),
        "strength": strength(p_r),
    }


def run():
    print("=" * 65)
    print("Phase 6 -- Statistical correlation analysis")
    print("=" * 65)
    print(f"Significance threshold: alpha = {ALPHA}")
    print("Note: years with no tourism data (2020, 2025, 2026) excluded.")

    conn = pymysql.connect(**DB_CONFIG)
    df = load_data(conn)
    conn.close()

    print(f"\n[OK] Loaded {len(df)} venue-year observations (with tourism data).")
    print(df[["year", "venue_name", "review_count", "avg_sentiment",
              "avg_rating", "total_visitors"]].to_string(index=False))

    results = []

    # --- 1. All venues pooled ---
    print("\n" + "-" * 65)
    print("1. POOLED — all venues combined")
    print("-" * 65)

    r = run_correlation(df["total_visitors"], df["avg_sentiment"],
                        "Total Visitors", "Avg Sentiment", "all venues")
    if r: results.append(r)

    r = run_correlation(df["total_visitors"], df["avg_rating"],
                        "Total Visitors", "Avg Rating", "all venues")
    if r: results.append(r)

    # --- 2. Per venue ---
    print("\n" + "-" * 65)
    print("2. PER VENUE (only venues with >= 3 year-observations)")
    print("-" * 65)

    for venue, grp in df.groupby("venue_name"):
        grp = grp.sort_values("year")
        short = venue.split(" ")[0]

        r = run_correlation(grp["total_visitors"], grp["avg_sentiment"],
                            "Total Visitors", "Avg Sentiment", short)
        if r: results.append(r)

        r = run_correlation(grp["total_visitors"], grp["avg_rating"],
                            "Total Visitors", "Avg Rating", short)
        if r: results.append(r)

    # --- 3. Review volume vs visitors ---
    print("\n" + "-" * 65)
    print("3. REVIEW VOLUME — do more visitors generate more reviews?")
    print("-" * 65)

    # Aggregate by year across all venues
    by_year = df.groupby("year").agg(
        total_reviews=("review_count", "sum"),
        total_visitors=("total_visitors", "first")
    ).reset_index()

    r = run_correlation(by_year["total_visitors"], by_year["total_reviews"],
                        "Total Visitors", "Total Reviews", "all venues by year")
    if r: results.append(r)

    # --- Save CSV ---
    os.makedirs("data/tableau_exports", exist_ok=True)
    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_PATH, sep=";", decimal=",", index=False, encoding="utf-8")

    # --- Summary ---
    print("\n" + "=" * 65)
    print("CORRELATION SUMMARY")
    print("=" * 65)
    sig_results = [r for r in results if r and r["pearson_p"] < ALPHA]
    print(f"Significant results (p < {ALPHA}): {len(sig_results)} of {len(results)}")
    for r in results:
        if r:
            flag = "* SIG" if r["pearson_p"] < ALPHA else "  n.s."
            print(f"  {flag}  {r['comparison']} [{r['scope']}]  "
                  f"Pearson r={r['pearson_r']:+.3f} p={r['pearson_p']:.3f}  "
                  f"Spearman r={r['spearman_r']:+.3f} p={r['spearman_p']:.3f}")

    print(f"\n[OK] Results saved -> {OUTPUT_PATH}")
    print("=" * 65)


if __name__ == "__main__":
    run()
