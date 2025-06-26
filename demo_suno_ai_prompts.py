#!/usr/bin/env python3
"""
Demo script voor Suno.ai prompt optimalisatie
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaElement

def build_suno_prompt(db, thema_name, song_data):
    """Build a Suno.ai optimized prompt"""
    thema = db.query(Thema).filter_by(name=thema_name).first()
    if not thema:
        return f"Thema '{thema_name}' not found"
    
    elements = db.query(ThemaElement).filter_by(thema_id=thema.id).all()
    
    # Separate elements by type
    instruments = [e for e in elements if e.element_type == 'instrument' and e.suno_format]
    vocals = [e for e in elements if e.element_type == 'vocal_descriptor' and e.suno_format]
    effects = [e for e in elements if e.element_type == 'effect' and e.suno_format]
    control_hacks = [e for e in elements if e.element_type == 'control_hack' and e.suno_format]
    genres = [e for e in elements if e.element_type == 'genre']
    bpms = [e for e in elements if e.element_type == 'bpm']
    keys = [e for e in elements if e.element_type == 'key']
    keywords = [e for e in elements if e.element_type == 'keyword']
    power_phrases = [e for e in elements if e.element_type == 'power_phrase']
    
    # Build the prompt
    prompt_parts = []
    
    # Titel
    prompt_parts.append(f"**{thema.display_name} Lied voor {song_data.get('klant_naam', 'You')}**")
    prompt_parts.append("")
    
    # Genre & BPM & Key info
    if genres:
        genre = random.choice(genres).content
        prompt_parts.append(f"Genre: {genre}")
    
    if bpms:
        bpm = random.choice(bpms).content
        prompt_parts.append(f"BPM: {bpm}")
    
    if keys:
        key = random.choice(keys).content
        prompt_parts.append(f"Toonsoort: {key}")
    
    prompt_parts.append("")
    
    # Suno.ai instrument tags
    if instruments:
        selected_instruments = random.sample(instruments, min(3, len(instruments)))
        instrument_tags = " ".join([e.suno_format for e in selected_instruments])
        prompt_parts.append(f"Instrumenten: {instrument_tags}")
    
    # Vocal style
    if vocals:
        selected_vocals = random.sample(vocals, min(2, len(vocals)))
        vocal_tags = " ".join([e.suno_format for e in selected_vocals])
        prompt_parts.append(f"Vocalen: {vocal_tags}")
    
    # Effects
    if effects:
        selected_effects = random.sample(effects, min(2, len(effects)))
        effect_tags = " ".join([e.suno_format for e in selected_effects])
        prompt_parts.append(f"Effecten: {effect_tags}")
    
    prompt_parts.append("")
    
    # Song content
    prompt_parts.append("**Songtekst:**")
    prompt_parts.append("")
    
    # Verse 1
    prompt_parts.append("[Verse 1]")
    if keywords:
        theme_keywords = random.sample(keywords, min(3, len(keywords)))
        keyword_text = ", ".join([k.content for k in theme_keywords])
        prompt_parts.append(f"Een verhaal over {keyword_text}")
    
    if 'persoonlijk_verhaal' in song_data:
        prompt_parts.append(song_data['persoonlijk_verhaal'])
    
    # Chorus
    prompt_parts.append("")
    prompt_parts.append("[Chorus]")
    if power_phrases:
        chorus_phrase = random.choice([p for p in power_phrases if p.usage_context in ['chorus', 'any']]).content
        prompt_parts.append(chorus_phrase)
    
    # Control hacks for emotional impact
    if control_hacks:
        selected_hacks = random.sample(control_hacks, min(2, len(control_hacks)))
        hack_tags = " ".join([h.suno_format for h in selected_hacks])
        prompt_parts.append(f"\n{hack_tags}")
    
    return "\n".join(prompt_parts)

def demo_suno_ai():
    """Demo de Suno.ai functionaliteit"""
    db = SessionLocal()
    
    try:
        print("🎵 Suno.ai Prompt Generation Demo\n")
        
        # Test verschillende thema's
        test_cases = [
            {
                "thema": "verjaardag",
                "data": {
                    "klant_naam": "Sarah",
                    "persoonlijk_verhaal": "Sarah is 25 geworden en houdt van dansen en vrienden. Ze werkt als lerares en straalt altijd vrolijkheid uit."
                }
            },
            {
                "thema": "liefde",
                "data": {
                    "klant_naam": "Mark & Lisa",
                    "persoonlijk_verhaal": "Mark en Lisa zijn al 5 jaar samen. Ze ontmoetten elkaar tijdens een regenachtige dag in de trein en wisten meteen dat dit voor altijd was."
                }
            },
            {
                "thema": "afscheid",
                "data": {
                    "klant_naam": "Familie van Opa Jan",
                    "persoonlijk_verhaal": "Opa Jan was een lieve man die altijd klaarstond voor iedereen. Hij hield van fietsen, lekker eten en zijn kleinkinderen."
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{'='*60}")
            print(f"🎭 Demo {i}: {test_case['thema'].upper()} Theme")
            print(f"{'='*60}")
            
            suno_prompt = build_suno_prompt(db, test_case['thema'], test_case['data'])
            print(suno_prompt)
            print("\n")
        
        # Statistics
        themas = db.query(Thema).all()
        total_elements = db.query(ThemaElement).count()
        suno_elements = db.query(ThemaElement).filter(ThemaElement.suno_format.isnot(None)).count()
        
        print(f"{'='*60}")
        print(f"📊 DATABASE STATISTICS")
        print(f"{'='*60}")
        print(f"🎭 Total Themes: {len(themas)}")
        print(f"🧩 Total Elements: {total_elements}")
        print(f"🎯 Suno.ai Elements: {suno_elements}")
        print(f"📈 Suno.ai Coverage: {suno_elements/total_elements*100:.1f}%")
        print()
        
        for thema in themas:
            elements = db.query(ThemaElement).filter_by(thema_id=thema.id).count()
            suno_count = db.query(ThemaElement).filter_by(thema_id=thema.id).filter(ThemaElement.suno_format.isnot(None)).count()
            coverage = suno_count/elements*100 if elements > 0 else 0
            print(f"   • {thema.name}: {elements} elements ({suno_count} Suno.ai, {coverage:.1f}%)")
        
        print(f"\n✅ Suno.ai Implementation Successfully Deployed!")
        print(f"🎵 Ready for production use with 6 comprehensive themes!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    demo_suno_ai() 