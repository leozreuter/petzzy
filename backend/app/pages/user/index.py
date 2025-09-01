from flask import Blueprint, request, jsonify
from app.models.usuarios import Usuario

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")

@bp.route('', methods=['POST'], strict_slashes=False)
async def criarUsuario():
    """
    Recebe `email, name, password, idperfil` e cria um novo usuário 
    """
    try:
        data = request.get_json()
        user = Usuario.criar(data)
        return jsonify(user.retornaDicionario()), 201
    except Exception as err:
        return jsonify(err.to_dict()),err.to_dict().get("status_code")


@bp.route('', methods=['GET'], strict_slashes=False)
async def listarUsuarios():
    """
    Retorna uma lista de usuários 
    """
    try:
        usuarios = Usuario.listaUsuarios()
        return jsonify(usuarios), 200
    except Exception as err:
        return jsonify(err.to_dict()),err.to_dict().get("status_code")
