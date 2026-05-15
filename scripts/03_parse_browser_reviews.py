"""
Parse reviews extracted manually from browser and save to CSV.
Venues: Billionaire Dubai, La Perle by Dragone, Dream Dubai, Immersive Show Subject (proxy via hotel reviews).
Run with: anaconda3 python scripts/03_parse_browser_reviews.py
"""

import pandas as pd
import os

# =============================================================================
# BILLIONAIRE DUBAI
# Source: https://www.tripadvisor.com/Restaurant_Review-g295424-d10397710
# =============================================================================

BILLIONAIRE_REVIEWS_P1 = [
    {"reviewer": "Oleg Ipatov", "location": "Dubai, UAE", "date": "Feb 2026", "trip_type": "Friends", "rating": 1, "review_text": "A beautiful wrapper with a very inconsistent filling. Food is an absolute gamble. Some dishes amazing, others awful. Show felt like a provincial amateur performance - no unified concept. Interior is the only good thing: brand new, clean, stylish."},
    {"reviewer": "Brox1", "location": "Myrtle Beach, SC, USA", "date": "Feb 2026", "trip_type": "Couples", "rating": 5, "review_text": "Billionaire Dubai delivers a high-gloss, ultra-luxury dining experience blending premium Italian cuisine with theatrical entertainment. Polished service, strong cocktails, lively dinner-show format transitions into late-night party. Ideal for groups seeking a glamorous night out."},
    {"reviewer": "Fra", "location": None, "date": "Dec 2024", "trip_type": "Friends", "rating": 5, "review_text": "Billionaire Dubai is an impressive venue: sophisticated, vibrant and electric. Spectacular performances, great ambiance and attention to every detail. The food was great. This isn't just dinner, this is a night of entertainment and style!"},
    {"reviewer": "Nihed H", "location": None, "date": "Jun 2025", "trip_type": "Friends", "rating": 5, "review_text": "Billionaire combines luxury dining with an electrifying live show — acrobatics, music, and high-end glam. Food is top-tier Italian & Asian fusion, cocktails on point, atmosphere pure elegance. Perfect for a special night."},
    {"reviewer": "Elaheh", "location": None, "date": "May 2025", "trip_type": "Friends", "rating": 5, "review_text": "The place was very luxurious and beautiful, and the music was great. One of the best nightclubs in Dubai in a very beautiful area."},
    {"reviewer": "Sally6", "location": "New Orleans, LA, USA", "date": "Mar 2025", "trip_type": "Couples", "rating": 5, "review_text": "Truly fantastic! The show was very entertaining! The food was delicious with beautiful presentations. Everyone in the audience was dancing and having the best time! The atmosphere was very special!"},
    {"reviewer": "Fabiana R", "location": None, "date": "Apr 2025", "trip_type": "Friends", "rating": 5, "review_text": "High quality cuisine and entertainment. Each dish is served in an elegant and engaging atmosphere. The shows are of the highest level. A unique place!"},
    {"reviewer": "Altynai J", "location": None, "date": "Mar 2025", "trip_type": "Friends", "rating": 5, "review_text": "Great place with beautiful interior, great show and cool DJ. Machine translated from Russian."},
    {"reviewer": "Antonio S", "location": None, "date": "Mar 2025", "trip_type": "Family", "rating": 5, "review_text": "Wonderful venue, exciting show, great food, excellent service and welcome. Machine translated from Italian."},
    {"reviewer": "Sean", "location": "London, UK", "date": "Feb 2025", "trip_type": "Couples", "rating": 5, "review_text": "Unforgettable dining and entertainment experience far exceeding expectations. Staff abundant and attentive. Food delicious Italian/Asian fusion. Entertainment top-notch with variety of talented acts. Atmosphere vibrant with DJ spinning great tunes. Highly recommend."},
    {"reviewer": "s-dacunha", "location": "Houilles, France", "date": "Feb 2025", "trip_type": "Couples", "rating": 5, "review_text": "Spectacular, incredible atmosphere. To be done again as a couple or with friends. Very friendly staff and good meal. Machine translated from French."},
    {"reviewer": "Aziza D", "location": None, "date": "Jan 2025", "trip_type": "Friends", "rating": 4, "review_text": "Club experience with techno & dance music and wide range of other music. Good quality alcohol. Very chic atmosphere with elegant interior."},
    {"reviewer": "Miruna C", "location": None, "date": "Feb 2025", "trip_type": "Friends", "rating": 5, "review_text": "Unique fusion of Italian and contemporary Japanese cuisines complemented by live performances and vibrant atmosphere. Amazing experience with friends."},
    {"reviewer": "Arina Ts", "location": None, "date": "Feb 2025", "trip_type": "Friends", "rating": 5, "review_text": "Place is very beautiful and classy. DJ was amazing and played the best mix."},
    {"reviewer": "Aisha A", "location": None, "date": "Jan 2025", "trip_type": "Friends", "rating": 5, "review_text": "Amazing atmosphere and high service. Had dinner and joined the party, it's a vibe. Highly recommended."},
]

