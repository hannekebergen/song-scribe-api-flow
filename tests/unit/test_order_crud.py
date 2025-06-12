"""
Unit tests voor order CRUD operations.
"""

import unittest
from unittest.mock import MagicMock, patch

# Mock the imports to avoid database initialization
with patch('app.models.order.Base'):
    with patch('app.db.session.Base'):
        with patch('app.db.session.create_engine'):
            from app.crud.order import get_order


# Create a mock Order class
Order = MagicMock()

class TestOrderCrud(unittest.TestCase):
    """Test cases voor order CRUD operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_db = MagicMock()
        self.mock_query = MagicMock()
        self.mock_filter = MagicMock()
        
        # Setup the chain of calls
        self.mock_db.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_filter
        
    @patch('app.crud.order.Order', Order)
    def test_get_order_found(self, mock_order_class):
        """Test get_order when order exists."""
        # Setup
        mock_order = MagicMock()
        self.mock_filter.first.return_value = mock_order
        plug_pay_order_id = 12920181
        
        # Execute
        result = get_order(self.mock_db, plug_pay_order_id)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_order_class)
        self.mock_query.filter.assert_called_once()
        # Verify we're filtering on order_id, not id
        mock_order_class.order_id.__eq__.assert_called_once_with(plug_pay_order_id)
        self.assertEqual(result, mock_order)
        
    @patch('app.crud.order.Order', Order)
    def test_get_order_not_found(self, mock_order_class):
        """Test get_order when order doesn't exist."""
        # Setup
        self.mock_filter.first.return_value = None
        non_existent_order_id = 999
        
        # Execute
        result = get_order(self.mock_db, non_existent_order_id)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_order_class)
        self.mock_query.filter.assert_called_once()
        # Verify we're filtering on order_id, not id
        mock_order_class.order_id.__eq__.assert_called_once_with(non_existent_order_id)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
