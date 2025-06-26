"""
CRUD operations voor Thema database management
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta

from app.models.thema import Thema, ThemaElement, ThemaRhymeSet
from app.schemas.thema import (
    ThemaCreate, ThemaUpdate, ThemaElementCreate, ThemaElementUpdate,
    ThemaRhymeSetCreate, ThemaRhymeSetUpdate, ThemaStats
)

class ThemaCRUD:
    """CRUD operations voor Thema management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Thema CRUD
    def get_themas(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Thema]:
        """Haal alle thema's op"""
        query = self.db.query(Thema)
        
        if active_only:
            query = query.filter(Thema.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    def get_themas_list(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Haal thema's op voor lijst weergave met element count"""
        query = self.db.query(
            Thema.id,
            Thema.name,
            Thema.display_name,
            Thema.description,
            Thema.is_active,
            Thema.created_at,
            Thema.updated_at,
            func.count(ThemaElement.id).label('element_count')
        ).outerjoin(ThemaElement).group_by(Thema.id)
        
        results = query.offset(skip).limit(limit).all()
        
        return [
            {
                'id': r.id,
                'name': r.name,
                'display_name': r.display_name,
                'description': r.description,
                'is_active': r.is_active,
                'element_count': r.element_count or 0,
                'created_at': r.created_at,
                'updated_at': r.updated_at
            }
            for r in results
        ]
    
    def get_thema(self, thema_id: int) -> Optional[Thema]:
        """Haal een specifiek thema op"""
        return self.db.query(Thema).filter(Thema.id == thema_id).first()
    
    def get_thema_by_name(self, name: str) -> Optional[Thema]:
        """Haal thema op o.b.v. naam"""
        return self.db.query(Thema).filter(Thema.name == name).first()
    
    def create_thema(self, thema: ThemaCreate) -> Thema:
        """Maak nieuw thema aan"""
        # Check of naam al bestaat
        existing = self.get_thema_by_name(thema.name)
        if existing:
            raise ValueError(f"Thema met naam '{thema.name}' bestaat al")
        
        db_thema = Thema(**thema.dict())
        self.db.add(db_thema)
        self.db.commit()
        self.db.refresh(db_thema)
        return db_thema
    
    def update_thema(self, thema_id: int, thema_update: ThemaUpdate) -> Optional[Thema]:
        """Update bestaand thema"""
        db_thema = self.get_thema(thema_id)
        if not db_thema:
            return None
        
        # Check naam uniekheid als naam wordt gewijzigd
        if thema_update.name and thema_update.name != db_thema.name:
            existing = self.get_thema_by_name(thema_update.name)
            if existing:
                raise ValueError(f"Thema met naam '{thema_update.name}' bestaat al")
        
        # Update velden
        update_data = thema_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_thema, field, value)
        
        db_thema.updated_at = func.now()
        self.db.commit()
        self.db.refresh(db_thema)
        return db_thema
    
    def delete_thema(self, thema_id: int) -> bool:
        """Verwijder thema (cascade delete elementen)"""
        db_thema = self.get_thema(thema_id)
        if not db_thema:
            return False
        
        self.db.delete(db_thema)
        self.db.commit()
        return True
    
    # Element CRUD
    def get_elements(self, thema_id: int, element_type: Optional[str] = None) -> List[ThemaElement]:
        """Haal elementen van een thema op"""
        query = self.db.query(ThemaElement).filter(ThemaElement.thema_id == thema_id)
        
        if element_type:
            query = query.filter(ThemaElement.element_type == element_type)
        
        return query.all()
    
    def get_element(self, element_id: int) -> Optional[ThemaElement]:
        """Haal specifiek element op"""
        return self.db.query(ThemaElement).filter(ThemaElement.id == element_id).first()
    
    def create_element(self, element: ThemaElementCreate) -> ThemaElement:
        """Maak nieuw thema element aan"""
        # Valideer dat thema bestaat
        if not self.get_thema(element.thema_id):
            raise ValueError(f"Thema met ID {element.thema_id} bestaat niet")
        
        db_element = ThemaElement(**element.dict())
        self.db.add(db_element)
        self.db.commit()
        self.db.refresh(db_element)
        return db_element
    
    def update_element(self, element_id: int, element_update: ThemaElementUpdate) -> Optional[ThemaElement]:
        """Update bestaand element"""
        db_element = self.get_element(element_id)
        if not db_element:
            return None
        
        update_data = element_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_element, field, value)
        
        self.db.commit()
        self.db.refresh(db_element)
        return db_element
    
    def delete_element(self, element_id: int) -> bool:
        """Verwijder element"""
        db_element = self.get_element(element_id)
        if not db_element:
            return False
        
        self.db.delete(db_element)
        self.db.commit()
        return True
    
    # Rhyme Set CRUD
    def get_rhyme_sets(self, thema_id: int) -> List[ThemaRhymeSet]:
        """Haal rijmsets van een thema op"""
        return self.db.query(ThemaRhymeSet).filter(ThemaRhymeSet.thema_id == thema_id).all()
    
    def get_rhyme_set(self, rhyme_set_id: int) -> Optional[ThemaRhymeSet]:
        """Haal specifieke rijmset op"""
        return self.db.query(ThemaRhymeSet).filter(ThemaRhymeSet.id == rhyme_set_id).first()
    
    def create_rhyme_set(self, rhyme_set: ThemaRhymeSetCreate) -> ThemaRhymeSet:
        """Maak nieuwe rijmset aan"""
        # Valideer dat thema bestaat
        if not self.get_thema(rhyme_set.thema_id):
            raise ValueError(f"Thema met ID {rhyme_set.thema_id} bestaat niet")
        
        db_rhyme_set = ThemaRhymeSet(**rhyme_set.dict())
        self.db.add(db_rhyme_set)
        self.db.commit()
        self.db.refresh(db_rhyme_set)
        return db_rhyme_set
    
    def update_rhyme_set(self, rhyme_set_id: int, rhyme_set_update: ThemaRhymeSetUpdate) -> Optional[ThemaRhymeSet]:
        """Update bestaande rijmset"""
        db_rhyme_set = self.get_rhyme_set(rhyme_set_id)
        if not db_rhyme_set:
            return None
        
        update_data = rhyme_set_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rhyme_set, field, value)
        
        self.db.commit()
        self.db.refresh(db_rhyme_set)
        return db_rhyme_set
    
    def delete_rhyme_set(self, rhyme_set_id: int) -> bool:
        """Verwijder rijmset"""
        db_rhyme_set = self.get_rhyme_set(rhyme_set_id)
        if not db_rhyme_set:
            return False
        
        self.db.delete(db_rhyme_set)
        self.db.commit()
        return True
    
    # Statistics
    def get_stats(self) -> ThemaStats:
        """Haal dashboard statistieken op"""
        total_themas = self.db.query(Thema).count()
        active_themas = self.db.query(Thema).filter(Thema.is_active == True).count()
        inactive_themas = total_themas - active_themas
        total_elements = self.db.query(ThemaElement).count()
        
        # Recent additions (laatste 7 dagen)
        week_ago = datetime.now() - timedelta(days=7)
        recent_additions = self.db.query(Thema).filter(Thema.created_at >= week_ago).count()
        
        return ThemaStats(
            total_themas=total_themas,
            active_themas=active_themas,
            inactive_themas=inactive_themas,
            total_elements=total_elements,
            recent_additions=recent_additions
        )
    
    # Bulk operations
    def bulk_toggle_active(self, thema_ids: List[int], is_active: bool) -> int:
        """Bulk toggle actief status"""
        updated = self.db.query(Thema).filter(Thema.id.in_(thema_ids)).update(
            {Thema.is_active: is_active, Thema.updated_at: func.now()},
            synchronize_session=False
        )
        self.db.commit()
        return updated
    
    def search_themas(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Zoek thema's op naam of beschrijving"""
        query = self.db.query(
            Thema.id,
            Thema.name,
            Thema.display_name,
            Thema.description,
            Thema.is_active,
            Thema.created_at,
            Thema.updated_at,
            func.count(ThemaElement.id).label('element_count')
        ).outerjoin(ThemaElement).filter(
            and_(
                Thema.display_name.ilike(f"%{search_term}%") |
                Thema.description.ilike(f"%{search_term}%") |
                Thema.name.ilike(f"%{search_term}%")
            )
        ).group_by(Thema.id)
        
        results = query.offset(skip).limit(limit).all()
        
        return [
            {
                'id': r.id,
                'name': r.name,
                'display_name': r.display_name,
                'description': r.description,
                'is_active': r.is_active,
                'element_count': r.element_count or 0,
                'created_at': r.created_at,
                'updated_at': r.updated_at
            }
            for r in results
        ]

# Factory function
def get_thema_crud(db: Session) -> ThemaCRUD:
    """Factory voor ThemaCRUD"""
    return ThemaCRUD(db) 