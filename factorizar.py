import math

def factorizar(n):
	factores = []
	if n > 1:
		for i in xrange(2, n + 1):
			while n % i == 0:
				n = n / i
				factores.append(i)
			if n == 1:
				break
	elif n == 1:
		factores.append(n)
	return factores
	
def divisores(factores):
	contadores = []
	auxiliar = factores[0]
	suma = 0
	for i in xrange(0, len(factores)):
		if factores[i] == auxiliar:
			suma += 1
		else:
			contadores.append((auxiliar, suma))
			auxiliar = factores[i]
			suma = 1
		if i == len(factores) - 1:
			contadores.append((auxiliar, suma))
	divisores = []
	if len(factores) > 1:
		divisores = [1]
		for i in xrange(0, len(contadores)):
			posicionultimo = len(divisores) - 1
			auxiliar = contadores[i]
			factor = auxiliar[0] # factor primo
			repeticiones = auxiliar[1] # potencias del factor primo de arriba
			for j in xrange(0, posicionultimo + 1):
				temporal = factor * divisores[j] # temporal es igual al factor por cada uno de los factores primos
				for k in xrange(1, repeticiones + 1):
					divisores.append(temporal)
					temporal = factor * temporal # temporal se multiplica con el factor, es decir, con las potencias del factor
	elif factores[0] == 1:
		divisores = [1]
	else:
		divisores = [1]
		divisores.append(factores[0])
	divisores.sort()
	return divisores
