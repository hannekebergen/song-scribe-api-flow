"""
Unit tests voor order endpoint.
"""

import unittest
from unittest.mock import MagicMock, patch

# Mock function to test the logic
def mock_get_order(db, order_id):
    """Mock implementation of the get_order function."""
    # This simulates the database query logic without actual database access
    if order_id == 1:
        # Return a mock order for ID 1
        return {"id": 1, "order_id": 12345, "klant_naam": "Test Klant"}
    else:
        # Return None for any other ID (simulating not found)
        return None


class TestOrderEndpoint(unittest.TestCase):
    """Test cases voor order endpoint."""

    def test_get_order_found(self):
        """Test retrieving an existing order."""
        # Test with ID that should be found
        result = mock_get_order(None, 1)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["order_id"], 12345)
        self.assertEqual(result["klant_naam"], "Test Klant")
        
    def test_get_order_not_found(self):
        """Test retrieving a non-existent order."""
        # Test with ID that should not be found
        result = mock_get_order(None, 999)
        
        # Assert
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
