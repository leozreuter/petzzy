from flask import Blueprint, request, jsonify
from app.models.especies import Especie, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('especie', __name__, url_prefix="/api/v1/especie")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarEspeciePage(current_user):
    try:
        data = request.get_json()
        especie = Especie.criarEspecie(data)
        return jsonify(especie.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarEspeciesPage(current_user):
    try:
        especies = Especie.listaEspecies()
        return jsonify(especies), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarEspeciePage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        especie_id = data.get('id')
        if not especie_id:
            raise ValidationError("É necessário fornecer o 'id' da espécie.")

        especie_selecionada = Especie.procuraPeloID(especie_id)
        especie_selecionada.inativarEspecie()

        return jsonify({"message": f"Espécie '{especie_selecionada.nome}' foi inativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarEspeciePage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        especie_id = data.get('id')
        if not especie_id:
            raise ValidationError("É necessário fornecer o 'id' da espécie.")

        especie_selecionada = Especie.procuraPeloID(especie_id)
        especie_selecionada.ativarEspecie()

        return jsonify({"message": f"Espécie '{especie_selecionada.nome}' foi ativada com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500