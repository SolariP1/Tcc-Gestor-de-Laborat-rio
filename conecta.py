import mysql.connector
from mysql.connector import Error

def conectar_ao_banco():
    """Conecta ao banco de dados MySQL e retorna a conexão e o cursor."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='testepython'
        )
        if conn.is_connected():
            print('Conexão bem-sucedida!')
            return conn, conn.cursor()
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

def fechar_conexao(conn, cursor):
    """Fecha a conexão e o cursor do banco de dados."""
    if cursor is not None:
        cursor.close()
    if conn is not None and conn.is_connected():
        conn.close()
        print('Conexão encerrada.')

def main():
    conn, cursor = conectar_ao_banco()
    if conn is not None and cursor is not None:
        try:
            nome = input('digite o nome : ')
            senha = input('digite a senha')
           
            sql = "INSERT INTO usuario (usu_usuario, usu_senha) VALUES (%s, %s)"
            val = (nome, senha)
            
            cursor.execute(sql,val)
            conn.commit()
            
            print('deu certo')
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
        finally:
            fechar_conexao(conn, cursor)

if __name__ == "__main__":
    main()