BILLIONAIRE_REVIEWS_P2 = [
    {"reviewer": "A R", "location": None, "date": "Jan 2024", "trip_type": "Friends", "rating": 5, "review_text": "The nightclub was the perfect place for a fun night out with vibrant music, dazzling light shows, and a stunning interior."},
    {"reviewer": "Alika A", "location": "Dubai, UAE", "date": "Mar 2024", "trip_type": "Friends", "rating": 5, "review_text": "Amazing place with very cool music and fantastic concerts by famous performers."},
    {"reviewer": "Alina D", "location": "Dubai, UAE", "date": "Sep 2023", "trip_type": "Friends", "rating": 5, "review_text": "A place where you can find luxury, delicious food, good vibes and great songs to dance!"},
    {"reviewer": "Rbe", "location": "Ontario, Canada", "date": "Feb 2024", "trip_type": "Friends", "rating": 5, "review_text": "Indulging in cocktails at Billionaire within the iconic Burj Khalifa was an unparalleled experience with breathtaking views."},
    {"reviewer": "Martina G", "location": "Sedriano, Italy", "date": "Dec 2023", "trip_type": "Friends", "rating": 5, "review_text": "Beautiful, elegant, and refined restaurant with a show featuring professional singers and dancers of the highest quality."},
    {"reviewer": "Maria B", "location": "Dubai, UAE", "date": "Feb 2024", "trip_type": "Friends", "rating": 5, "review_text": "Amazing experience with an exceptional DJ set featuring a diverse mix of music."},
    {"reviewer": "PIRANDAS", "location": "Abu Dhabi, UAE", "date": "Sep 2023", "trip_type": "Friends", "rating": 2, "review_text": "Despite good food, the show was indecent and painful with no artistic direction."},
    {"reviewer": "Natali V", "location": None, "date": "Dec 2023", "trip_type": "Friends", "rating": 5, "review_text": "Lavish nightlife experience with opulent ambiance, pulsating music, and VIP service creating an unforgettable atmosphere."},
    {"reviewer": "Luci Vidal", "location": "Naples, Italy", "date": "Feb 2024", "trip_type": "Solo", "rating": 5, "review_text": "Fantastic experience with fancy décor and great music making it a favorite spot."},
    {"reviewer": "cay man", "location": "Dubai, UAE", "date": "Mar 2023", "trip_type": "Friends", "rating": 1, "review_text": "Amazing location and top ambience but staff is not friendly and welcoming at all."},
    {"reviewer": "Anastasia L", "location": None, "date": "Sep 2023", "trip_type": "Friends", "rating": 5, "review_text": "Electrifying atmosphere from the moment stepping inside with courteous and attentive staff ensuring a seamless experience."},
    {"reviewer": "Metin M", "location": "Cyprus", "date": "Mar 2024", "trip_type": "Business", "rating": 4, "review_text": "Reminiscent of 1960s London nightclubs with good shows, very attentive staff, and above-average food."},
    {"reviewer": "Maria S", "location": None, "date": "Mar 2024", "trip_type": "Friends", "rating": 5, "review_text": "Wonderful place with great music and atmosphere where you can relax and spend a wonderful night with decent people."},
    {"reviewer": "Valeriya", "location": None, "date": "Oct 2023", "trip_type": "Friends", "rating": 5, "review_text": "Great time with friends among beautiful people, with everyone dancing and having fun."},
]

