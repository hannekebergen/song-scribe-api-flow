"""
Admin API endpoints voor Thema database management
"""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.auth.token import get_api_key
from app.crud.thema import get_thema_crud
from app.models.order import Order
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

# Order Management endpoints
class OrderArchiveRequest(BaseModel):
    """Request model voor order archivering"""
    order_ids: List[int] = Field(..., description="Lijst van order IDs om te archiveren")

class OrderDeleteRequest(BaseModel):
    """Request model voor order verwijdering"""
    order_ids: List[int] = Field(..., description="Lijst van order IDs om te verwijderen")
    confirm: bool = Field(False, description="Bevestiging voor verwijdering (moet True zijn)")

class OrderCleanupRequest(BaseModel):
    """Request model voor automatische cleanup van oude orders"""
    days_old: int = Field(90, ge=30, le=365, description="Orders ouder dan X dagen")
    dry_run: bool = Field(True, description="Droog-run (geen echte verwijdering)")

class OrderManagementResponse(BaseModel):
    """Response model voor order management operaties"""
    success: bool
    processed_count: int
    failed_count: int
    message: str
    affected_orders: Optional[List[int]] = None

@router.get("/orders/stats")
async def get_order_stats(db: Session = Depends(get_db)):
    """Haal order statistieken op voor cleanup management"""
    try:
        total_orders = db.query(Order).count()
        
        # Orders per leeftijd
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        quarter_ago = now - timedelta(days=90)
        year_ago = now - timedelta(days=365)
        
        recent_orders = db.query(Order).filter(Order.bestel_datum >= week_ago).count()
        month_orders = db.query(Order).filter(
            and_(Order.bestel_datum >= month_ago, Order.bestel_datum < week_ago)
        ).count()
        quarter_orders = db.query(Order).filter(
            and_(Order.bestel_datum >= quarter_ago, Order.bestel_datum < month_ago)
        ).count()
        old_orders = db.query(Order).filter(Order.bestel_datum < quarter_ago).count()
        
        return {
            "total_orders": total_orders,
            "recent_orders": recent_orders,  # < 1 week
            "month_orders": month_orders,    # 1 week - 1 month
            "quarter_orders": quarter_orders, # 1 month - 3 months
            "old_orders": old_orders,        # > 3 months
            "cleanup_candidates": old_orders,
            "stats_generated_at": now.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen order statistieken: {str(e)}"
        )

@router.get("/orders/old")
async def get_old_orders(
    days_old: int = Query(90, ge=30, le=365, description="Orders ouder dan X dagen"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum aantal resultaten"),
    db: Session = Depends(get_db)
):
    """Haal oude orders op die kandidaat zijn voor cleanup"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        old_orders = db.query(Order).filter(
            Order.bestel_datum < cutoff_date
        ).order_by(Order.bestel_datum.asc()).limit(limit).all()
        
        return {
            "cutoff_date": cutoff_date.isoformat(),
            "days_old": days_old,
            "count": len(old_orders),
            "orders": [
                {
                    "id": order.id,
                    "order_id": order.order_id,
                    "klant_naam": order.klant_naam,
                    "bestel_datum": order.bestel_datum.isoformat() if order.bestel_datum else None,
                    "thema": order.thema,
                    "product_naam": order.product_naam
                }
                for order in old_orders
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij ophalen oude orders: {str(e)}"
        )

@router.delete("/orders/bulk-delete", response_model=OrderManagementResponse)
async def bulk_delete_orders(
    request: OrderDeleteRequest,
    db: Session = Depends(get_db)
):
    """Bulk verwijdering van orders (definitief!)"""
    try:
        if not request.confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bevestiging vereist voor verwijdering (confirm=True)"
            )
        
        if len(request.order_ids) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 100 orders per keer verwijderen"
            )
        
        # Verwijder orders
        deleted_count = db.query(Order).filter(
            Order.id.in_(request.order_ids)
        ).delete(synchronize_session=False)
        
        db.commit()
        
        return OrderManagementResponse(
            success=True,
            processed_count=deleted_count,
            failed_count=len(request.order_ids) - deleted_count,
            message=f"{deleted_count} orders succesvol verwijderd",
            affected_orders=request.order_ids[:deleted_count]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij verwijderen orders: {str(e)}"
        )

@router.post("/orders/cleanup", response_model=OrderManagementResponse)
async def cleanup_old_orders(
    request: OrderCleanupRequest,
    db: Session = Depends(get_db)
):
    """Automatische cleanup van oude orders"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=request.days_old)
        
        # Zoek orders die verwijderd zouden worden
        old_orders_query = db.query(Order).filter(
            Order.bestel_datum < cutoff_date
        )
        
        if request.dry_run:
            # Dry run: tel alleen
            count = old_orders_query.count()
            sample_orders = old_orders_query.limit(10).all()
            
            return OrderManagementResponse(
                success=True,
                processed_count=0,
                failed_count=0,
                message=f"DRY RUN: {count} orders zouden worden verwijderd (ouder dan {request.days_old} dagen)",
                affected_orders=[order.id for order in sample_orders]
            )
        else:
            # Echte verwijdering
            old_orders = old_orders_query.all()
            order_ids = [order.id for order in old_orders]
            
            if len(order_ids) > 500:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Te veel orders voor cleanup ({len(order_ids)}). Maximum 500 per keer."
                )
            
            deleted_count = old_orders_query.delete(synchronize_session=False)
            db.commit()
            
            return OrderManagementResponse(
                success=True,
                processed_count=deleted_count,
                failed_count=0,
                message=f"Cleanup voltooid: {deleted_count} oude orders verwijderd",
                affected_orders=order_ids
            )
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fout bij cleanup: {str(e)}"
        ) 