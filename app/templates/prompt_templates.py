"""
Module voor het beheren van prompt templates voor verschillende songstijlen.
Nu geïntegreerd met de Thema Database voor dynamische elementen.
"""

import random
from sqlalchemy.orm import Session
from app.services.thema_service import ThemaService, get_thema_service

# Originele templates blijven beschikbaar als fallback
FALLBACK_TEMPLATES = {
    "verjaardag": """🎵 Prompt voor ManusAI – verjaardagslied voor {ontvanger}, geïnspireerd door de 30 populairste Nederlandse feestnummers. 

Je bent een ervaren Nederlandstalige songwriter gespecialiseerd in liefdevolle, grappige verjaardagsteksten.

Schrijf een origineel, vrolijk verjaardagslied voor {ontvanger}, van {van}.
Over {ontvanger}: {beschrijving}

Het lied moet:
- Een pakkend refrein hebben
- Persoonlijk voelen door details over {ontvanger} te verwerken
- Een vrolijke, feestelijke toon hebben
- Geschikt zijn om te zingen op een feest

Extra wensen: {extra_wens}

Maak een complete songtekst met coupletten en refrein.""",

    "liefde": """🎵 Prompt voor ManusAI – liefdeslied voor {ontvanger}, geïnspireerd door Nederlandse romantische hits.

Je bent een getalenteerde Nederlandstalige songwriter gespecialiseerd in emotionele, oprechte liefdesteksten.

Schrijf een hartverwarmend liefdeslied voor {ontvanger}, van {van}.
Over {ontvanger}: {beschrijving}

Het lied moet:
- Emotioneel en oprecht zijn
- Persoonlijke details over {ontvanger} bevatten
- Een romantische toon hebben
- Een memorabel refrein hebben dat de liefde viert

Extra wensen: {extra_wens}

Maak een complete songtekst met coupletten en refrein.""",

    "afscheid": """🎵 Prompt voor ManusAI – afscheidslied voor {ontvanger}, geïnspireerd door betekenisvolle Nederlandse ballads.

Je bent een gevoelige Nederlandstalige songwriter gespecialiseerd in betekenisvolle afscheidsteksten.

Schrijf een waardig afscheidslied voor {ontvanger}, van {van}.
Over {ontvanger}: {beschrijving}

Het lied moet:
- Respectvol en waardig zijn
- Mooie herinneringen en kwaliteiten van {ontvanger} bevatten
- Een hoopvolle boodschap hebben, ondanks het afscheid
- Troostend zijn voor de luisteraars

Extra wensen: {extra_wens}

Maak een complete songtekst met coupletten en refrein.""",

    "bedankt": """🎵 Prompt voor ManusAI – bedanklied voor {ontvanger}, geïnspireerd door hartverwarmende Nederlandse liedjes.

Je bent een oprechte Nederlandstalige songwriter gespecialiseerd in dankbare, waarderende teksten.

Schrijf een oprecht bedanklied voor {ontvanger}, van {van}.
Over {ontvanger}: {beschrijving}

Het lied moet:
- Oprecht dankbaar zijn
- Specifiek benoemen waarom {ontvanger} zo speciaal is
- Warm en persoonlijk aanvoelen
- Een memorabel refrein hebben dat de dankbaarheid benadrukt

Extra wensen: {extra_wens}

Maak een complete songtekst met coupletten en refrein.""",
}

def get_template(style: str) -> str:
    """
    Haalt de template op voor een specifieke stijl.
    Als de stijl niet bestaat, wordt een algemene template gebruikt.
    
    Args:
        style: De gewenste stijl voor de songtekst
        
    Returns:
        De template string voor de opgegeven stijl
    """
    style_lower = style.lower()
    
    if style_lower in FALLBACK_TEMPLATES:
        return FALLBACK_TEMPLATES[style_lower]
    
    # Zoek naar gedeeltelijke matches
    for key in FALLBACK_TEMPLATES:
        if key in style_lower or style_lower in key:
            return FALLBACK_TEMPLATES[key]
    
    # Fallback naar algemene template
    return """🎵 Prompt voor ManusAI – lied voor {ontvanger}.

Schrijf een origineel Nederlandstalig lied voor {ontvanger}, van {van}.
Over {ontvanger}: {beschrijving}
Stijl gewenst: {stijl}

Het lied moet:
- Persoonlijk voelen door details over {ontvanger} te verwerken
- Een memorabel refrein hebben
- Passen bij de gewenste stijl: {stijl}

Extra wensen: {extra_wens}

Maak een complete songtekst met coupletten en refrein."""

