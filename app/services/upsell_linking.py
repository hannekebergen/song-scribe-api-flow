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
    Vindt de originele order die hoort bij een UpSell order met confidence scoring.
    
    Strategie:
    1. Zoek naar orders met dezelfde klant (email/naam) binnen 7 dagen voor de UpSell
    2. Filter op standaard orders (product_id 274588 of 289456)
    3. Bereken confidence score voor elke match
    4. Selecteer alleen matches met hoge confidence (>70%)
    5. Selecteer de beste match
    
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
        # Zoek 7 dagen terug vanaf de UpSell order
        search_start = upsell_datetime - timedelta(days=7)
        
        # Query voor potentiële originele orders
        query = db_session.query(Order).filter(
            Order.bestel_datum >= search_start,
            Order.bestel_datum < upsell_datetime,
            Order.order_id != upsell_order_id  # Niet de UpSell order zelf
        )
        
        # Filter op standaard orders (product_id 274588 = Standaard 72u, 289456 = Spoed 24u)
        potential_orders = query.all()
        
        original_orders_with_scores = []
        
        for order in potential_orders:
            if order.raw_data and order.raw_data.get("products"):
                for product in order.raw_data["products"]:
                    product_id = product.get("id")
                    pivot_type = product.get("pivot", {}).get("type")
                    
                    # Standaard orders hebben product_id 274588 of 289456 en geen upsell type
                    if product_id in [274588, 289456] and pivot_type != "upsell":
                        # Bereken confidence score
                        confidence = calculate_linking_confidence(
                            upsell_order_data, order, customer_email, customer_name, upsell_datetime, db_session
                        )
                        
                        if confidence > 70:  # Alleen hoge confidence matches
                            original_orders_with_scores.append((order, confidence))
                            logger.info(f"Originele order {order.order_id} gevonden met confidence {confidence}%")
                        else:
                            logger.info(f"Originele order {order.order_id} afgewezen (confidence {confidence}% < 70%)")
                        break
        
        if not original_orders_with_scores:
            logger.info(f"Geen originele order gevonden voor UpSell {upsell_order_id} (geen matches met hoge confidence)")
            return None
        
        # Selecteer de order met de hoogste confidence score
        original_orders_with_scores.sort(key=lambda x: x[1], reverse=True)
        best_match, best_confidence = original_orders_with_scores[0]
        
        # Als er meerdere matches zijn met vergelijkbare confidence, log een waarschuwing
        if len(original_orders_with_scores) > 1:
            second_best_confidence = original_orders_with_scores[1][1]
            if best_confidence - second_best_confidence < 10:  # Minder dan 10% verschil
                logger.warning(f"AMBIGUOUS MATCH voor UpSell {upsell_order_id}: "
                             f"Best match {best_match.order_id} ({best_confidence}%) vs "
                             f"Second best {original_orders_with_scores[1][0].order_id} ({second_best_confidence}%)")
        
        logger.info(f"Originele order {best_match.order_id} geselecteerd voor UpSell {upsell_order_id} (confidence: {best_confidence}%)")
        return best_match.order_id
        
    except Exception as e:
        logger.error(f"Fout bij zoeken naar originele order voor UpSell {upsell_order_id}: {str(e)}")
        return None


def calculate_linking_confidence(upsell_data: Dict[str, Any], original_order, customer_email: str, customer_name: str, upsell_datetime: datetime, db_session: Session) -> float:
    """
    Bereken confidence score voor een potentiële match tussen UpSell en originele order.
    
    Args:
        upsell_data: UpSell order data
        original_order: Originele order object
        customer_email: Customer email (kan None zijn)
        customer_name: Customer name
        upsell_datetime: UpSell order timestamp
        
    Returns:
        float: Confidence score (0-100)
    """
    confidence = 0.0
    
    # Email matching (hoogste prioriteit)
    if customer_email and original_order.klant_email:
        if customer_email.lower() == original_order.klant_email.lower():
            confidence += 50.0  # Email match is zeer betrouwbaar
            logger.debug(f"Email match: +50% confidence")
    
    # Naam matching
    if customer_name:
        # Exacte naam match
        if original_order.klant_naam and customer_name.lower() == original_order.klant_naam.lower():
            confidence += 30.0
            logger.debug(f"Exacte naam match: +30% confidence")
        # Voornaam match
        elif original_order.voornaam and customer_name.split()[0].lower() == original_order.voornaam.lower():
            confidence += 15.0
            logger.debug(f"Voornaam match: +15% confidence")
        # Gedeeltelijke naam match
        elif original_order.klant_naam and customer_name.split()[0].lower() in original_order.klant_naam.lower():
            confidence += 10.0
            logger.debug(f"Gedeeltelijke naam match: +10% confidence")
    
    # Tijdsperiode matching
    time_diff = (upsell_datetime - original_order.bestel_datum).total_seconds() / 3600  # uren
    
    if time_diff <= 1:  # Binnen 1 uur
        confidence += 20.0
        logger.debug(f"Binnen 1 uur: +20% confidence")
    elif time_diff <= 24:  # Binnen 24 uur
        confidence += 15.0
        logger.debug(f"Binnen 24 uur: +15% confidence")
    elif time_diff <= 168:  # Binnen 7 dagen
        confidence += 10.0
        logger.debug(f"Binnen 7 dagen: +10% confidence")
    else:
        confidence -= 10.0  # Penalty voor te oude orders
        logger.debug(f"Te oude order: -10% confidence")
    
    # Product type validatie
    if original_order.raw_data and original_order.raw_data.get("products"):
        for product in original_order.raw_data["products"]:
            product_id = product.get("id")
            pivot_type = product.get("pivot", {}).get("type")
            
            if product_id in [274588, 289456] and pivot_type != "upsell":
                confidence += 5.0  # Bonus voor correcte product type
                logger.debug(f"Correcte product type: +5% confidence")
                break
    
    # Check voor dubbele orders van dezelfde klant
    if original_order.klant_naam:
        # Tel hoeveel orders deze klant heeft in de afgelopen 7 dagen
        from datetime import timedelta
        recent_orders = db_session.query(Order).filter(
            Order.klant_naam == original_order.klant_naam,
            Order.bestel_datum >= upsell_datetime - timedelta(days=7),
            Order.bestel_datum < upsell_datetime,
            Order.order_id != original_order.order_id
        ).count()
        
        if recent_orders > 0:
            confidence -= (recent_orders * 5.0)  # Penalty voor meerdere orders
            logger.debug(f"Meerdere orders van klant: -{recent_orders * 5}% confidence")
    
    # Cap confidence op 100%
    confidence = min(confidence, 100.0)
    
    return confidence


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