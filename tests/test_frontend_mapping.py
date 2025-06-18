"""
Tests voor de frontend mapOrder functie om te controleren of deze correct werkt met de nieuwe velden.
"""

import pytest
from src.hooks.useFetchOrders import mapOrder


def test_map_order_with_api_derived_fields():
    """Test dat mapOrder correct werkt met velden die al door de API zijn afgeleid."""
    # Mock order met afgeleide velden
    order = {
        "id": 1,
        "order_id": 12345,
        "klant_naam": "Jan Jansen",
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": "2023-06-15T12:00:00Z",
        "thema": "Verjaardag",
        "toon": "Vrolijk",
        "structuur": "Vers/Refrein",
        "beschrijving": "Een lied voor een speciale verjaardag",
        "deadline": "Binnen 24 uur"
    }
    
    # Map de order
    mapped = mapOrder(order)
    
    # Controleer of de velden correct zijn overgenomen
    assert mapped.ordernummer == 12345
    assert "2023" in mapped.datum
    assert mapped.thema == "Verjaardag"
    assert mapped.klant == "Jan Jansen"
    assert mapped.deadline == "Binnen 24 uur"


def test_map_order_with_fallback_to_custom_fields():
    """Test dat mapOrder terugvalt op custom fields als afgeleide velden ontbreken."""
    # Mock order zonder afgeleide velden maar met raw_data
    order = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": "2023-06-15T12:00:00Z",
        "raw_data": {
            "custom_field_inputs": [
                {"name": "Gewenste stijl", "value": "Verjaardag"},
                {"name": "Toon", "value": "Vrolijk"}
            ],
            "address": {
                "full_name": "Jan Jansen"
            },
            "products": [
                {"title": "Songtekst - Binnen 24 uur"}
            ]
        }
    }
    
    # Map de order
    mapped = mapOrder(order)
    
    # Controleer of de velden correct zijn afgeleid uit custom fields
    assert mapped.ordernummer == 12345
    assert "2023" in mapped.datum
    assert mapped.thema == "Verjaardag"
    assert mapped.klant == "Jan Jansen"
    assert "24 uur" in mapped.deadline


def test_map_order_with_fallback_to_label_input_format():
    """Test dat mapOrder werkt met label/input format in custom fields."""
    # Mock order zonder afgeleide velden maar met raw_data in label/input format
    order = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": "2023-06-15T12:00:00Z",
        "raw_data": {
            "custom_field_inputs": [
                {"label": "Vertel over de gelegenheid", "input": "Jubileum"},
                {"label": "Sfeer", "input": "Nostalgisch"}
            ],
            "address": {
                "firstname": "Jan",
                "lastname": "Jansen"
            },
            "products": [
                {"title": "Songtekst - Binnen 48 uur"}
            ]
        }
    }
    
    # Map de order
    mapped = mapOrder(order)
    
    # Controleer of de velden correct zijn afgeleid uit custom fields
    assert mapped.ordernummer == 12345
    assert "2023" in mapped.datum
    assert mapped.thema == "Jubileum"
    assert mapped.klant == "Jan Jansen"
    assert "48 uur" in mapped.deadline


def test_map_order_with_missing_fields():
    """Test dat mapOrder fallback waarden gebruikt als velden ontbreken."""
    # Mock order zonder velden
    order = {
        "id": 1,
        "order_id": 12345,
        "klant_email": "test@example.com",
        "product_naam": "Songtekst",
        "bestel_datum": "2023-06-15T12:00:00Z"
    }
    
    # Map de order
    mapped = mapOrder(order)
    
    # Controleer of de fallback waarden worden gebruikt
    assert mapped.ordernummer == 12345
    assert "2023" in mapped.datum
    assert mapped.thema == "-"
    assert mapped.klant == "-"
    assert mapped.deadline == "-"