BILLIONAIRE_REVIEWS_P3 = [
    {"reviewer": "Kimberly A", "location": None, "date": "Dec 2023", "trip_type": "Friends", "rating": 5, "review_text": "Billionaire club never fails to reach expectations. Amazing when DJ Smash played."},
    {"reviewer": "Tiziana B", "location": None, "date": "Nov 2024", "trip_type": "Friends", "rating": 5, "review_text": "Fabulous place! You eat like God with friendly and caring staff pampering you."},
    {"reviewer": "Batuhan F", "location": "Dubai, UAE", "date": "Jan 2023", "trip_type": "Friends", "rating": 5, "review_text": "Where you can find luxury, delicious food, good vibes and great songs to dance."},
    {"reviewer": "Nicole H", "location": None, "date": "Jan 2024", "trip_type": "Friends", "rating": 5, "review_text": "Liked from the start with very nice and polite securities and hostesses with 5-star organization."},
    {"reviewer": "Antonella S", "location": None, "date": "Dec 2023", "trip_type": "Friends", "rating": 5, "review_text": "Unforgettable evening with impeccable everything, great food, and beautiful show with real professionals."},
    {"reviewer": "Tati z", "location": None, "date": "Oct 2023", "trip_type": "Friends", "rating": 5, "review_text": "Place truly transcends from usual life with real professionals in events and entertainment."},
    {"reviewer": "Saule T", "location": None, "date": "Nov 2023", "trip_type": "Friends", "rating": 5, "review_text": "Incredible experience with stunning interior and top-notch service creating unforgettable nightlife vibe."},
    {"reviewer": "Viva La Vida", "location": "Porto Cervo, Italy", "date": "Nov 2023", "trip_type": "Friends", "rating": 5, "review_text": "Unforgettable experience in elegant venue with excellent service and quality food—a must-do."},
    {"reviewer": "Shreya K", "location": "Hatta, UAE", "date": "Oct 2023", "trip_type": "Friends", "rating": 1, "review_text": "Very bad experience with biased door staff who refused entry despite confirmed booking."},
    {"reviewer": "Milana S", "location": "Dubai, UAE", "date": "Sep 2023", "trip_type": "Friends", "rating": 5, "review_text": "Best club in Dubai with real Dubai nightlife vibe. Place is literally WOW with great music."},
    {"reviewer": "Irina S", "location": None, "date": "Jul 2023", "trip_type": "Friends", "rating": 5, "review_text": "Amazing experience with best show in Dubai. All acrobats, singers, and dancers are unbelievable."},
    {"reviewer": "Hasmeleata1", "location": "Durham, NC, USA", "date": "Jun 2024", "trip_type": "Couples", "rating": 5, "review_text": "Most fantastic time with fantastic food, terrific energy, and entertainment out of this world."},
    {"reviewer": "Mihriban A", "location": None, "date": "Oct 2023", "trip_type": "Solo", "rating": 5, "review_text": "Best night out in Dubai with very high quality atmosphere and beautiful environment."},
    {"reviewer": "Sasha L", "location": None, "date": "Dec 2023", "trip_type": "Friends", "rating": 5, "review_text": "Glamorous venue with superb vibe, world-class entertainment, and scrumptious exquisite food."},
    {"reviewer": "Minodora D", "location": None, "date": "Nov 2023", "trip_type": "Couples", "rating": 5, "review_text": "Everything perfect from moment we stepped out of car. Amazing show, very good food, excellent wine."},
]

# =============================================================================
# LA PERLE BY DRAGONE
# Source: https://www.tripadvisor.com/Attraction_Review-g295424-d12558848
# =============================================================================

