"""
Test om te verifiëren dat de raw_data van orders de volledige Plug&Pay payload bevat.
"""

import unittest
from unittest.mock import patch, MagicMock, Mock

# We moeten alle database-gerelateerde modules mocken voordat we de app importeren
patches = [
    patch('sqlalchemy.orm.Session'),
    patch('sqlalchemy.Column'),
    patch('sqlalchemy.Integer'),
    patch('sqlalchemy.String'),
    patch('sqlalchemy.DateTime'),
    patch('sqlalchemy.UniqueConstraint'),
    patch('sqlalchemy.dialects.postgresql.JSONB'),
    patch('sqlalchemy.exc.IntegrityError'),
    patch('app.db.session.Base'),
    patch('logging.getLogger')
]

# Start alle patches
for p in patches:
    p.start()

# Nu kunnen we veilig de app modules importeren
from app.services.plugpay_client import fetch_and_store_recent_orders


class TestRawDataCompleteness(unittest.TestCase):
    """Test cases voor de volledigheid van raw_data in orders."""

    def setUp(self):
        """Setup voor elke test."""
        # Maak een mock logger die we kunnen gebruiken
        self.mock_logger = MagicMock()
        patch('logging.getLogger', return_value=self.mock_logger).start()

    def tearDown(self):
        """Cleanup na elke test."""
        patch.stopall()

    @patch('app.services.plugpay_client.get_recent_orders')
    @patch('app.services.plugpay_client.get_order_details')
    def test_fetch_and_store_includes_complete_payload(self, mock_get_order_details, mock_get_recent_orders):
        """Test dat fetch_and_store_recent_orders de volledige payload opslaat in raw_data."""
        # Mock data voor recente orders (summary list)
        mock_get_recent_orders.return_value = {
            "data": [
                {"id": 12345, "customer": {"name": "Test Klant"}}
            ]
        }
        
        # Mock data voor order details met custom fields en products
        mock_order_details = {
            "id": 12345,
            "customer": {"name": "Test Klant", "email": "test@example.com"},
            "custom_field_inputs": [
                {"label": "Gewenste stijl", "input": "verjaardag"},
                {"label": "Beschrijf", "input": "Een vrolijk verjaardagslied"}
            ],
            "products": [
                {"id": 1, "title": "Persoonlijk lied - Deadline 7 dagen", "name": "Persoonlijk lied"}
            ],
            "address": {
                "full_name": "Test Klant",
                "email": "test@example.com"
            }
        }
        mock_get_order_details.return_value = mock_order_details
        
        # Mock voor Order.create_from_plugpay_data
        mock_order = MagicMock()
        mock_order_class = MagicMock()
        mock_order_class.create_from_plugpay_data.return_value = (mock_order, True)
        
        with patch('app.models.order.Order', mock_order_class):
            # Mock voor de database sessie
            mock_db = MagicMock()
            mock_db.query.return_value.filter_by.return_value.first.return_value = None
            
            # Voer de functie uit die we testen
            fetch_and_store_recent_orders(mock_db)
            
            # Verifieer dat get_order_details is aangeroepen
            mock_get_order_details.assert_called_once_with(12345)
            
            # Verifieer dat Order.create_from_plugpay_data is aangeroepen met de volledige order details
            mock_order_class.create_from_plugpay_data.assert_called_once()
            args = mock_order_class.create_from_plugpay_data.call_args[0]
            self.assertEqual(args[0], mock_db)  # Eerste argument is db_session
            self.assertEqual(args[1], mock_order_details)  # Tweede argument is order_data
            
            # Verifieer dat de order_data de volledige payload bevat
            self.assertIn("custom_field_inputs", mock_order_details)
            self.assertIn("products", mock_order_details)
            self.assertIn("address", mock_order_details)
            self.assertTrue(len(mock_order_details["custom_field_inputs"]) > 0)
            self.assertTrue(len(mock_order_details["products"]) > 0)

    @patch('app.services.plugpay_client.get_recent_orders')
    @patch('app.services.plugpay_client.get_order_details')
    def test_update_existing_order_with_complete_payload(self, mock_get_order_details, mock_get_recent_orders):
        """Test dat bestaande orders worden bijgewerkt met de volledige payload in raw_data."""
        # Mock data voor recente orders (summary list)
        mock_get_recent_orders.return_value = {
            "data": [
                {"id": 12345, "customer": {"name": "Test Klant"}}
            ]
        }
        
        # Mock data voor order details met custom fields en products
        mock_order_details = {
            "id": 12345,
            "customer": {"name": "Test Klant", "email": "test@example.com"},
            "custom_field_inputs": [
                {"label": "Gewenste stijl", "input": "verjaardag"},
                {"label": "Beschrijf", "input": "Een vrolijk verjaardagslied"}
            ],
            "products": [
                {"id": 1, "title": "Persoonlijk lied - Deadline 7 dagen", "name": "Persoonlijk lied"}
            ],
            "address": {
                "full_name": "Test Klant",
                "email": "test@example.com"
            }
        }
        mock_get_order_details.return_value = mock_order_details
        
        # Mock voor een bestaande order in de database
        mock_existing_order = MagicMock()
        mock_existing_order.order_id = 12345
        mock_existing_order.raw_data = {}
        
        # Mock voor de database sessie die de bestaande order teruggeeft
        mock_db = MagicMock()
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_existing_order
        
        # Voer de functie uit die we testen
        fetch_and_store_recent_orders(mock_db)
        
        # Verifieer dat de bestaande order is bijgewerkt met de volledige raw_data
        self.assertEqual(mock_existing_order.raw_data, mock_order_details)
        mock_db.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
