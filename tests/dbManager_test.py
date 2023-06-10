import unittest
from unittest.mock import patch

from dbManager import generateDfPurchaseReturns, create_connection, executeQuery
import pandas as pd


class TestDbManagerFunctions(unittest.TestCase):
    def test_generateDfPurchaseReturns(self):
        # Mock the transactions DataFrame
        transactions = pd.DataFrame({
            'transaction_type': ['PurchaseActivity', 'ReturnActivity', 'PurchaseActivity'],
            'amount_cents': [1000, 500, 1500]
        })

        # Mock the expected purchases and returns DataFrames
        expected_purchases = pd.DataFrame({
            'transaction_type': ['PurchaseActivity', 'PurchaseActivity'],
            'amount_cents': [1000, 1500]
        })
        expected_returns = pd.DataFrame({
            'transaction_type': ['ReturnActivity'],
            'amount_cents': [500]
        })

        # Call the function and retrieve the actual purchases and returns DataFrames
        actual_purchases, actual_returns = generateDfPurchaseReturns(transactions)

        # Compare the expected and actual DataFrames
        pd.testing.assert_frame_equal(expected_purchases, actual_purchases)
        pd.testing.assert_frame_equal(expected_returns, actual_returns)

    @patch('dbManager.create_connection')
    def test_execute_query_success(self, mock_create_connection):
        # Mock the create_connection function to return a mock connection object
        mock_connection = mock_create_connection.return_value
        mock_cursor = mock_connection.cursor.return_value

        # Mock the fetchall result
        mock_result = [('data1', 'data2'), ('data3', 'data4')]
        mock_cursor.fetchall.return_value = mock_result

        # Call the executeQuery function with a sample query
        query = "SELECT * FROM table"
        db_file = 'database.db'  # Provide the correct database file path
        result = executeQuery(query, db_file)

        # Assertions
        mock_create_connection.assert_called_once_with('database.db')
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, mock_result)

    @patch('dbManager.create_connection')
    def test_execute_query_exception(self, mock_create_connection):
        # Mock the create_connection function to raise an exception
        mock_create_connection.side_effect = Exception("Connection error")

        # Call the executeQuery function with a sample query
        query = "SELECT * FROM table"
        db_file = 'database.db'  # Provide the correct database file path
        result = executeQuery(query, db_file)

        # Assertions
        mock_create_connection.assert_called_once_with('database.db')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
