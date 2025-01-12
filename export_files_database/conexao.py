import mysql.connector
import ssl

db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "ssl_disabled": "True"
}

try:
    connection = mysql.connector.connect(**db_config)
    print("Conexão bem-sucedida!")
    connection.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar: {err}")
