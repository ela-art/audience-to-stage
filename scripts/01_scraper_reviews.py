import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

VENUES = {
    "show_subject": {
        "url": "https://www.tripadvisor.com/Hotel_Review-[undisclosed]",
        # Filter hotel reviews mentioning the show — only available proxy source for this venue
        "keywords": ["show", "performance", "stage", "dance", "entertainment", "cabaret"]
    },
    "billionaire": {
        "url": "https://www.tripadvisor.com/Restaurant_Review-g295424-d10397710-Reviews-Billionaire_Dubai-Dubai_Emirate_of_Dubai.html",
        "keywords": []
    },
    "la_perle": {
        "url": "https://www.tripadvisor.com/Attraction_Review-g295424-d14579966-Reviews-La_Perle_by_Dragone-Dubai_Emirate_of_Dubai.html",
        "keywords": []
    },
    "the_theater": {
        "url": "https://www.tripadvisor.com/Restaurant_Review-g295424-d23483292-Reviews-The_Theater-Dubai_Emirate_of_Dubai.html",
        "keywords": []
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_venue(venue_name, config, max_pages=5):
    reviews = []
    status = "complete"

    for page in range(max_pages):
        url = config["url"] if page == 0 else config["url"].replace("-Reviews-", f"-Reviews-or{page * 10}-")

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", {"data-automation": "reviewCard"})

            if not cards:
                # TripAdvisor nos bloqueó o llegamos al final — marcamos como parcial
                status = "partial"
                break

            for card in cards:
                text_el = card.find("span", {"data-automation": "reviewText"})
                rating_el = card.find("svg", {"aria-label": True})
                date_el = card.find("div", {"data-automation": "reviewedDate"})

                text = text_el.get_text(strip=True) if text_el else ""
                if not text:
                    continue

                # For subject show: skip hotel reviews that don't mention the show
                # Descartamos reseñas del hotel que hablen solo de habitaciones o playa
                if config["keywords"] and not any(kw in text.lower() for kw in config["keywords"]):
                    continue

                reviews.append({
                    "venue": venue_name,
                    "review_text": text,
                    "rating_raw": rating_el["aria-label"] if rating_el else None,
                    "review_date": date_el.get_text(strip=True) if date_el else None,
                    "source_status": status
                })

            # Pausa aleatoria — imitar comportamiento humano para evitar bloqueo
            time.sleep(random.uniform(2, 5))

        except requests.RequestException as e:
            print(f"[{venue_name}] Failed on page {page}: {e}")
            status = "partial"
            break

    return reviews, status


def run():
    all_reviews = []

    for name, config in VENUES.items():
        print(f"Scraping {name}...")
        reviews, status = scrape_venue(name, config)
        all_reviews.extend(reviews)
        print(f"  {len(reviews)} reviews | status: {status}")

    df = pd.DataFrame(all_reviews)
    df.to_csv("data_raw/tripadvisor/reviews_raw.csv", index=False, encoding="utf-8")
    print(f"\nDone. {len(df)} total reviews saved.")


if __name__ == "__main__":
    run()
