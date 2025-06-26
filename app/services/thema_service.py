"""
Thema Database Service
Handles all database operations for thema elements
"""

import random
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.thema import Thema, ThemaElement, ThemaRhymeSet
from app.db.session import get_db

class ThemaService:
    """Service voor het beheren van thema database operaties"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_thema_by_name(self, thema_name: str) -> Optional[Thema]:
        """Haal een thema op o.b.v. naam"""
        return self.db.query(Thema).filter(
            and_(Thema.name == thema_name.lower(), Thema.is_active == True)
        ).first()
    
    def get_thema_elements(self, thema_id: int, element_type: str = None) -> List[ThemaElement]:
        """Haal thema elementen op, optioneel gefilterd op type"""
        query = self.db.query(ThemaElement).filter(ThemaElement.thema_id == thema_id)
        
        if element_type:
            query = query.filter(ThemaElement.element_type == element_type)
        
        return query.all()
    
    def get_random_elements(self, thema_id: int, element_type: str, 
                          count: int = 3, context: str = None) -> List[ThemaElement]:
        """Haal random elementen op, rekening houdend met weight"""
        query = self.db.query(ThemaElement).filter(
            and_(
                ThemaElement.thema_id == thema_id,
                ThemaElement.element_type == element_type
            )
        )
        
        if context:
            query = query.filter(
                ThemaElement.usage_context.in_([context, 'any', None])
            )
        
        elements = query.all()
        
        # Weighted random selection
        weighted_elements = []
        for element in elements:
            weighted_elements.extend([element] * element.weight)
        
        if not weighted_elements:
            return []
            
        selected_count = min(count, len(set(weighted_elements)))
        return random.sample(list(set(weighted_elements)), selected_count)
    
    def get_rhyme_sets(self, thema_id: int, pattern: str = None) -> List[ThemaRhymeSet]:
        """Haal rijmwoorden sets op"""
        query = self.db.query(ThemaRhymeSet).filter(ThemaRhymeSet.thema_id == thema_id)
        
        if pattern:
            query = query.filter(ThemaRhymeSet.rhyme_pattern == pattern)
        
        return query.all()
    
    def get_random_rhyme_set(self, thema_id: int, pattern: str = None) -> Optional[ThemaRhymeSet]:
        """Haal een random rijmwoorden set op"""
        rhyme_sets = self.get_rhyme_sets(thema_id, pattern)
        
        if not rhyme_sets:
            return None
            
        return random.choice(rhyme_sets)
    
    def generate_thema_data(self, thema_name: str) -> Dict[str, Any]:
        """Genereer een complete dataset voor een thema"""
        thema = self.get_thema_by_name(thema_name)
        
        if not thema:
            return self._get_fallback_data(thema_name)
        
        # Haal verschillende element types op
        keywords = self.get_random_elements(thema.id, 'keyword', count=4)
        power_phrases = self.get_random_elements(thema.id, 'power_phrase', count=2, context='chorus')
        genres = self.get_random_elements(thema.id, 'genre', count=1)
        bpm_elements = self.get_random_elements(thema.id, 'bpm', count=1)
        key_elements = self.get_random_elements(thema.id, 'key', count=1)
        instruments = self.get_random_elements(thema.id, 'instrument', count=3)
        effects = self.get_random_elements(thema.id, 'effect', count=2)
        verse_starters = self.get_random_elements(thema.id, 'verse_starter', count=1)
        
        # Haal een rijmset op
        rhyme_set = self.get_random_rhyme_set(thema.id, 'AABB')
        
        return {
            'thema_name': thema.name,
            'display_name': thema.display_name,
            'keywords': [el.content for el in keywords],
            'power_phrases': [el.content for el in power_phrases],
            'genres': [el.content for el in genres],
            'bpm': bpm_elements[0].content if bpm_elements else '120',
            'key': key_elements[0].content if key_elements else 'C majeur',
            'instruments': [el.suno_format or el.content for el in instruments],
            'effects': [el.suno_format or el.content for el in effects],
            'verse_starters': [el.content for el in verse_starters],
            'rhyme_words': rhyme_set.words if rhyme_set else ['hart', 'start', 'apart'],
            'rhyme_pattern': rhyme_set.rhyme_pattern if rhyme_set else 'AABB'
        }
    
    def _get_fallback_data(self, thema_name: str) -> Dict[str, Any]:
        """Fallback data als thema niet in database staat"""
        return {
            'thema_name': thema_name,
            'display_name': thema_name.title(),
            'keywords': ['mooi', 'speciaal', 'bijzonder'],
            'power_phrases': [f'Voor {thema_name}', 'Een speciaal moment'],
            'genres': ['pop'],
            'bpm': '120',
            'key': 'C majeur',
            'instruments': ['[piano]', '[guitar]'],
            'effects': ['[warm tone]'],
            'verse_starters': ['Vandaag is een bijzondere dag'],
            'rhyme_words': ['dag', 'mag', 'zag', 'vraag'],
            'rhyme_pattern': 'AABB'
        }

# Convenience function
def get_thema_service(db: Session = None) -> ThemaService:
    """Factory function voor ThemaService"""
    if db is None:
        db = next(get_db())
    return ThemaService(db) 