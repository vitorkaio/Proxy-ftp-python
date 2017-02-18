# coding: utf-8

import socket
import dados
import mensagens
from threading import Thread

# ****************** Define o endereço do proxy e do servidor ******************
IP_PROXY = '192.168.0.133'
PORTA_PROXY = 5500

IP_SERVIDOR = '192.168.0.133'
PORTA_SERVIDOR = 58791

# ******************************************************************************

# ****************** Define uma lista com o nome dos diretórios bloquados ******************
bloqueados = mensagens.blocks()

# ****************************************************************************************** 

# Fica ouvindo na porta IP_PROXY o cliente(FileZilla)
con = mensagens.inicia_proxy_modo_servidor(IP_PROXY, PORTA_PROXY)

# Inicia uma conexão paralela através de uma thread.
Thread(target=dados.tranfere_dados, args=(IP_PROXY, PORTA_PROXY)).start()

# Cria uma conexão com o servidor FTP.
sock_servidor = mensagens.inicia(IP_SERVIDOR, PORTA_SERVIDOR)

# Como o cliente FTP escuta primeiro... Manda uma msg para o servidor, a msg que o servidor responder
# Envia para o cliente.
mensagem_recebida = ''
recebe = mensagens.envia_recebe_mensagem(mensagem_recebida, sock_servidor)

# Se esta variável mudar para 1, o diretório passado pelo cliente é inválido.
cwd_controle = 0

# Envia saudação para o cliente.
con.send(recebe + '\n')

while mensagem_recebida != 'EXIT':
    mensagem_recebida = con.recv(1024)

    print '**************** Fora da thread ***************************'
    print 'FileZilla: ' + mensagem_recebida

    # Envia a mensagem do cliente para o servidor, recebe a resposta do servidor(Conexão de controle)
    recebe = mensagens.envia_recebe_mensagem(mensagem_recebida, sock_servidor)

    # Veririca se o cliente tem permissão para acessar o diretório, se tiver, acessa
    # sem problemas, caso contrário retorna um código informando o erro.
    if(mensagem_recebida.find('CWD') != -1):
        # Percorre a lista de diretórios bloquados
        for linha in bloqueados:
            if(mensagem_recebida.find(linha) != -1):
                cwd_controle = 1

    # Verifica se o cliente tentou acessar um diretório bloquado.
    if(cwd_controle == 1):
        con.send('550 Diretório bloqueado' + '\n')
        cwd_controle = 0
        continue

    con.send(recebe + '\n')
    
    # Quando o cliente utilia o comando MSLD, ele espera duas resposta do servidor.
    if mensagem_recebida == 'MLSD\r\n':
        con.sendall(mensagens.recebe_mensagem(sock_servidor))
    

    #conmn = mensagens.inicia_proxy_modo_servidor('192.168.0.133', 6050)


s.close()
con.close()
sock_servidor.close()
