markdown# audience-to-stage

> Can the rotation of tourism in a city inform  
> the detailed design of a live entertainment show?  
> How far? In what ways? What would that be worth?

## The Question

Live entertainment shows are typically designed once 
and run unchanged for months or years. Yet the 
audience in front of them changes constantly — by 
nationality, travel purpose, group composition, 
cultural background, and season.

This project asks: if we can measure and model that 
rotation, can we use it to make better artistic and 
programming decisions? And if so, which decisions 
exactly — and how?

The hypothesis is that tourism data is not just a 
market sizing tool. It is a design brief.

## What This Analysis Could Change

| Artistic Element | Data Input | Decision |
|-----------------|------------|----------|
| Music style and references | Dominant nationality by season | Rotate setlist or live repertoire |
| MC language and interaction | Visitor language profile | Adjust performer briefing |
| Sensory intensity | Group type (families vs couples vs solo) | Modulate show pacing |
| Cultural references | Origin market cultural profile | Include or avoid specific content |
| Show duration | Average length of stay + evening behavior | Optimize runtime |
| Pricing strategy | Spend profile by nationality | Segment ticket tiers |

## Why This Matters

Most producers make artistic decisions based on 
instinct, tradition, or a single audience profile 
snapshot. This project builds the infrastructure to 
make those decisions from data — systematically, 
seasonally, and at scale.

A show that adapts to its audience without losing 
its identity is more commercially resilient and 
creatively stronger.

## Data Sources

| Source | Content | Method |
|--------|---------|--------|
| Dubai DET Annual Visitor Report 2024 | Visitor volume, nationality mix, purpose, spend, behavior | PDF extraction + Python |
| TripAdvisor (competitor venues) | Customer reviews, ratings, sentiment by nationality | Web scraping + Python |
| Manual competition profiles | Format, pricing, capacity, cultural positioning | Qualitative research |
| MySQL database | Structured storage for all processed datasets | SQL queries |

## Competitor Venues Analyzed

- La Perle by Dragone — market benchmark, 9 years, 
  universal cultural accessibility, 1,300 capacity
- Billionaire Dubai — dinner-show, CIS and expat audience
- Dream Dubai — 5.0 rating, 1,829 reviews, 
  dominant Russian-speaking audience

## Project Structure
audience-to-stage/
│
├── data_raw/
│   ├── tripadvisor/       # Scraped reviews
│   └── tourism/           # DET Annual Report + extracted CSV
│
├── data_processed/        # Cleaned and structured outputs
│
├── data_manual/           # Qualitative competition profiles
│
├── scripts/
│   ├── 01_scraper_reviews.py
│   ├── 02_extract_tourism.py
│   ├── 03_parse_browser_reviews.py
│   └── 04_build_competition_profiles.py
│
├── sql/                   # MySQL queries and schema
├── tableau/               # Workbooks and exports
├── .env.example
├── requirements.txt
└── README.md

## Stack

Python (Pandas, BeautifulSoup, pdfplumber) · 
MySQL · Tableau · Jupyter Notebook · GitHub

## Pipeline

1. Extract tourism statistics from DET PDF
2. Scrape and parse competitor reviews from TripAdvisor
3. Build qualitative competition profiles
4. Load all datasets into MySQL
5. Query seasonal and demographic patterns via SQL
6. Visualize findings and recommendations in Tableau

## Key Questions the Analysis Will Answer

- Which nationalities dominate Dubai's entertainment 
  audience by season?
- Which competitor formats attract which audience profiles?
- What elements of show design correlate with higher 
  satisfaction across different cultural groups?
- What is the optimal show design brief for each 
  seasonal audience window?

## Data Limitations

**Gap de datos turísticos 2020:** tourism_stats no contiene datos de visitantes para 2020 debido al cierre de fronteras de Dubai durante la pandemia COVID-19. Las reseñas de ese año están presentes pero sin contexto turístico asociado. Fuente: DET Annual Visitor Report 2024.

## Status

Data collection and pipeline complete.  
SQL schema and Tableau dashboards in progress.

## Author
Ela Ruiz
Data Analyst · Python + MySQL + Tableau  
Project personal · 2025–2026
