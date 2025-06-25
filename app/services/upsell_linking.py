"""
Service voor het linken van UpSell orders aan hun originele orders.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def find_original_order_for_upsell(db_session: Session, upsell_order_data: Dict[str, Any]) -> Optional[int]:
    """
    Vindt de originele order die hoort bij een UpSell order.
    
    Strategie:
    1. Zoek naar orders met dezelfde klant (email/naam) binnen 24 uur voor de UpSell
    2. Filter op standaard orders (product_id 274588 of 289456)
    3. Selecteer de meest recente match
    
    Args:
        db_session: SQLAlchemy database sessie
        upsell_order_data: De UpSell order data van de Plug&Pay API
        
    Returns:
        Optional[int]: Het order_id van de originele order, of None als niet gevonden
    """
    from app.models.order import Order
    
    try:
        # Haal basis informatie op uit de UpSell order
        upsell_order_id = upsell_order_data.get("id")
        upsell_created_at = upsell_order_data.get("created_at")
        
        if not upsell_created_at:
            logger.warning(f"UpSell order {upsell_order_id} heeft geen created_at timestamp")
            return None
        
        # Parse de timestamp
        try:
            upsell_datetime = datetime.fromisoformat(upsell_created_at.replace("Z", "+00:00"))
        except ValueError:
            logger.warning(f"Kan timestamp niet parsen voor UpSell order {upsell_order_id}: {upsell_created_at}")
            return None
        
        # Zoek naar klant informatie
        customer_email = None
        customer_name = None
        
        # Probeer email uit verschillende velden
        if upsell_order_data.get("customer", {}).get("email"):
            customer_email = upsell_order_data["customer"]["email"]
        elif upsell_order_data.get("address", {}).get("email"):
            customer_email = upsell_order_data["address"]["email"]
        
        # Probeer naam uit verschillende velden
        if upsell_order_data.get("address", {}).get("full_name"):
            customer_name = upsell_order_data["address"]["full_name"]
        elif upsell_order_data.get("customer", {}).get("name"):
            customer_name = upsell_order_data["customer"]["name"]
        elif upsell_order_data.get("address", {}).get("firstname"):
            firstname = upsell_order_data["address"]["firstname"]
            lastname = upsell_order_data["address"].get("lastname", "")
            customer_name = f"{firstname} {lastname}".strip()
        
        if not customer_email and not customer_name:
            logger.warning(f"Geen klant informatie gevonden voor UpSell order {upsell_order_id}")
            return None
        
        # Zoek naar mogelijke originele orders
        # Zoek 24 uur terug vanaf de UpSell order
        search_start = upsell_datetime - timedelta(hours=24)
        
        # Query voor potentiële originele orders
        query = db_session.query(Order).filter(
            Order.bestel_datum >= search_start,
            Order.bestel_datum < upsell_datetime,
            Order.order_id != upsell_order_id  # Niet de UpSell order zelf
        )
        
        # Filter op klant email als beschikbaar
        if customer_email:
            query = query.filter(Order.klant_email == customer_email)
        
        # Filter op standaard orders (product_id 274588 = Standaard 72u, 289456 = Spoed 24u)
        # We checken de raw_data voor product informatie
        potential_orders = query.all()
        
        original_orders = []
        for order in potential_orders:
            if order.raw_data and order.raw_data.get("products"):
                for product in order.raw_data["products"]:
                    product_id = product.get("id")
                    pivot_type = product.get("pivot", {}).get("type")
                    
                    # Standaard orders hebben product_id 274588 of 289456 en geen upsell type
                    if product_id in [274588, 289456] and pivot_type != "upsell":
                        original_orders.append(order)
                        break
        
        # Als we geen match op email hebben, probeer op naam
        if not original_orders and customer_name and not customer_email:
            query = db_session.query(Order).filter(
                Order.bestel_datum >= search_start,
                Order.bestel_datum < upsell_datetime,
                Order.order_id != upsell_order_id
            )
            
            # Zoek op klant_naam of voornaam
            name_query = query.filter(
                (Order.klant_naam.ilike(f"%{customer_name}%")) |
                (Order.voornaam.ilike(f"%{customer_name.split()[0]}%"))
            )
            
            potential_orders = name_query.all()
            
            for order in potential_orders:
                if order.raw_data and order.raw_data.get("products"):
                    for product in order.raw_data["products"]:
                        product_id = product.get("id")
                        pivot_type = product.get("pivot", {}).get("type")
                        
                        if product_id in [274588, 289456] and pivot_type != "upsell":
                            original_orders.append(order)
                            break
        
        if not original_orders:
            logger.info(f"Geen originele order gevonden voor UpSell {upsell_order_id}")
            return None
        
        # Selecteer de meest recente originele order
        original_order = max(original_orders, key=lambda o: o.bestel_datum)
        
        logger.info(f"Originele order {original_order.order_id} gevonden voor UpSell {upsell_order_id}")
        return original_order.order_id
        
    except Exception as e:
        logger.error(f"Fout bij zoeken naar originele order voor UpSell {upsell_order_id}: {str(e)}")
        return None


def inherit_theme_from_original(db_session: Session, upsell_order, original_order_id: int) -> bool:
    """
    Neemt het thema over van de originele order naar de UpSell order.
    
    Args:
        db_session: SQLAlchemy database sessie
        upsell_order: Het UpSell Order object
        original_order_id: Het order_id van de originele order
        
    Returns:
        bool: True als het thema succesvol is overgenomen, False anders
    """
    from app.models.order import Order
    
    try:
        # Haal de originele order op
        original_order = db_session.query(Order).filter_by(order_id=original_order_id).first()
        
        if not original_order:
            logger.warning(f"Originele order {original_order_id} niet gevonden in database")
            return False
        
        # Neem het thema over
        if original_order.thema:
            upsell_order.thema = original_order.thema
            logger.info(f"Thema '{original_order.thema}' overgenomen van order {original_order_id} naar UpSell {upsell_order.order_id}")
            return True
        else:
            logger.info(f"Originele order {original_order_id} heeft geen thema om over te nemen")
            return False
            
    except Exception as e:
        logger.error(f"Fout bij overnemen thema van order {original_order_id}: {str(e)}")
        return False 