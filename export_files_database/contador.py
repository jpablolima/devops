import mysql.connector

# Configuração do banco de dados
db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "ssl_disabled": True
}

try:
    # Conexão com o banco
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Substitua 'CLIENTE_ID' pelo ID do cliente
    cliente_id = 

    # Consulta para contar os arquivos do cliente
    count_query = f"""
    SELECT COUNT(*)
    FROM mantis_bug_file_table bf
    JOIN mantis_bug_table b ON bf.bug_id = b.id
    WHERE b.id IN (
        SELECT b.id
        FROM mantis_bug_table b
        JOIN mantis_project_table p ON b.project_id = p.id
        WHERE p.id IN (
            SELECT pht.child_id
            FROM mantis_project_hierarchy_table pht
            WHERE pht.parent_id = {cliente_id}
            UNION
            SELECT {cliente_id}
        )
    );
    """
    cursor.execute(count_query)

    # Obter o total de arquivos
    total_arquivos = cursor.fetchone()[0]
    print(f"Total de arquivos a serem exportados: {total_arquivos}")

    # Fechar conexão
    cursor.close()
    connection.close()

except mysql.connector.Error as err:
    print(f"Erro na conexão: {err}")
except Exception as e:
    print(f"Erro geral: {e}")
