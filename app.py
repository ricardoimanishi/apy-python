from flask import Flask, request, jsonify
from database import get_db_connection
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta111'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token de autenticação não fornecido'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']

            # Verifica a ativação do usuário no banco de dados
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s AND status = 1"
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


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

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


@app.route('/api/protegido')
@token_required
def protegido(current_user):
    # Obtém a conexão com o banco de dados
    connection = get_db_connection()

    # Executa uma consulta no banco de dados
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")

    # Obtém os resultados da consulta
    results = cursor.fetchall()

    # Processa os resultados, por exemplo, retornando-os como resposta JSON
    users = [{'id': row[0], 'username': row[1]} for row in results]
    return jsonify(users)

@app.route('/api/get_user_from_token', methods=['POST'])
@token_required
def get_user_from_token(current_user):
    token = request.json.get('token')
    secret_key = request.json.get('secret_key')
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get('id')
        username = payload.get('username')
        
        user_info = {
            'id': user_id,
            'username': username
        }
        
        return jsonify(user_info)
    except jwt.ExpiredSignatureError:
        # Token expirado
        return jsonify({'message': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        # Token inválido
        return jsonify({'message': 'Token inválido'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
