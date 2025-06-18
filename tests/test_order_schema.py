"""
Tests voor de OrderRead schema, met name de root_validator die velden afleidt uit raw_data.
"""

import pytest
from datetime import datetime
from app.schemas.order import OrderRead


def test_derive_fields_from_custom_field_inputs():
    """Test dat de root_validator correct velden afleidt uit custom_field_inputs."""
    # Mock data met custom fields in raw_data
    order_data = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "custom_field_inputs": [
                {"name": "Gewenste stijl", "value": "Verjaardag"},
                {"name": "Toon", "value": "Vrolijk"},
                {"name": "Structuur", "value": "Vers/Refrein"},
                {"name": "Beschrijf", "value": "Een lied voor een speciale verjaardag"}
            ],
            "products": [
                {"title": "Songtekst - Binnen 24 uur"}
            ]
        }
    }
    
    # Maak een OrderRead object
    order = OrderRead(**order_data)
    
    # Controleer of de afgeleide velden correct zijn
    assert order.thema == "Verjaardag"
    assert order.toon == "Vrolijk"
    assert order.structuur == "Vers/Refrein"
    assert order.beschrijving == "Een lied voor een speciale verjaardag"
    assert order.deadline == "Binnen 24 uur"


def test_derive_fields_with_label_input_format():
    """Test dat de root_validator werkt met label/input format in plaats van name/value."""
    # Mock data met custom fields in label/input format
    order_data = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "custom_field_inputs": [
                {"label": "Vertel over de gelegenheid", "input": "Jubileum"},
                {"label": "Sfeer", "input": "Nostalgisch"},
                {"label": "Song structuur", "input": "Vrije vorm"},
                {"label": "Beschrijf", "input": "Een lied over 25 jaar samen"}
            ],
            "address": {
                "full_name": "Jan Jansen"
            }
        }
    }
    
    # Maak een OrderRead object
    order = OrderRead(**order_data)
    
    # Controleer of de afgeleide velden correct zijn
    assert order.thema == "Jubileum"
    assert order.toon == "Nostalgisch"
    assert order.structuur == "Vrije vorm"
    assert order.beschrijving == "Een lied over 25 jaar samen"
    assert order.klant_naam == "Jan Jansen"


def test_derive_fields_with_existing_values():
    """Test dat de root_validator bestaande waarden niet overschrijft."""
    # Mock data met zowel bestaande velden als custom fields
    order_data = {
        "id": 1,
        "order_id": 12345,
        "klant_naam": "Bestaande Klant",
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "thema": "Bestaand Thema",
        "toon": "Bestaande Toon",
        "raw_data": {
            "custom_field_inputs": [
                {"name": "Gewenste stijl", "value": "Verjaardag"},
                {"name": "Toon", "value": "Vrolijk"}
            ]
        }
    }
    
    # Maak een OrderRead object
    order = OrderRead(**order_data)
    
    # Controleer of de bestaande waarden behouden blijven
    assert order.thema == "Bestaand Thema"
    assert order.toon == "Bestaande Toon"
    assert order.klant_naam == "Bestaande Klant"


def test_derive_fields_with_empty_raw_data():
    """Test dat de root_validator geen fouten geeft bij lege raw_data."""
    # Mock data zonder raw_data
    order_data = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow()
    }
    
    # Maak een OrderRead object
    order = OrderRead(**order_data)
    
    # Controleer of er geen fouten zijn en de velden None zijn
    assert order.thema is None
    assert order.toon is None
    assert order.structuur is None
    assert order.beschrijving is None
    assert order.deadline is None


def test_derive_fields_with_invalid_custom_field_inputs():
    """Test dat de root_validator geen fouten geeft bij ongeldige custom_field_inputs."""
    # Mock data met ongeldige custom_field_inputs
    order_data = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "custom_field_inputs": "niet een lijst maar een string"
        }
    }
    
    # Maak een OrderRead object
    order = OrderRead(**order_data)
    
    # Controleer of er geen fouten zijn en de velden None zijn
    assert order.thema is None
    assert order.toon is None
    assert order.structuur is None
    assert order.beschrijving is None
