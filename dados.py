# coding: utf-8
import mensagens

def tranfere_dados(ip, porta):
	''' Gerência a transferência de dados '''

	blocks = mensagens.blocks()
	cwdd = 0

	conexao_dados_cliente = mensagens.inicia_proxy_modo_servidor(str(ip), porta)

	# Cria uma conexão com o servidor.
	servidor = mensagens.inicia('192.168.0.133', 58791)

	# Como o cliente FTP escuta primeiro... Manda uma msg para o servidor, a msg que o servidor responder
    # Envia para o cliente.
	messenger = ''
	recebida = mensagens.envia_recebe_mensagem(messenger, servidor)

	# Envia saudação para o cliente.
	conexao_dados_cliente.send(recebida + '\n')

	# Recebe informações do cliente.
	men = ''
	while men != 'EXIT':
		men = conexao_dados_cliente.recv(1024)

		print '**************** Dentro da thread ***************************'
		print 'FileZilla: ' + men

		resposta = mensagens.envia_recebe_mensagem(men, servidor)

		if(men.find('CWD') != -1):
			for line in blocks:
				if(men.find(line) != -1):
					cwdd = 1

		if(cwdd == 1):
			conexao_dados_cliente.send('550 Diretório Bloqueado' + '\n')
			cwdd = 0
			continue

		#if men == 'PASV\r\n':
		#	print 'converter este' + str(resposta)
		#	modo_passivo = resposta
		#	ipp, portt = mensagens.parse(modo_passivo)
		#	dados = mensagens.inicia(ipp, portt)

		# Quando o Cliente passar o comando RETR, quer dizer que vai começar a tranferência de dados.
		#if men.find('RETR') != -1:
		#	print 'Aquiaasdsad->' + men
		#	title = formata_titulo(men)
		#	envia = mensagens.baixa_arquivo(servidor, conexao_dados_cliente, men, dados, title)
		#	conexao_dados_cliente.sendall(envia + '\n')

		conexao_dados_cliente.sendall(resposta + '\n')

		# Bloco abaixo controla o download do arquivo do servidor para o cliente.
		# O cache deve ser implementado abaixo.
		if(men.find('RETR') != -1):
			envia = mensagens.recebe_mensagem(servidor)
			conexao_dados_cliente.sendall(envia + '\n')

		# Bloco abaixo controla o upload do arquivo do cliente para o servidor.
		if(men.find('STOR') != -1):
			envia = mensagens.recebe_mensagem(servidor)
			conexao_dados_cliente.sendall(envia + '\n')

		if men == 'MLSD\r\n':
			enviaa = mensagens.recebe_mensagem(servidor)
			conexao_dados_cliente.sendall(enviaa + '\n')

	print 'Fim da Thread'
	conexao_dados_cliente.close()
	servidor.close()

	# Ao terminar a transferência dos arquivos, as conexões são encerradas, e por isso
	# deve-se iniciar uma nova thread.
	Thread(target=dados.tranfere_dados, args=(str(ip), porta)).start()


def manda(sk_cliente, sk_servidor):
	while 1:
		tmp = sk_servidor.recv(1024)
		if not tmp:
			break;
	sk_cliente.sendall(tmp)
	sk_cliente.sendall(mensagens.recebe_mensagem(sk_servidor) + '\n')

def recebe_arquivo(sk_cliente, sk_servidor, titulo):
	''' Recebe o arquivo do servidor, tenta fazer o cache e repassa para o servidor.
	    Tem como paramtros, socket com a conexão cliente-proxy e proxy-servidor '''
	    #fhandle = open("baixado.txt","wb")
	title = formata_titulo(titulo)
	fhandle = open(title, 'wb')

	while 1:
		tmp = sk_servidor.recv(1024)
		if not tmp:
			break;
		fhandle.write(tmp)
	fhandle.close()

	envia_arquivo(sk_cliente, title)

	return 1

def envia_arquivo(sk_cliente, title):
	''' Envia o arquivo para o cliente '''
	arq = open(title, 'rb')
	conteudo = arq.readlines()

	for linha in conteudo:
		sk_cliente.send(linha)

	return 1


def formata_titulo(st):
	''' Formata o título que vem: RETR titulo para titulo'''
	title = st[5:]
	print title
	return str(title)