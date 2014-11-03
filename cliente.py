from rsa import RSA
import codecs
import sys
import os.path
import socket
from manipular_archivos_rsa import buscar_usuario, crear_usuario, actualizar_usuario
import transformar
import random

def desafiar_servidor(correo):
	clave_personal = recuperar_clave_personal(correo)
	if clave_personal is None:
		clave_personal = recuperar_clave_personal(correo)
	e = int(clave_personal[1])
	d = int(clave_personal[2])
	n = int(clave_personal[3])
	repetir = True
	respuesta = False
	while repetir:
		reto = random.randrange(100, 2000)
		respuesta_esperada = reto * 2
		cadena_socket = "desafiar_servidor " + correo + " " + str(reto)
		mensaje_servidor = conectar_socket(cadena_socket, True) #False indica que no se espera respuesta del servidor
		mensaje_servidor_lista = mensaje_servidor.split()
		respuesta_servidor = int(mensaje_servidor_lista[0])
		e_servidor = int(mensaje_servidor_lista[1])
		n_servidor = int(mensaje_servidor_lista[2])
		descifrar_respuesta = pow(respuesta_servidor, d, n)
		cancelar_firma = pow(descifrar_respuesta, e_servidor, n_servidor)
		if respuesta_esperada == cancelar_firma:
			reto_servidor = esperar_respuesta()
			reto = int(reto_servidor)
			responder_reto = reto * 2
			respuesta_al_servidor = pow(responder_reto, d, n)
			if respuesta_al_servidor > n_servidor:
				repetir = True
			else:
				repetir = False
			cifrar_respuesta = pow(respuesta_al_servidor, e_servidor, n_servidor)
			cadena_socket = str(cifrar_respuesta)
			respuesta = conectar_socket(cadena_socket, True)
			if respuesta == "True":
				respuesta = True
			else:
				respuesta = False
		else:
			print "El servidor no es quien dice que es"
			exit()
	if respuesta:
		print "El servidor es quien dice que es"
		print "El servidor confirma que soy yo"
	else:
		print "Fallo la autenticacion"

def existe_archivo(correo, mostrar_info):
	filename = "../archivos/" + correo + '.dat'
	existe_archivo_usuario = os.path.isfile(filename)
	longitud_datos = True
	son_numeros = True
	existe = False
	if existe_archivo_usuario:
		archivo = open(filename)
		auxiliar_datos = archivo.readline()
		datos = auxiliar_datos.split()
		archivo.close()
		if len(datos) == 4: #correo, e, d, n
			if datos[1].isdigit() and datos[2].isdigit() and datos[3].isdigit(): #e, d y n son numeros
				if datos[0] == correo: #el correo si coincide
					existe = True
			else:
				verificar_numeros = False
		else:
			longitud_datos = False
	if mostrar_info:
		if not existe_archivo_usuario or not existe or not longitud_datos or not son_numeros: #solo es verdadero si todos son lo son
			print 'Crear nuevo archivo de usuario, porque:'
			if not existe_archivo_usuario:
				print '\t-No existe tu archivo personal.'
			elif not existe:
				print '\t-Tu correo no coincide con el del archivo personal, quizas alguien lo modifico.'
			elif not longitud_datos or not son_numeros:
				print '\t-Es probable que se perdieron o se corrompieron'
			print
	else:
		print "No existe datos del usuario " + correo + ", por favor registrese de nuevo"
	return existe
	
def nueva_clave(correo):
	clave = RSA()
	filename = "../archivos/" + correo + ".dat"
	archivo_usuario = codecs.open(filename, 'w', 'utf-8')
	cadena = correo + ' ' + str(clave[0]) + ' ' + str(clave[1]) + ' ' + str(clave[2]) + '\n'
	archivo_usuario.write(cadena)
	archivo_usuario.close()
	
	#Mandar nueva clave al servidor
	cadena_socket = "nuevo_correo " + correo + " " + str(clave[0]) + " " + str(clave[2])
	conectar_socket(cadena_socket, False) #False indica que no se espera respuesta del servidor

	
def recuperar_clave_personal(correo):
	filename = "../archivos/" + correo + '.dat'
	if os.path.isfile(filename):
		archivo = open(filename)
		auxiliar_datos = archivo.readline()
		datos = auxiliar_datos.split()
		archivo.close()
		return datos
	else:
		print "No existe archivo de usuario, crear llaves"
		nueva_clave(correo)

