"""
Phase 2 — Manual competition profiles.
Qualitative data not available in reviews: format, pricing, capacity, cultural positioning.
Output: data_manual/competition_profiles.csv
Run with: anaconda3 python scripts/04_build_competition_profiles.py
"""

import pandas as pd
import os

# =============================================================================
# Perfiles cualitativos por venue
# Escala 1-5: visual_register, cultural_barriers, sensory_intensity
#   visual_register  : 1=minimalista, 5=espectáculo visual total
#   cultural_barriers: 1=universal, 5=muy específico culturalmente
#   sensory_intensity: 1=contemplativo, 5=inmersivo/abrumador
# producer_relation  : "competitor" | "same_producer" | "subject"
# =============================================================================

COMPETITION_PROFILES = [
    {
        "venue_key": "la_perle",
        "show_name": "La Perle by Dragone",
        "venue_name": "La Perle Theatre (Al Habtoor City)",
        "producer": "Dragone / Al Habtoor Group",
        "artistic_director": "Franco Dragone",
        "producer_relation": "competitor",
        "format": "dedicated_theater",
        "venue_type": "standalone_theater",
        "location_district": "Al Habtoor City / Business Bay",
        "years_active": 9,                       # opened 2017
        "ticket_price_usd": 76,                  # minimum price per TripAdvisor 2026
        "audience_capacity": 1300,
        "tripadvisor_reviews": 3306,
        "tripadvisor_rating": 4.6,
        "visual_register": 5,
        "cultural_barriers": 1,                  # universal — water, acrobatics, spectacle
        "sensory_intensity": 5,
        "music_style": "orchestral_electronic_hybrid",
        "audience_profile": "international_tourist",
        "conflict_resilience": "low",
        "estilo_show": "circo_agua",
        "estilo_movimiento": "acrobacia|circo|aereo|contemporaneo",
        "registro_corporal": "tecnico_virtuoso",
        "relacion_publico": "contemplativo",
        "carga_erotica": "neutro",
        "referente_cultural": "universal|fusion_global",
        "nivel_habilidad": "elite",
        "paleta_vestuario": "dorado|plateado|negro|multicolor",
        "diseno_vestuario": "theatrical_fantasy",
        "estilo_musical": "clasico_orquestal|electronico|fusion",
        "notes": "Gold standard del mercado Dubai. Benchmark principal. Comparado repetidamente con Cirque du Soleil. Audiencia internacional. 9 anos de operacion — marca consolidada."
    },
    {
        "venue_key": "billionaire",
        "show_name": "Billionaire Dubai",
        "venue_name": "Billionaire Dubai (Burj Khalifa area)",
        "producer": "Majestas Group (Flavio Briatore)",
        "artistic_director": "Irma Di Paola",
        "producer_relation": "competitor",
        "format": "dinner_show_nightclub",
        "venue_type": "restaurant_nightclub",
        "location_district": "Downtown Dubai",
        "years_active": 8,
        "ticket_price_usd": None,                # no ticket — minimum spend
        "audience_capacity": None,
        "tripadvisor_reviews": 473,
        "tripadvisor_rating": 4.0,
        "visual_register": 4,
        "cultural_barriers": 2,
        "sensory_intensity": 4,
        "music_style": "pop_dance_DJ_live_acts",
        "audience_profile": "mixed_expat_tourist_CIS",
        "conflict_resilience": "medium",
        "estilo_show": "dinner_show",
        "estilo_movimiento": "acrobacia|aereo|contemporaneo|jazz",
        "registro_corporal": "entretenimiento_accesible",
        "relacion_publico": "contemplativo",
        "carga_erotica": "sugerente",
        "referente_cultural": "occidental|fusion_global",
        "nivel_habilidad": "profesional",
        "paleta_vestuario": "plateado|negro|blanco|rojo",
        "diseno_vestuario": "glamour_vintage|luxury_couture",
        "estilo_musical": "pop_internacional|RnB|dance|banda_en_vivo",
        "notes": "Formato dinner-show con transicion a nightclub. Calidad del show muy inconsistente segun reviews. Fuerte branding italiano de lujo. Audiencia CIS + expats + turista occidental. Reviews mencionan acrobatas, cantantes, bailarines."
    },
    {
        "venue_key": "dream_dubai",
        "show_name": "Dream Dubai",
        "venue_name": "Dream Dubai Dinner Show",
        "producer": "Sunset Hospitality Group",
        "artistic_director": "Pierre Khadra",
        "producer_relation": "competitor",
        "format": "dinner_show",
        "venue_type": "dinner_theater",
        "location_district": "Dubai (exact district unconfirmed)",
        "years_active": None,
        "ticket_price_usd": None,
        "audience_capacity": None,
        "tripadvisor_reviews": 1829,
        "tripadvisor_rating": 5.0,
        "visual_register": 4,
        "cultural_barriers": 1,
        "sensory_intensity": 4,
        "music_style": "varied_high_energy",
        "audience_profile": "CIS_russian_speaking_dominant",
        "conflict_resilience": "medium",
        "estilo_show": "dinner_show",
        "estilo_movimiento": "acrobacia|contemporaneo|latino|jazz",
        "registro_corporal": "entretenimiento_accesible",
        "relacion_publico": "inmersivo",
        "carga_erotica": "sugerente",
        "referente_cultural": "occidental|fusion_global",
        "nivel_habilidad": "profesional",
        "paleta_vestuario": "negro|dorado|neon|multicolor",
        "diseno_vestuario": "glamour_vintage|luxury_couture",
        "estilo_musical": "electronico|pop_internacional|latino|DJ",
        "notes": "5.0 perfecto con 1829 resenas — extraordinario. Audiencia mayoritariamente rusa/CIS. Reviews mencionan acrobacia, bailarines, cantantes, efectos visuales, vestuario. Competidor directo en formato dinner-show."
    },
    {
        "venue_key": "the_theater",
        "show_name": "The Theater",
        "venue_name": "Fairmont Dubai",
        "producer": "7 Management",
        "artistic_director": "Guy Manoukian",
        "producer_relation": "competitor",
        "format": "dinner_show",
        "venue_type": "restaurant_nightclub",
        "location_district": "Sheikh Zayed Road",
        "years_active": 4,
        "ticket_price_usd": None,
        "audience_capacity": None,
        "tripadvisor_reviews": 52,
        "tripadvisor_rating": 3.8,
        "visual_register": 4,
        "cultural_barriers": 2,
        "sensory_intensity": 4,
        "music_style": "jazz_swing|pop_internacional|electronico|banda_en_vivo|DJ",
        "audience_profile": "mixed_expat_tourist",
        "conflict_resilience": "medium",
        "estilo_show": "dinner_show",
        "estilo_movimiento": "aereo|contemporaneo|jazz|fusion",
        "registro_corporal": "expresivo_emocional",
        "relacion_publico": "inmersivo",
        "carga_erotica": "sugerente",
        "referente_cultural": "occidental|arabe|fusion_global",
        "nivel_habilidad": "elite",
        "paleta_vestuario": "rojo|dorado|negro",
        "diseno_vestuario": "glamour_vintage|theatrical_fantasy",
        "estilo_musical": "jazz_swing|pop_internacional|electronico|banda_en_vivo|DJ",
        "notes": "Conceptualizado por Guy Manoukian. Fusion oriental y occidental. Aerialists de Las Vegas. Lleva mas de 4 anos operando en Fairmont Dubai Sheikh Zayed Road."
    },
]


def run():
    os.makedirs("data_manual", exist_ok=True)
    output_path = "data_manual/competition_profiles.csv"

    df = pd.DataFrame(COMPETITION_PROFILES)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Saved {len(df)} venue profiles to {output_path}")
    print()

    print("Producer relations:")
    print(df.groupby("producer_relation")[["venue_key"]].count().to_string())
    print()
    print("Format distribution:")
    print(df["format"].value_counts().to_string())
    print()
    print("Nivel de habilidad por venue:")
    print(df[["venue_key", "nivel_habilidad", "estilo_show"]].to_string(index=False))


if __name__ == "__main__":
    run()