LA_PERLE_REVIEWS_P1 = [
    {"reviewer": "R1150rss", "location": "Bottrop, Germany", "date": "Feb 2026", "trip_type": "Couples", "rating": 5, "review_text": "90 minutes of non-stop entertainment. La Perle in Dubai is the best show I have ever seen in my life. We returned to the show after four years and the impression it made on us remains intact."},
    {"reviewer": "nadi", "location": "Israel", "date": "Feb 2026", "trip_type": "Friends", "rating": 5, "review_text": "This is a real wow!! Outstanding acrobatics, very skilled. The show is amazing."},
    {"reviewer": "bianca t", "location": None, "date": "Mar 2026", "trip_type": None, "rating": 1, "review_text": "No respect for customers. Flights cancelled due to war situation, no refund offered despite exceptional circumstances. Team support was awful."},
    {"reviewer": "Julita", "location": "Northampton, UK", "date": "Mar 2026", "trip_type": "Couples", "rating": 5, "review_text": "Show out of this world! Fantastic experience!"},
    {"reviewer": "Kim P", "location": "London, UK", "date": "Feb 2026", "trip_type": None, "rating": 5, "review_text": "Wow wow wow never seen a show like it. So entertaining. Had my attention all throughout. The stage, the water, the motorbikes - wow the motorbikes. The flexibility of the performers amazing. Popcorn and drinks on the pricey side but to be expected."},
    {"reviewer": "Rick W", "location": "Barton-le-Clay, UK", "date": "Feb 2026", "trip_type": "Couples", "rating": 5, "review_text": "Absolutely amazing show with variety of performers. Everything from motorbikes to high dives into pool and high wire artistes."},
    {"reviewer": "Gappsha", "location": "Kreuzlingen, Switzerland", "date": "Feb 2026", "trip_type": "Couples", "rating": 5, "review_text": "My wife and I went to many similar shows (including several Cirque du Soleil) but this was the best of all! It was impressive from start to finish! A must-visit if you stay in Dubai!"},
    {"reviewer": "afbf18", "location": None, "date": "Dec 2025", "trip_type": None, "rating": 5, "review_text": "Magnificent and very entertaining show. The stage was impressive and there were amazing numbers, particularly the motorcycles. All in a circular elevated café four to six meters high. Exceptional and unique staging. Highly recommended."},
    {"reviewer": "mdgroot94", "location": "Roosendaal, Netherlands", "date": "Feb 2026", "trip_type": "Couples", "rating": 5, "review_text": "The show is incredible! From acrobatics to dance, it had everything! Definitely at the level of a Cirque du Soleil show. Gold tickets in the front row. A bit too close as there are many aerial numbers. Row 4 or 5 would be better. In the front rows you can get wet!"},
    {"reviewer": "Marca D", "location": None, "date": "Jan 2026", "trip_type": "Family", "rating": 5, "review_text": "We didn't know what to expect but wow what a show. A must-see! My whole family was on the edge of our seats, spectacular! An hour and a half of incredible entertainment."},
]

