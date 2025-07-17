#!/usr/bin/env python3
"""
Script om bestaande rijmwoorden te converteren naar rijmende paren
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.thema import ThemaRhymeSet

def migrate_rhyme_words_to_pairs():
    """Converteer bestaande rijmwoorden naar rijmende paren"""
    
    db = SessionLocal()
    try:
        # Haal alle bestaande rijmwoorden sets op
        rhyme_sets = db.query(ThemaRhymeSet).all()
        
        print(f"🔍 Gevonden: {len(rhyme_sets)} rijmwoorden sets om te converteren")
        
        converted_count = 0
        
        for rhyme_set in rhyme_sets:
            try:
                # Check of dit al geconverteerd is (heeft rhyme_pairs)
                if hasattr(rhyme_set, 'rhyme_pairs') and rhyme_set.rhyme_pairs:
                    print(f"   ⏭️  Set {rhyme_set.id} is al geconverteerd, sla over...")
                    continue
                
                # Converteer words naar rhyme_pairs
                words = rhyme_set.words if hasattr(rhyme_set, 'words') else []
                
                if len(words) < 2:
                    print(f"   ⚠️  Set {rhyme_set.id} heeft te weinig woorden, sla over...")
                    continue
                
                # Maak paren van 2 woorden
                rhyme_pairs = []
                for i in range(0, len(words), 2):
                    if i + 1 < len(words):
                        rhyme_pairs.append([words[i], words[i + 1]])
                    else:
                        # Als er een oneven aantal woorden is, voeg het laatste toe met een lege string
                        rhyme_pairs.append([words[i], ''])
                
                # Update de database
                rhyme_set.rhyme_pairs = rhyme_pairs
                
                print(f"   ✅ Set {rhyme_set.id}: {len(words)} woorden → {len(rhyme_pairs)} paren")
                print(f"      Paren: {rhyme_pairs}")
                
                converted_count += 1
                
            except Exception as e:
                print(f"   ❌ Fout bij converteren set {rhyme_set.id}: {e}")
        
        # Commit alle wijzigingen
        db.commit()
        
        print(f"\n🎉 Conversie voltooid! {converted_count} sets geconverteerd.")
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_rhyme_words_to_pairs() 