# audience-to-stage

> **Can the rotation of tourism in a city inform the design of a live entertainment show?**  
> How far? In what ways? What would that be worth?

A data analysis portfolio project exploring the relationship between Dubai's tourism cycles and the design, perception, and competitive positioning of live entertainment shows.

---

## Business Question

Live entertainment shows are typically designed once and run unchanged for months or years. Yet the audience changes constantly — by nationality, travel purpose, group composition, cultural background, and season.

This project asks: **if we can measure and model that rotation, can we use it to make better artistic and programming decisions?**

The hypothesis is that tourism data is not just a market sizing tool. It is a design brief.

| Artistic Element | Data Input | Decision |
|---|---|---|
| Music style and references | Dominant nationality by season | Rotate setlist or live repertoire |
| MC language and interaction | Visitor language profile | Adjust performer briefing |
| Sensory intensity | Group type (families vs couples vs solo) | Modulate show pacing |
| Cultural references | Origin market cultural profile | Include or avoid specific content |
| Pricing strategy | Spend profile by nationality | Segment ticket tiers |

---

## Stack

| Layer | Tools |
|---|---|
| Data extraction | Python · pdfplumber · BeautifulSoup · requests |
| Data processing | Pandas · langdetect · vaderSentiment |
| Storage | MySQL 8.0 · pymysql · python-dotenv |
| Analysis exports | SQL queries · CSV |
| Visualization | Tableau Desktop Public |
| Version control | Git · GitHub |
| AI-assisted development | Claude by Anthropic |

Python environment: Anaconda 3 · Windows

---

## Project Structure