LA_PERLE_REVIEWS_P2 = [
    # Reviews 21-30, Oct-Dec 2025 — extracted via browser
    {"reviewer": "spena", "location": "Chester, UK", "date": "Dec 2025", "trip_type": None, "rating": 5, "review_text": "Audio/visual overload throughout the performance with death-defying stunts. Expected Cirque de Soleil style, this exceeded my expectations. VIP admission, arrive 40 minutes early for complimentary food. Simply awesome!"},
    {"reviewer": "Antonella01_12", "location": "Milan, Italy", "date": "Nov 2025", "trip_type": "Couples", "rating": 5, "review_text": "Beautiful show in a very nice and cozy theater specially created. Crazy acrobatic performances in a context where water is the protagonist."},
    {"reviewer": "Cheekybaldy", "location": "Newton Aycliffe, UK", "date": "Nov 2025", "trip_type": "Couples", "rating": 5, "review_text": "Absolutely outstanding. Seen many shows over the years, but La Perle outshone everything I've experienced. Venue exceptional, staff who greeted us guided us perfectly."},
    {"reviewer": "David W", "location": "Wedmore, UK", "date": "Oct 2025", "trip_type": None, "rating": 5, "review_text": "Storyline is a little odd and difficult to follow however as a visual feast for the senses it is spectacular to watch for all ages. Our kids loved it. From start to finish full of action mixed with amazing aquatics!"},
    {"reviewer": "Val", "location": None, "date": "Oct 2025", "trip_type": "Solo", "rating": 5, "review_text": "Incredible, I loved every bit of the entire moment and didn't want the show to end. Every stunt, splash and spotlight at La Perle had me completely enthralled."},
    {"reviewer": "Wander785304", "location": None, "date": "Oct 2025", "trip_type": None, "rating": 5, "review_text": "La Perle is a mesmerizing spectacle! The performers are incredibly talented and the show is a true masterpiece. The combination of acrobatics, dance, and stunning visuals left me in awe."},
    {"reviewer": "Bryan Neil R", "location": None, "date": "Oct 2025", "trip_type": None, "rating": 5, "review_text": "Really good, I enjoyed the show. Their performance is really good and overall 10 out of 10. Hoping to come back really soon."},
    {"reviewer": "Ramlickatz", "location": None, "date": "Oct 2025", "trip_type": None, "rating": 5, "review_text": "One of the best live performances in the city — a stunning aqua acrobatic show that combines breathtaking stunts, lights, and water effects. Even my 1-year-old was fascinated. La Perle is 100% my top recommendation."},
    {"reviewer": "iansums", "location": "Headcorn, UK", "date": "Oct 2025", "trip_type": None, "rating": 5, "review_text": "As someone who has enjoyed many Cirque Du Soleil shows this is as good or even better than all the ones we have watched in London. Brilliant, it's a must do while in Dubai."},
    {"reviewer": "Jane & Jan", "location": "Nottingham, UK", "date": "Oct 2025", "trip_type": "Couples", "rating": 5, "review_text": "Celebrating our wedding anniversary. Wow wow this show mind blowing! Few different things this time even though it was only 6 months since our last visit. Highly recommend for all the family."},
]

LA_PERLE_REVIEWS_P3 = [
    # Reviews 31-40, 2020-2022 era — includes COVID-era refund complaints
    {"reviewer": "679richardo", "location": "Abu Dhabi, UAE", "date": "Sep 2021", "trip_type": "Couples", "rating": 5, "review_text": "Praised show performances but noted inadequate social distancing and pool/floor effects didn't significantly enhance experience."},
    {"reviewer": "Anthony Fernando", "location": "Dubai, UAE", "date": "Apr 2021", "trip_type": "Couples", "rating": 5, "review_text": "Must-see with amazing stunts and effects. Front-row seats recommended for optimal views."},
    {"reviewer": "Haberfieldk", "location": "Dubai, UAE", "date": "May 2021", "trip_type": "Couples", "rating": 5, "review_text": "Thrilling acrobatics and motorcycle acts. Front-row seats limited visibility of elevated walkway performances but still spectacular."},
    {"reviewer": "Michal D", "location": "Brno, Czech Republic", "date": "Jan 2022", "trip_type": "Couples", "rating": 1, "review_text": "Frustrated about denied refund for COVID-related cancellation despite purchasing insurance coverage."},
    {"reviewer": "Frequencia", "location": "Dubai, UAE", "date": "Mar 2021", "trip_type": "Business", "rating": 5, "review_text": "Among finest shows in town with classical acrobatics and musical elements unique from other Dubai entertainment."},
    {"reviewer": "Hufflepuff33", "location": "London, UK", "date": "Dec 2020", "trip_type": None, "rating": 1, "review_text": "Company refused refunds during pandemic travel disruptions affecting holiday plans."},
    {"reviewer": "paolo b", "location": "Dubai, UAE", "date": "Mar 2021", "trip_type": None, "rating": 5, "review_text": "Commended scenography, acrobatics, and pacing. The 1.5-hour duration felt brief despite comprehensive content."},
    {"reviewer": "Lorna", "location": "Dubai, UAE", "date": "Jul 2021", "trip_type": None, "rating": 2, "review_text": "Show was merely adequate with significant booking coordination delays affecting hotel check-in."},
    {"reviewer": "TimeTravellers01", "location": "Dubai, UAE", "date": "Oct 2020", "trip_type": None, "rating": 3, "review_text": "Noted reduced water elements compared to original production; ticket prices should reflect modified show quality."},
    {"reviewer": "Yekaterina S", "location": None, "date": "Sep 2021", "trip_type": None, "rating": 2, "review_text": "Hotel limousine service pricing was 3x more expensive than alternatives, with poor AC in vehicle."},
]

