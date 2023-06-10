from flask import Blueprint, request, jsonify, current_app
from controller import allByUser, netMerchant

routes = Blueprint('routes', __name__)


@routes.route('/allByUser', methods=['POST'])
def allByUserPost():
    """
    Handle a POST request to retrieve all data for a specific user.

    Request JSON:
    {
        "user_id": int
    }

    Returns:
    JSON response containing the data for the user.

    Error Responses:
    - 400 Bad Request: If the 'user_id' key is missing in the JSON payload.
    - 400 Bad Request: If the request Content-Type is not 'application/json'.
    - 500 Internal Server Error: If an unexpected error occurs.
    """
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'."}), 415

        data = request.get_json()
        response = handle_allByUser_request(data)
        return response
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/netMerchant', methods=['POST'])
def netMerchantPost():
    """
    Handle a POST request to retrieve net merchant data for a specific merchant type code.

    Request JSON:
    {
        "merchant_type_code": int
    }

    Returns:
    JSON response containing the net merchant data.

    Error Responses:
    - 400 Bad Request: If the 'merchant_type_code' key is missing in the JSON payload.
    - 400 Bad Request: If the request Content-Type is not 'application/json'.
    - 500 Internal Server Error: If an unexpected error occurs.
    """
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'."}), 415

        data = request.get_json()
        response = handle_netMerchant_request(data)
        return response
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_allByUser_request(data):
    """
    Handle the request to retrieve all data for a specific user.

    Args:
        data (dict): JSON data from the request containing the 'user_id' key.

    Returns:
        Response data for the user.

    Raises:
        ValueError: If there are extra fields found in the JSON payload.
        KeyError: If the 'user_id' key is missing in the JSON payload.
    """
    with current_app.app_context():
        if 'user_id' in data:

            # Check if there are extra fields in the JSON data
            if len(data) > 1:
                extra_fields = [field for field in data if field != 'user_id']
                raise ValueError(f"Invalid JSON payload: Extra fields found: {', '.join(extra_fields)}")

            user_id = data['user_id']
            return allByUser(user_id)
        else:
            raise KeyError(f"Invalid JSON payload: 'user_id' key is missing.")


def handle_netMerchant_request(data):
    """
    Handle the request to retrieve net merchant data for a specific merchant type code.

    Args:
        data (dict): JSON data from the request containing the 'merchant_type_code' key.

    Returns:
        Response data for the net merchant.

    Raises:
        ValueError: If there are extra fields found in the JSON payload.
        KeyError: If the 'merchant_type_code' key is missing in the JSON payload.
    """
    with current_app.app_context():
        if 'merchant_type_code' in data:

            # Check if there are extra fields in the JSON data
            if len(data) > 1:
                extra_fields = [field for field in data if field != 'merchant_type_code']
                raise ValueError(f"Invalid JSON payload: Extra fields found: {', '.join(extra_fields)}")

            merchant_type_code = data['merchant_type_code']
            return netMerchant(merchant_type_code)
        else:
            raise KeyError("Invalid JSON payload: 'merchant_type_code' key is missing.")


# Create a separate Blueprint object for each set of routes
allByUser_bp = Blueprint('allByUser', __name__)
netMerchant_bp = Blueprint('netMerchant', __name__)

# Register the routes with the corresponding Blueprint objects
allByUser_bp.register_blueprint(routes)
netMerchant_bp.register_blueprint(routes)
