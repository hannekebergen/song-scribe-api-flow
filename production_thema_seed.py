#!/usr/bin/env python3
"""
Productie Thema Database Seed Script
Gegenereerd op: 2025-06-26T16:39:24.769028
Bevat: 6 themas, 313 elements, 8 rhyme sets
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaElement, ThemaRhymeSet

def seed_production_themas():
    """Seed alle thema data in productie database"""
    db = SessionLocal()
    
    try:
        print("🎵 Seeding Production Thema Database...")
        print("=" * 50)
        
        # Check of er al data is
        existing_count = db.query(Thema).count()
        if existing_count > 0:
            print(f"⚠️  Database bevat al {existing_count} themas")
            confirm = input("Doorgaan en bestaande data overschrijven? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Seeding geannuleerd")
                return
            
            # Clear existing data
            print("🗑️ Clearing existing data...")
            db.query(ThemaRhymeSet).delete()
            db.query(ThemaElement).delete()
            db.query(Thema).delete()
            db.commit()
        
        now = datetime.now()
        thema_id_map = {}
        
        # Seed themas
        print("\n📁 Seeding themas...")
        thema_data = [
        {
                "name": "verjaardag",
                "display_name": "Verjaardag Viering",
                "description": "Vrolijke verjaardagsliedjes met feestelijke sfeer",
                "is_active": true
        },
        {
                "name": "liefde",
                "display_name": "Liefde & Romantiek",
                "description": "Romantische liedjes vol emotie en tederheid",
                "is_active": true
        },
        {
                "name": "huwelijk",
                "display_name": "Huwelijk & Trouw",
                "description": "Speciale liedjes voor trouwdag en huwelijksfeest",
                "is_active": true
        },
        {
                "name": "afscheid",
                "display_name": "Afscheid & Herinnering",
                "description": "Emotionele liedjes over verlies, herinnering en troost",
                "is_active": true
        },
        {
                "name": "vaderdag",
                "display_name": "Vaderdag & Waardering",
                "description": "Eerbetoon aan vaders, hun inzet en liefde",
                "is_active": true
        },
        {
                "name": "anders",
                "display_name": "Anders & Dankbaarheid",
                "description": "Bedankliedjes, steunliedjes en specifieke gelegenheden",
                "is_active": true
        }
]
        
        for thema_info in thema_data:
            thema = Thema(
                name=thema_info['name'],
                display_name=thema_info['display_name'],
                description=thema_info['description'],
                is_active=thema_info['is_active'],
                created_at=now,
                updated_at=now
            )
            db.add(thema)
            db.flush()  # Get ID
            thema_id_map[thema_info['name']] = thema.id
            print(f"✅ {thema.display_name} (ID: {thema.id})")
        
        # Seed elements
        print("\n🏷️ Seeding elements...")
        element_data = [
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "feest",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "party",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "taart",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "kaarsjes",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "wensen",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "cadeaus",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "hoera",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "jarig",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "keyword",
                "content": "vieren",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "power_phrase",
                "content": "Het is jouw speciale dag",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "power_phrase",
                "content": "Hoera, vandaag ben jij de ster",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "power_phrase",
                "content": "Een feest voor jou alleen",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "power_phrase",
                "content": "Laat het feest beginnen",
                "usage_context": "intro",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "genre",
                "content": "pop",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "genre",
                "content": "acoustic pop",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "genre",
                "content": "happy folk",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "genre",
                "content": "party anthem",
                "usage_context": "any",
                "weight": 1,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "bpm",
                "content": "120",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "bpm",
                "content": "130",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "bpm",
                "content": "110",
                "usage_context": "any",
                "weight": 1,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "key",
                "content": "C majeur",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "key",
                "content": "G majeur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "key",
                "content": "D majeur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[drums]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[drums]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[celebration bells]",
                "usage_context": "any",
                "weight": 1,
                "suno_format": "[celebration bells]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[party atmosphere]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[party atmosphere]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[happy vibes]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[happy vibes]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "verse_starter",
                "content": "Vandaag is een bijzondere dag",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "verse_starter",
                "content": "Er wordt een feestje gevierd",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "verse_starter",
                "content": "Kaarsjes op de taart",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "[upbeat vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[upbeat vocal]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "[enthusiastic vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[enthusiastic vocal]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(cheers)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(cheers)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(laughter)",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "(laughter)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(group vocals)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(group vocals)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[brass section]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[brass section]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[synthesizer]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[synthesizer]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[electric guitar]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[electric guitar]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[bright tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[bright tone]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[energetic]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[energetic]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[upbeat]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[upbeat]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "control_hack",
                "content": "[[FEEST]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[FEEST]]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "control_hack",
                "content": "[[VIERING]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[VIERING]]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "special_tag",
                "content": "[party sounds]",
                "usage_context": "intro",
                "weight": 2,
                "suno_format": "[party sounds]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "[upbeat vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[upbeat vocal]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "[enthusiastic vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[enthusiastic vocal]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(cheers)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(cheers)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(laughter)",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "(laughter)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "vocal_descriptor",
                "content": "(group vocals)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(group vocals)"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[brass section]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[brass section]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[synthesizer]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[synthesizer]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "instrument",
                "content": "[electric guitar]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[electric guitar]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[bright tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[bright tone]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[energetic]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[energetic]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "effect",
                "content": "[upbeat]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[upbeat]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "control_hack",
                "content": "[[FEEST]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[FEEST]]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "control_hack",
                "content": "[[VIERING]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[VIERING]]"
        },
        {
                "thema_name": "verjaardag",
                "element_type": "special_tag",
                "content": "[party sounds]",
                "usage_context": "intro",
                "weight": 2,
                "suno_format": "[party sounds]"
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "hart",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "liefde",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "samen",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "eeuwig",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "dromen",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "kussen",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "omhelzen",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "keyword",
                "content": "verliefd",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "power_phrase",
                "content": "Jij bent mijn alles",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "power_phrase",
                "content": "Voor altijd samen",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "power_phrase",
                "content": "Mijn hart klopt voor jou",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "power_phrase",
                "content": "Onze liefde is sterk",
                "usage_context": "bridge",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "genre",
                "content": "romantic ballad",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "genre",
                "content": "acoustic love song",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "genre",
                "content": "soft pop",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "genre",
                "content": "singer-songwriter",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "bpm",
                "content": "80",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "bpm",
                "content": "90",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "bpm",
                "content": "70",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "key",
                "content": "A mineur",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "key",
                "content": "E mineur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "key",
                "content": "C majeur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "liefde",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "liefde",
                "element_type": "instrument",
                "content": "[strings]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[strings]"
        },
        {
                "thema_name": "liefde",
                "element_type": "instrument",
                "content": "[soft drums]",
                "usage_context": "any",
                "weight": 1,
                "suno_format": "[soft drums]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[intimate atmosphere]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[intimate atmosphere]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[warm reverb]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[warm reverb]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[romantic mood]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[romantic mood]"
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Toen ik jou ontmoette",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "In jouw ogen zie ik",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Samen door het leven",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "[soft female vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[soft female vocal]"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "[warm male vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm male vocal]"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(harmonies)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(harmonies)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(whispering)",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": "(whispering)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(emotioneel)",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "(emotioneel)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(passievol)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(passievol)"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[reverb heavy]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[reverb heavy]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[dreamy]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[dreamy]"
        },
        {
                "thema_name": "liefde",
                "element_type": "control_hack",
                "content": "[[WARMTE]]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[[WARMTE]]"
        },
        {
                "thema_name": "liefde",
                "element_type": "control_hack",
                "content": "[[PASSIE]]",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": "[[PASSIE]]"
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Toen ik jou ontmoette",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "In jouw ogen zie ik",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Samen door het leven",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Jouw hand in de mijne",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "[soft female vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[soft female vocal]"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "[warm male vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm male vocal]"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(harmonies)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(harmonies)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(whispering)",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": "(whispering)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(emotioneel)",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "(emotioneel)"
        },
        {
                "thema_name": "liefde",
                "element_type": "vocal_descriptor",
                "content": "(passievol)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(passievol)"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[reverb heavy]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[reverb heavy]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "liefde",
                "element_type": "effect",
                "content": "[dreamy]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[dreamy]"
        },
        {
                "thema_name": "liefde",
                "element_type": "control_hack",
                "content": "[[WARMTE]]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[[WARMTE]]"
        },
        {
                "thema_name": "liefde",
                "element_type": "control_hack",
                "content": "[[PASSIE]]",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": "[[PASSIE]]"
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Toen ik jou ontmoette",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "In jouw ogen zie ik",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Samen door het leven",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "liefde",
                "element_type": "verse_starter",
                "content": "Jouw hand in de mijne",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "trouwen",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "bruiloft",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "ja-woord",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "ringen",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "beloftes",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "voor altijd",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "bruid",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "keyword",
                "content": "bruidegom",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "power_phrase",
                "content": "Vandaag zeggen we ja",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "power_phrase",
                "content": "Voor het leven verbonden",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "power_phrase",
                "content": "Onze liefde wordt bezegeld",
                "usage_context": "bridge",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "genre",
                "content": "wedding ballad",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "genre",
                "content": "ceremonial",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "genre",
                "content": "acoustic wedding",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "bpm",
                "content": "85",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "bpm",
                "content": "95",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "instrument",
                "content": "[wedding bells]",
                "usage_context": "intro",
                "weight": 3,
                "suno_format": "[wedding bells]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "instrument",
                "content": "[strings section]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[strings section]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "[warm male vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm male vocal]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "[soft female vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[soft female vocal]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(harmonies)",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": "(harmonies)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(duet)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(duet)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(plechtig)",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "(plechtig)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(vreugdevol)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(vreugdevol)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[reverb heavy]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[reverb heavy]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[lush]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[lush]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "control_hack",
                "content": "[[EEUWIG]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[EEUWIG]]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "control_hack",
                "content": "[[VERBINTENIS]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[VERBINTENIS]]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Van die eerste blik, een vonk zo klein",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Jouw hand in de mijne, een belofte gedaan",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Door alle seizoenen, hand in hand",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "[warm male vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm male vocal]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "[soft female vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[soft female vocal]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(harmonies)",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": "(harmonies)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(duet)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(duet)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(plechtig)",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "(plechtig)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "vocal_descriptor",
                "content": "(vreugdevol)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(vreugdevol)"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[reverb heavy]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[reverb heavy]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "effect",
                "content": "[lush]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[lush]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "control_hack",
                "content": "[[EEUWIG]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[EEUWIG]]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "control_hack",
                "content": "[[VERBINTENIS]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[VERBINTENIS]]"
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Van die eerste blik, een vonk zo klein",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Jouw hand in de mijne, een belofte gedaan",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "huwelijk",
                "element_type": "verse_starter",
                "content": "Door alle seizoenen, hand in hand",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "genre",
                "content": "Ballad",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "genre",
                "content": "Folk",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "genre",
                "content": "Klassiek",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "genre",
                "content": "Soul",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "genre",
                "content": "Ambient",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "herinnering",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "troost",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "verlies",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "rust",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "vrede",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "koesteren",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "dierbaar",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "respectvol",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "keyword",
                "content": "sereen",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "power_phrase",
                "content": "Herinneringen koesteren we",
                "usage_context": "verse",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "power_phrase",
                "content": "In ons hart leef je voort",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "power_phrase",
                "content": "Vaarwel, maar niet vergeten",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "power_phrase",
                "content": "Voor altijd in onze gedachten",
                "usage_context": "bridge",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "power_phrase",
                "content": "Jouw aanwezigheid, een zonnestraal",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "bpm",
                "content": "50",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "bpm",
                "content": "60",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "bpm",
                "content": "65",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "bpm",
                "content": "70",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "bpm",
                "content": "80",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "key",
                "content": "A mineur",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "key",
                "content": "E mineur",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "key",
                "content": "D mineur",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "key",
                "content": "C majeur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[strings]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[strings]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[cello]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[cello]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[violin]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[violin]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[choir]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[choir]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "instrument",
                "content": "[soft percussion]",
                "usage_context": "any",
                "weight": 1,
                "suno_format": "[soft percussion]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "[soft vocal]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[soft vocal]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "[empathetic vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[empathetic vocal]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "[sincere vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[sincere vocal]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "[whispering]",
                "usage_context": "verse",
                "weight": 2,
                "suno_format": "[whispering]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "(troostend)",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "(troostend)"
        },
        {
                "thema_name": "afscheid",
                "element_type": "vocal_descriptor",
                "content": "(herinnerend)",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": "(herinnerend)"
        },
        {
                "thema_name": "afscheid",
                "element_type": "effect",
                "content": "[reverb heavy]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[reverb heavy]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "effect",
                "content": "[dreamy]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[dreamy]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "effect",
                "content": "[ethereal]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[ethereal]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "control_hack",
                "content": "[[RUST]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[RUST]]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "control_hack",
                "content": "[[HERINNERING]]",
                "usage_context": "verse",
                "weight": 5,
                "suno_format": "[[HERINNERING]]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "special_tag",
                "content": "[silence]",
                "usage_context": "bridge",
                "weight": 2,
                "suno_format": "[silence]"
        },
        {
                "thema_name": "afscheid",
                "element_type": "verse_starter",
                "content": "De fietsroutes, de tosti's, elke dag een lach",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "verse_starter",
                "content": "Herinneringen koesteren we, zo dierbaar en zo fijn",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "afscheid",
                "element_type": "verse_starter",
                "content": "In stilte denken we aan jou",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "genre",
                "content": "Pop",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "genre",
                "content": "Folk",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "genre",
                "content": "Country",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "genre",
                "content": "Akoestisch",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "genre",
                "content": "Ballad",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "vader",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "papa",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "held",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "trots",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "dankbaar",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "waardering",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "sterke handen",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "groot hart",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "wijsheid",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "keyword",
                "content": "bescherming",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "power_phrase",
                "content": "De beste papa ter wereld",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "power_phrase",
                "content": "Voor alles wat je deed",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "power_phrase",
                "content": "Een echte held in elke situatie",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "power_phrase",
                "content": "Met humor en liefde ons gezin versterkt",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "power_phrase",
                "content": "Altijd hard gewerkt",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "bpm",
                "content": "70",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "bpm",
                "content": "80",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "bpm",
                "content": "90",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "bpm",
                "content": "100",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "key",
                "content": "C majeur",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "key",
                "content": "G majeur",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "key",
                "content": "D majeur",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "key",
                "content": "F majeur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[bass]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[bass]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[light drums]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[light drums]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[strings]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[strings]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "instrument",
                "content": "[harmonica]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[harmonica]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "vocal_descriptor",
                "content": "[warm male vocal]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[warm male vocal]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "vocal_descriptor",
                "content": "[sincere vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[sincere vocal]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "vocal_descriptor",
                "content": "[grateful vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[grateful vocal]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "vocal_descriptor",
                "content": "(trots)",
                "usage_context": "chorus",
                "weight": 3,
                "suno_format": "(trots)"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "vocal_descriptor",
                "content": "(liefdevol)",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "(liefdevol)"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "effect",
                "content": "[clear production]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[clear production]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "effect",
                "content": "[subtle reverb]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[subtle reverb]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "control_hack",
                "content": "[[HELD]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[HELD]]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "control_hack",
                "content": "[[TROTS]]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[[TROTS]]"
        },
        {
                "thema_name": "vaderdag",
                "element_type": "verse_starter",
                "content": "Lieve papa, altijd hard gewerkt",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "verse_starter",
                "content": "Jouw handen, zo sterk, jouw hart, zo groot",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "vaderdag",
                "element_type": "verse_starter",
                "content": "Van jongs af aan leerde je ons",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "genre",
                "content": "Pop",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "genre",
                "content": "Folk",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "genre",
                "content": "Ballad",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "genre",
                "content": "Akoestisch",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "dankbaar",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "bedankt",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "hulp",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "steun",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "vriendschap",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "oprecht",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "waardering",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "dankbaarheid",
                "usage_context": "any",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "geschenk",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "keyword",
                "content": "bijzonder",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "power_phrase",
                "content": "Voor alles wat je deed",
                "usage_context": "verse",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "power_phrase",
                "content": "Een diepe buiging nu",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "power_phrase",
                "content": "Jouw vriendschap, jouw liefde",
                "usage_context": "chorus",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "power_phrase",
                "content": "Een dankbaar hart",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "power_phrase",
                "content": "Ik dank je, ik dank je",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "bpm",
                "content": "65",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "bpm",
                "content": "75",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "bpm",
                "content": "85",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "bpm",
                "content": "95",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "key",
                "content": "C majeur",
                "usage_context": "any",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "key",
                "content": "G majeur",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "key",
                "content": "F majeur",
                "usage_context": "any",
                "weight": 3,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "key",
                "content": "A mineur",
                "usage_context": "any",
                "weight": 2,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "instrument",
                "content": "[piano]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[piano]"
        },
        {
                "thema_name": "anders",
                "element_type": "instrument",
                "content": "[acoustic guitar]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[acoustic guitar]"
        },
        {
                "thema_name": "anders",
                "element_type": "instrument",
                "content": "[strings]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[strings]"
        },
        {
                "thema_name": "anders",
                "element_type": "instrument",
                "content": "[light percussion]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[light percussion]"
        },
        {
                "thema_name": "anders",
                "element_type": "instrument",
                "content": "[warm bass]",
                "usage_context": "any",
                "weight": 2,
                "suno_format": "[warm bass]"
        },
        {
                "thema_name": "anders",
                "element_type": "vocal_descriptor",
                "content": "[warm vocal]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[warm vocal]"
        },
        {
                "thema_name": "anders",
                "element_type": "vocal_descriptor",
                "content": "[empathetic vocal]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[empathetic vocal]"
        },
        {
                "thema_name": "anders",
                "element_type": "vocal_descriptor",
                "content": "[sincere vocal]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[sincere vocal]"
        },
        {
                "thema_name": "anders",
                "element_type": "vocal_descriptor",
                "content": "[spoken word]",
                "usage_context": "bridge",
                "weight": 3,
                "suno_format": "[spoken word]"
        },
        {
                "thema_name": "anders",
                "element_type": "effect",
                "content": "[warm tone]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[warm tone]"
        },
        {
                "thema_name": "anders",
                "element_type": "effect",
                "content": "[subtle reverb]",
                "usage_context": "any",
                "weight": 3,
                "suno_format": "[subtle reverb]"
        },
        {
                "thema_name": "anders",
                "element_type": "effect",
                "content": "[clear production]",
                "usage_context": "any",
                "weight": 4,
                "suno_format": "[clear production]"
        },
        {
                "thema_name": "anders",
                "element_type": "control_hack",
                "content": "[[OPRECHT]]",
                "usage_context": "any",
                "weight": 5,
                "suno_format": "[[OPRECHT]]"
        },
        {
                "thema_name": "anders",
                "element_type": "control_hack",
                "content": "[[DANKBAARHEID]]",
                "usage_context": "chorus",
                "weight": 5,
                "suno_format": "[[DANKBAARHEID]]"
        },
        {
                "thema_name": "anders",
                "element_type": "verse_starter",
                "content": "Na die zware tijd, stond jij daar klaar",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "verse_starter",
                "content": "Jouw hulp, een lichtpunt",
                "usage_context": "verse",
                "weight": 4,
                "suno_format": null
        },
        {
                "thema_name": "anders",
                "element_type": "verse_starter",
                "content": "Met elke stap, elk gebaar",
                "usage_context": "verse",
                "weight": 3,
                "suno_format": null
        }
]
        
        for element_info in element_data:
            thema_id = thema_id_map.get(element_info['thema_name'])
            if thema_id:
                element = ThemaElement(
                    thema_id=thema_id,
                    element_type=element_info['element_type'],
                    content=element_info['content'],
                    usage_context=element_info['usage_context'],
                    weight=element_info['weight'],
                    suno_format=element_info['suno_format'],
                    created_at=now
                )
                db.add(element)
        
        # Seed rhyme sets
        print("\n🎵 Seeding rhyme sets...")
        rhyme_data = [
        {
                "thema_name": "verjaardag",
                "rhyme_pattern": "AABB",
                "words": [
                        "dag",
                        "mag",
                        "zag",
                        "vraag"
                ],
                "difficulty_level": "medium"
        },
        {
                "thema_name": "verjaardag",
                "rhyme_pattern": "AABB",
                "words": [
                        "taart",
                        "hart",
                        "start",
                        "apart"
                ],
                "difficulty_level": "easy"
        },
        {
                "thema_name": "verjaardag",
                "rhyme_pattern": "ABAB",
                "words": [
                        "feest",
                        "jarig",
                        "meest",
                        "waardig"
                ],
                "difficulty_level": "medium"
        },
        {
                "thema_name": "verjaardag",
                "rhyme_pattern": "AABB",
                "words": [
                        "vieren",
                        "versieren",
                        "gieren",
                        "plezieren"
                ],
                "difficulty_level": "hard"
        },
        {
                "thema_name": "liefde",
                "rhyme_pattern": "AABB",
                "words": [
                        "hart",
                        "start",
                        "apart",
                        "smart"
                ],
                "difficulty_level": "easy"
        },
        {
                "thema_name": "liefde",
                "rhyme_pattern": "ABAB",
                "words": [
                        "liefde",
                        "samen",
                        "blijde",
                        "dramen"
                ],
                "difficulty_level": "medium"
        },
        {
                "thema_name": "liefde",
                "rhyme_pattern": "AABB",
                "words": [
                        "kussen",
                        "tussen",
                        "wissen",
                        "missen"
                ],
                "difficulty_level": "medium"
        },
        {
                "thema_name": "liefde",
                "rhyme_pattern": "ABCB",
                "words": [
                        "droom",
                        "ogen",
                        "boom",
                        "verborgen"
                ],
                "difficulty_level": "hard"
        }
]
        
        for rhyme_info in rhyme_data:
            thema_id = thema_id_map.get(rhyme_info['thema_name'])
            if thema_id:
                rhyme_set = ThemaRhymeSet(
                    thema_id=thema_id,
                    rhyme_pattern=rhyme_info['rhyme_pattern'],
                    words=rhyme_info['words'],
                    difficulty_level=rhyme_info['difficulty_level'],
                    created_at=now
                )
                db.add(rhyme_set)
        
        # Commit all
        db.commit()
        
        # Verify
        final_themas = db.query(Thema).count()
        final_elements = db.query(ThemaElement).count()
        final_rhymes = db.query(ThemaRhymeSet).count()
        
        print(f"\n🎉 SEEDING VOLTOOID!")
        print(f"✅ {final_themas} themas")
        print(f"✅ {final_elements} elements")
        print(f"✅ {final_rhymes} rhyme sets")
        
    except Exception as e:
        print(f"❌ Fout tijdens seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_production_themas()
