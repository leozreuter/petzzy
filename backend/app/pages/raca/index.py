from flask import Blueprint, request, jsonify
from app.models.racas import Raca, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('raca', __name__, url_prefix="/api/v1/raca")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarRacaPage(current_user):
    try:
        data = request.get_json()
        raca = Raca.criarRaca(data)
        return jsonify(raca.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarRacasPage(current_user):
    try:
        racas = Raca.listaRacas()
        return jsonify(racas), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarRacaPage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        raca_id = data.get('id')
        if not raca_id:
            raise ValidationError("É necessário fornecer o 'id' da raça.")

        raca_selecionada = Raca.procuraPeloID(raca_id)
        raca_selecionada.inativarRaca()

        return jsonify({"message": f"Raça '{raca_selecionada.nome}' foi inativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarRacaPage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        raca_id = data.get('id')
        if not raca_id:
            raise ValidationError("É necessário fornecer o 'id' da raça.")

        raca_selecionada = Raca.procuraPeloID(raca_id)
        raca_selecionada.ativarRaca()

        return jsonify({"message": f"Raça '{raca_selecionada.nome}' foi ativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500