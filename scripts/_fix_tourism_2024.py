"""Update tourism_stats 2024 rows with calculated visitor_count from PDF total (18.72M)."""
import pymysql, pandas as pd

TOTAL_2024 = 18_720_000  # DET Annual Visitor Report 2024

conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234',
                       database='audience_to_stage', charset='utf8mb4')

with conn.cursor() as cur:
    cur.execute("SELECT * FROM tourism_stats WHERE year = 2024")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

df = pd.DataFrame(rows, columns=cols)
print("Current 2024 rows:")
print(df.to_string(index=False))

# Calculate visitor_count from percentage
df["pct_float"] = df["percentage"].str.replace("%", "").astype(float) / 100
df["visitor_count_calc"] = (df["pct_float"] * TOTAL_2024).round(0).astype(int)
pct_total = df["pct_float"].sum()
print(f"\nPercentages sum: {pct_total*100:.0f}%  (remaining {(1-pct_total)*100:.0f}% = Other/Americas/etc.)")
print(f"\nCalculated visitor counts (based on 18.72M total):")
print(df[["country", "percentage", "visitor_count_calc"]].to_string(index=False))

# Update visitor_count in MySQL for each 2024 row
with conn.cursor() as cur:
    for _, row in df.iterrows():
        cur.execute(
            "UPDATE tourism_stats SET visitor_count = %s WHERE id_stat = %s",
            (int(row["visitor_count_calc"]), int(row["id_stat"]))
        )
    conn.commit()
    print(f"\nUpdated {len(df)} rows in tourism_stats.")

    # Verify
    cur.execute("SELECT year, SUM(visitor_count) AS total FROM tourism_stats GROUP BY year ORDER BY year")
    for r in cur.fetchall():
        print(f"  year {r[0]}: SUM(visitor_count) = {r[1]:,}")

conn.close()
