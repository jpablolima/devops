#!/bin/bash

# CABEÇALHO DO ARQUIVO DE SAIDA CHAMADO DE ping.csv
echo "hostname, ip, rtt, perda_de_pacotes, status" | tee ping.csv 

# NOME DO ARQUIVO DE ENTRADA ips.csv
filename="ips.csv"
{
    # faz a leitura linha a linha separado por "," pegando os valores servidor e ip
    read
    while IFS="," read -r servidor ip
    do 
        # imprime qual linha esta executando
        echo "${servidor}-${ip}"
        # imprime qual será o comando de ping e para qual ip
        echo "ping -c3 ${ip}"
        # guarda o resultado comando de ping
        dados=$(ping -c3 ${ip}) 

        # recorda do resultado, na linha que informa os pacotes perdidos qual foi a %
        packetloss=`echo $dados | grep "packet loss" | awk -F ',' '{print $3}' | awk '{print $1}'`
        # recorda do resultado, na linha que informa o RTT qual foi o tempo medio (sexto texto separado por "/")
        rrt=`echo $dados | grep "rtt" | cut -f 6 -d "/"`
        
        # TESTES DA QUANTIDADE DE PACOTES PERDIDOS
        # NÃO CONSEGUI USAR O COMANDO IF ENTÃO USEI O CASE
        # SITUACAO PADRÃO É CIRCUITO DEGRADADO
        situacao="ERRO"
        case $packetloss in
            '0%') 
                # CASO SEJA 0.0%
                situacao="Conectividade ok"
            ;;
            '100%')
                # CASO SEJA 100.0%
                situacao="Hostname inacessível"
            ;;
            *)
                # QUALQUER OUTRO VALOR
                situacao="Circuito degradado"
            ;;
        esac
        # IMPRIME O RESULTADO SEPARADO POR "," NO ARQUIVO DE SAIDA CHAMADO output.csv 
        # USANDO O COMANDO tee COM O ARGUMANTO -a PARA ANEXAR
        echo "${servidor},${ip},${rrt}ms,${packetloss},${situacao}" | tee -a ping.csv 
    done
} < $filename
# O COMANDO ACIMA É PARA DIZER QUE O ARQUIVO É A ENTRADA DO BLOCO