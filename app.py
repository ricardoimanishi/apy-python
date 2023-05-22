from flask import Flask, request, jsonify
from database import get_db_connection
from functools import wraps
import jwt

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
    query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        # Credenciais válidas, gera um token JWT
        token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/api/protegido')
@token_required
def protegido(current_user):
    # Obtém a conexão com o banco de dados
    connection = get_db_connection()

    # Executa uma consulta no banco de dados
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios")

    # Obtém os resultados da consulta
    results = cursor.fetchall()

    # Processa os resultados, por exemplo, retornando-os como resposta JSON
    users = [{'id': row[0], 'username': row[1]} for row in results]
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