def solicitar_datos(correo, correo_destinatario, guardar):
	desafiar_servidor(correo)
	correo_temporal = [correo_destinatario, correo]
	resultados = buscar_usuario(correo_temporal, False)
	if resultados is not None: #Busqueda en archivo local
		resultados.append(correo)
		if guardar: #Si se encontro datos en el archivo local, pero se desea actualizar, hay que consultar de nuevo al servidor
			nuevos_resultados = busqueda_servidor(correo, correo_destinatario)
			if nuevos_resultados is not None:
				son_iguales = comparar_datos(resultados, nuevos_resultados)
				if not son_iguales:
					actualizar_usuario(nuevos_resultados, False)
					return nuevos_resultados
				else:
					del resultados[-1]
			else:
				print "No se encontro datos en el servidor, trabajar con esos datos con cierto riesgo"
		else:
			del resultados[-1]
	else: #Busqueda en archivo del servidor
		resultados = busqueda_servidor(correo, correo_destinatario)
		if resultados is not None:
			if guardar:
				crear_usuario(resultados, False)
			else:
				del resultados[-1]
		else:
			print "No se encontro datos en el servidor"
	return resultados

def busqueda_servidor(correo, correo_destinatario):
	cadena = "buscar_usuario " + correo_destinatario
	resultados_cadena = conectar_socket(cadena, True)
	if resultados_cadena != "NULL":
		resultados = resultados_cadena.split()
		resultados.append(correo)
		return resultados
	else:
		return None

def comparar_datos(datos_local, datos_servidor):
	if len(datos_local) == len(datos_servidor):
		for i in xrange(len(datos_local)):
			if datos_local[i] != datos_servidor[i]:
				return False
	return True

def abrir_archivo(nombre_archivo, datos_solicitados):
	clave_personal = recuperar_clave_personal(correo) #IMPORTANTE
	clave = [int(clave_personal[1]), int(clave_personal[2]), int(clave_personal[3])]
	clave_del_otro = [int(datos_solicitados[1]), int(datos_solicitados[2])]
	max = len(nombre_archivo)
	min = max - 4
	if nombre_archivo[min:max] == ".txt":
		archivo = open(nombre_archivo, 'r')
		mensaje = archivo.read()
		archivo.close()
		mensaje_cifrado = transformar.cifrar(mensaje, clave, clave_del_otro)
		texto_cifrado = []
		for i in mensaje_cifrado:
			texto_cifrado.append(" ".join(i) + "\n")
		archivo = open("texto_cifrado.txx", 'w')
		archivo.writelines(texto_cifrado)
		archivo.close()
	elif nombre_archivo[min:max] == ".txx":
		archivo = open(nombre_archivo, 'r')
		bloques_cifrados = archivo.read().splitlines()
		for i in xrange(len(bloques_cifrados)):
			bloques_cifrados[i] = [bloques_cifrados[i]]
		mensaje_recuperado = transformar.descifrar(bloques_cifrados, clave, clave_del_otro)
		print " ".join(mensaje_recuperado)
		archivo.close()
		#mensaje_descifrado = transformar.descifrar()
	
def verificar_usuario(correo):
	existe_archivo(correo, True)
	nueva_clave(correo)

def conectar_socket(cadena, servidor_contesta):
	socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_cliente.connect(('localhost', 8089))
	socket_cliente.send(cadena) #enviar cadena
	string = ""
	if servidor_contesta:
		string = socket_cliente.recv(100) #recibir
		return string
	return "NULL"

def esperar_respuesta():
	socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_cliente.connect(('localhost', 8089))
	string = socket_cliente.recv(100) 
	return string
	
def ayuda():
	print "python cliente.py -help -> Ayuda"
	print "python cliente.py 'correo' -nrsa -> Crear o actualizar llaves RSA para 'correo'"
	print "python cliente.py 'correo' 'archivo' 'destinatario'-> Crear 'archivo cifrado' para el correo 'destinatario'" 
	print "python cliente.py 'correo' 'archivo' 'destinatario' -save -> Crear 'archivo cifrado' para el correo 'destinatario', guardar 'destinatario' en el disco duro"
	
if len(sys.argv) == 2 and sys.argv[1] == "-help":
	print "-help"
	ayuda()
elif len(sys.argv) >= 3:
	if len(sys.argv) == 3 and sys.argv[2] == "-nrsa":
		print "-nrsa"
		verificar_usuario(sys.argv[1])
	elif len(sys.argv) == 4 or len(sys.argv) == 5:
		correo = sys.argv[1]
		nombre_archivo = sys.argv[2]
		correo_destinatario = sys.argv[3]
		if correo != correo_destinatario:
			guardar = False
			if len(sys.argv) == 5 and sys.argv[4] == "-save":
				guardar = True
			datos_solicitados = solicitar_datos(correo, correo_destinatario, guardar)
			if datos_solicitados is not None:
				abrir_archivo(nombre_archivo, datos_solicitados)
			else:
				print "No existe ese usuario"
		else:
			print "El correo del usuario y del destinatario es el mismo"
	else:
		print "Escribe python cliente.py -help para mas ayuda"