```
audience-to-stage/
│
├── data_raw/
│   ├── tripadvisor/
│   │   └── reviews_raw.csv          # 136 competitor reviews (gitignored)
│   └── tourism/
│       ├── dubai_visitor_stats.csv  # Curated tourism stats (gitignored)
│       └── det-annual-visitor-report-2024.pdf
│
├── data_processed/
│   └── reviews_enriched.csv         # 136 rows with sentiment + language (gitignored)
│
├── data_manual/
│   └── competition_profiles.csv     # 4 venues, 31 qualitative attributes
│
├── data/
│   └── tableau_exports/             # CSVs for Tableau (gitignored)
│       ├── sentiment_over_time.csv
│       ├── rating_distribution.csv
│       ├── reviews_vs_tourism.csv
│       ├── competition_profiles.csv
│       └── correlation_tourism_sentiment.csv
│
├── dashboards/                      # Tableau workbooks (.twbx)
│
├── scripts/
│   ├── 01_scraper_reviews.py        # TripAdvisor scraper (blocked in production — see Limitations)
│   ├── 02_extract_tourism.py        # PDF table extractor (image-based PDF — see Limitations)
│   ├── 03_parse_browser_reviews.py  # Manual review loader (proxy source)
│   ├── 04_build_competition_profiles.py  # Qualitative venue profiles
│   ├── 05_build_database.py         # MySQL star schema + CSV loader
│   ├── 06_clean_enrich.py           # Date normalization, language detection, VADER sentiment
│   ├── 07_export_tableau.py         # Export analysis CSVs for Tableau
│   ├── 07_load_dim_venue.py         # Utility: reload dim_venue without touching fact_reviews
│   └── _*.py                        # Session utilities (audit, restore, fix scripts)
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Pipeline

### Phase 1 — Data Collection
**Script:** `01_scraper_reviews.py`, `03_parse_browser_reviews.py`

TripAdvisor blocks automated scraping (HTTP 403). Reviews were collected via browser for 4 competitor venues and loaded through `03_parse_browser_reviews.py`. Total: **136 reviews** across La Perle (30), Billionaire Dubai (44), Dream Dubai (10), The Theater / Fairmont Dubai (52).

### Phase 2 — Competition Profiles
**Script:** `04_build_competition_profiles.py`

Manual qualitative profiling of 4 competitor venues. **31 attributes** per venue including: show format, movement style, sensory intensity, cultural barriers, erotic charge, audience relationship, costume palette, skill level, artistic director, and TripAdvisor metrics.

### Phase 3 — Database
**Script:** `05_build_database.py`

MySQL star schema with 3 tables:
- `dim_venue` — 4 venues, 31 columns
- `fact_reviews` — 136 rows with FK to dim_venue
- `tourism_stats` — 35 rows, 2021–2024 annual data by region

### Phase 4 — Enrichment
**Script:** `06_clean_enrich.py`

For each review:
- Date normalization (`"Feb 2024"` → `"2024-02"`)
- Language detection via `langdetect` (seed=0 for reproducibility)
- Audience region inference from ISO language code
- VADER sentiment analysis (compound score + label)

Result: 0 NULLs in any enriched column across 136 reviews.

### Phase 5 — Tableau Exports
**Script:** `07_export_tableau.py`

5 analysis-ready CSVs exported with Spanish regional settings (`sep=";"`, `decimal=","`):
- `sentiment_over_time.csv` — avg sentiment + rating by venue × month (69 rows)
- `rating_distribution.csv` — rating counts by venue (12 rows)
- `reviews_vs_tourism.csv` — reviews + annual visitor totals by venue × month (69 rows)
- `competition_profiles.csv` — full qualitative comparison table (4 rows)
- `correlation_tourism_sentiment.csv` — annual aggregate for scatter analysis (17 rows)

---

## Key Findings

### Sentiment by venue
| Venue | Avg sentiment | Avg rating | Reviews | Stddev rating |
|---|---|---|---|---|
| Dream Dubai | +0.844 | 5.00 | 10 | 0.00 |
| Billionaire Dubai | +0.737 | 4.61 | 44 | 1.09 |
| The Theater (Fairmont) | +0.592 | 3.85 | 52 | **1.68** |
| La Perle by Dragone | +0.523 | 4.33 | 30 | 1.37 |

**The Theater** is the most polarizing venue: highest rating variance and highest share of negative reviews (17%). This points to a gap between artistic ambition (elite skill level, immersive format) and execution consistency.

**La Perle** has the lowest VADER sentiment despite being the market benchmark — VADER underweights spectacle language ("breathtaking", "stunning") that is descriptive rather than emotional.

### Seasonality
Reviews from November–February (Dubai high season, cooler months) have consistently higher sentiment (+0.748 to +0.848). September is the lowest (+0.353), coinciding with the end of summer and a transition in visitor profile.

### Tourism correlation
Review volume tracks annual visitor totals. The 2023 peak (17.15M international visitors) coincides with the highest review volume in the dataset (280 reviews across venues in that calendar year). The relationship is directional but not linear — sample sizes per venue are too small for statistical significance.

### Competitive positioning
| Dimension | La Perle | Billionaire | Dream Dubai | The Theater |
|---|---|---|---|---|
| Format | Dedicated theater | Dinner/nightclub | Dinner show | Dinner show |
| Cultural barriers | 1 (universal) | 2 | 1 | 2 |
| Audience relationship | Contemplative | Contemplative | **Immersive** | **Immersive** |
| Skill level | **Elite** | Professional | Professional | **Elite** |
| Erotic charge | Neutral | Suggestive | Suggestive | Suggestive |

The Theater is the only venue that combines elite skill + immersive format + dinner show, making it the most direct competitor in terms of artistic ambition — yet it has the lowest satisfaction scores.

---

## Known Limitations

**1. TripAdvisor scraping blocked**
`01_scraper_reviews.py` returns HTTP 403 on all requests. All 136 reviews were collected manually via browser. The scraper script is included for reference and pipeline documentation but does not produce data in practice.

**2. PDF tourism extraction**
The DET Annual Visitor Report PDF uses image-based tables. `02_extract_tourism.py` cannot extract structured data from it. Tourism statistics were manually curated from the report and entered into `dubai_visitor_stats.csv`.

**3. Tourism data gap — 2020 (COVID-19)**
`tourism_stats` contains no visitor data for 2020. Dubai closed its borders during the pandemic. Reviews from that year are present in `fact_reviews` but have no associated tourism context.

**4. Tourism data gap — 2025 and 2026**
No official visitor statistics are available yet for 2025–2026. Reviews collected in those years have NULL in `total_visitors` in the tourism join.

**5. Tourism data is annual, not monthly**
`tourism_stats` provides annual aggregates by region. Monthly granularity is not available. The join to `fact_reviews` by year approximates seasonal context but cannot reflect month-by-month visitor fluctuations.

**6. All reviews in English**
TripAdvisor displays machine-translated English for non-English reviews. `langdetect` correctly identifies all 136 as English, but the original language and cultural nuance of reviews from Russian, Arabic, or Hindi speakers is lost. VADER sentiment is calibrated for English.

**7. Small sample sizes**
Dream Dubai has only 10 reviews. Its 5.0 average rating and 0.00 stddev are artifacts of sample size, not statistical robustness. All findings should be treated as directional signals, not statistically significant results.

**8. Schema partially managed outside main script**
`05_build_database.py` creates the base schema. Four additional columns (`venue_name`, `producer_relation`, `audience_capacity`, `notes`) were added later via `07_load_dim_venue.py`. Running `05_build_database.py` alone produces an incomplete schema.

---

## How to Reproduce

### Prerequisites
- Python 3.10+ (Anaconda recommended)
- MySQL 8.0
- Tableau Desktop or Tableau Public

### Install dependencies
```bash
pip install pymysql pandas python-dotenv langdetect vaderSentiment pdfplumber beautifulsoup4 requests
```

### Configure credentials
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### Run the pipeline
```bash
# Phase 2 — Competition profiles
python scripts/04_build_competition_profiles.py

# Phase 3 — Build database
python scripts/05_build_database.py

# Phase 4 — Enrich reviews
python scripts/06_clean_enrich.py

# Phase 5 — Export for Tableau
python scripts/07_export_tableau.py
```

> **Note:** `01_scraper_reviews.py` is blocked by TripAdvisor. `02_extract_tourism.py` requires a text-based PDF. Both scripts are included for transparency. The data they would produce is already loaded in the pipeline via `reviews_raw.csv` and `dubai_visitor_stats.csv`.

### Database connection
```
Host:     localhost
Port:     3306
Database: audience_to_stage
Tables:   dim_venue, fact_reviews, tourism_stats
```

---

## Status

| Phase | Status |
|---|---|
| Data collection (reviews + tourism) | Complete |
| Competition profiles | Complete |
| MySQL star schema | Complete |
| Enrichment (sentiment, language, dates) | Complete |
| Tableau dashboard | Complete |
| Written analysis and conclusions | Complete |

---

## Author

**Ela Ruiz**  
Data Analyst · Python + MySQL + Tableau  
Personal portfolio project · 2025–2026
