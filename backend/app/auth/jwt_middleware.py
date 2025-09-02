from functools import wraps
from flask import request, jsonify
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.models.usuarios import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token ausente"}), 401

        try:
            token = token.replace("Bearer ", "")
            # decodifica o token; verifica expiração por padrão
            data = jwt.decode(token, "KEY", algorithms=["HS256"])
            current_user = Usuario.query.get(data["user_id"])
            if not current_user:
                return jsonify({"error": "Usuário não encontrado"}), 404
        except ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        except Exception:
            return jsonify({"error": "Erro ao processar o token"}), 500

        return f(current_user, *args, **kwargs)

    return decorated