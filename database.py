import mysql.connector

# Configurações do banco de dados
db_host = 'ura.clxkj5rsplq0.sa-east-1.rds.amazonaws.com'
db_user = 'ura_orthodontic'
db_password = 'iyy@4587GHS!sbh3'
db_name = 'api-python'

# Função para obter a conexão com o banco de dados
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection