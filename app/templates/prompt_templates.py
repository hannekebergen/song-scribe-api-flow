"""
Module voor het beheren van prompt templates voor verschillende songstijlen.
Templates worden gebruikt om AI-prompts te genereren op basis van klantinput.
"""

# Dictionary met templates per stijl
# Elke template bevat placeholders die worden ingevuld met klantgegevens
TEMPLATES = {
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

    # Voeg hier meer templates toe voor andere stijlen
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
    # Converteer naar lowercase voor case-insensitive vergelijking
    style_lower = style.lower()
    
    # Probeer een exacte match te vinden
    if style_lower in TEMPLATES:
        return TEMPLATES[style_lower]
    
    # Zoek naar gedeeltelijke matches als er geen exacte match is
    for key in TEMPLATES:
        if key in style_lower or style_lower in key:
            return TEMPLATES[key]
    
    # Fallback naar een algemene template als er geen match is
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

def generate_prompt(song_data: dict) -> str:
    """
    Genereert een AI-prompt op basis van de songdata en de bijbehorende template.
    
    Args:
        song_data: Dictionary met de songdata (ontvanger, van, beschrijving, etc.)
        
    Returns:
        Een gegenereerde prompt string
    """
    # Haal de juiste template op
    template = get_template(song_data["stijl"])
    
    # Zorg ervoor dat extra_wens een waarde heeft als het niet is opgegeven
    if "extra_wens" not in song_data or not song_data["extra_wens"]:
        song_data["extra_wens"] = "Geen extra wensen opgegeven"
    
    # Vul de template in met de songdata
    return template.format(**song_data)
