from flask import Blueprint, request, jsonify
from app.models.usuarios import Usuario, ValidationError
from app.auth.jwt_middleware import token_required

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")

@bp.route('', methods=['POST'], strict_slashes=False)
async def criarUsuarioPage(current_user):
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
@token_required
def listarUsuariosPage(current_user):
    """
    Retorna uma lista de usuários 
    """
    try:
        usuarios = Usuario.listaUsuarios()
        return jsonify(usuarios), 200
    except Exception as err:
        return jsonify(err.to_dict()),err.to_dict().get("status_code")
    
@bp.route('/inativar', methods=['POST'], strict_slashes=False)
@token_required
def inativarUsuarioPage(current_user):
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
@token_required
def ativarUsuarioPage(current_user):
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
    
@bp.route('/login', methods=['POST'], strict_slashes=False) 
def autenticarUsuario(): 
    data = request.get_json() 
    if not data: 
        return jsonify({"error": "Corpo da requisição não pode ser vazio."}), 400 
 
    senha = data.get('senha') 
    email = data.get('email') 
    if not email or not senha: 
        raise ValidationError("É necessário fornecer o 'email' e 'senha'.") 
    usuarioSelecionado = Usuario.verificaEmail(email) 
    
    if not usuarioSelecionado.verificaSenha(senha):
        return jsonify({"error": "Senha incorreta"}), 401

    token, expiracao = usuarioSelecionado.gerarToken()
    return jsonify({
        "token": token,
        "expiracao": expiracao
    }), 200