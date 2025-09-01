from flask import Blueprint, request, jsonify
from app.models.perfis import Perfil

bp = Blueprint('perfil', __name__, url_prefix="/api/v1/perfil")

@bp.route('', methods=['POST'], strict_slashes=False)
async def criarPerfil():
    try:
        data = request.get_json()
        perfil = Perfil.criar(data)
        return jsonify(perfil.retornaDicionario()), 201
    except Exception as err:
        return jsonify(err.to_dict()),err.to_dict().get("status_code")