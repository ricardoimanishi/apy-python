from flask import Flask, request, jsonify
import jwt
from controllers.authentication import Authentication
from controllers.token_required import TokenRequired
from controllers.user import User
from datetime import datetime

app = Flask(__name__)

data_atual = datetime.now()
chave = data_atual.strftime('%Y-%m-%d')

app.config['SECRET_KEY'] = chave

token_required = TokenRequired(app)

# Rota de exemplo
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/login', methods=['POST'])
def login():
    # Obtém o nome de usuário e senha do corpo da requisição
    username = request.json.get('username')
    password = request.json.get('password')
    # Chama o método para autenticar o usuário
    return Authentication.authenticate_user(username, password, app)

@app.route('/api/users_create', methods=['POST'])
@token_required
def create_user(current_user):
    try:
        # Obtém os dados do usuário do corpo da requisição
        username = request.json.get('username')
        password = request.json.get('password')
        status = request.json.get('status')

        # Verifica se o nome de usuário e senha estão presentes
        if not username or not password:
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios'}), 400

        # Cria um novo usuário chamando o método 'create' da classe 'User'
        user = User.create(username, password, status)

        # Prepara os dados do usuário para retornar como resposta JSON
        user_data = {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'status': user.status,
        }

        return jsonify(user_data), 201
    except Exception as e:
        return jsonify({'message': 'Erro ao criar usuário', 'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    try:
        # Cria uma instância da classe 'User'
        user = User()
        # Obtém os dados do usuário pelo ID
        user_data = user.get_by_id(user_id)

        if user_data:
            # Retorna os dados do usuário como resposta JSON
            return jsonify(user_data.__dict__)
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao obter usuário', 'error': str(e)}), 500

    
@app.route('/api/users/<string:user_name>', methods=['GET'])
@token_required
def get_by_username(current_user, user_name):
    try:
        # Instancia a classe User
        user = User()

        # Obtém o usuário pelo nome de usuário
        user_data = user.get_by_username(user_name)

        if user_data:
            # Retorna os dados do usuário como resposta JSON
            return jsonify(user_data.__dict__)
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404

    except Exception as e:
        return jsonify({'message': 'Erro ao obter usuário', 'error': str(e)}), 500

@app.route('/api/get_user_from_token', methods=['POST'])
@token_required
def get_user_from_token(current_user):
    token = request.json.get('token')
    secret_key = request.json.get('secret_key')
    
    try:
        # Decodifica o token usando a chave secreta
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
    # Executa a aplicação Flask
    app.run(host='0.0.0.0', port=8000, debug=True)
