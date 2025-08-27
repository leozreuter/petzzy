from flask import Flask, Blueprint, request, jsonify
from app.models.usuarios import Usuario

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")

@bp.route('', methods=['POST'], strict_slashes=False)
async def createUser():
    """
    Recebe `email, name, password, idperfil` e cria um novo usuário 
    """
    data = request.get_json()

    try:
        user = Usuario.create(data)
        return jsonify(user.to_dict()), 201
    except Exception as err:
        return jsonify(err.to_dict()),err.to_dict().get("status_code")
