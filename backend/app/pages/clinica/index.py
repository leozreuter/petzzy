from flask import Blueprint, request, jsonify
from app.models.clinicas import Clinica, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('clinica', __name__, url_prefix="/api/v1/clinica")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarClinicaPage(current_user):
    try:
        data = request.get_json()
        clinica = Clinica.criarClinica(data)
        return jsonify(clinica.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarClinicasPage(current_user):
    try:
        clinicas = Clinica.listaClinicas()
        return jsonify(clinicas), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarClinicaPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' da clínica é obrigatório."}), 400
        
    try:
        clinica = Clinica.procuraPeloID(data.get('id'))
        clinica.inativarClinica()
        return jsonify({"message": f"Clínica '{clinica.nome_fantasia}' foi inativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarClinicaPage(current_user):
    data = request.get_json()
    if not data or not data.get('id'):
        return jsonify({"error": "O 'id' da clínica é obrigatório."}), 400
        
    try:
        clinica = Clinica.procuraPeloID(data.get('id'))
        clinica.ativarClinica()
        return jsonify({"message": f"Clínica '{clinica.nome_fantasia}' foi ativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500