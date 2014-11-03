def preparar_mensaje(mensaje, abecedario):
	mensaje_lista = []
	for i in mensaje:
		if buscar_en_abecedario(i, abecedario):
			mensaje_lista.append(i)
		else:
			mensaje_lista.append(abecedario[len(abecedario)-1])
	return "".join(mensaje_lista)
	
def buscar_en_abecedario(letra, abecedario):
	for i in abecedario:
		if letra == i:
			return True
	return False

def transformar_mensaje(contenido, clave, clave_otro, cifrar):	
	e = clave[0]
	d = clave[1]
	n = clave[2]
	
	
	e_otro = clave_otro[0]
	n_otro= clave_otro[1]
	
	abecedario = "$%abcdefghijklmnopqrstuvwxyz.:;?"

	max = "{0:b}".format(len(abecedario) - 1) #binario de 32 - 1
	dummy = len(max) #la longitud de 31 en binario es de 5 bits 
	
	formato = "{0:0" + str(dummy) + "b}" #para representar las cadenas a tantos bits
	tam_bloque = 3
	
	if cifrar:
		mensaje_raw = contenido[0]
		temporal = mensaje_raw.lower()

		mensaje = preparar_mensaje(temporal, abecedario)
		bloques = mensaje_a_bloques(mensaje, tam_bloque, abecedario)
		cadenas = bloques_a_binarios(bloques, formato, abecedario)  #convertir los bloques de letra en cadenas
		numeros = binarios_a_numeros(cadenas) #convertir las cadenas a numeros
		numeros_firmados = encrip_des_bloque(numeros, d, n)
		numeros_cifrados = encrip_des_bloque(numeros_firmados, e_otro, n_otro)
		binarios_cifrados = numeros_a_binarios(numeros_cifrados, dummy, formato)
		bloques_cifrados = binarios_a_bloques(binarios_cifrados, dummy, abecedario)
		print
		print "CIFRAR"
		print
		print mensaje
		print bloques
		print cadenas
		print numeros
		print numeros_firmados
		print numeros_cifrados
		print binarios_cifrados
		print bloques_cifrados
		return bloques_cifrados
	else:
		bloques_cifrados = contenido
		cadenas = bloques_a_binarios(bloques_cifrados, formato, abecedario) 
		numeros = binarios_a_numeros(cadenas)
		descifrar_numeros = encrip_des_bloque(numeros, d, n)
		verificar_firmas = encrip_des_bloque(descifrar_numeros, e_otro, n_otro)
		binarios = numeros_a_binarios(verificar_firmas, dummy, formato)
		bloques = binarios_a_bloques(binarios, dummy, abecedario)
		recuperar_mensaje = bloques_a_mensaje(bloques)
		print
		print "DESCIFRAR"
		print
		print bloques_cifrados
		print cadenas
		print numeros
		print descifrar_numeros
		print verificar_firmas
		print binarios
		print bloques
		print recuperar_mensaje

		return recuperar_mensaje

def mensaje_a_bloques(mensaje, tam_bloque, abecedario):
	bloques = []
	for i in xrange(len(mensaje)):
		if i % tam_bloque == 0:
			bloque_peque = []
			bloque_peque.append(mensaje[i].lower())
		else:
			bloque_peque.append(mensaje[i].lower())
		if i % tam_bloque == (tam_bloque - 1) or i == (len(mensaje) - 1):
			bloques.append(bloque_peque)
	return bloques
	
def bloques_a_mensaje(bloques):
	mensaje_temporal = []
	for i in bloques:
		mensaje_temporal.append(i)
	mensaje = "".join(mensaje_temporal)
	return mensaje

	

def bloques_a_binarios(bloque, formato, abecedario):
	cadenas = []
	for i in bloque:
		cadenabinaria = []
		i = preparar_mensaje(i, abecedario)
		for j in i:
			cadenabinaria.append(formato.format(abecedario.index(j)))
		cadena_string = "".join(cadenabinaria)
		cadenas.append(cadena_string)
	return cadenas
	
def binarios_a_numeros(binario):
	numeros = []
	for i in binario:
		temporal = int(i, 2)
		numeros.append(temporal)
	return numeros
	
def numeros_a_binarios(numeros, dummy, formato):
	binarios = []
	for i in numeros:
		cadena_temporal =  "{0:0b}".format(i)
		if len(cadena_temporal) % dummy != 0:
			bits_dummy = ((len(cadena_temporal) / dummy) + 1) * dummy  # por ejemplo, 14 / 5 = 2.8 -> 3 -> 3 * 5 -> 15 bits en la cadena
			formato_temporal = "{0:0" + str(bits_dummy) + "b}"
			cadena_temporal = formato_temporal.format(i)
		binarios.append(cadena_temporal)
	return binarios
	
def binarios_a_bloques(binarios, dummy, abecedario):
	bloques = []
	for i in binarios:
		contador = 1
		bloque_palabra = []
		bloque_letra = []
		for j in xrange(len(i)):
			bloque_letra.append(i[j])
			if contador % dummy == 0:
				cadena_string = "".join(bloque_letra)
				numero_temporal = int(cadena_string, 2)
				bloque_palabra.append(abecedario[numero_temporal])
				bloque_letra = []
			contador += 1
		bloques.append("".join(bloque_palabra))
	return bloques
	
def encrip_des_bloque(numeros, clave, n):
	numeros_encrip_des = []
	for i in numeros:
		if i == -1:
			numeros_encrip_des.append(-1)
		else:
			numeros_encrip_des.append(pow(i, clave, n))
	return numeros_encrip_des

def cifrar(mensaje, clave, clave_otro):
	mensaje_lista = mensaje.split()
	mensaje_cifrado = []
	for i in mensaje_lista:
		texto_cifrado = transformar_mensaje([i], clave, clave_otro, True)
		mensaje_cifrado.append(texto_cifrado)
	return mensaje_cifrado

def descifrar(mensaje_cifrado, clave, clave_otro):
	mensaje_recuperado = []
	for i in mensaje_cifrado:
		elemento = i[0].split()
		texto_recuperado = transformar_mensaje(elemento, clave, clave_otro, False)
		mensaje_recuperado.append(texto_recuperado)
	return mensaje_recuperado
