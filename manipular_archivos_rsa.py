import os.path


# datos = [correo, e, n] -> servidor
# datos = [correo, e, n, correo_cliente] -> cliente
def crear_usuario(datos, es_servidor):
	print "Crear usuario"
	if es_servidor:
		correo = datos[0]
		filename = "../archivos/sakura/usuarios.dat"
	else:
		correo_cliente = datos[3]
		del datos[-1] #remover el correo del usuario local
		filename = "../archivos/" + correo_cliente + "_usuarios.usuarios"
		correo = datos[0]
	cadena_datos = " ".join(datos) + "\n" #NOTA: buscar una mejor forma de poner el salto de linea
	archivo = open(filename, 'a')
	archivo.write(cadena_datos)
	archivo.close()

# correo_temporal = [correo, None] -> servidor
# correo_temporal = [correo, correo_cliente] -> cliente
def buscar_usuario(correo_temporal, es_servidor):
	if es_servidor:
		correo = correo_temporal[0]
		filename = "../archivos/sakura/usuarios.dat"
	else:
		correo = correo_temporal[0]
		filename = "../archivos/" + correo_temporal[1] + "_usuarios.usuarios"

	if os.path.isfile(filename):
		archivo = open(filename, "r")
		lista_usuarios = []
		for linea in archivo:
			lista_usuarios.append(linea)
		archivo.close()
		for elemento in lista_usuarios:
			array_temporal = elemento.split()
			if len(array_temporal) == 3 and correo == array_temporal[0] and array_temporal[1].isdigit() and array_temporal[2].isdigit(): 
				return array_temporal
	return None
	
# datos = [correo, e, n] -> servidor
# datos = [correo, e, n, correo_cliente] -> cliente
def actualizar_usuario(datos, es_servidor):
	print "Actualizar usuario"
	if es_servidor:
		correo = datos[0]
		filename = "../archivos/sakura/usuarios.dat"
	else:
		correo_cliente = datos[3]
		del datos[-1] #remover el correo del cliente
		correo = datos[0]
		filename = "../archivos/" + correo_cliente + "_usuarios.usuarios"
	cadena_datos = " ".join(datos) + "\n"
	if os.path.isfile(filename): #---> el archivo del servidor si existe
		archivo = open(filename, 'r')
		lista_usuarios_temporal = archivo.readlines()
		nueva_lista = []
		for elemento in lista_usuarios_temporal:
			auxiliar = elemento.split()
			if correo == auxiliar[0]:
				nueva_lista.append(cadena_datos)
			else:
				nueva_lista.append(elemento)
		archivo.close()
		archivo = open(filename, 'w')
		archivo.writelines(nueva_lista)
		archivo.close()
	else: #---> el archivo del servidor no existe
		archivo = open(filename, 'a')
		archivo.write(datos)
		archivo.close()
