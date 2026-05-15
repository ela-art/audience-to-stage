"""
Utility: add The Theater reviews (collected manually from browser) to reviews_raw.csv.
52 reviews across 4 TripAdvisor pages. Run once.
"""
import pandas as pd
import os

THE_THEATER_REVIEWS = [
    # ── PAGE 1 ──────────────────────────────────────────────────────────────
    {"reviewer": "Ksyusha S", "location": None, "date": "May 2026", "trip_type": "Friends", "rating": 5,
     "review_text": "I had a wonderful experience at the Teatr Restaurant. The atmosphere is truly refined and elegant, creating the perfect setting for a special evening. The show program was superb. The rooms were beautiful. The staff was friendly, attentive, and professional, ensuring all our needs were met. The menu offered a wide variety of delicious dishes, expertly prepared and beautifully presented. I especially enjoyed the main course, which was both delicious and filling. Overall, the Teatr Restaurant offers excellent service, exquisite cuisine, and an unforgettable atmosphere. I highly recommend it to anyone looking for a fine dining experience."},
    {"reviewer": "Paula K", "location": None, "date": "Jan 2026", "trip_type": "Friends", "rating": 5,
     "review_text": "I was truly impressed by The Theater Dubai. The performances were absolutely stunning, and the level of talent on stage was exceptional. The service was equally outstanding — professional, attentive, and perfectly organized. It is without a doubt one of the best dinner shows I have ever experienced. An unforgettable evening that combines world-class entertainment with an amazing atmosphere. Highly recommended."},
    {"reviewer": "Nick P", "location": "Easton, United Kingdom", "date": "Dec 2025", "trip_type": "Couples", "rating": 3,
     "review_text": "Nice but very over-priced food and drinks with a show that does not get anywhere near the standard set by La Perle. Instead of a set entry ticket price, you get a minimum spend per person, which is set by the level and position of the table you choose. Show was OK. The couple spinning above the stage whilst hanging onto a pole with various parts of their bodies, were very good, but it all got a bit repetitive. There's only so many people hanging on a rope with flaming torches that you need to see in one show. It's a decent night out, but with these high prices it's not something that everyone will be able to afford."},
    {"reviewer": "Ayda M", "location": None, "date": "Oct 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "The Theatre Dubai is truly an unforgettable dining experience! The combination of gourmet food, luxury ambience, and breathtaking live performances makes it one of the most unique places in the city. Every detail, from the service to the spectacular shows, is world-class. Perfect for a glamorous night out in Dubai – highly recommended!"},
    {"reviewer": "Nia L", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Every thing was perfect vibe foods drinks. I like there, i hope go again. Also service was good and they were nice people."},
    {"reviewer": "bella k", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "They have the most beautiful and elegant show with incredibly professional dancers. I love it here because the food is unique and wonderful."},
    {"reviewer": "Setare S", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 1,
     "review_text": "A place where three secretaries and a security guard have to approve your outfit. And if they don't like it, they'll reject you in 30 minutes, right from the top of your nose. I really feel sorry for the management and the owner of this place for their choice of staff."},
    {"reviewer": "emel y", "location": None, "date": "Sep 2025", "trip_type": "Friends", "rating": 1,
     "review_text": "I am a Dubai resident and I usually go to at least 3 to 5 different high-end, 5-star venues every week. However, tonight, despite having a reservation with my friend, after waiting for half an hour, a young girl who was in charge of coordinating the entry did not allow us to enter. She said that our clothes were not expensive or elegant enough. This is the height of disrespect towards people."},
    {"reviewer": "RRR", "location": None, "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "A nice mix of dining and performance — the atmosphere makes you slow down, enjoy the food, and take in the show. It's more than just a meal, it's an experience."},
    {"reviewer": "Tatiana", "location": None, "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "One of the best show I've seen in Dubai!!! The artist are incredible. The food, the music and the vibes of the place was really amazing."},
    {"reviewer": "Asya", "location": "Dubai, United Arab Emirates", "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Cool place, music, service, kitchen, show, van love. Were with friends, come back again! This show should be seen by everyone!!!!"},
    {"reviewer": "Darya V", "location": None, "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Dubai's The Teatro atmosphere restaurant: impeccable service, stylish interiors and dishes that captivate the first time!"},
    {"reviewer": "Roving15838456963", "location": None, "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "A pleasant evening atmosphere where you can immerse yourself in the atmosphere of the various shows that are created. Delicious food, and I will return here many times in the future."},
    {"reviewer": "flyhigh", "location": "Dubai, United Arab Emirates", "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Just want to say that this is really Amazing place, great performances, nice atmosphere & food. Definitely will be back."},
    {"reviewer": "Diana", "location": "Dubai, United Arab Emirates", "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "amazing place, with incredibly beautiful music and gorgeous performances of professional artists, singers and dancers with various tricks and a gorgeous program with costumes. delicious food and cool music."},
    # ── PAGE 2 ──────────────────────────────────────────────────────────────
    {"reviewer": "Zumzet H", "location": "Dubai, United Arab Emirates", "date": "Aug 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "The best dinner show in Dubai. Not check for other places, this is best. The show is just blowmind, costumes, music, choreography are all on their best. Food is delicious and service is impeccable. We had a fabulous night. Recommend it for sure 100%."},
    {"reviewer": "Maria K", "location": "Kokshetau, Kazakhstan", "date": "Jul 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "I really enjoyed the performance. The actors were amazing, and the atmosphere was magical. Everything — from the stage design to the music — was well done. I would definitely go again!"},
    {"reviewer": "Alana M", "location": None, "date": "Jul 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Absolutely loved this place! The food was delicious, full of flavor and beautifully presented. The dance show was energetic and captivating – a perfect combination of great dining and entertainment. Highly recommend for a fun and memorable night out."},
    {"reviewer": "Ameriki Habibi", "location": "Kuwait City, Kuwait", "date": "Jul 2025", "trip_type": "Couples", "rating": 3,
     "review_text": "The decor was nice and their service was amazing! Food very tasty! The show itself was average. I have been to similar places in Dubai and the shows are much more exciting! Overall this is a decent place for a date night."},
    {"reviewer": "Maria Shota", "location": None, "date": "May 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "It was amazing night! Incredible show with so professional artists, good sound and light, tasty food and great service. I also would like to highlight the DJ, he created a great musical atmosphere between the numbers of the show and helped the artists set the right vibe. I definitely recommend visiting."},
    {"reviewer": "Ghada H", "location": None, "date": "Jun 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "One of the best places I have ever attended in Dubai! The show is fascinating!!!! Simply wow! The service was beyond expectation! The food is sooo delicious! The drinks are top! The Music and the Vibes are the best! Thank you The Theater for an unforgettable night!"},
    {"reviewer": "Lady Omnia", "location": "Dubai, United Arab Emirates", "date": "Jun 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "The show at The Theater is absolutely stunning! The performers are highly professional, and the performance truly takes you to another world. The food is excellent — rich in flavor and beautifully presented. The service is quick, attentive, and very friendly. The atmosphere is comfortable and elegant, making it perfect for both friends and couples. Highly recommended for a special and unforgettable night out!"},
    {"reviewer": "Irina G", "location": None, "date": "May 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "The Theater Dubai delivers a luxurious dining experience paired with dazzling live performances, including music, dance, and acrobatics. Located at the Fairmont Hotel, it offers a glamorous atmosphere with elegant decor and world-class service. Ideal for special occasions, it's a standout spot for those seeking an unforgettable night out in Dubai."},
    {"reviewer": "cristina S", "location": "Dubai, United Arab Emirates", "date": "Jan 2025", "trip_type": "Friends", "rating": 5,
     "review_text": "Yesterday night was in The Theatre to see the new show, had one fantastic night. So many talented performers on the stage all night long, staff very friendly one Romanian girl on the entrance was very welcoming and nice. The food was great. Had one amazing night. Will be back for sure. My favorite restaurant show."},
    {"reviewer": "xriso", "location": None, "date": "Nov 2024", "trip_type": "Couples", "rating": 3,
     "review_text": "We came here a few years back when it was the Cavalli Club and we loved it. The food and the show were both great. Booking was easy. Got there at 9.40pm as advised to arrive 20 mins before. Doors didn't open until 10pm. The service from George was AMAZING. The food was amazing and the setting and theatre was first class. Unfortunately the show was very standard and quite Butlins style. The costumes were amazing but some of the acts were not so great. Some were good but some were quite boring and amateurish. The pauses inbetween are too long so you get bored. The acrobats were good but the singing and dancing was quite standard. I've done it twice and I wouldn't go again as I feel like it didn't reach my expectations from the previous visit."},
    {"reviewer": "Ksyusha P", "location": "Dubai, United Arab Emirates", "date": "Sep 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "It's amazing place with the greatest show in Dubai with perfect atmosphere and great food, I was so happy to see it in person."},
    {"reviewer": "Nabeel A", "location": None, "date": "Sep 2024", "trip_type": "Friends", "rating": 1,
     "review_text": "I am writing this review to share my deeply disappointing and alarming experience with The Theater Dubai, located in the Fairmont, on Friday, September 13, 2024. To confirm my booking, staff requested my credit card details over the phone including the CVV. The following morning I was charged AED 2,999 from the Apple Store. I immediately contacted my bank and deactivated my card. When I called The Theater, management never got in touch with me despite assurances. I strongly advise all potential visitors to be extremely cautious when dealing with their staff, especially when it comes to sharing sensitive credit card information."},
    {"reviewer": "Lana", "location": None, "date": "Jul 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "Amazing place with the dinner show. Delicious food, good service, amazing singers, everything is just perfect. Highly recommended."},
    {"reviewer": "Lamitta", "location": None, "date": "Apr 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "Amazing place, top entertainment.. one of the best in Dubai. Dining, music, show.. All nice, must see!! Crowd from everywhere."},
    {"reviewer": "Elliki J", "location": None, "date": "May 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "One of the most amazing place in Dubai. Food is amazing. They have so many live shows. The atmosphere is excellent. The service was very great. Was really really surprised. It was my first time there and I recommend this place to everyone who wants to go have amazing experience in every way."},
    # ── PAGE 3 ──────────────────────────────────────────────────────────────
    {"reviewer": "Lana B", "location": None, "date": "May 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "An absolutely stunning dinner show with very talented acrobat artists and singer Natalie. One of the best shows I have ever been to, I highly recommend this place to anyone who appreciates quality service and shows."},
    {"reviewer": "Abdullah A", "location": None, "date": "Mar 2024", "trip_type": "Friends", "rating": 3,
     "review_text": "The show was amazing, but the menu is pricy… food is overpriced. But overall the experience was good, however I won't repeat it."},
    {"reviewer": "Viviana M", "location": "Dubai, United Arab Emirates", "date": "Feb 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "My evening at the Theater was nothing short of spectacular. From the moment I stepped into the opulent venue, I was transported to a realm of elegance and sophistication. The culinary experience was a symphony of flavors. From the sushi rolls to the decadent tiramisu, every bite was a culinary delight. The service was impeccable. The highlight of the night was undoubtedly the mesmerizing show. The performers were world-class, captivating the audience with their skill, grace, and charisma. From stunning aerial acrobatics to beautiful musical performances, every moment was filled with wonder and awe. A must-try for those seeking a memorable, high-end entertainment experience."},
    {"reviewer": "Seda P", "location": None, "date": "Feb 2024", "trip_type": "Friends", "rating": 5,
     "review_text": "Its an number 1 place of dubai which has shows. Its totally incredible high quality costumes and dancers and everything else. They totally deserve an award."},
    {"reviewer": "Ximena P", "location": "Minnesota, USA", "date": "Apr 2023", "trip_type": "Family", "rating": 3,
     "review_text": "Very expensive for what it is and the tables close to the stage, not to mention the price. The logistics are not very clear. The food is ok but not the best."},
    {"reviewer": "Donna", "location": None, "date": "Oct 2023", "trip_type": "Friends", "rating": 5,
     "review_text": "This place is amazing to come with friends or as a couple. The vibe is amazing and the food is great. Good music and the service is impeccable. Definitely recommend."},
    {"reviewer": "Mariam A", "location": None, "date": "Sep 2023", "trip_type": "Couples", "rating": 1,
     "review_text": "There is no privacy policy in this place. They don't care about their guests. I was here with my husband and the next day a girl called him hundred times with a request to meet. When he asked where she got the number from, she reluctantly admitted that she was given it at the theater. Apparently at the reception someone is selling guest numbers or giving them away for free. What a shame! Shame!!!"},
    {"reviewer": "KMA", "location": None, "date": "Aug 2023", "trip_type": "Couples", "rating": 1,
     "review_text": "We had a terrible experience with one of the staff.. and when we complained even the GM of the place wasn't helpful… terrible customer service.. the worst ever."},
    {"reviewer": "Parisa R", "location": "Emirate of Dubai, United Arab Emirates", "date": "Jun 2023", "trip_type": "Friends", "rating": 1,
     "review_text": "We are not happy at all! Been there last week for a vvip table. First of all at entrance they made us waiting in hot weather summer to check our reservation. Its really annoying how they treat at entrance. The worst part is the amount that they blocked from my debit card at booking as guaranty deposit, they considered in table bill payment. Being 10 years living in Dubai and booking hundreds of different places its first time I see this. My first experience with Theater was terrible and I don't recommend at all!"},
    {"reviewer": "MGH", "location": "Dubai, United Arab Emirates", "date": "Jun 2023", "trip_type": "Couples", "rating": 1,
     "review_text": "Overpriced and the show is so mediocre and more like a circus. Food average."},
    {"reviewer": "Nitro Jul", "location": "Dubai, United Arab Emirates", "date": "May 2023", "trip_type": "Friends", "rating": 5,
     "review_text": "My third time in the Theater! And I'm still excited! If you wanna go for show, performances, not just dinner or party, come here! You'll be definitely entertained. P.S. truffle risotto is still my favorite."},
    {"reviewer": "Chris", "location": "Denpasar, Indonesia", "date": "Feb 2023", "trip_type": "Couples", "rating": 5,
     "review_text": "I would definitely recommend this place, fantastic show, very tasty food and excellent service. The staff was very attentive to all our requests and we had an amazing night!"},
    {"reviewer": "Noa veri", "location": "Barcelona, Spain", "date": "Jan 2023", "trip_type": "Friends", "rating": 5,
     "review_text": "Good show and service! The prices are not crazy and that's a plus!!! Good club to hang out on weekends."},
    {"reviewer": "Maya T", "location": None, "date": "Dec 2022", "trip_type": "Solo", "rating": 1,
     "review_text": "Rude staff, not a welcome atmosphere. Went there once with an invitation for a table but hostess at the door was acting like she is the owner of the place."},
    {"reviewer": "Tembo0o", "location": "Dubai, United Arab Emirates", "date": "Oct 2022", "trip_type": None, "rating": 1,
     "review_text": "Worst staff ever. I have been to theatre several times because my girlfriend wants to go there for the atmosphere and every time I get disappointed. Once you step in the staff tries to push you to a super bad table either on far corners or directly below the speakers so you can object and then they sell you a better table but they increase the price you already agreed on. Today I came 20 minutes early and they put me on a table in far corner and below the speaker. A waiter dropped steak sauce on my Versace shoes and the manager asked me to go to toilet to let the staff clean it. The shoe was never cleaned properly. So unless you want to be scammed, try to avoid this place."},
    # ── PAGE 4 ──────────────────────────────────────────────────────────────
    {"reviewer": "Lina w", "location": "Al Khobar, Saudi Arabia", "date": "Oct 2022", "trip_type": "Friends", "rating": 1,
     "review_text": "I did not visit it yet because I tried to call your number but no one answered me. Please i want reservations ASAP I will be back home after two days."},
    {"reviewer": "Abdulmoez Tahmaz", "location": "Riyadh, Saudi Arabia", "date": "Jun 2022", "trip_type": "Friends", "rating": 3,
     "review_text": "The place is amazing with live Arabic and non Arabic shows. The food was the best things as it was so delicious specially the lamb chops and Salmon Sushi. Services was little bit horrible and very slow. The shows was so beautiful and from different cultures."},
    {"reviewer": "Dr. F", "location": "Nottingham, United Kingdom", "date": "May 2022", "trip_type": None, "rating": 1,
     "review_text": "I was highly disappointed by The Theater and arrogance of their staff from security personnel to the hostess. More sadly it has replaced the venue which was known for its excellence and hospitality. Cavalli Club was our go-to venue on every visit to Dubai. I found very unwelcoming attitude from the hostess at Theater. Their attitude makes it worse and is enough to destroy your club night."},
    {"reviewer": "AmalAlsadi", "location": "Dubai, United Arab Emirates", "date": "Jan 2022", "trip_type": "Friends", "rating": 5,
     "review_text": "Food quality is good. Service is excellent. Atmosphere is great. If you're looking for a restaurant with a show the theater is the place!"},
    {"reviewer": "Wellness F", "location": None, "date": "Mar 2022", "trip_type": "Friends", "rating": 1,
     "review_text": "For someone who hasn't been there before, when you do your table bookings and you ask where exactly the table is located they might tell you it's 10 meters from the stage but actually your table will be 50 meters from the stage without any visible contact. The food is not nice, we paid 200aed for a truffle pizza among other dishes, it was very small and the taste average, no truffle taste at all. During the night they decided to take our full bottle from the table. If you just want to see the show, be very careful with the place."},
    {"reviewer": "danielemazzola1991", "location": "Dubai, United Arab Emirates", "date": "Mar 2022", "trip_type": None, "rating": 5,
     "review_text": "What a fabulous place. The shows and the performers were all amazing. Very nice environment, very well organized, dark and loud music during the show, brighter and more quiet otherwise. Food was ok, nothing incredible but tasty and good, drinks were fresh and quite quick to arrive, service was on point. Definitely you should pay a visit if you are nearby. Stunning shows."},
    {"reviewer": "RachelRizkallah", "location": "Lebanon", "date": "Nov 2021", "trip_type": "Couples", "rating": 5,
     "review_text": "Amazing amazing amazing. I loved it and would definitely visit again when in Dubai. Performance is extremely nice. Service is great and waiters are professionals. For the drinks, i ordered a gin basil but got something else. When we informed the waiters they changed it and it took them around 30 minutes to get my drink. But when i got the real gin basil it was so tasty and one of the best i had. I loved the elevator with the seating in it. Food is nice: the salmon tartare salad and truffle pizza are very tasty."},
]


def run():
    csv_path = "data_raw/tripadvisor/reviews_raw.csv"

    # Load existing CSV
    existing = pd.read_csv(csv_path, encoding="utf-8")
    print(f"Existing rows: {len(existing)}")

    # Build new rows
    new_rows = pd.DataFrame([{
        "venue": "the_theater",
        "reviewer": r["reviewer"],
        "location": r["location"],
        "date": r["date"],
        "trip_type": r["trip_type"],
        "rating": r["rating"],
        "review_text": r["review_text"],
        "source_status": "complete",
        "source": "tripadvisor_browser",
    } for r in THE_THEATER_REVIEWS])

    combined = pd.concat([existing, new_rows], ignore_index=True)
    combined.drop_duplicates(subset=["venue", "reviewer", "date"], inplace=True)
    combined.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"Added {len(new_rows)} the_theater reviews")
    print(f"Total rows now: {len(combined)}")
    print()
    print("Reviews per venue:")
    print(combined["venue"].value_counts().to_string())


if __name__ == "__main__":
    run()
