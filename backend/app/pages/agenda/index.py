from flask import Blueprint, request, jsonify
from app.models.agendas import Agenda, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('agenda', __name__, url_prefix="/api/v1/agenda")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarAgendaPage(current_user):
    try:
        data = request.get_json()
        agenda = Agenda.criarAgenda(data)
        return jsonify(agenda.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarAgendasPage(current_user):
    try:
        agendas = Agenda.listaAgendas()
        return jsonify(agendas), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarAgendaPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' da agenda é obrigatório."}), 400
        
    try:
        agenda = Agenda.procuraPeloID(data.get('id'))
        agenda.inativarAgenda()
        return jsonify({"message": f"Agenda ID '{agenda.id}' foi inativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarAgendaPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' da agenda é obrigatório."}), 400
        
    try:
        agenda = Agenda.procuraPeloID(data.get('id'))
        agenda.ativarAgenda()
        return jsonify({"message": f"Agenda ID '{agenda.id}' foi ativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500