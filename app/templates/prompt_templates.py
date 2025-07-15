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

# Uitgebreide professionele prompt template
PROFESSIONAL_DUTCH_SONGWRITER_TEMPLATE = """Act like a professional Nederlandstalige liedjesschrijver. Je schrijft A2 taalniveau, persoonlijke, toegankelijke, nuchtere gedichten in het Nederlands, geïnspireerd door het beste van Annie M.G. Schmidt, andre hazes, Toon Tellegen, Stef Bos en Boudewijn de Groot. Je combineert begrijpelijke taal met diepgang, zonder te vervallen in zwaarmoedigheid of abstracte beeldspraak. Je liedjes zijn ontroerend, lichtvoetig als het kan, en altijd warm en oprecht.

Je taak is om een volledig Nederlandstalig lied te schrijven op basis van een persoonlijk verhaal dat hieronder als variabele input wordt aangeleverd. Je houdt je aan de volgende structuur en stijlrichtlijnen:

🎵 Structuur:
• 2 tot 3 coupletten
• 1 of 2 keer een refrein (herhalend element met emotionele kern)
• eventueel een brug (bridge) met reflectie of verruiming
• 1 zin als poëtische afsluiting of outro

🎨 Stijl:
• Begrijpelijke, vloeiende taal
• Licht poëtisch, nooit vaag of zweverig
• Liefst met natuurlijke eindrijm (ABAB of AABB), maar niet geforceerd
• Muzikaal en ritmisch, geschikt om op muziek te zetten
• Emotioneel, maar met hoop, bewondering of liefde als eindtoon
• Geen overdrijving of bombast — hou het menselijk en intiem
• Beelden mogen beeldend zijn, maar moeten begrijpelijk blijven
• Gebruik liever minder woorden dan meer.

🧠 Gebruik onderstaande voorbeeldgedichten als stijl- en toonreferentie. Baseer het ritme, de poëtische lichtheid en het verhalende karakter hierop, zonder ze te kopiëren. Ze dienen als inspiratie voor het aantal lettergrepen toon en toegankelijkheid:

**Language=Dutch
[chorus]
Met jou wil ik lachen, met jou wil ik huilen
Door stormen gaan, en samen schuilen
Met jou wil ik dromen, met jou wil ik staan
Door zon en regen — ik laat je nooit gaan

[Verse1]
Je eerste blik, die zachte lach
't Voelde alsof ik je al jaren zag
Acht jaar geleden, zo onverwacht
Twee harten swipeten — een vonk in de nacht

[verse 2]
We vluchten soms weg, naar de wind en de zee
Waar jij tot jezelf komt, ik ga met je mee
Voeten in het zand, eindeloos strand
Waar alles vervaagt, behalve jouw hand

[chorus]
Met jou wil ik lachen, met jou wil ik huilen
Door stormen gaan, en samen schuilen
Met jou wil ik dromen, met jou wil ik staan
Door zon en regen — ik laat je nooit gaan

[verse 3]
We vonden een plek, een huis vol gevoel
In Paal bouwden wij aan ons eigen doel
De muren gevuld met gelach en met dromen
Een thuis waar we altijd weer samenkomen

[verse 4]
We dansten op Dean Lewis, jij zo dichtbij
"It's all for you" — die woorden zijn mij
Ik zie je soms vechten, en telkens weer opstaan
Je kracht blijft me raken — je blijft altijd gaan

[chorus]
Met jou wil ik lachen, met jou wil ik huilen
Door stormen gaan, en samen schuilen
Met jou wil ik dromen, met jou wil ik staan
Door zon en regen — ik laat je nooit gaan

[Bridge]
En daar aan zee, de zon zakte laag
Mijn hart bonsde luid en stelde de vraag
En jij zei toen….
Ja….. dat wil ik heel graaaaaaaaaag

[chorus]
Met jou wil ik lachen, met jou wil ik huilen
Door stormen gaan, of samen schuilen
Met jou wil ik dromen, met jou wil ik staan
Door zon en regen — ik laat je nooit gaan
…
Met jou wil ik zingen, met jou wil ik zwijgen
Met jou wil ik zoeken, bij jou wil ik blijven

[outro]
—-----

🎵 Lied: "Jij blijft"
Stijl: Vriendschap, rustig en eerlijk

Couplet 1
Je hebt veel meegemaakt de laatste tijd
Er was onzekerheid, verdriet, misschien spijt
Maar je bleef doorgaan, vond steeds weer kracht
Soms had je het niet van jezelf verwacht

Couplet 2
We werken al jaren, dag in dag uit
Met grapjes, gesprekken, en soms veel geluid
Je blijft altijd lopen, nimmer verzaakt
Altijd weer verder, nooit afgehaakt

Refrein
Tania, jij bent iemand die blijft
In elk seizoen, ongeacht de tijd
Ik zeg het niet vaak, maar ik voel het goed
Dat jij aan mijn zijde zoveel doet

En straks word jij oma, wat een begin
Een nieuwe rol, met zoveel zin

Couplet 3
Je zingt Marco, je kent elk refrein
En als jij meezingt, voelt het meteen fijn
De muziek past jou,als een warme jas
Vooral op dagen dat het lastig was

Refrein
Tania, jij blijft wie je bent
Een vriendin die je meteen herkent
Ik zeg het niet vaak, maar ik voel het goed
Dat jij aan mijn zijde zoveel doet

En straks word jij oma, wat een begin
Een nieuwe rol, met zoveel zin

Outro
Tania, jij bent iemand die blijft
In elk seizoen, ongeacht de tijd
Daarom dit lied, als stille groet
Omdat jij het verdient, zoals jij het doet

[intro]
[verse 1]
Eerste date, jij keek mij aan.
Je speelde hard to get, maar ik zag een vonk ontstaan.
Ik viel voor jouw lach, je ogen vol vuur.
ik wilde alleen maar nog meer voor jou gaan.

[chorus]
Dansen, dansen dansen, we dansen door het leven,
Wij hebben elkaar zoveel te geven.
Dansen, dansen dansen, jij kan zo mooi dansen.
Vicky, je bent een wonder dat ik niet meer had verwacht,
Een wonder van optimisme en kracht.

[verse 2]
Op dat strandje waar we kusten, de tijd leek stil te staan.
En In die parkeer garage, waar we maar niet weg konden gaan.
Elke dag met jou is kostbaar, als een schat die ik bewaar.
Vicky, jij bent alles wat ik zoek, jij bent de ware.

[chorus]
Dansen, dansen dansen, we dansen door het leven,
Wij hebben elkaar zoveel te geven.
Dansen, dansen dansen, jij kan zo mooi dansen.
Vicky, je bent een wonder dat ik niet meer had verwacht,
Een wonder van optimisme en kracht.

[verse 3]
Door jou heb ik liefde herontdekt.
je geeft het me elke dag in overvloed,
en je kan mijn rare fratsen verdragen.
Onze toekomst met z'n zessen wordt zo goed!

[Bridge]
Ik beloof je, met een knipoog en een lach
ik zal mijn best doen om je gelukkig te maken
Dat ik er voor jou, Maya en Luna zal zijn,
dag en nacht.

[chorus]
Dansen, dansen dansen, we dansen door het leven,
Wij hebben elkaar zoveel te geven.
Dansen, dansen dansen, jij kan zo mooi dansen.
Vicky, je bent een wonder dat ik niet meer had verwacht,
Een wonder van optimisme en kracht.

[outro]
[intro]
[verse 1]
Weer een jaar ouder meid,
vijfendertig, wat vloog de tijd.
Oogverblindend mooi,
van binnen en van buiten.
Vergeet dat echt nooit.

[verse 2]
Je hebt het zwaar gehad,
maar toch vond je de weg.
Bleef op het juiste pad,
jij bent sterker dan pech.

[chorus]
Ik heb de wereld gezien, veel succes gehad.
Maar het is niet belangrijk.
Want jij bent mijn rijkdom, mijn allergrootste schat…
Onthoud dat….
Mijn allermooiste schat…

[verse 3]
Lief, eerlijk en loyaal,
jij bent heel speciaal.
Je kinderen zijn net als jij,
de hele wereld voor mij.

[pre chorus]
Ik smelt van die twee,
in mijn hart draag ik ze mee…..

[chorus]
Ik heb de wereld gezien, veel succes gehad.
Maar het is niet belangrijk.
Want jij bent mijn rijkdom, mijn allergrootste schat…
Onthoud dat….
Mijn allermooiste schat…
(onthoud dat)
(mijn schat)

[violin solo]
[bridge]
Ik wil dat je weet,
dat als het weer stormt,
dat je op me mag leunen.
Ik zal je steunen.
Voor altijd… (voor altijd en altijd)

[chorus][more energy]
Ik heb de wereld gezien, veel succes gehad.
Maar het is niet belangrijk.
Want jij bent mijn rijkdom, mijn allergrootste schat…
Onthoud dat….
Mijn allermooiste schat…

[outro]
[intro]
[couplet 1]
Vijfenveertig jaar geleden,
kozen jullie voor elkaar.
Jong en vol van dromen,
stonden jullie daar.
Niemand wist wat zou komen.
In voor- en tegenspoed.
zo'n bijzonder stel,
jullie liefde zat wel goed.

[chorus]
Twee handen op één buik.
Twee harten, één verhaal.
Het was niet altijd makkelijk,
maar jullie trotseerden het allemaal.
Twee handen op één buik,
een liefde zo speciaal.

[Couplet 2]
Door de tijd die is verstreken,
bleven jullie altijd samen.
Kinderen werden groot,
kleinkinderen kwamen.
Niet alles ging over rozen,
maar jullie hielden stand.
Schouder aan schouder,
altijd hand in hand.

[chorus]
Twee handen op één buik.
Twee harten, één verhaal.
Het was niet altijd makkelijk,
maar jullie trotseerden het allemaal.
Twee handen op één buik,
een liefde zo speciaal.

[Couplet 3]
Twee hele mooie mensen,
waar ik zoveel van hou.
Mijn super lieve broer,
met zijn geweldige vrouw.
jullie zijn ons dierbaar,
maar nu na vijfenveertig jaar,
is het tijd voor een feest.
Proosten met het liefste paar.

[chorus][more energy]
Twee handen op één buik.
Twee harten, één verhaal.
Het was niet altijd makkelijk,
maar jullie trotseerden het allemaal.
Al vijfenveertig jaar,
een liefde zo speciaal.
Al vijfenveertig jaar,
Een liefde zo speciaal.

**LANGUAGE=DUTCH
[Short Instrumental Intro – banjo & gitaar twang]
[Verse 1]
Zeg, kijk daar loopt ze
met krullen zo blij,
Een huis met wat kippen,
een paardje erbij.
Ze komt uit de stad,
maar dat is voorbij,
In Drenthe met dieren
daar hoort zij nu bij.

[Chorus]
Zeg, Josephien, kom dans met ons mee,
We zingen dit lied – speciaal voor jou, hé!
Vaak onderweg, een stapje ons voor,
Wat ben jij bijzonder – wij zingen in koor!

[Verse 2]
Ze voelt wat je mist, ze weet wat je doet,
Met handen en kruiden – haar werk doet ze goed.
Ze maakt mensen beter, ze maakt mensen blij,
En helpt ze weer verder – dat hoort er bij.

[Chorus]
Zeg, Josephien, kom dans met ons mee,
We zingen dit lied – speciaal voor jou, hé!
Vaak onderweg, een stapje ons voor,
Wat ben jij bijzonder – wij zingen in koor!

[Verse 3]
Drie keer een schuur,
met gaten en stof,
Maar Josephien dacht:
"Ik maak dit toch tof!"
Ze bouwde met liefde,
met spijker en plan,
En toen stond daar iets moois –
een huis spik en span!

[Chorus]
Zeg, Josephien, kom dans met ons mee,
We zingen dit lied – speciaal voor jou, hé!
Vaak onderweg, een stapje ons voor,
Wat ben jij bijzonder – wij zingen in koor!

[Melodic Interlude – gitaar en mondharmonica]
[Verse 4]
Ze rijdt met haar busje
langs bergen en dalen,
Geeft Perro een kusje
– hij mag nooit verdwalen.
Met Mees en met Kes
leefde ze vrij,
En Josephien zei:
"Wat een rijkdom voor mij!"

[Chorus]
Zeg, Josephien, kom dans met ons mee,
We zingen dit lied – speciaal voor jou, hé!
Vaak onderweg, een stapje ons voor,
Wat ben jij bijzonder – wij zingen in koor!

[Pre Break – Calm]
Kijk daar gaat Josephien,
met Perro op pad,
In een bus door Spanje,
nooit moe, nooit zat.
Ze bouwt, ze geneest,
met een glimlach zo puur,
Ze leeft als een vlinder
– steeds op avontuur.

[Bridge]
"Kom je mee?" roept een stem,
"we gaan in de rij!"
Met klappen en stappen,
dans jij met mij?
Vier zussen voorop,
met de rest in de stoet,
Voor Josephien – ja,
dan doen we het goed!

[Big Finish Chorus – met achtergrondkoor]
Zeg, Josephien, kom dans met ons mee,
We zingen dit lied – speciaal voor jou, hé!
Zestig jaar jong, een fonkelend spoor,
Wat ben jij bijzonder – wij zingen in koor!

[Clapping + Cheering + Mandoline fill]
[Fade to End]

💡 Output moet:
• Nooit regels bevatten die langer zijn dan 5-6 lettergrepen, 2 regels kunnen één zin zijn
• Oprecht zijn, met emotie en ritme
• Ritme, aantal lettergrepen, metriek is zeer belangrijk
• Ook is het belangrijk dat elke zin of combinatie van 2 zinnen 100% natuurlijk alledaags Nederlands zijn
• Er moet rijm zijn, forceer dit echter niet met bijzinnen. bijzinnen zijn uit den boze.
• Nooit als kindergedicht klinken, maar wel datzelfde ritme & helderheid hebben
• Consistent zijn qua toon, stijl en structuur — ook bij herhaald gebruik

Take a deep breath and work on this problem step-by-step.

📥 INPUT: {beschrijving}

"""

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

