from flask import Blueprint, request, jsonify
from app.models.atendimentos import Atendimento, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('atendimento', __name__, url_prefix="/api/v1/atendimento")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarAtendimentoPage(current_user):
    try:
        data = request.get_json()
        atendimento = Atendimento.criarAtendimento(data)
        return jsonify(atendimento.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarAtendimentosPage(current_user):
    try:
        atendimentos = Atendimento.listaAtendimentos()
        return jsonify(atendimentos), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

# Rotas específicas de status para Atendimento
@bp.route('/realizar', methods=['POST'], strict_slashes=False)
@token_required
def realizarAtendimentoPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' do atendimento é obrigatório."}), 400
    try:
        atendimento = Atendimento.procuraPeloID(data.get('id'))
        atendimento.realizarAtendimento()
        return jsonify({"message": f"Atendimento ID '{atendimento.id}' foi marcado como realizado."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/cancelar', methods=['POST'], strict_slashes=False)
@token_required
def cancelarAtendimentoPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' do atendimento é obrigatório."}), 400
    try:
        atendimento = Atendimento.procuraPeloID(data.get('id'))
        atendimento.cancelarAtendimento()
        return jsonify({"message": f"Atendimento ID '{atendimento.id}' foi cancelado."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500