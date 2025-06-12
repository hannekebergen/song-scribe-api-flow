"""
CRUD operations voor Order model.

Deze module bevat database operaties voor het Order model.
"""

from sqlalchemy.orm import Session
from app.models.order import Order


def get_order(db: Session, order_id: int):
    """
    Haalt een specifieke bestelling op uit de database op basis van het Plug&Pay order_id.
    
    Args:
        db (Session): SQLAlchemy database sessie
        order_id (int): Plug&Pay order_id van de bestelling
        
    Returns:
        Order: De opgevraagde bestelling of None als deze niet bestaat
    """
    return db.query(Order).filter(Order.order_id == order_id).first()