# =============================================================================
# DREAM DUBAI (dinner show)
# Source: https://www.tripadvisor.com/Attraction_Review-g295424-d27856941
# Nota: 1,829 reseñas, 5.0 rating. Audiencia mayoritariamente rusa/CIS.
# =============================================================================

DREAM_DUBAI_REVIEWS_P1 = [
    {"reviewer": "Aleksandra N", "location": "Dubai, UAE", "date": "Jan 2026", "trip_type": "Couples", "rating": 5, "review_text": "Outstanding dining with spectacular show, refined cuisine, and professional entertainment made the evening truly memorable."},
    {"reviewer": "Natalia C", "location": None, "date": "Dec 2025", "trip_type": "Friends", "rating": 5, "review_text": "Fantastic blend of entertainment and dining with visually impressive show, excellent food, and attentive service."},
    {"reviewer": "Nastya A", "location": None, "date": "Dec 2025", "trip_type": "Friends", "rating": 5, "review_text": "Pleasant, stylish atmosphere with tasty food, balanced cocktails, and attentive service. Felt comfortable immediately."},
    {"reviewer": "Melnyk I", "location": None, "date": "Dec 2025", "trip_type": "Friends", "rating": 5, "review_text": "Best restaurant in Dubai with spectacular show, outstanding food, and flawless service at the highest level exceeding all expectations."},
    {"reviewer": "Mila", "location": "Dubai, UAE", "date": "Sep 2025", "trip_type": "Friends", "rating": 5, "review_text": "Magical place with incredible performances and talented dancers and singers keeping audience mesmerized. Exquisite, beautifully presented dishes."},
    {"reviewer": "Kristina E", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 5, "review_text": "Best dinner show in Dubai with exceptional performance quality, top-tier artists, world-class choreography, acrobatics and visual effects."},
    {"reviewer": "Lana S", "location": None, "date": "Dec 2025", "trip_type": "Friends", "rating": 5, "review_text": "Spectacular performance combining acrobatics and storytelling with stunning effects, incredible choreography, gorgeous costumes, cinematic emotional experience."},
    {"reviewer": "Victoria Kat", "location": "Dubai, UAE", "date": "Sep 2025", "trip_type": "Friends", "rating": 5, "review_text": "Special place with chic atmosphere, talented artists delivering fantastic shows mesmerizing the whole night. High-level service with professional warm team."},
    {"reviewer": "Maria Georgieva", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 5, "review_text": "Most impressive dining and nightlife experience — perfect blend of fine cuisine, art, music, and performance. Stunning interiors, world-class shows."},
    {"reviewer": "Lyubov Kh", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 5, "review_text": "Amazing evening with luxurious interiors, spectacular dinner show featuring professional creative performances full of energy, and excellent food."},
]

# =============================================================================
# SHOW SUBJECT — PROXY REVIEWS (hotel guests mentioning the show)
# Source: Booking.com and TripAdvisor hotel reviews (undisclosed property)
# source_status = "partial" — guests describe show elements without naming the show
# Note: immersive multi-zone format (basement zone + champagne bar + ambient performers)
# =============================================================================

