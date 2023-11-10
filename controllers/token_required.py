from flask import request, jsonify
from functools import wraps
from database import get_db_connection
import jwt

class TokenRequired:
    def __init__(self, app):
        self.app = app

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'Token de autenticação não fornecido'}), 401

            try:
                data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = data['username']

                # Verifica a ativação do usuário no banco de dados
                connection = get_db_connection()
                cursor = connection.cursor()
                query = "SELECT * FROM usuarios WHERE username = %s AND status = 1"
                cursor.execute(query, (current_user,))
                result = cursor.fetchone()
                cursor.close()
                connection.close()

                if not result:
                    return jsonify({'message': 'Usuário inativo'}), 401

            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expirado'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token inválido'}), 401

            return f(current_user, *args, **kwargs)

        return decorated