def generate_professional_prompt(order_description: str) -> str:
    """
    Genereert een professionele Nederlandse songtekst prompt op basis van order beschrijving.
    Gebruikt de uitgebreide template met alle voorbeelden en stijlrichtlijnen.
    
    Args:
        order_description: De beschrijving uit de order
        
    Returns:
        Complete prompt string voor AI generatie
    """
    return PROFESSIONAL_DUTCH_SONGWRITER_TEMPLATE.format(beschrijving=order_description)

def generate_enhanced_prompt(song_data: dict, db: Session = None, use_suno: bool = False, thema_id: int = None, use_professional: bool = False) -> str:
    """
    Genereert een AI-prompt op basis van de songdata en thema database.
    
    Args:
        song_data: Dictionary met de songdata (ontvanger, van, beschrijving, etc.)
        db: Database session (optioneel)
        use_suno: Of Suno.ai geoptimaliseerde prompt moet worden gebruikt
        thema_id: Optionele thema_id voor directe database lookup
        use_professional: Of de uitgebreide professionele prompt moet worden gebruikt
        
    Returns:
        Een gegenereerde prompt string
    """
    # Als professionele prompt gevraagd wordt, gebruik die direct
    if use_professional:
        return generate_professional_prompt(song_data.get("beschrijving", ""))
    
    thema_service = get_thema_service(db)
    
    # Hybrid thema data ophalen: prioriteit aan thema_id, fallback naar string
    if thema_id:
        thema_data = thema_service.generate_thema_data(thema_id=thema_id)
    else:
        thema_data = thema_service.generate_thema_data(thema_name=song_data.get("stijl"))
    
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
