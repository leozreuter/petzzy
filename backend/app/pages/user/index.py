from flask import Blueprint, request, jsonify
from app.models.usuarios import Usuario, ValidationError
from flask_jwt_extended import jwt_required

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")

@bp.route('', methods=['POST'], strict_slashes=False)
async def criarUsuario():
    """
    Recebe `email, name, password, idperfil` e cria um novo usuário 
    """
    try:
        data = request.get_json()
        user = Usuario.criarUsuario(data)
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
    
@bp.route('/inativar', methods=['POST'], strict_slashes=False)
#@jwt_required()
def inativarUsuario():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
    try:
        id = data.get('id')
        if not id:
            raise ValidationError("É necessário fornecer o 'id' do usuário.")

        usuarioSelecionado = Usuario.procuraUsuarioPorId(id)
        if not usuarioSelecionado:
            return jsonify({"error": "Usuário não encontrado."}), 404

        usuarioSelecionado.inativarUsuario()

        return jsonify({"message": f"Usuário '{usuarioSelecionado.nome}' foi inativado com sucesso."}), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400 
    
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor.{e}"}), 500
    
@bp.route('/ativar', methods=['POST'], strict_slashes=False)
#@jwt_required()
def ativarUsuario():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400
    try:
        id = data.get('id')
        if not id:
            raise ValidationError("É necessário fornecer o 'id' do usuário.")

        usuarioSelecionado = Usuario.procuraUsuarioPorId(id)
        if not usuarioSelecionado:
            return jsonify({"error": "Usuário não encontrado."}), 404

        usuarioSelecionado.ativarUsuario()

        return jsonify({"message": f"Usuário '{usuarioSelecionado.nome}' foi ativado com sucesso."}), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400 
    
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno no servidor.{e}"}), 500
    