SHOW_SUBJECT_PROXY_REVIEWS = [
    # Booking.com reviews — guests mention live music/performers
    {"reviewer": "Aliaksandra", "location": "UAE", "date": "Apr 2026", "trip_type": "Couples", "rating": 9, "review_text": "For breakfast and dinner live music and singers is amazing — and the buffet is so good! This hotel is more for parties and young people."},
    {"reviewer": "Haydar", "location": "UAE", "date": "Apr 2026", "trip_type": "Solo", "rating": 8, "review_text": "Facilities and music, DJ and musicians great. Check-in process slow but overall good experience."},
    {"reviewer": "Marharyta", "location": "Ukraine", "date": "Mar 2026", "trip_type": "Couples", "rating": 8, "review_text": "Live music for dinner: the guy who plays saxophone is phenomenal, his performance is absolutely fantastic. Music choice was amazing for the pool, DJ knew what he was doing."},
    {"reviewer": "Sandeep", "location": "UAE", "date": "Nov 2025", "trip_type": "Couples", "rating": 8, "review_text": "Musical show at the breakfast was brilliant. Maldives-like ambience. Hotel room was clean and cozy."},
    {"reviewer": "Tomáš", "location": "Czech Republic", "date": "Nov 2025", "trip_type": "Couples", "rating": 8, "review_text": "The hotel is an all-day party hotel. Breakfast and dinner was really tasty. Pool and beach working 24/7 is also very cool."},
    {"reviewer": "Julialba", "location": "Switzerland", "date": "May 2023", "trip_type": "Couples", "rating": 6, "review_text": "Buena música en vivo, es romántico y a la vez ambiente de fiesta. El concepto del lugar es único, los atardeceres, los jardines, la arena es suave."},
    # TripAdvisor hotel reviews — show-specific mentions
    {"reviewer": "HFW2411", "location": "Zürich, Switzerland", "date": "May 2025", "trip_type": "Business", "rating": 5, "review_text": "Champagne bar, disco and cabaret in the basement. The Rive restaurant serves excellent food. Beach is fantastic, water crystal clear even in May. Well worth the 45-50 min boat trip."},
    {"reviewer": "Sal D", "location": "UK", "date": "May 2025", "trip_type": "Couples", "rating": 5, "review_text": "Pool music is accompanied by live violin or saxophone — a very innovative idea and it works! The champagne room is new and feels like stepping into prohibition but it's got a great atmosphere."},
    {"reviewer": "Gihan A", "location": "UAE", "date": "Mar 2026", "trip_type": "Couples", "rating": 5, "review_text": "Amazing gala dinner at the beach with great vibes, lights and music. Staff are really helpful and supportive and respond quickly on WhatsApp."},
]


# =============================================================================
# HELPERS
# =============================================================================

def build_dataframe(reviews, venue, source_status="complete", source="tripadvisor_browser"):
    df = pd.DataFrame(reviews)
    df["venue"] = venue
    df["source_status"] = source_status
    df["source"] = source
    return df


def run():
    os.makedirs("data_raw/tripadvisor", exist_ok=True)
    output_path = "data_raw/tripadvisor/reviews_raw.csv"

    # --- Build all dataframes ---
    df_billionaire = pd.concat([
        build_dataframe(BILLIONAIRE_REVIEWS_P1, "billionaire"),
        build_dataframe(BILLIONAIRE_REVIEWS_P2, "billionaire"),
        build_dataframe(BILLIONAIRE_REVIEWS_P3, "billionaire"),
    ], ignore_index=True)

    df_la_perle = pd.concat([
        build_dataframe(LA_PERLE_REVIEWS_P1, "la_perle"),
        build_dataframe(LA_PERLE_REVIEWS_P2, "la_perle"),
        build_dataframe(LA_PERLE_REVIEWS_P3, "la_perle"),
    ], ignore_index=True)

    df_dream = build_dataframe(DREAM_DUBAI_REVIEWS_P1, "dream_dubai")

    # Subject show: proxy via hotel reviews — source_status = partial
    df_show_subject = build_dataframe(
        SHOW_SUBJECT_PROXY_REVIEWS, "show_subject",
        source_status="partial",
        source="hotel_review_proxy"
    )

    all_new = pd.concat(
        [df_billionaire, df_la_perle, df_dream, df_show_subject],
        ignore_index=True
    )

    # --- Save: overwrite cleanly (all data is defined here) ---
    all_new.drop_duplicates(subset=["venue", "reviewer", "date"], inplace=True)
    all_new.to_csv(output_path, index=False, encoding="utf-8")

    # Summary
    counts = all_new.groupby("venue").size()
    print("Reviews saved per venue:")
    for venue, n in counts.items():
        print(f"  {venue}: {n}")
    print(f"Total: {len(all_new)}")


if __name__ == "__main__":
    run()
