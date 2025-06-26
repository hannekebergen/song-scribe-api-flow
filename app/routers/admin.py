"""
Admin API endpoints voor Thema database management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.token import get_api_key
from app.crud.thema import get_thema_crud
from app.schemas.thema import (
    Thema, ThemaCreate, ThemaUpdate, ThemaListItem, ThemaStats,
    ThemaElement, ThemaElementCreate, ThemaElementUpdate,
    ThemaRhymeSet, ThemaRhymeSetCreate, ThemaRhymeSetUpdate,
    BulkThemaResponse
)

router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(get_api_key)]
)

# Thema endpoints
@router.get("/themes/stats", response_model=ThemaStats)
async def get_thema_stats(db: Session = Depends(get_db)):
    """Haal dashboard statistieken op"""
    try:
        crud = get_thema_crud(db)
        return crud.get_stats()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen statistieken: {str(e)}"
        )

@router.get("/themes", response_model=List[ThemaListItem])
async def get_themas(
    skip: int = Query(0, ge=0, description="Aantal over te slaan"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum aantal resultaten"),
    search: Optional[str] = Query(None, description="Zoekterm"),
    active_only: bool = Query(False, description="Alleen actieve thema's"),
    db: Session = Depends(get_db)
):
    """Haal thema's op voor lijst weergave"""
    try:
        crud = get_thema_crud(db)
        
        if search:
            return crud.search_themas(search, skip=skip, limit=limit)
        else:
            return crud.get_themas_list(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen thema's: {str(e)}"
        )

@router.get("/themes/{thema_id}", response_model=Thema)
async def get_thema(thema_id: int, db: Session = Depends(get_db)):
    """Haal specifiek thema op met alle details"""
    try:
        crud = get_thema_crud(db)
        thema = crud.get_thema(thema_id)
        
        if not thema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thema met ID {thema_id} niet gevonden"
            )
        
        return thema
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen thema: {str(e)}"
        )

@router.post("/themes", response_model=Thema, status_code=status.HTTP_201_CREATED)
async def create_thema(thema: ThemaCreate, db: Session = Depends(get_db)):
    """Maak nieuw thema aan"""
    try:
        crud = get_thema_crud(db)
        return crud.create_thema(thema)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij aanmaken thema: {str(e)}"
        )

@router.put("/themes/{thema_id}", response_model=Thema)
async def update_thema(
    thema_id: int, 
    thema_update: ThemaUpdate, 
    db: Session = Depends(get_db)
):
    """Update bestaand thema"""
    try:
        crud = get_thema_crud(db)
        updated_thema = crud.update_thema(thema_id, thema_update)
        
        if not updated_thema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thema met ID {thema_id} niet gevonden"
            )
        
        return updated_thema
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij updaten thema: {str(e)}"
        )

@router.delete("/themes/{thema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thema(thema_id: int, db: Session = Depends(get_db)):
    """Verwijder thema"""
    try:
        crud = get_thema_crud(db)
        success = crud.delete_thema(thema_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thema met ID {thema_id} niet gevonden"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij verwijderen thema: {str(e)}"
        )

# Element endpoints
@router.get("/themes/{thema_id}/elements", response_model=List[ThemaElement])
async def get_thema_elements(
    thema_id: int,
    element_type: Optional[str] = Query(None, description="Filter op element type"),
    db: Session = Depends(get_db)
):
    """Haal elementen van een thema op"""
    try:
        crud = get_thema_crud(db)
        
        # Check of thema bestaat
        if not crud.get_thema(thema_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thema met ID {thema_id} niet gevonden"
            )
        
        return crud.get_elements(thema_id, element_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen elementen: {str(e)}"
        )

@router.post("/elements", response_model=ThemaElement, status_code=status.HTTP_201_CREATED)
async def create_element(element: ThemaElementCreate, db: Session = Depends(get_db)):
    """Maak nieuw thema element aan"""
    try:
        crud = get_thema_crud(db)
        return crud.create_element(element)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij aanmaken element: {str(e)}"
        )

@router.put("/elements/{element_id}", response_model=ThemaElement)
async def update_element(
    element_id: int,
    element_update: ThemaElementUpdate,
    db: Session = Depends(get_db)
):
    """Update bestaand element"""
    try:
        crud = get_thema_crud(db)
        updated_element = crud.update_element(element_id, element_update)
        
        if not updated_element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Element met ID {element_id} niet gevonden"
            )
        
        return updated_element
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij updaten element: {str(e)}"
        )

@router.delete("/elements/{element_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_element(element_id: int, db: Session = Depends(get_db)):
    """Verwijder element"""
    try:
        crud = get_thema_crud(db)
        success = crud.delete_element(element_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Element met ID {element_id} niet gevonden"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij verwijderen element: {str(e)}"
        )

# Rhyme Set endpoints
@router.get("/themes/{thema_id}/rhyme-sets", response_model=List[ThemaRhymeSet])
async def get_thema_rhyme_sets(thema_id: int, db: Session = Depends(get_db)):
    """Haal rijmsets van een thema op"""
    try:
        crud = get_thema_crud(db)
        
        # Check of thema bestaat
        if not crud.get_thema(thema_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Thema met ID {thema_id} niet gevonden"
            )
        
        return crud.get_rhyme_sets(thema_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen rijmsets: {str(e)}"
        )

@router.post("/rhyme-sets", response_model=ThemaRhymeSet, status_code=status.HTTP_201_CREATED)
async def create_rhyme_set(rhyme_set: ThemaRhymeSetCreate, db: Session = Depends(get_db)):
    """Maak nieuwe rijmset aan"""
    try:
        crud = get_thema_crud(db)
        return crud.create_rhyme_set(rhyme_set)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij aanmaken rijmset: {str(e)}"
        )

@router.put("/rhyme-sets/{rhyme_set_id}", response_model=ThemaRhymeSet)
async def update_rhyme_set(
    rhyme_set_id: int,
    rhyme_set_update: ThemaRhymeSetUpdate,
    db: Session = Depends(get_db)
):
    """Update bestaande rijmset"""
    try:
        crud = get_thema_crud(db)
        updated_rhyme_set = crud.update_rhyme_set(rhyme_set_id, rhyme_set_update)
        
        if not updated_rhyme_set:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rijmset met ID {rhyme_set_id} niet gevonden"
            )
        
        return updated_rhyme_set
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij updaten rijmset: {str(e)}"
        )

@router.delete("/rhyme-sets/{rhyme_set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rhyme_set(rhyme_set_id: int, db: Session = Depends(get_db)):
    """Verwijder rijmset"""
    try:
        crud = get_thema_crud(db)
        success = crud.delete_rhyme_set(rhyme_set_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rijmset met ID {rhyme_set_id} niet gevonden"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij verwijderen rijmset: {str(e)}"
        )

# Bulk operations
@router.put("/themes/bulk/toggle-active")
async def bulk_toggle_thema_active(
    thema_ids: List[int],
    is_active: bool,
    db: Session = Depends(get_db)
):
    """Bulk toggle actief status van thema's"""
    try:
        crud = get_thema_crud(db)
        updated_count = crud.bulk_toggle_active(thema_ids, is_active)
        
        return {
            "success_count": updated_count,
            "error_count": len(thema_ids) - updated_count,
            "errors": []
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij bulk update: {str(e)}"
        ) 