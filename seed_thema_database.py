#!/usr/bin/env python3
"""
Seed script voor Thema Database
Laadt basis thema's en elementen gebaseerd op de Suno.ai prompting data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaElement, ThemaRhymeSet

def seed_database():
    """Laad basis thema data in de database"""
    db = SessionLocal()
    
    try:
        # Check of we al data hebben
        if db.query(Thema).first():
            print("Database heeft al thema data. Gebruik --force om opnieuw te seeden.")
            return
        
        print("🎵 Seeding Thema Database...")
        
        # VERJAARDAG THEMA
        verjaardag_thema = Thema(
            name="verjaardag",
            display_name="Verjaardag Viering",
            description="Vrolijke verjaardagsliedjes met feestelijke sfeer",
            is_active=True
        )
        db.add(verjaardag_thema)
        db.flush()  # Get ID
        
        # Verjaardag elementen
        verjaardag_elements = [
            # Keywords
            ("keyword", "feest", "any", 3),
            ("keyword", "party", "any", 3),
            ("keyword", "taart", "any", 3),
            ("keyword", "kaarsjes", "any", 2),
            ("keyword", "wensen", "any", 2),
            ("keyword", "cadeaus", "any", 2),
            ("keyword", "hoera", "chorus", 4),
            ("keyword", "jarig", "any", 4),
            ("keyword", "vieren", "any", 3),
            
            # Power Phrases
            ("power_phrase", "Het is jouw speciale dag", "chorus", 4),
            ("power_phrase", "Hoera, vandaag ben jij de ster", "chorus", 3),
            ("power_phrase", "Een feest voor jou alleen", "chorus", 3),
            ("power_phrase", "Laat het feest beginnen", "intro", 2),
            
            # Genres (Suno.ai formatted)
            ("genre", "pop", "any", 3),
            ("genre", "acoustic pop", "any", 2),
            ("genre", "happy folk", "any", 2),
            ("genre", "party anthem", "any", 1),
            
            # BPM
            ("bpm", "120", "any", 3),
            ("bpm", "130", "any", 2),
            ("bpm", "110", "any", 1),
            
            # Key
            ("key", "C majeur", "any", 3),
            ("key", "G majeur", "any", 2),
            ("key", "D majeur", "any", 2),
            
            # Instruments (Suno format)
            ("instrument", "[acoustic guitar]", "any", 3),
            ("instrument", "[piano]", "any", 3),
            ("instrument", "[drums]", "any", 2),
            ("instrument", "[celebration bells]", "any", 1),
            
            # Effects
            ("effect", "[warm tone]", "any", 2),
            ("effect", "[party atmosphere]", "any", 2),
            ("effect", "[happy vibes]", "any", 3),
            
            # Verse starters
            ("verse_starter", "Vandaag is een bijzondere dag", "verse", 3),
            ("verse_starter", "Er wordt een feestje gevierd", "verse", 2),
            ("verse_starter", "Kaarsjes op de taart", "verse", 2),
        ]
        
        for element_type, content, context, weight in verjaardag_elements:
            element = ThemaElement(
                thema_id=verjaardag_thema.id,
                element_type=element_type,
                content=content,
                usage_context=context,
                weight=weight,
                suno_format=content if "[" in content else None
            )
            db.add(element)
        
        # Verjaardag rijmsets
        verjaardag_rhymes = [
            ("AABB", ["dag", "mag", "zag", "vraag"], "medium"),
            ("AABB", ["taart", "hart", "start", "apart"], "easy"),
            ("ABAB", ["feest", "jarig", "meest", "waardig"], "medium"),
            ("AABB", ["vieren", "versieren", "gieren", "plezieren"], "hard"),
        ]
        
        for pattern, words, difficulty in verjaardag_rhymes:
            rhyme_set = ThemaRhymeSet(
                thema_id=verjaardag_thema.id,
                rhyme_pattern=pattern,
                words=words,
                difficulty_level=difficulty
            )
            db.add(rhyme_set)
        
        # LIEFDE THEMA
        liefde_thema = Thema(
            name="liefde",
            display_name="Liefde & Romantiek",
            description="Romantische liedjes vol emotie en tederheid",
            is_active=True
        )
        db.add(liefde_thema)
        db.flush()
        
        # Liefde elementen
        liefde_elements = [
            # Keywords
            ("keyword", "hart", "any", 4),
            ("keyword", "liefde", "any", 4),
            ("keyword", "samen", "any", 3),
            ("keyword", "eeuwig", "any", 2),
            ("keyword", "dromen", "any", 2),
            ("keyword", "kussen", "any", 2),
            ("keyword", "omhelzen", "any", 2),
            ("keyword", "verliefd", "any", 3),
            
            # Power Phrases
            ("power_phrase", "Jij bent mijn alles", "chorus", 4),
            ("power_phrase", "Voor altijd samen", "chorus", 3),
            ("power_phrase", "Mijn hart klopt voor jou", "chorus", 3),
            ("power_phrase", "Onze liefde is sterk", "bridge", 2),
            
            # Genres
            ("genre", "romantic ballad", "any", 4),
            ("genre", "acoustic love song", "any", 3),
            ("genre", "soft pop", "any", 2),
            ("genre", "singer-songwriter", "any", 2),
            
            # BPM (langzamer voor romantiek)
            ("bpm", "80", "any", 3),
            ("bpm", "90", "any", 2),
            ("bpm", "70", "any", 2),
            
            # Key (vaak mineur voor emotie)
            ("key", "A mineur", "any", 3),
            ("key", "E mineur", "any", 2),
            ("key", "C majeur", "any", 2),
            
            # Instruments
            ("instrument", "[acoustic guitar]", "any", 4),
            ("instrument", "[piano]", "any", 4),
            ("instrument", "[strings]", "any", 2),
            ("instrument", "[soft drums]", "any", 1),
            
            # Effects
            ("effect", "[intimate atmosphere]", "any", 3),
            ("effect", "[warm reverb]", "any", 2),
            ("effect", "[romantic mood]", "any", 3),
            
            # Verse starters
            ("verse_starter", "Toen ik jou ontmoette", "verse", 3),
            ("verse_starter", "In jouw ogen zie ik", "verse", 3),
            ("verse_starter", "Samen door het leven", "verse", 2),
        ]
        
        for element_type, content, context, weight in liefde_elements:
            element = ThemaElement(
                thema_id=liefde_thema.id,
                element_type=element_type,
                content=content,
                usage_context=context,
                weight=weight,
                suno_format=content if "[" in content else None
            )
            db.add(element)
        
        # Liefde rijmsets
        liefde_rhymes = [
            ("AABB", ["hart", "start", "apart", "smart"], "easy"),
            ("ABAB", ["liefde", "samen", "blijde", "dramen"], "medium"),
            ("AABB", ["kussen", "tussen", "wissen", "missen"], "medium"),
            ("ABCB", ["droom", "ogen", "boom", "verborgen"], "hard"),
        ]
        
        for pattern, words, difficulty in liefde_rhymes:
            rhyme_set = ThemaRhymeSet(
                thema_id=liefde_thema.id,
                rhyme_pattern=pattern,
                words=words,
                difficulty_level=difficulty
            )
            db.add(rhyme_set)
        
        # HUWELIJK THEMA
        huwelijk_thema = Thema(
            name="huwelijk",
            display_name="Huwelijk & Trouw",
            description="Speciale liedjes voor trouwdag en huwelijksfeest",
            is_active=True
        )
        db.add(huwelijk_thema)
        db.flush()
        
        # Huwelijk elementen
        huwelijk_elements = [
            ("keyword", "trouwen", "any", 4),
            ("keyword", "bruiloft", "any", 3),
            ("keyword", "ja-woord", "any", 3),
            ("keyword", "ringen", "any", 2),
            ("keyword", "beloftes", "any", 2),
            ("keyword", "voor altijd", "any", 3),
            ("keyword", "bruid", "any", 2),
            ("keyword", "bruidegom", "any", 2),
            
            ("power_phrase", "Vandaag zeggen we ja", "chorus", 4),
            ("power_phrase", "Voor het leven verbonden", "chorus", 3),
            ("power_phrase", "Onze liefde wordt bezegeld", "bridge", 2),
            
            ("genre", "wedding ballad", "any", 4),
            ("genre", "ceremonial", "any", 2),
            ("genre", "acoustic wedding", "any", 3),
            
            ("bpm", "85", "any", 3),
            ("bpm", "95", "any", 2),
            
            ("instrument", "[wedding bells]", "intro", 3),
            ("instrument", "[acoustic guitar]", "any", 3),
            ("instrument", "[piano]", "any", 4),
            ("instrument", "[strings section]", "any", 2),
        ]
        
        for element_type, content, context, weight in huwelijk_elements:
            element = ThemaElement(
                thema_id=huwelijk_thema.id,
                element_type=element_type,
                content=content,
                usage_context=context,
                weight=weight,
                suno_format=content if "[" in content else None
            )
            db.add(element)
        
        # Commit alle wijzigingen
        db.commit()
        
        print("✅ Database succesvol geseeded!")
        print(f"   - {db.query(Thema).count()} thema's toegevoegd")
        print(f"   - {db.query(ThemaElement).count()} elementen toegevoegd")
        print(f"   - {db.query(ThemaRhymeSet).count()} rijmsets toegevoegd")
        
    except Exception as e:
        print(f"❌ Fout bij seeden: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    force = "--force" in sys.argv
    if force:
        print("🧹 Force mode: removing existing data first...")
        db = SessionLocal()
        try:
            db.query(ThemaRhymeSet).delete()
            db.query(ThemaElement).delete()
            db.query(Thema).delete()
            db.commit()
            print("   Existing data removed.")
        finally:
            db.close()
    
    seed_database() 