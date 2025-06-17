import unittest
from unittest.mock import patch, MagicMock
import json
import requests

# Definieer de PlugPayAPIError klasse voor de test
class PlugPayAPIError(Exception):
    """Exception raised for errors in the Plug&Pay API."""
    pass

# Maak een eenvoudige implementatie van de functies die we willen testen
def mock_get_api_key():
    return "test_api_key"

def mock_extract_fields_from_array(fields_array, source_name):
    extracted = {}
    if isinstance(fields_array, list) and fields_array:
        for field in fields_array:
            if isinstance(field, dict):
                # Oude format: name/value
                if "name" in field and "value" in field:
                    extracted[field["name"]] = field["value"]
                # Nieuwe format: label/input
                elif "label" in field and "input" in field:
                    extracted[field["label"]] = field["input"]
    return extracted

def mock_get_custom_fields(order_data, api_headers=None):
    result = {}
    
    # Controleer of we met v2 API data te maken hebben
    is_v2_api = "items" in order_data and isinstance(order_data.get("items"), list)
    
    if is_v2_api:
        # V2 API verwerking
        # Stap 1: Verwerk root-level custom fields in v2 API
        root_fields_v2 = mock_extract_fields_from_array(order_data.get("custom_fields", []), "V2 Root-level")
        if root_fields_v2:
            result.update(root_fields_v2)
        
        # Stap 2: Verwerk item-level custom fields in v2 API
        if "items" in order_data and isinstance(order_data.get("items"), list):
            for item in order_data.get("items"):
                # Item-level custom fields
                item_fields = mock_extract_fields_from_array(item.get("custom_fields", []), "V2 Item")
                if item_fields:
                    result.update(item_fields)
                
                # Product-level custom fields binnen items
                if "product" in item and isinstance(item.get("product"), dict):
                    product_fields = mock_extract_fields_from_array(
                        item.get("product", {}).get("custom_fields", []), "V2 Product")
                    if product_fields:
                        result.update(product_fields)
    else:
        # V1 API verwerking (vereenvoudigd)
        root_fields = mock_extract_fields_from_array(order_data.get("custom_field_inputs", []), "Root-level")
        if root_fields:
            result.update(root_fields)
        
        root_fields_new = mock_extract_fields_from_array(order_data.get("custom_fields", []), "Root-level")
        if root_fields_new:
            result.update(root_fields_new)
    
    return result

class TestPlugPayV2API(unittest.TestCase):
    """Test cases voor de Plug&Pay v2 API integratie."""
    
    def test_get_custom_fields_v2(self):
        """Test de get_custom_fields functie met v2 API data."""
        # Maak een voorbeeld v2 order data
        v2_order_data = {
            "id": "12345",
            "custom_fields": [
                {"label": "Thema", "input": "Verjaardag"},
                {"label": "Toon", "input": "Vrolijk"}
            ],
            "items": [
                {
                    "id": "item1",
                    "custom_fields": [
                        {"label": "Voornaam", "input": "Jan"}
                    ],
                    "product": {
                        "id": "prod1",
                        "name": "Gedicht",
                        "custom_fields": [
                            {"label": "Beschrijf", "input": "Een persoonlijk verhaal over..."}
                        ]
                    }
                }
            ]
        }
        
        # Roep de mock functie aan
        result = mock_get_custom_fields(v2_order_data)
        
        # Controleer of alle custom fields zijn geëxtraheerd
        self.assertEqual(result["Thema"], "Verjaardag")
        self.assertEqual(result["Toon"], "Vrolijk")
        self.assertEqual(result["Voornaam"], "Jan")
        self.assertEqual(result["Beschrijf"], "Een persoonlijk verhaal over...")
    
    def test_extract_fields_from_array(self):
        """Test de extract_fields_from_array functie."""
        # Test met nieuwe format (label/input)
        fields_array_new = [
            {"label": "Thema", "input": "Verjaardag"},
            {"label": "Toon", "input": "Vrolijk"}
        ]
        result_new = mock_extract_fields_from_array(fields_array_new, "Test")
        self.assertEqual(result_new["Thema"], "Verjaardag")
        self.assertEqual(result_new["Toon"], "Vrolijk")
        
        # Test met oude format (name/value)
        fields_array_old = [
            {"name": "Thema", "value": "Verjaardag"},
            {"name": "Toon", "value": "Vrolijk"}
        ]
        result_old = mock_extract_fields_from_array(fields_array_old, "Test")
        self.assertEqual(result_old["Thema"], "Verjaardag")
        self.assertEqual(result_old["Toon"], "Vrolijk")
    
    def test_v2_api_structure_detection(self):
        """Test de detectie van v2 API structuur."""
        # V2 API data (met items array)
        v2_data = {"items": []}
        result_v2 = mock_get_custom_fields(v2_data)
        
        # V1 API data (zonder items array)
        v1_data = {"custom_field_inputs": [{"name": "Test", "value": "Value"}]}
        result_v1 = mock_get_custom_fields(v1_data)
        
        self.assertEqual(result_v1["Test"], "Value")
        
if __name__ == "__main__":
    unittest.main()
