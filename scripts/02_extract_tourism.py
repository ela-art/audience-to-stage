import pdfplumber
import pandas as pd

PDF_PATH = "data_raw/tourism/det-annual-visitor-report-2024.pdf"
OUTPUT_PATH = "data_raw/tourism/dubai_visitor_stats.csv"


def extract_tables(pdf_path):
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table in tables:
                if not table or not table[0]:
                    continue
                df = pd.DataFrame(table[1:], columns=table[0])
                df["source_page"] = page_num
                all_tables.append(df)

    if not all_tables:
        # El PDF usa tablas como imagen — pdfplumber no puede leerlas
        # Creamos CSV vacío con estructura esperada para no romper el pipeline
        print("WARNING: No tables found. PDF may be image-based. Manual entry needed.")
        pd.DataFrame(columns=["year", "month", "nationality", "visitor_count", "granularity", "source_page"]) \
            .to_csv(OUTPUT_PATH, index=False)
        return

    combined = pd.concat(all_tables, ignore_index=True)
    combined["granularity"] = "annual"
    combined.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Extracted {len(combined)} rows → {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_tables(PDF_PATH)
