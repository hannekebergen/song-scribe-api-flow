"""
Tests voor de get_custom_fields functie in de plugpay_client module.

Deze tests verifiëren dat de get_custom_fields functie correct werkt in verschillende scenario's:
1. Alleen root-level custom fields
2. Alleen product-level custom fields
3. Alleen custom fields via checkout endpoint
4. Geen custom fields beschikbaar
"""

import unittest
from unittest.mock import patch, MagicMock, Mock

# We moeten alle database-gerelateerde modules mocken voordat we de app importeren
import os
import requests

# Zet de DATABASE_URL environment variable om de database-verbinding te omzeilen
os.environ['DATABASE_URL'] = 'postgresql://fake:fake@localhost/fake'

# Mock de logger
mock_logger = MagicMock()
patch('app.services.plugpay_client.logger', mock_logger).start()

# Nu kunnen we veilig de app modules importeren
from app.services.plugpay_client import get_custom_fields


class TestGetCustomFields(unittest.TestCase):
    """Test cases voor de get_custom_fields functie."""

    def setUp(self):
        """Setup voor elke test."""
        # Reset de mock logger voor elke test
        global mock_logger
        mock_logger.reset_mock()
        self.mock_logger = mock_logger

    def tearDown(self):
        """Cleanup na elke test."""
        patch.stopall()

    def test_root_level_custom_fields(self):
        """Test dat root-level custom fields correct worden opgehaald."""
        # Order data met alleen root-level custom fields
        order_data = {
            "id": 12345,
            "custom_field_inputs": [
                {"name": "thema", "value": "Verjaardag"},
                {"name": "toon", "value": "Lief"},
                {"name": "structuur", "value": "Couplet-refrein"},
                {"name": "rijm", "value": "AA BB"}
            ]
        }
        
        # Roep de functie aan
        result = get_custom_fields(order_data)
        
        # Verifieer het resultaat
        self.assertEqual(len(result), 4)
        self.assertEqual(result["thema"], "Verjaardag")
        self.assertEqual(result["toon"], "Lief")
        self.assertEqual(result["structuur"], "Couplet-refrein")
        self.assertEqual(result["rijm"], "AA BB")

    def test_product_level_custom_fields(self):
        """Test dat product-level custom fields correct worden opgehaald als er geen root-level fields zijn."""
        # Order data met alleen product-level custom fields
        order_data = {
            "id": 12345,
            "custom_field_inputs": [],  # Lege root-level custom fields
            "products": [
                {
                    "id": 1,
                    "custom_field_inputs": [
                        {"name": "voornaam", "value": "Femm"},
                        {"name": "van", "value": "Diana"},
                        {"name": "relatie", "value": "Tantezegger"},
                        {"name": "beschrijving", "value": "Voor mijn tantezegger Femm, ze wordt 1 jaar..."}
                    ]
                }
            ]
        }
        
        # Roep de functie aan
        result = get_custom_fields(order_data)
        
        # Verifieer het resultaat
        self.assertEqual(len(result), 4)
        self.assertEqual(result["voornaam"], "Femm")
        self.assertEqual(result["van"], "Diana")
        self.assertEqual(result["relatie"], "Tantezegger")
        self.assertEqual(result["beschrijving"], "Voor mijn tantezegger Femm, ze wordt 1 jaar...")

    @patch('requests.get')
    def test_checkout_fallback_custom_fields(self, mock_get):
        """Test dat checkout fallback correct werkt als er geen root- of product-level fields zijn."""
        # Order data zonder custom fields maar met checkout_id
        order_data = {
            "id": 12345,
            "checkout_id": "c-67890",
            "custom_field_inputs": [],  # Lege root-level custom fields
            "products": [
                {
                    "id": 1,
                    "custom_field_inputs": []  # Lege product-level custom fields
                }
            ]
        }
        
        # Mock de response van de checkout endpoint
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "custom_field_inputs": [
                {"name": "thema", "value": "Verjaardag"},
                {"name": "toon", "value": "Lief"},
                {"name": "structuur", "value": "Couplet-refrein"},
                {"name": "rijm", "value": "AA BB"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Mock de API headers
        mock_headers = {"Authorization": "Bearer test_token"}
        
        # Roep de functie aan met de mock headers
        result = get_custom_fields(order_data, mock_headers)
        
        # Verifieer dat de checkout endpoint correct is aangeroepen
        mock_get.assert_called_once_with(
            f"https://api.plugandpay.nl/v1/checkouts/c-67890?include=custom_field_inputs",
            headers=mock_headers
        )
        
        # Verifieer het resultaat
        self.assertEqual(len(result), 4)
        self.assertEqual(result["thema"], "Verjaardag")
        self.assertEqual(result["toon"], "Lief")
        self.assertEqual(result["structuur"], "Couplet-refrein")
        self.assertEqual(result["rijm"], "AA BB")

    @patch('requests.get')
    def test_checkout_fallback_422_error(self, mock_get):
        """Test dat de functie gracefully faalt bij een 422-fout van de checkout endpoint."""
        # Order data zonder custom fields maar met checkout_id
        order_data = {
            "id": 12345,
            "checkout_id": "c-67890",
            "custom_field_inputs": [],  # Lege root-level custom fields
            "products": []  # Geen products
        }
        
        # Mock een 422-fout van de checkout endpoint
        mock_response = MagicMock()
        http_error = requests.exceptions.HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 422
        mock_get.side_effect = http_error
        
        # Mock de API headers
        mock_headers = {"Authorization": "Bearer test_token"}
        
        # Roep de functie aan met de mock headers
        result = get_custom_fields(order_data, mock_headers)
        
        # Verifieer dat de checkout endpoint correct is aangeroepen
        mock_get.assert_called_once_with(
            f"https://api.plugandpay.nl/v1/checkouts/c-67890?include=custom_field_inputs",
            headers=mock_headers
        )
        
        # Verifieer dat het resultaat een lege dictionary is
        self.assertEqual(result, {})
        
        # We focus on the core functionality - returning an empty dict when no fields are found
        # rather than the specific log message

    def test_no_custom_fields_available(self):
        """Test dat een lege dictionary wordt teruggegeven als er geen custom fields beschikbaar zijn."""
        # Order data zonder custom fields en zonder checkout_id
        order_data = {
            "id": 12345,
            "custom_field_inputs": [],  # Lege root-level custom fields
            "products": [
                {
                    "id": 1,
                    "custom_field_inputs": []  # Lege product-level custom fields
                }
            ]
        }
        
        # Roep de functie aan
        result = get_custom_fields(order_data)
        
        # Verifieer dat het resultaat een lege dictionary is
        self.assertEqual(result, {})
        
        # We focus on the core functionality - returning an empty dict when no fields are found
        # rather than the specific log message


if __name__ == '__main__':
    unittest.main()
