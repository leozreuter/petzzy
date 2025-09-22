from flask import Blueprint, request, jsonify
from app.models.prontuarios import Prontuario, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('prontuario', __name__, url_prefix="/api/v1/prontuario")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarProntuarioPage(current_user):
    try:
        data = request.get_json()
        prontuario = Prontuario.criarProntuario(data)
        return jsonify(prontuario.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarProntuariosPage(current_user):
    try:
        prontuarios = Prontuario.listaProntuarios()
        return jsonify(prontuarios), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarProntuarioPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' do prontuário é obrigatório."}), 400
        
    try:
        prontuario = Prontuario.procuraPeloID(data.get('id'))
        prontuario.inativarProntuario()
        return jsonify({"message": f"Prontuário ID '{prontuario.id}' foi inativado com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarProntuarioPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' do prontuário é obrigatório."}), 400
        
    try:
        prontuario = Prontuario.procuraPeloID(data.get('id'))
        prontuario.ativarProntuario()
        return jsonify({"message": f"Prontuário ID '{prontuario.id}' foi ativado com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500