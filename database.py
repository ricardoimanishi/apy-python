import mysql.connector

# Configurações do banco de dados
db_host = 'medicalshare.cp4hccu4to1h.us-east-1.rds.amazonaws.com'
db_user = 'medical_prd'
db_password = 'hA2zuyywQXNx9kz'
db_name = 'clientes-auth'

# Função para obter a conexão com o banco de dados
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection