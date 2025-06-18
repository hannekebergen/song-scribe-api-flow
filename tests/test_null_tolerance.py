"""
Test om te verifiëren dat het OrderRead schema null-tolerant is en geen ValidationError geeft bij ontbrekende velden.
"""

import unittest
from unittest import mock
import os
from datetime import datetime
from pydantic import ValidationError

# Set up environment variables for testing
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

# Import the schema directly - we don't need to mock database modules for this test
from app.schemas.order import OrderRead


class TestNullTolerance(unittest.TestCase):
    """Test cases voor de null-tolerantie van het OrderRead schema."""

    def setUp(self):
        """Setup voor elke test."""
        # Maak een mock logger die we kunnen gebruiken
        self.mock_logger = mock.MagicMock()
        mock.patch('logging.getLogger', return_value=self.mock_logger).start()

    def tearDown(self):
        """Cleanup na elke test."""
        mock.patch.stopall()

    def make_stub(self, **kwargs):
        """Helper om een stub dictionary te maken."""
        return kwargs

    def test_order_without_product_name(self):
        """Test dat een order zonder product_naam geen ValidationError geeft."""
        stub = self.make_stub(
            id=1, 
            order_id=123,
            product_naam=None,
            bestel_datum=None,
            raw_data={"products": [{"title": "Liedje – Binnen 24 uur", "created_at": "2023-01-01T12:00:00Z"}]}
        )
        o = OrderRead.model_validate(stub)
        self.assertEqual(o.product_naam, "Liedje – Binnen 24 uur")
        self.assertIsNotNone(o.bestel_datum)

    def test_order_without_bestel_datum(self):
        """Test dat een order zonder bestel_datum geen ValidationError geeft."""
        stub = self.make_stub(
            id=1, 
            order_id=123,
            product_naam="Test Product",
            bestel_datum=None,
            raw_data={"created_at": "2023-01-01T12:00:00Z"}
        )
        o = OrderRead.model_validate(stub)
        self.assertEqual(o.product_naam, "Test Product")
        self.assertIsNotNone(o.bestel_datum)

    def test_order_with_empty_raw_data(self):
        """Test dat een order met lege raw_data geen ValidationError geeft."""
        stub = self.make_stub(
            id=1, 
            order_id=123,
            product_naam="Test Product",
            bestel_datum=datetime.now(),
            raw_data={}
        )
        o = OrderRead.model_validate(stub)
        self.assertEqual(o.product_naam, "Test Product")
        self.assertIsNotNone(o.bestel_datum)

    def test_order_with_null_raw_data(self):
        """Test dat een order met raw_data=None geen ValidationError geeft."""
        stub = self.make_stub(
            id=1, 
            order_id=123,
            product_naam="Test Product",
            bestel_datum=datetime.now(),
            raw_data=None
        )
        o = OrderRead.model_validate(stub)
        self.assertEqual(o.product_naam, "Test Product")
        self.assertIsNotNone(o.bestel_datum)
        self.assertEqual(o.raw_data, {})  # Controleer dat raw_data een lege dict is geworden


if __name__ == '__main__':
    unittest.main()
