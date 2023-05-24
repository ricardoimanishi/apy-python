from flask import jsonify
from database import get_db_connection
import jwt
from datetime import datetime, timedelta

class Authentication:
    @staticmethod
    def authenticate_user(username, password, app):

        # Obtém a conexão com o banco de dados
        connection = get_db_connection()

        # Executa uma consulta para verificar as credenciais do usuário
        cursor = connection.cursor()
        query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            username = result[1]
            
            # Credenciais válidas, gera um token JWT, válido indefinidamente
            token = jwt.encode({'id': user_id, 'username': username}, app.config['SECRET_KEY'], algorithm='HS256')

            # Credenciais válidas, gera um token JWT com validade de 1 hora
            # expiration_time = datetime.utcnow() + timedelta(hours=1)
            # token = jwt.encode({'id': user_id, 'username': username, 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token})

        return jsonify({'message': 'Credenciais inválidas'}), 401
