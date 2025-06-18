import pytest
from sqlalchemy import inspect
from app.database import get_db
from app.models.order import Order


def test_order_columns_exist():
    """
    Test that the new columns added in the migration exist in the database schema.
    This test verifies that the Alembic migration was applied correctly.
    """
    # Get a database session
    db = next(get_db())
    
    # Get the inspector to examine the database schema
    inspector = inspect(db.bind)
    
    # Get the columns for the orders table
    columns = inspector.get_columns('orders')
    column_names = [col['name'] for col in columns]
    
    # Check that all the new columns exist
    assert 'thema' in column_names, "Column 'thema' not found in orders table"
    assert 'toon' in column_names, "Column 'toon' not found in orders table"
    assert 'structuur' in column_names, "Column 'structuur' not found in orders table"
    assert 'beschrijving' in column_names, "Column 'beschrijving' not found in orders table"
    assert 'deadline' in column_names, "Column 'deadline' not found in orders table"


def test_order_model_attributes():
    """
    Test that the SQLAlchemy Order model has the new attributes defined.
    """
    # Create a new Order instance
    order = Order()
    
    # Check that all the new attributes exist
    assert hasattr(order, 'thema'), "Order model missing 'thema' attribute"
    assert hasattr(order, 'toon'), "Order model missing 'toon' attribute"
    assert hasattr(order, 'structuur'), "Order model missing 'structuur' attribute"
    assert hasattr(order, 'beschrijving'), "Order model missing 'beschrijving' attribute"
    assert hasattr(order, 'deadline'), "Order model missing 'deadline' attribute"


def test_order_nullable_columns():
    """
    Test that the new columns are nullable as specified in the migration.
    """
    # Get a database session
    db = next(get_db())
    
    # Get the inspector to examine the database schema
    inspector = inspect(db.bind)
    
    # Get the columns for the orders table
    columns = {col['name']: col for col in inspector.get_columns('orders')}
    
    # Check that all the new columns are nullable
    assert columns['thema']['nullable'], "Column 'thema' should be nullable"
    assert columns['toon']['nullable'], "Column 'toon' should be nullable"
    assert columns['structuur']['nullable'], "Column 'structuur' should be nullable"
    assert columns['beschrijving']['nullable'], "Column 'beschrijving' should be nullable"
    assert columns['deadline']['nullable'], "Column 'deadline' should be nullable"
