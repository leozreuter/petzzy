from flask import Blueprint, request, jsonify


bp = Blueprint('home', __name__, url_prefix="/api/v1/home")

@bp.route('', methods=['GET'], strict_slashes=False)
def home():
    return jsonify({"message": "OK", "status_code": 200}),200