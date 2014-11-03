import socket
from manipular_archivos_rsa import buscar_usuario, crear_usuario, actualizar_usuario
import random

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5)

e = 33905 
d = 85470676418957 #si, es mala idea, pero se acaba el tiempo
n = 811050542095813


while True:
	print "Esperando..."
	socket_servidor, address = serversocket.accept()
	cadena_temporal = socket_servidor.recv(100)
	cadena = cadena_temporal.split()
	consulta_servidor = True #datos del servidor

	if cadena[0] == "buscar_usuario":
		print "Buscar usuario"
		correo = cadena[1]
		temporal = [correo, None]
		datos_usuario_servidor = buscar_usuario(temporal, consulta_servidor)
		if datos_usuario_servidor is not None:
			datos = " ".join(datos_usuario_servidor) #datos del usuario, string
			socket_servidor.send(datos)
		else:
			socket_servidor.send("NULL")
	elif cadena[0] == "nuevo_correo":
		if cadena[2].isdigit() and cadena[3].isdigit():	#por si... acaso
			print "Crear o actualizar usuario"
			lista_de_datos = [cadena[1], cadena[2], cadena[3]]
			temporal = [lista_de_datos[0], None]
			datos_usuario_servidor = buscar_usuario(temporal, consulta_servidor) #buscar usuario en el archivo del servidor
			if datos_usuario_servidor == None: #si no existe, crear
					crear_usuario(lista_de_datos, consulta_servidor)
			else:								#si existe, actualizar
					actualizar_usuario(lista_de_datos, consulta_servidor)
	elif cadena[0] == "desafiar_servidor":
		correo = cadena[1]
		temporal = [correo, None]
		datos_usuario_servidor = buscar_usuario(temporal, consulta_servidor)
		if datos_usuario_servidor is not None:
			e_cliente = int(datos_usuario_servidor[1])
			n_cliente = int(datos_usuario_servidor[2])
			reto = int(cadena[2])
			responder_reto = reto * 2
			respuesta_al_cliente = pow(responder_reto, d, n)
			cifrar_respuesta = pow(respuesta_al_cliente, e_cliente, n_cliente)
			mensaje = str(cifrar_respuesta) + " " + str(e) + " " + str(n)
			socket_servidor.send(mensaje)
			
			#desafiar al cliente
			reto = random.randrange(100, 2000)
			respuesta_esperada = reto * 2
			socket_servidor, address = serversocket.accept()
			socket_servidor.send(str(reto))
			socket_servidor, address = serversocket.accept()
			respuesta_firmada_usuario = int(socket_servidor.recv(100))
			descifrar_usuario = pow(respuesta_firmada_usuario, d, n)
			quitar_firma = pow(descifrar_usuario, e_cliente, n_cliente)
			if respuesta_esperada == quitar_firma:
				print "El usuario es quien dice que es"
				socket_servidor.send("True")
			else:
				print "El usuario no es quien dice que es"
				socket_servidor.send("False")
		else:
			socket_servidor.send("NULL")
