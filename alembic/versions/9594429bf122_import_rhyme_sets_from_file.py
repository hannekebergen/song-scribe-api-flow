"""import_rhyme_sets_from_file

Revision ID: 9594429bf122
Revises: 850f5780a049
Create Date: 2025-07-22 14:45:27.045714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect
import os
import json
import logging

# Logging configureren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = '9594429bf122'
down_revision = '850f5780a049'
branch_labels = None
depends_on = None

# SQLAlchemy setup
Base = declarative_base()

# Modellen
class Thema(Base):
    __tablename__ = 'themas'
    
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

def parse_rhymes(content):
    """
    Parse de rijmparen uit het tekstbestand.
    
    Args:
        content (str): Inhoud van het tekstbestand
        
    Returns:
        dict: Dictionary met thema's als keys en lijsten van rijmparen als values
    """
    thema_blocks = []
    current_block = []
    lines = content.split("\n")
    
    # Verdeel de inhoud in thema-blokken
    for line in lines:
        if line.strip().startswith("Thema") and current_block:
            thema_blocks.append("\n".join(current_block))
            current_block = [line]
        else:
            current_block.append(line)
    
    # Voeg het laatste blok toe
    if current_block:
        thema_blocks.append("\n".join(current_block))
    
    themes = {}
    
    for block in thema_blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split("\n")
        first_line = lines[0].strip()
        
        # Check of dit een nieuwe thema-sectie is
        if first_line.startswith("Thema"):
            theme_match = first_line.replace("Thema", "").replace(":", "").strip().lower()
            current_theme = theme_match
            if current_theme not in themes:
                themes[current_theme] = []
            
            # Verwerk de rijmparen in dit thema-blok
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Formaat: woord1-woord2
                if "-" in line:
                    words = line.split("-")
                    if len(words) >= 2:
                        word1 = words[0].strip()
                        word2 = words[1].strip()
                        if word1 and word2:
                            # Controleer of dit paar al bestaat
                            if not any((p[0] == word1 and p[1] == word2) or 
                                      (p[0] == word2 and p[1] == word1) for p in themes[current_theme]):
                                themes[current_theme].append([word1, word2])
    
    return themes

def upgrade() -> None:
    # Verbinding maken met de database
    connection = op.get_bind()
    
    # Controleer welke kolommen bestaan in de tabel
    inspector = inspect(connection)
    columns = [column['name'] for column in inspector.get_columns('thema_rhyme_sets')]
    
    logger.info(f"Gevonden kolommen in thema_rhyme_sets: {columns}")
    
    # Controleer of we de words kolom moeten toevoegen of converteren
    has_words = 'words' in columns
    has_rhyme_pairs = 'rhyme_pairs' in columns
    
    # Als words bestaat maar rhyme_pairs niet, voeg rhyme_pairs toe
    if has_words and not has_rhyme_pairs:
        logger.info("Toevoegen van rhyme_pairs kolom...")
        op.add_column('thema_rhyme_sets', sa.Column('rhyme_pairs', JSON, nullable=True))
        
        # Haal alle rijen op met words
        result = connection.execute(sa.text("SELECT id, words FROM thema_rhyme_sets WHERE words IS NOT NULL"))
        rows = result.fetchall()
        
        # Converteer words naar rhyme_pairs
        for row in rows:
            id_val, words = row
            if words:
                # Groepeer woorden in paren
                pairs = []
                for i in range(0, len(words), 2):
                    if i + 1 < len(words):
                        pairs.append([words[i], words[i+1]])
                
                # Update de rij met rhyme_pairs
                connection.execute(
                    sa.text("UPDATE thema_rhyme_sets SET rhyme_pairs = :pairs WHERE id = :id"),
                    {"pairs": json.dumps(pairs), "id": id_val}
                )
        
        logger.info(f"Geconverteerd {len(rows)} rijen van words naar rhyme_pairs")
    
    # Pad naar het tekstbestand
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Songteksten1-10.txt")
    
    # Controleer of het bestand bestaat
    if not os.path.exists(file_path):
        logger.error(f"Bestand niet gevonden: {file_path}")
        return
    
    # Lees het bestand
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse de rijmparen
    themes = parse_rhymes(content)
    
    # Haal alle thema's op uit de database
    result = connection.execute(sa.text("SELECT id, name FROM themas"))
    db_themes = result.fetchall()
    theme_map = {theme[1].lower(): theme[0] for theme in db_themes}
    
    logger.info(f"Gevonden thema's in database: {list(theme_map.keys())}")
    logger.info(f"Gevonden thema's in tekstbestand: {list(themes.keys())}")
    
    # Importeer rijmparen voor elk thema
    for theme_name, rhyme_pairs in themes.items():
        # Zoek het thema ID
        theme_id = None
        for db_theme_name, db_theme_id in theme_map.items():
            if theme_name in db_theme_name or db_theme_name in theme_name:
                theme_id = db_theme_id
                logger.info(f"Thema '{theme_name}' gematcht met database thema '{db_theme_name}'")
                break
        
        if not theme_id:
            logger.warning(f"Thema '{theme_name}' niet gevonden in de database, sla over")
            continue
        
        logger.info(f"Importeren van {len(rhyme_pairs)} rijmparen voor thema '{theme_name}' (ID: {theme_id})")
        
        # Maak rhyme sets met verschillende patronen
        patterns = ["AABB", "ABAB"]
        
        for pattern in patterns:
            # Controleer of er al een rhyme set bestaat voor dit thema en patroon
            result = connection.execute(
                sa.text("SELECT id, rhyme_pairs, words FROM thema_rhyme_sets WHERE thema_id = :thema_id AND rhyme_pattern = :pattern"),
                {"thema_id": theme_id, "pattern": pattern}
            )
            existing_set = result.fetchone()
            
            if existing_set:
                set_id, existing_rhyme_pairs, existing_words = existing_set
                logger.info(f"Bijwerken van bestaande rhyme set (ID: {set_id}) voor thema '{theme_name}' met patroon {pattern}")
                
                # Update op basis van welke kolommen bestaan
                if has_rhyme_pairs:
                    # Haal bestaande paren op
                    if existing_rhyme_pairs:
                        if isinstance(existing_rhyme_pairs, str):
                            existing_pairs = json.loads(existing_rhyme_pairs)
                        else:
                            existing_pairs = existing_rhyme_pairs
                    else:
                        existing_pairs = []
                    
                    # Voeg nieuwe paren toe
                    added_count = 0
                    for pair in rhyme_pairs:
                        if not any((p[0] == pair[0] and p[1] == pair[1]) or 
                                  (p[0] == pair[1] and p[1] == pair[0]) for p in existing_pairs):
                            existing_pairs.append(pair)
                            added_count += 1
                    
                    # Update de database
                    connection.execute(
                        sa.text("UPDATE thema_rhyme_sets SET rhyme_pairs = :pairs WHERE id = :id"),
                        {"pairs": json.dumps(existing_pairs), "id": set_id}
                    )
                    logger.info(f"  - {added_count} nieuwe rijmparen toegevoegd aan bestaande set (rhyme_pairs)")
                
                if has_words:
                    # Haal bestaande woorden op
                    existing_words_list = existing_words if existing_words else []
                    
                    # Voeg nieuwe woorden toe
                    added_count = 0
                    new_words = [word for pair in rhyme_pairs for word in pair]
                    for word in new_words:
                        if word not in existing_words_list:
                            existing_words_list.append(word)
                            added_count += 1
                    
                    # Update de database
                    connection.execute(
                        sa.text("UPDATE thema_rhyme_sets SET words = :words WHERE id = :id"),
                        {"words": existing_words_list, "id": set_id}
                    )
                    logger.info(f"  - {added_count} nieuwe woorden toegevoegd aan bestaande set (words array)")
            else:
                # Maak een nieuwe rhyme set
                logger.info(f"Maken van nieuwe rhyme set voor thema '{theme_name}' met patroon {pattern}")
                
                # Bereid de insert voor
                insert_values = {
                    "thema_id": theme_id,
                    "rhyme_pattern": pattern,
                    "difficulty_level": "medium",
                    "created_at": "NOW()"
                }
                
                # Voeg rhyme_pairs of words toe op basis van schema
                if has_rhyme_pairs:
                    insert_values["rhyme_pairs"] = json.dumps(rhyme_pairs)
                
                if has_words:
                    words = [word for pair in rhyme_pairs for word in pair]
                    insert_values["words"] = words
                
                # Voer de insert uit - behandel created_at speciaal
                columns_without_created_at = [k for k in insert_values.keys() if k != "created_at"]
                columns_str = ", ".join(columns_without_created_at) + ", created_at"
                placeholders = ", ".join(f":{key}" for key in columns_without_created_at) + ", NOW()"
                
                # Verwijder created_at uit insert_values voor de query
                insert_values_clean = {k: v for k, v in insert_values.items() if k != "created_at"}
                
                connection.execute(
                    sa.text(f"INSERT INTO thema_rhyme_sets ({columns_str}) VALUES ({placeholders})"),
                    insert_values_clean
                )
                
                logger.info(f"  - Nieuwe rhyme set aangemaakt voor thema '{theme_name}' met patroon {pattern}")
    
    logger.info("Rijmparen succesvol geïmporteerd!")


def downgrade() -> None:
    # Geen downgrade functionaliteit voor data import
    pass
