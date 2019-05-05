import sys
sys.stdout.write("importando bibliotecas")
import urllib2
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection
import time
import socket
sys.stdout.write("...OK\n")
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def corrigirpath(path):
	path = path.split("/")
	redo = False
	x = 0
	while x < len(path):
		if path[x] == "..":
			del path[x-1]
			del path[x-1]
			x = 0
		x += 1
		
	saida = ""
	for x in path:
		saida += x + "/"
	return saida
	
def shell(user,pas):
	print "setando variaveis"
	director = urllib2.build_opener(SMBHandler)
	ip = "192.168.10.9" #ip
	print "inicinado conexao"
	try:
		print "iniciando conexao smb na porta 445"
		conn = SMBConnection(user,pas,'name',ip,'',use_ntlm_v2=True,sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,is_direct_tcp=True) 
		conn.connect(ip,445)
	except:
		return
	Response = conn.listShares(timeout=30)  # obtain a list of shares
	print "pastas"
	for i in range(len(Response)):  #iterate through the list of shares
		if "$" not in Response[i].name:
			print " ("+str(i)+") " + Response[i].name
			
	try:
		try:
			antigocami = None
			atualcami = ""
			firt = True
			caminho = raw_input("pipe :")
			
			x = atualcami+Response[int(caminho)].name
			
			arquivos = conn.listPath(x,'/',timeout=5)
			
			for x in range(len(arquivos)):
			
				print "("+str(x)+") "+arquivos[x].filename
					
			share = Response[int(caminho)].name
			while True:
				caminho = raw_input("caminho :")
				if "D" == caminho[0]:
					try:
						arquivo = caminho[2:]
						x = arquivos[int(arquivo)].filename
						
						if "." in x:
							h =atualcami+arquivos[int(arquivo)].filename
							print share+"/"+h
							print "baixando arquivo "+x
							arq = open(arquivos[int(arquivo)].filename,"wb")
							h = corrigirpath(h)
							conn.retrieveFile(share, h, arq)
							print "salvando arquivo"
							arq.close()
							print "OK"
					except Exception as e:
						print "arqui :" +e
						
				elif "AD" == caminho:
					try:
						t = atualcami + "/"
						arquivos = conn.listPath(share,t,timeout=5)
						for x in range(2,len(arquivos)):
							try:
								t = arquivos[x].filename
								if "." in t:
									h =atualcami+t
									print share+"/"+h
									print "baixando arquivo "+t
									arq = open(arquivos[x].filename,"wb")
									h = corrigirpath(h)
									conn.retrieveFile(share, h, arq)
									print "salvando arquivo"
									arq.close()
									print "OK"
							except Exception as e:
								print "error :",e
					except Exception as e:
						print "aqui :",e
				else:
					try:
						t = atualcami+arquivos[int(caminho)].filename + "/"
						print t
						ARQ = arquivos
						arquivos = conn.listPath(share,t,timeout=5)
						for t in range(len(arquivos)):
							print "("+str(t)+") "+arquivos[t].filename
							
						atualcami += ARQ[int(caminho)].filename + "/"
						print atualcami
						antigocami = caminho
						print "D + numero (DOWLOAD DO ARQUIVO)"
						print "AD (DOWLOAD DE TODOS OS ARQUIVOS DA PASTA)"
					except Exception as e:
						for x in range(len(ARQ)):
							print "("+str(x)+") "+ARQ[x].filename
						#print e
						print "houve um erro"
		
		except:
			pass
	except:
		pass
		
	
def conectar(user,pas):
	sys.stdout.write("[!] Iniciando conexao com credenciais "+user+" ")
	director = urllib2.build_opener(SMBHandler)
	system_name = "192.168.10.9"
	try:
		conn = SMBConnection(user,pas,'name',system_name,'',use_ntlm_v2=True,sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,is_direct_tcp=True) 
		connected = conn.connect(system_name,445)
		Response = conn.listShares(timeout=30)
		sys.stdout.write("...OK")
		shell(user,pas)
	except Exception as e:
		sys.stdout.write("...FAIL\n")
		print e
conectar("user","1234")
