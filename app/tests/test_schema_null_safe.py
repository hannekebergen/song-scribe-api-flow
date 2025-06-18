"""
Test voor null-safe schema validatie.

Deze test controleert of de OrderRead schema correct omgaat met null/None waarden
in raw_data.
"""

import pytest
from datetime import datetime
from app.schemas.order import OrderRead


def test_order_read_with_null_raw_data():
    """Test dat OrderRead correct werkt met raw_data=None."""
    order_stub = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": None,  # ← trigger!
    }
    parsed = OrderRead.model_validate(order_stub)
    assert parsed.raw_data == {}              # omgezet naar leeg dict
    assert parsed.thema is None               # blijft None, geen crash


def test_order_read_with_empty_raw_data():
    """Test dat OrderRead correct werkt met een lege raw_data dict."""
    order_stub = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {},  # lege dict
    }
    parsed = OrderRead.model_validate(order_stub)
    assert parsed.raw_data == {}
    assert parsed.thema is None
    assert parsed.toon is None
    assert parsed.beschrijving is None


def test_order_read_with_invalid_custom_fields():
    """Test dat OrderRead correct werkt met ongeldige custom_field_inputs."""
    order_stub = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "custom_field_inputs": "dit is geen lijst maar een string",
            "address": {"full_name": "Test Klant"}
        },
    }
    parsed = OrderRead.model_validate(order_stub)
    assert parsed.thema is None
    assert parsed.klant_naam == "Test Klant"  # moet nog steeds uit address komen


def test_order_read_with_valid_custom_fields():
    """Test dat OrderRead correct werkt met geldige custom_field_inputs."""
    order_stub = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "custom_field_inputs": [
                {"name": "Thema", "value": "Verjaardag"},
                {"label": "Toon", "input": "Vrolijk"},
                {"label": "Beschrijf", "input": "Een lied voor mijn vriend"}
            ],
            "address": {"full_name": "Test Klant"}
        },
    }
    parsed = OrderRead.model_validate(order_stub)
    assert parsed.thema == "Verjaardag"
    assert parsed.toon == "Vrolijk"
    assert parsed.beschrijving == "Een lied voor mijn vriend"
    assert parsed.klant_naam == "Test Klant"


def test_order_read_with_product_deadline():
    """Test dat OrderRead correct de deadline uit product titel haalt."""
    order_stub = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": datetime.utcnow(),
        "raw_data": {
            "products": [
                {"title": "Songtekst - Binnen 24 uur"}
            ]
        },
    }
    parsed = OrderRead.model_validate(order_stub)
    assert parsed.deadline == "Binnen 24 uur"
