import unittest
from flask import Flask, jsonify
from Task1.routes import allByUser_bp, netMerchant_bp


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app.app_context().push()

        # Register the blueprints
        self.app.register_blueprint(allByUser_bp)
        self.app.register_blueprint(netMerchant_bp)

    def test_allByUserPost_with_valid_payload(self):
        # Prepare a valid payload
        payload = {
            'user_id': 12345
        }

        # Send a POST request to the /allByUser endpoint
        response = self.client.post('/allByUser', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 200)  # Expected status code

    def test_allByUserPost_with_missing_user_id(self):
        # Prepare a payload with a missing 'user_id' key
        payload = {}

        # Send a POST request to the /allByUser endpoint
        response = self.client.post('/allByUser', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 400)  # Expected status code
        expected_response = jsonify({"error": '"Invalid JSON payload: \'user_id\' key is missing."'})
        self.assertEqual(response.get_json(), expected_response.get_json())  # Expected response body

    def test_allByUserPost_with_extra_fields(self):
        # Prepare a payload with extra fields
        payload = {
            'user_id': 12345,
            'extra_field': 'extra'
        }

        # Send a POST request to the /allByUser endpoint
        response = self.client.post('/allByUser', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 400)  # Expected status code
        expected_response = jsonify({"error": "Invalid JSON payload: Extra fields found: extra_field"})
        self.assertEqual(response.get_json(), expected_response.get_json())  # Expected response body

    def test_netMerchant_with_valid_payload(self):
        # Prepare a valid payload
        payload = {
            'merchant_type_code': 12345
        }

        # Send a POST request to the /allByUser endpoint
        response = self.client.post('/netMerchant', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 200)  # Expected status code

    def test_netMerchant_with_missing_merchant_type_code(self):
        # Prepare a payload with a missing 'merchant_type_code' key
        payload = {}

        # Send a POST request to the /netMerchant endpoint
        response = self.client.post('/netMerchant', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 400)  # Expected status code
        expected_response = jsonify({"error": "\"Invalid JSON payload: 'merchant_type_code' key is missing.\""})
        self.assertEqual(response.get_json(), expected_response.get_json())  # Expected response body

    def test_netMerchant_with_extra_fields(self):
        # Prepare a payload with extra fields
        payload = {
            'merchant_type_code': 12345,
            'extra_field': 'extra'
        }

        # Send a POST request to the /netMerchant endpoint
        response = self.client.post('/netMerchant', json=payload)

        # Verify the response
        self.assertEqual(response.status_code, 400)  # Expected status code
        expected_response = jsonify({"error": "Invalid JSON payload: Extra fields found: extra_field"})
        self.assertEqual(response.get_json(), expected_response.get_json())  # Expected response body


if __name__ == '__main__':
    unittest.main()
