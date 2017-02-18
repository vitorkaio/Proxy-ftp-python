# coding: utf-8
import socket
import time
import dados

def blocks():
    ''' Retorna uma lista com os diretórios bloquados '''
    bloqueados = ['Downloads', 'Yosemite']
    return bloqueados

def inicia_proxy_modo_servidor(ip, porta):
    ''' Conecta o proxy ao cliente'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, porta))
    s.listen(2)
    
    print('Aguardando conexão...\n')
    con, info_cli = s.accept()
    print('Conexão Estabelecida')
    
    return con

def inicia(ip, porta):
    ''' Conecta o proxy ao servidor '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((ip, porta))
    return s


def envia_mensagem(mensagem, s):
    ''' Apenas envia uma mensagem para o servidor '''
    s.send(mensagem + '\n')

def recebe_mensagem(sock):
    '''  Apenas Recebe uma mensagem do servidor. '''
    mensagem = sock.recv(1024)
    print 'Resposta do servidor ' + mensagem
    return mensagem

def envia_recebe_mensagem(mensagem, s):
    ''' Envia uma mensagem para o servidor e retorna a resposta'''
    s.send(mensagem)
    cmd = s.recv(1024)
    print 'Resposta do servidor ' + cmd
    return cmd

def parse(st):
    ''' Configura uma string '''
    x = st[st.rindex("(")+1:st.rindex(")")]
    y = x.split(",")
    ipaddr=y[0]+"."+y[1]+"."+y[2]+"."+y[3]
    portnum=(int(y[4])*256)+int(y[5])

    return ipaddr,portnum

def baixa_arquivo(s, s_cliente, cmd, dados, title):
    ''' Baixa um arquivo do servidor FTP para o proxy '''

    print 'Ola adasdasdsd -> ' + title
    sed = envia_recebe_mensagem(cmd, s)
    print '********** Recebeu do servidor: ' + sed

    arq = open(title, 'wb')

    while 1:
        tmp = dados.recv(1024)
        if not tmp:
            break;
        arq.write(tmp)

    arq.close()
    recebe = recebe_mensagem(s)
    dados.close()
    time.sleep(1) #this delay is required
    s_cliente.sendall(sed + '\n')
    s_cliente.sendall(recebe + '\n')
    return 1

def envia_arquivo(s):
    ''' Cria uma conexão para tranferir dados com o cliente e o envia '''

    arq = open('baixado.txt', 'rb')
    data = arq.readlines()

    for line in data:
        s.send(line)