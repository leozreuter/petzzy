from flask import Blueprint, request, jsonify
from app.models.pets import Pet, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('pet', __name__, url_prefix="/api/v1/pet")

@bp.route('', methods=['POST'], strict_slashes=False)
@token_required
def criarPetPage(current_user):
    try:
        data = request.get_json()
        pet = Pet.criarPet(data)
        return jsonify(pet.retornaDicionario()), 201
    except ValidationError as err:
        return jsonify(err.to_dict()), err.to_dict().get("status_code", 400)
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('', methods=['GET'], strict_slashes=False)
@token_required
def listarPetsPage(current_user):
    try:
        pets = Pet.listaPets()
        return jsonify(pets), 200
    except Exception as err:
        return jsonify({"error": "Ocorreu um erro inesperado", "details": str(err)}), 500

@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarPetPage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        pet_id = data.get('id')
        if not pet_id:
            raise ValidationError("É necessário fornecer o 'id' do pet.")

        pet_selecionado = Pet.procuraPeloID(pet_id)
        pet_selecionado.inativarPet()

        return jsonify({"message": f"Pet '{pet_selecionado.nome}' foi inativado com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor: {e}"}), 500

@bp.route('/ativar', methods=['POST'], strict_slashes=False)
@token_required
def ativarPetPage(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
        
    try:
        pet_id = data.get('id')
        if not pet_id:
            raise ValidationError("É necessário fornecer o 'id' do pet.")

        pet_selecionado = Pet.procuraPeloID(pet_id)
        pet_selecionado.ativarPet()

        return jsonify({"message": f"Pet '{pet_selecionado.nome}' foi ativado com sucesso."}), 200
    except ValidationError as e:
        return jsonify(e.to_dict()), e.to_dict().get("status_code", 400)
    except Exception as e:
        return