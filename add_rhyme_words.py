#!/usr/bin/env python3
"""
Script om rijmwoorden toe te voegen aan de thema database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.thema import Thema, ThemaRhymeSet
from app.crud.thema import get_thema_crud

def add_rhyme_words():
    """Voeg rijmwoorden toe aan bestaande thema's"""
    
    db = SessionLocal()
    try:
        crud = get_thema_crud(db)
        
        # Rijmwoorden per thema
        rhyme_data = {
            "verjaardag": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["dag", "mag", "zag", "vraag", "draag", "laag", "slaag", "waag"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB", 
                    "words": ["jaar", "daar", "paar", "gaar", "klaar", "waar", "naar", "zaar"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["feest", "geest", "beest", "meest", "leest", "neest", "reest", "seest"],
                    "difficulty_level": "hard"
                }
            ],
            "liefde": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["hart", "start", "apart", "smart", "kart", "part", "tart", "wart"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["lief", "dief", "grief", "brief", "stief", "wief", "kief", "pief"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["kussen", "bussen", "russen", "tussen", "mussen", "pussen", "lussen", "nussen"],
                    "difficulty_level": "hard"
                }
            ],
            "huwelijk": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["ring", "ding", "zing", "kling", "sling", "wring", "bring", "spring"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["trouw", "bouw", "kouw", "mouw", "pouw", "souw", "wouw", "zouw"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["bruid", "luid", "ruid", "suid", "tuid", "vuur", "duur", "muur"],
                    "difficulty_level": "hard"
                }
            ],
            "vriendschap": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["vriend", "kind", "wind", "bind", "hind", "mind", "pind", "rind"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["samen", "namen", "ramen", "tamen", "vamen", "wamen", "zamen", "lamen"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["delen", "spelen", "stelen", "welen", "kelen", "melen", "pelen", "telen"],
                    "difficulty_level": "hard"
                }
            ],
            "familie": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["huis", "muis", "puis", "suis", "tuis", "vuis", "wuis", "zuis"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["thuis", "luis", "ruis", "suis", "tuis", "vuis", "wuis", "zuis"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["mama", "papa", "oma", "opa", "tante", "oom", "zus", "broer"],
                    "difficulty_level": "easy"
                }
            ],
            "afscheid": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["weg", "zeg", "leg", "teg", "veg", "weg", "zeg", "leg"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["dood", "goed", "moed", "rood", "soed", "toed", "voed", "woed"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["missen", "kussen", "bussen", "russen", "tussen", "mussen", "pussen", "lussen"],
                    "difficulty_level": "hard"
                }
            ],
            "feest": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["feest", "geest", "beest", "meest", "leest", "neest", "reest", "seest"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["dansen", "glansen", "kansen", "lansen", "mansen", "pansen", "ransen", "sansen"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["muziek", "luziek", "puziek", "ruziek", "suziek", "tuziek", "vuziek", "wuziek"],
                    "difficulty_level": "hard"
                }
            ],
            "natuur": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["boom", "doom", "goom", "loom", "moom", "poom", "room", "soom"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["bloem", "doem", "goem", "loem", "moem", "poem", "roem", "soem"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["zon", "ton", "von", "gon", "lon", "mon", "pon", "ron"],
                    "difficulty_level": "easy"
                }
            ],
            "reizen": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["reis", "weis", "keis", "leis", "meis", "peis", "reis", "seis"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["weg", "zeg", "leg", "teg", "veg", "weg", "zeg", "leg"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["land", "hand", "band", "kand", "mand", "pand", "rand", "sand"],
                    "difficulty_level": "hard"
                }
            ],
            "werk": [
                {
                    "rhyme_pattern": "AABB",
                    "words": ["werk", "merk", "perk", "serk", "terk", "verk", "werk", "zerk"],
                    "difficulty_level": "easy"
                },
                {
                    "rhyme_pattern": "ABAB",
                    "words": ["baan", "gaan", "haan", "kaan", "laan", "maan", "paan", "raan"],
                    "difficulty_level": "medium"
                },
                {
                    "rhyme_pattern": "ABBA",
                    "words": ["kantoor", "lantoor", "mantoor", "pantoor", "rantoor", "santoor", "tantoor", "vantoor"],
                    "difficulty_level": "hard"
                }
            ]
        }
        
        added_count = 0
        
        for thema_name, rhyme_sets in rhyme_data.items():
            # Zoek thema op naam
            thema = crud.get_thema_by_name(thema_name)
            if not thema:
                print(f"⚠️  Thema '{thema_name}' niet gevonden, sla over...")
                continue
                
            print(f"🎵 Voeg rijmwoorden toe aan thema: {thema.display_name}")
            
            for rhyme_data in rhyme_sets:
                try:
                    # Check of deze rijmset al bestaat
                    existing_sets = crud.get_rhyme_sets(thema.id)
                    pattern_exists = any(rs.rhyme_pattern == rhyme_data["rhyme_pattern"] for rs in existing_sets)
                    
                    if pattern_exists:
                        print(f"   ⏭️  Patroon {rhyme_data['rhyme_pattern']} bestaat al, sla over...")
                        continue
                    
                    # Maak nieuwe rijmset aan
                    from app.schemas.thema import ThemaRhymeSetCreate
                    rhyme_set_create = ThemaRhymeSetCreate(
                        thema_id=thema.id,
                        rhyme_pattern=rhyme_data["rhyme_pattern"],
                        words=rhyme_data["words"],
                        difficulty_level=rhyme_data["difficulty_level"]
                    )
                    
                    crud.create_rhyme_set(rhyme_set_create)
                    print(f"   ✅ Toegevoegd: {rhyme_data['rhyme_pattern']} ({len(rhyme_data['words'])} woorden)")
                    added_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Fout bij toevoegen {rhyme_data['rhyme_pattern']}: {e}")
        
        print(f"\n🎉 Klaar! {added_count} rijmsets toegevoegd aan de database.")
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_rhyme_words() 