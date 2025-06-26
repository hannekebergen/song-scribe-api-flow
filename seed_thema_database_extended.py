#!/usr/bin/env python3
"""
Extended Seed Script voor Thema Database
Implementeert alle Suno.ai thema data uit de prompting guide
Voegt alleen ontbrekende thema's toe en breidt bestaande uit
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaElement, ThemaRhymeSet

def seed_extended_database():
    """Laad alle uitgebreide thema data in de database"""
    db = SessionLocal()
    
    try:
        print("🎵 Extending Thema Database with Suno.ai data...\n")
        
        now = datetime.now()
        
        # Check bestaande thema's
        existing_themes = {t.name: t for t in db.query(Thema).all()}
        print(f"📊 Found {len(existing_themes)} existing themes: {list(existing_themes.keys())}")
        
        # ==== THEMA 1: LIEFDE (Uitbreiden) ====
        if "liefde" in existing_themes:
            print("💕 Extending LIEFDE theme with Suno.ai elements...")
            liefde_thema = existing_themes["liefde"]
            
            # Voeg nieuwe Suno.ai elementen toe
            liefde_new_elements = [
                # Vocale descriptors
                ("vocal_descriptor", "[soft female vocal]", "any", 4, "[soft female vocal]"),
                ("vocal_descriptor", "[warm male vocal]", "any", 4, "[warm male vocal]"),
                ("vocal_descriptor", "(harmonies)", "chorus", 3, "(harmonies)"),
                ("vocal_descriptor", "(whispering)", "verse", 2, "(whispering)"),
                ("vocal_descriptor", "(emotioneel)", "any", 3, "(emotioneel)"),
                ("vocal_descriptor", "(passievol)", "chorus", 3, "(passievol)"),
                
                # Effect tags
                ("effect", "[reverb heavy]", "any", 3, "[reverb heavy]"),
                ("effect", "[warm tone]", "any", 4, "[warm tone]"),
                ("effect", "[dreamy]", "any", 3, "[dreamy]"),
                
                # Control hacks
                ("control_hack", "[[WARMTE]]", "any", 4, "[[WARMTE]]"),
                ("control_hack", "[[PASSIE]]", "chorus", 4, "[[PASSIE]]"),
                
                # Verse starters
                ("verse_starter", "Toen ik jou ontmoette", "verse", 4),
                ("verse_starter", "In jouw ogen zie ik", "verse", 4),
                ("verse_starter", "Samen door het leven", "verse", 3),
                ("verse_starter", "Jouw hand in de mijne", "verse", 3),
            ]
            
            for element_type, content, context, weight, *suno_format in liefde_new_elements:
                element = ThemaElement(
                    thema_id=liefde_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # ==== THEMA 2: HUWELIJK (Uitbreiden) ====
        if "huwelijk" in existing_themes:
            print("💒 Extending HUWELIJK theme with Suno.ai elements...")
            huwelijk_thema = existing_themes["huwelijk"]
            
            huwelijk_new_elements = [
                # Vocale descriptors
                ("vocal_descriptor", "[warm male vocal]", "any", 4, "[warm male vocal]"),
                ("vocal_descriptor", "[soft female vocal]", "any", 4, "[soft female vocal]"),
                ("vocal_descriptor", "(harmonies)", "chorus", 4, "(harmonies)"),
                ("vocal_descriptor", "(duet)", "chorus", 3, "(duet)"),
                ("vocal_descriptor", "(plechtig)", "any", 3, "(plechtig)"),
                ("vocal_descriptor", "(vreugdevol)", "chorus", 3, "(vreugdevol)"),
                
                # Effects
                ("effect", "[reverb heavy]", "any", 4, "[reverb heavy]"),
                ("effect", "[warm tone]", "any", 4, "[warm tone]"),
                ("effect", "[lush]", "any", 3, "[lush]"),
                
                # Control hacks
                ("control_hack", "[[EEUWIG]]", "chorus", 5, "[[EEUWIG]]"),
                ("control_hack", "[[VERBINTENIS]]", "any", 5, "[[VERBINTENIS]]"),
                
                # Verse starters
                ("verse_starter", "Van die eerste blik, een vonk zo klein", "verse", 4),
                ("verse_starter", "Jouw hand in de mijne, een belofte gedaan", "verse", 4),
                ("verse_starter", "Door alle seizoenen, hand in hand", "verse", 3),
            ]
            
            for element_type, content, context, weight, *suno_format in huwelijk_new_elements:
                element = ThemaElement(
                    thema_id=huwelijk_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # ==== THEMA 3: VERJAARDAG (Uitbreiden) ====
        if "verjaardag" in existing_themes:
            print("🎉 Extending VERJAARDAG theme with Suno.ai elements...")
            verjaardag_thema = existing_themes["verjaardag"]
            
            verjaardag_new_elements = [
                # Vocale descriptors
                ("vocal_descriptor", "[upbeat vocal]", "any", 4, "[upbeat vocal]"),
                ("vocal_descriptor", "[enthusiastic vocal]", "any", 4, "[enthusiastic vocal]"),
                ("vocal_descriptor", "(cheers)", "chorus", 3, "(cheers)"),
                ("vocal_descriptor", "(laughter)", "any", 2, "(laughter)"),
                ("vocal_descriptor", "(group vocals)", "chorus", 3, "(group vocals)"),
                
                # Nieuwe instrumenten
                ("instrument", "[brass section]", "any", 3, "[brass section]"),
                ("instrument", "[synthesizer]", "any", 3, "[synthesizer]"),
                ("instrument", "[electric guitar]", "any", 2, "[electric guitar]"),
                
                # Nieuwe effects
                ("effect", "[bright tone]", "any", 4, "[bright tone]"),
                ("effect", "[energetic]", "any", 4, "[energetic]"),
                ("effect", "[upbeat]", "any", 4, "[upbeat]"),
                
                # Control hacks
                ("control_hack", "[[FEEST]]", "chorus", 5, "[[FEEST]]"),
                ("control_hack", "[[VIERING]]", "any", 5, "[[VIERING]]"),
                
                # Party sounds
                ("special_tag", "[party sounds]", "intro", 2, "[party sounds]"),
            ]
            
            for element_type, content, context, weight, *suno_format in verjaardag_new_elements:
                element = ThemaElement(
                    thema_id=verjaardag_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # ==== THEMA 4: AFSCHEID (Nieuw) ====
        if "afscheid" not in existing_themes:
            print("🕊️ Creating AFSCHEID theme...")
            afscheid_thema = Thema(
                name="afscheid",
                display_name="Afscheid & Herinnering",
                description="Emotionele liedjes over verlies, herinnering en troost",
                is_active=True,
                created_at=now,
                updated_at=now
            )
            db.add(afscheid_thema)
            db.flush()
            
            afscheid_elements = [
                # Hoofdgenres
                ("genre", "Ballad", "any", 5),
                ("genre", "Folk", "any", 4),
                ("genre", "Klassiek", "any", 3),
                ("genre", "Soul", "any", 3),
                ("genre", "Ambient", "any", 2),
                
                # Keywords
                ("keyword", "herinnering", "any", 5),
                ("keyword", "troost", "any", 4),
                ("keyword", "verlies", "any", 3),
                ("keyword", "rust", "any", 4),
                ("keyword", "vrede", "any", 4),
                ("keyword", "koesteren", "any", 4),
                ("keyword", "dierbaar", "any", 4),
                ("keyword", "respectvol", "any", 3),
                ("keyword", "sereen", "any", 3),
                
                # Power Phrases
                ("power_phrase", "Herinneringen koesteren we", "verse", 5),
                ("power_phrase", "In ons hart leef je voort", "chorus", 5),
                ("power_phrase", "Vaarwel, maar niet vergeten", "chorus", 4),
                ("power_phrase", "Voor altijd in onze gedachten", "bridge", 4),
                ("power_phrase", "Jouw aanwezigheid, een zonnestraal", "verse", 3),
                
                # BPM (vaak laag)
                ("bpm", "50", "any", 2),
                ("bpm", "60", "any", 4),
                ("bpm", "65", "any", 4),
                ("bpm", "70", "any", 3),
                ("bpm", "80", "any", 2),
                
                # Toonsoorten (vaak mineur)
                ("key", "A mineur", "any", 5),
                ("key", "E mineur", "any", 4),
                ("key", "D mineur", "any", 4),
                ("key", "C majeur", "any", 2),
                
                # Instrumenten
                ("instrument", "[piano]", "any", 5, "[piano]"),
                ("instrument", "[strings]", "any", 5, "[strings]"),
                ("instrument", "[acoustic guitar]", "any", 4, "[acoustic guitar]"),
                ("instrument", "[cello]", "any", 4, "[cello]"),
                ("instrument", "[violin]", "any", 3, "[violin]"),
                ("instrument", "[choir]", "any", 3, "[choir]"),
                ("instrument", "[soft percussion]", "any", 1, "[soft percussion]"),
                
                # Vocale descriptors
                ("vocal_descriptor", "[soft vocal]", "any", 5, "[soft vocal]"),
                ("vocal_descriptor", "[empathetic vocal]", "any", 4, "[empathetic vocal]"),
                ("vocal_descriptor", "[sincere vocal]", "any", 4, "[sincere vocal]"),
                ("vocal_descriptor", "[whispering]", "verse", 2, "[whispering]"),
                ("vocal_descriptor", "(troostend)", "any", 4, "(troostend)"),
                ("vocal_descriptor", "(herinnerend)", "verse", 3, "(herinnerend)"),
                
                # Effects
                ("effect", "[reverb heavy]", "any", 5, "[reverb heavy]"),
                ("effect", "[warm tone]", "any", 4, "[warm tone]"),
                ("effect", "[dreamy]", "any", 3, "[dreamy]"),
                ("effect", "[ethereal]", "any", 3, "[ethereal]"),
                
                # Control hacks
                ("control_hack", "[[RUST]]", "any", 5, "[[RUST]]"),
                ("control_hack", "[[HERINNERING]]", "verse", 5, "[[HERINNERING]]"),
                
                # Special tags
                ("special_tag", "[silence]", "bridge", 2, "[silence]"),
                
                # Verse starters
                ("verse_starter", "De fietsroutes, de tosti's, elke dag een lach", "verse", 3),
                ("verse_starter", "Herinneringen koesteren we, zo dierbaar en zo fijn", "verse", 4),
                ("verse_starter", "In stilte denken we aan jou", "verse", 4),
            ]
            
            for element_type, content, context, weight, *suno_format in afscheid_elements:
                element = ThemaElement(
                    thema_id=afscheid_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # ==== THEMA 5: VADERDAG (Nieuw) ====
        if "vaderdag" not in existing_themes:
            print("👨‍👧‍👦 Creating VADERDAG theme...")
            vaderdag_thema = Thema(
                name="vaderdag",
                display_name="Vaderdag & Waardering",
                description="Eerbetoon aan vaders, hun inzet en liefde",
                is_active=True,
                created_at=now,
                updated_at=now
            )
            db.add(vaderdag_thema)
            db.flush()
            
            vaderdag_elements = [
                # Hoofdgenres
                ("genre", "Pop", "any", 4),
                ("genre", "Folk", "any", 4),
                ("genre", "Country", "any", 3),
                ("genre", "Akoestisch", "any", 4),
                ("genre", "Ballad", "any", 3),
                
                # Keywords
                ("keyword", "vader", "any", 5),
                ("keyword", "papa", "any", 5),
                ("keyword", "held", "any", 4),
                ("keyword", "trots", "any", 4),
                ("keyword", "dankbaar", "any", 4),
                ("keyword", "waardering", "any", 4),
                ("keyword", "sterke handen", "any", 3),
                ("keyword", "groot hart", "any", 3),
                ("keyword", "wijsheid", "any", 3),
                ("keyword", "bescherming", "any", 3),
                
                # Power Phrases
                ("power_phrase", "De beste papa ter wereld", "chorus", 5),
                ("power_phrase", "Voor alles wat je deed", "verse", 4),
                ("power_phrase", "Een echte held in elke situatie", "chorus", 4),
                ("power_phrase", "Met humor en liefde ons gezin versterkt", "verse", 3),
                ("power_phrase", "Altijd hard gewerkt", "verse", 3),
                
                # BPM
                ("bpm", "70", "any", 3),
                ("bpm", "80", "any", 4),
                ("bpm", "90", "any", 3),
                ("bpm", "100", "any", 2),
                
                # Toonsoorten
                ("key", "C majeur", "any", 4),
                ("key", "G majeur", "any", 4),
                ("key", "D majeur", "any", 3),
                ("key", "F majeur", "any", 2),
                
                # Instrumenten
                ("instrument", "[acoustic guitar]", "any", 5, "[acoustic guitar]"),
                ("instrument", "[piano]", "any", 4, "[piano]"),
                ("instrument", "[bass]", "any", 3, "[bass]"),
                ("instrument", "[light drums]", "any", 3, "[light drums]"),
                ("instrument", "[strings]", "any", 3, "[strings]"),
                ("instrument", "[harmonica]", "any", 2, "[harmonica]"),
                
                # Vocale descriptors
                ("vocal_descriptor", "[warm male vocal]", "any", 5, "[warm male vocal]"),
                ("vocal_descriptor", "[sincere vocal]", "any", 4, "[sincere vocal]"),
                ("vocal_descriptor", "[grateful vocal]", "any", 4, "[grateful vocal]"),
                ("vocal_descriptor", "(trots)", "chorus", 3, "(trots)"),
                ("vocal_descriptor", "(liefdevol)", "any", 4, "(liefdevol)"),
                
                # Effects
                ("effect", "[warm tone]", "any", 5, "[warm tone]"),
                ("effect", "[clear production]", "any", 3, "[clear production]"),
                ("effect", "[subtle reverb]", "any", 3, "[subtle reverb]"),
                
                # Control hacks
                ("control_hack", "[[HELD]]", "chorus", 5, "[[HELD]]"),
                ("control_hack", "[[TROTS]]", "any", 4, "[[TROTS]]"),
                
                # Verse starters
                ("verse_starter", "Lieve papa, altijd hard gewerkt", "verse", 4),
                ("verse_starter", "Jouw handen, zo sterk, jouw hart, zo groot", "verse", 4),
                ("verse_starter", "Van jongs af aan leerde je ons", "verse", 3),
            ]
            
            for element_type, content, context, weight, *suno_format in vaderdag_elements:
                element = ThemaElement(
                    thema_id=vaderdag_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # ==== THEMA 6: ANDERS (Nieuw) ====
        if "anders" not in existing_themes:
            print("🙏 Creating ANDERS theme...")
            anders_thema = Thema(
                name="anders",
                display_name="Anders & Dankbaarheid",
                description="Bedankliedjes, steunliedjes en specifieke gelegenheden",
                is_active=True,
                created_at=now,
                updated_at=now
            )
            db.add(anders_thema)
            db.flush()
            
            anders_elements = [
                # Hoofdgenres
                ("genre", "Pop", "any", 3),
                ("genre", "Folk", "any", 4),
                ("genre", "Ballad", "any", 3),
                ("genre", "Akoestisch", "any", 4),
                
                # Keywords
                ("keyword", "dankbaar", "any", 5),
                ("keyword", "bedankt", "any", 5),
                ("keyword", "hulp", "any", 4),
                ("keyword", "steun", "any", 4),
                ("keyword", "vriendschap", "any", 4),
                ("keyword", "oprecht", "any", 4),
                ("keyword", "waardering", "any", 4),
                ("keyword", "dankbaarheid", "any", 5),
                ("keyword", "geschenk", "any", 3),
                ("keyword", "bijzonder", "any", 3),
                
                # Power Phrases
                ("power_phrase", "Voor alles wat je deed", "verse", 5),
                ("power_phrase", "Een diepe buiging nu", "chorus", 4),
                ("power_phrase", "Jouw vriendschap, jouw liefde", "chorus", 4),
                ("power_phrase", "Een dankbaar hart", "verse", 4),
                ("power_phrase", "Ik dank je, ik dank je", "chorus", 5),
                
                # BPM
                ("bpm", "65", "any", 2),
                ("bpm", "75", "any", 3),
                ("bpm", "85", "any", 4),
                ("bpm", "95", "any", 2),
                
                # Toonsoorten
                ("key", "C majeur", "any", 4),
                ("key", "G majeur", "any", 3),
                ("key", "F majeur", "any", 3),
                ("key", "A mineur", "any", 2),
                
                # Instrumenten
                ("instrument", "[piano]", "any", 5, "[piano]"),
                ("instrument", "[acoustic guitar]", "any", 5, "[acoustic guitar]"),
                ("instrument", "[strings]", "any", 3, "[strings]"),
                ("instrument", "[light percussion]", "any", 2, "[light percussion]"),
                ("instrument", "[warm bass]", "any", 2, "[warm bass]"),
                
                # Vocale descriptors
                ("vocal_descriptor", "[warm vocal]", "any", 5, "[warm vocal]"),
                ("vocal_descriptor", "[empathetic vocal]", "any", 4, "[empathetic vocal]"),
                ("vocal_descriptor", "[sincere vocal]", "any", 5, "[sincere vocal]"),
                ("vocal_descriptor", "[spoken word]", "bridge", 3, "[spoken word]"),
                
                # Effects
                ("effect", "[warm tone]", "any", 5, "[warm tone]"),
                ("effect", "[subtle reverb]", "any", 3, "[subtle reverb]"),
                ("effect", "[clear production]", "any", 4, "[clear production]"),
                
                # Control hacks
                ("control_hack", "[[OPRECHT]]", "any", 5, "[[OPRECHT]]"),
                ("control_hack", "[[DANKBAARHEID]]", "chorus", 5, "[[DANKBAARHEID]]"),
                
                # Verse starters
                ("verse_starter", "Na die zware tijd, stond jij daar klaar", "verse", 4),
                ("verse_starter", "Jouw hulp, een lichtpunt", "verse", 4),
                ("verse_starter", "Met elke stap, elk gebaar", "verse", 3),
            ]
            
            for element_type, content, context, weight, *suno_format in anders_elements:
                element = ThemaElement(
                    thema_id=anders_thema.id,
                    element_type=element_type,
                    content=content,
                    usage_context=context,
                    weight=weight,
                    suno_format=suno_format[0] if suno_format else None,
                    created_at=now
                )
                db.add(element)
        
        # Commit all changes
        db.commit()
        
        # Statistics
        total_themas = db.query(Thema).count()
        total_elements = db.query(ThemaElement).count()
        total_rhyme_sets = db.query(ThemaRhymeSet).count()
        
        print(f"\n🎉 Extended Database Implementation Complete!")
        print(f"   📊 Total themas: {total_themas}")
        print(f"   🧩 Total elements: {total_elements}")
        print(f"   🎵 Total rhyme sets: {total_rhyme_sets}")
        
        # Show per theme statistics
        print(f"\n📈 Per-theme statistics:")
        for thema in db.query(Thema).all():
            count = db.query(ThemaElement).filter_by(thema_id=thema.id).count()
            print(f"   • {thema.name} ({thema.display_name}): {count} elementen")
        
        print(f"\n✅ All Suno.ai theme data successfully implemented!")
        
    except Exception as e:
        print(f"❌ Implementation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_extended_database() 