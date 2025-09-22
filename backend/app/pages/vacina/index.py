from flask import Blueprint, request, jsonify
from app.models.vacinas import Vacina, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('vacina', __name__, url_prefix="/api/v1/vacina")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarVacinaPage(current_user):
    try:
        data = request.get_json()
        vacina = Vacina.criarVacina(data)
        return jsonify(vacina.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarVacinasPage(current_user):
    try:
        vacinas = Vacina.listaVacinas()
        return jsonify(vacinas), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500
