"""
Sample order data for testing the description field extraction logic
"""

# Sample order data with product-level custom fields containing description
sample_order = {
    "order_id": 12946543,
    "custom_field_inputs": [
        {"label": "Voornaam", "input": "John"},
        {"label": "Van", "input": "Doe"},
        {"label": "Relatie", "input": "Vriend"}
    ],
    "products": [
        {
            "id": 123456,
            "name": "Lied op maat",
            "custom_field_inputs": [
                {"label": "Beschrijf", "input": "Dit is een lang persoonlijk verhaal over mijn vriend John. Hij is een geweldige persoon die altijd voor anderen klaarstaat. Hij houdt van muziek en natuur. We kennen elkaar al 15 jaar en hebben samen veel meegemaakt. Ik wil hem verrassen met een lied voor zijn verjaardag."},
                {"label": "Thema", "input": "Verjaardag"},
                {"label": "Toon", "input": "Vrolijk"}
            ]
        }
    ],
    "address": {
        "note": ""  # Empty note, so we should use the product-level "Beschrijf" field
    }
}

# Sample order data with description in address.note
sample_order_with_note = {
    "order_id": 12946544,
    "custom_field_inputs": [
        {"label": "Voornaam", "input": "Jane"},
        {"label": "Van", "input": "Smith"},
        {"label": "Relatie", "input": "Zus"}
    ],
    "products": [
        {
            "id": 123457,
            "name": "Lied op maat",
            "custom_field_inputs": [
                {"label": "Thema", "input": "Huwelijk"},
                {"label": "Toon", "input": "Romantisch"}
            ]
        }
    ],
    "address": {
        "note": "Mijn zus Jane gaat trouwen en ik wil haar verrassen met een lied. Ze is een lieve persoon die altijd voor haar familie klaarstaat."
    }
}

# Sample order data with no description fields
sample_order_no_description = {
    "order_id": 12946545,
    "custom_field_inputs": [
        {"label": "Voornaam", "input": "Bob"},
        {"label": "Van", "input": "Johnson"},
        {"label": "Relatie", "input": "Collega"},
        {"label": "Thema", "input": "Pensioen"},
        {"label": "Toon", "input": "Humoristisch"}
    ],
    "products": [
        {
            "id": 123458,
            "name": "Lied op maat",
            "custom_field_inputs": []
        }
    ],
    "address": {
        "note": ""
    }
}

# Sample order data with old format custom fields
sample_order_old_format = {
    "order_id": 12946546,
    "custom_fields": {
        "Voornaam": "Mike",
        "Van": "Brown",
        "Relatie": "Vader",
        "Beschrijf": "Mijn vader is een geweldige man die altijd voor zijn gezin heeft gezorgd."
    },
    "products": [
        {
            "id": 123459,
            "name": "Lied op maat",
            "custom_fields": {
                "Thema": "Vaderdag",
                "Toon": "Dankbaar"
            }
        }
    ],
    "address": {
        "note": ""
    }
}

# Sample order data with description in alternative field
sample_order_alt_description = {
    "order_id": 12946547,
    "custom_field_inputs": [
        {"label": "Voornaam", "input": "Sarah"},
        {"label": "Van", "input": "Wilson"},
        {"label": "Relatie", "input": "Dochter"},
        {"label": "Opmerking", "input": "Mijn dochter Sarah wordt 18 jaar en ik wil haar verrassen met een lied over haar jeugd en toekomst."}
    ],
    "products": [
        {
            "id": 123460,
            "name": "Lied op maat",
            "custom_field_inputs": [
                {"label": "Thema", "input": "Verjaardag"},
                {"label": "Toon", "input": "Emotioneel"}
            ]
        }
    ],
    "address": {
        "note": ""
    }
}
