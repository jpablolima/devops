import mysql.connector
import os
import time  

db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "ssl_disabled": True
}

try:
    # Registrar o tempo de início
    start_time = time.time()

    # Conexão com o banco
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Substitua 'CLIENTE_ID' pelo ID ou outra identificação do cliente específico
    cliente_id =   # Exemplo de cliente específico

    # Consulta SQL para contar o total de arquivos
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
    total_arquivos = cursor.fetchone()[0]  # Obter o total de arquivos
    print(f"Total de arquivos a exportar: {total_arquivos}")

   
    batch_size = 500
    arquivos_exportados = 0

  
    while arquivos_exportados < total_arquivos:
       
        fetch_query = f"""
        SELECT 
            b.id AS bug_id,
            bf.filename AS nome_arquivo,
            bf.content AS conteudo_arquivo
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
        )
        LIMIT {batch_size} OFFSET {arquivos_exportados};
        """
        cursor.execute(fetch_query)

      
        output_dir = f"arquivos_cliente_{cliente_id}"
        os.makedirs(output_dir, exist_ok=True)

       
        for bug_id, nome_arquivo, conteudo_arquivo in cursor.fetchall():
            # Caminho completo do arquivo
            file_path = os.path.join(output_dir, nome_arquivo)

        
            try:
                with open(file_path, "wb") as file:
                    file.write(conteudo_arquivo)

                # Incrementar o contador e calcular a porcentagem
                arquivos_exportados += 1
                porcentagem = (arquivos_exportados / total_arquivos) * 100

                
                print(f"Exportando arquivo {arquivos_exportados}/{total_arquivos} ({porcentagem:.2f}%) - {nome_arquivo}")

            except Exception as e:
                print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

 
    cursor.close()
    connection.close()

    # Registrar o tempo de término
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Todos os arquivos do cliente {cliente_id} foram processados com sucesso!")
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

except mysql.connector.Error as err:
    print(f"Erro na conexão: {err}")
except Exception as e:
    print(f"Erro geral: {e}")
