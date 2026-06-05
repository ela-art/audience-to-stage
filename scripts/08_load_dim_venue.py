"""Utility: reload dim_venue from competition_profiles.csv (no other tables touched)."""
import pymysql, pandas as pd, math

df = pd.read_csv("data_manual/competition_profiles.csv", encoding="utf-8")
print(f"CSV rows: {len(df)} | Columns: {list(df.columns)}")

conn = pymysql.connect(
    host="localhost", port=3306, user="root",
    password="root1234", database="audience_to_stage", charset="utf8mb4"
)

def none_if_nan(v):
    if v is None:
        return None
    try:
        if isinstance(v, float) and math.isnan(v):
            return None
    except Exception:
        pass
    return v

with conn.cursor() as cur:
    # Add missing columns if needed
    cur.execute("""
        SELECT COLUMN_NAME FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'audience_to_stage' AND TABLE_NAME = 'dim_venue'
    """)
    existing_cols = {r[0] for r in cur.fetchall()}
    missing = [
        ("venue_name",       "VARCHAR(150)"),
        ("producer_relation","VARCHAR(50)"),
        ("audience_capacity","INT"),
        ("notes",            "TEXT"),
    ]
    for col_name, col_type in missing:
        if col_name not in existing_cols:
            cur.execute(f"ALTER TABLE dim_venue ADD COLUMN `{col_name}` {col_type}")
            print(f"  [ALTER] Added column: {col_name}")
        else:
            print(f"  [SKIP]  Column exists: {col_name}")
    conn.commit()

    # Check which venue_keys already exist
    cur.execute("SELECT venue_key FROM dim_venue")
    existing_keys = {r[0] for r in cur.fetchall()}

    cols = list(df.columns)
    non_key_cols = [c for c in cols if c != "venue_key"]

    updated = 0
    inserted = 0
    for _, row in df.iterrows():
        vk = row["venue_key"]
        if vk in existing_keys:
            set_clause = ", ".join(f"`{c}` = %s" for c in non_key_cols)
            vals = tuple(none_if_nan(row[c]) for c in non_key_cols) + (vk,)
            cur.execute(f"UPDATE dim_venue SET {set_clause} WHERE venue_key = %s", vals)
            updated += 1
        else:
            cur.execute("""
                INSERT INTO dim_venue (
                    venue_key, show_name, venue_name, producer, artistic_director,
                    producer_relation, format, venue_type, location_district,
                    years_active, ticket_price_usd, audience_capacity,
                    tripadvisor_reviews, tripadvisor_rating,
                    visual_register, cultural_barriers, sensory_intensity,
                    music_style, audience_profile, conflict_resilience,
                    estilo_show, estilo_movimiento, registro_corporal,
                    relacion_publico, carga_erotica, referente_cultural,
                    nivel_habilidad, paleta_vestuario, diseno_vestuario,
                    estilo_musical, notes
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, tuple(none_if_nan(row[c]) for c in cols))
            inserted += 1

    conn.commit()
    print(f"Updated: {updated} | Inserted: {inserted} rows in dim_venue")

    cur.execute("SELECT COUNT(*) FROM audience_to_stage.dim_venue")
    count = cur.fetchone()[0]
    print(f"SELECT COUNT(*) FROM dim_venue -> {count}")

conn.close()