def generate_enhanced_prompt(song_data: dict, db: Session = None, use_suno: bool = False) -> str:
    """
    Genereert een AI-prompt op basis van de songdata en thema database.
    
    Args:
        song_data: Dictionary met de songdata (ontvanger, van, beschrijving, etc.)
        db: Database session (optioneel)
        use_suno: Of Suno.ai geoptimaliseerde prompt moet worden gebruikt
        
    Returns:
        Een gegenereerde prompt string
    """
    thema_service = get_thema_service(db)
    
    # Probeer thema data op te halen uit database
    thema_data = thema_service.generate_thema_data(song_data["stijl"])
    
    # Zorg ervoor dat extra_wens een waarde heeft
    if "extra_wens" not in song_data or not song_data["extra_wens"]:
        song_data["extra_wens"] = "Geen extra wensen opgegeven"
    
    if use_suno and thema_data:
        return _generate_suno_prompt(song_data, thema_data)
    else:
        return _generate_standard_prompt(song_data, thema_data)

def _generate_suno_prompt(song_data: dict, thema_data: dict) -> str:
    """Genereer Suno.ai geoptimaliseerde prompt"""
    keywords = ", ".join(thema_data['keywords'][:3])
    power_phrase = random.choice(thema_data['power_phrases']) if thema_data['power_phrases'] else "Speciaal voor jou"
    rhyme_words = " - ".join(thema_data['rhyme_words'][:3])
    instruments = " ".join(thema_data['instruments'][:3])
    effects = " ".join(thema_data['effects'][:2])
    
    return f"""🎵 Suno.ai Enhanced Prompt voor {song_data["ontvanger"]}

THEMA: {thema_data['display_name'].upper()}
VOOR: {song_data["ontvanger"]}
VAN: {song_data["van"]}

BESCHRIJVING: {song_data["beschrijving"]}

[intro][{", ".join(thema_data['genres'])}][language:Dutch] BPM {thema_data['bpm']} {thema_data['rhyme_pattern']}
Toonsoort: {thema_data['key']}

MUZIKALE PARAMETERS:
- Instrumenten: {instruments}
- Effecten: {effects}
- Ritme: {thema_data['rhyme_pattern']}

THEMA-SPECIFIEKE ELEMENTEN:
- Kernwoorden: {keywords}
- Power phrase: "{power_phrase}"
- Rijmwoorden: {rhyme_words}

[verse]
{random.choice(thema_data['verse_starters']) if thema_data['verse_starters'] else 'Begin het lied'}

[chorus]
(Integreer: "{power_phrase}")

EXTRA WENSEN: {song_data["extra_wens"]}

Genereer een professionele Nederlandse songtekst die deze parameters optimaal gebruikt!"""

def _generate_standard_prompt(song_data: dict, thema_data: dict) -> str:
    """Genereer standaard enhanced prompt"""
    base_template = get_template(song_data["stijl"])
    
    if thema_data and thema_data['keywords']:
        # Verrijk de template met database elementen
        keywords = ", ".join(thema_data['keywords'][:4])
        power_phrase = random.choice(thema_data['power_phrases']) if thema_data['power_phrases'] else ""
        
        enhanced_template = base_template + f"""

THEMA-SPECIFIEKE ELEMENTEN:
- Gebruik deze woorden: {keywords}
- Probeer deze zin te integreren: "{power_phrase}"
- Rijmwoorden suggestie: {" - ".join(thema_data['rhyme_words'][:3])}"""
        
        return enhanced_template.format(**song_data)
    else:
        # Fallback naar originele template
        return base_template.format(**song_data)

def generate_prompt(song_data: dict, db: Session = None) -> str:
    """
    Backward compatibility function - werkt met bestaande code
    """
    return generate_enhanced_prompt(song_data, db, use_suno=False)
