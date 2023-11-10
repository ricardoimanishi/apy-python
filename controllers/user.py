# Esta classe User possui os seguintes métodos:
# create(username, password, status=None): Cria um novo usuário no banco de dados com o nome de usuário, senha e status (opcional) fornecidos. Retorna uma instância da classe User representando o novo usuário criado.
# get_by_id(user_id): Obtém um usuário pelo seu ID. Retorna uma instância da classe User correspondente ou None se o usuário não for encontrado.
# get_by_username(username): Obtém um usuário pelo nome de usuário. Retorna uma instância da classe User correspondente ou None se o usuário não for encontrado.
# update(): Atualiza as informações do usuário no banco de dados com base nos valores atualizados nos atributos da instância da classe User.
# delete(): Exclui o usuário do banco de dados.

from database import get_db_connection

class User:
    def __init__(self, id=None, username=None, password=None, status=None, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(username, password, status=None):
        """
        Cria um novo usuário no banco de dados com o nome de usuário, senha e status fornecidos.

        Args:
            username (str): O nome de usuário do usuário.
            password (str): A senha do usuário.
            status (str): O status do usuário (opcional).

        Returns:
            User: Uma instância da classe User representando o novo usuário criado.
        """
        if not status:
            status = 1
            
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO usuarios (username, password, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, status))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return User(id=user_id, username=username, password=password, status=status)

    @staticmethod
    def get_by_id(user_id):
        """
        Obtém um usuário pelo seu ID.

        Args:
            user_id (int): O ID do usuário a ser obtido.

        Returns:
            User or None: Uma instância da classe User correspondente ao ID fornecido, ou None se o usuário não for encontrado.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT id, username, password, status, created_at, updated_at FROM usuarios WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return User(*result)
        return None

    @staticmethod
    def get_by_username(username):
        """
        Obtém um usuário pelo nome de usuário.

        Args:
            username (str): O nome de usuário do usuário a ser obtido.

        Returns:
            User or None: Uma instância da classe User correspondente ao nome de usuário fornecido, ou None se o usuário não for encontrado.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT id, username, password, status, created_at, updated_at FROM usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return User(*result)
        return None

    def update(self):
        """
        Atualiza as informações do usuário no banco de dados com base nos valores atualizados nos atributos da instância da classe User.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE usuarios SET username = %s, password = %s, status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (self.username, self.password, self.status, self.id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        """
        Exclui o usuário do banco de dados.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query, (self.id,))
        connection.commit()
        cursor.close()
        connection.close()
