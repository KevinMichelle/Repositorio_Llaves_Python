from factorizar import factorizar
from gcd import gcd, egcd
import random, math

def RSA():
	nfn = generarN()
	n = nfn[0]
	fn = nfn[1]
	e = generarE(fn)
	efn = (e, fn)
	d = generarD(efn)
	clave = (e, d, n)
	return clave
	
def generarprimo():
	minimo = 17 #en esta implementacion de un generador de primo fuerte el primo mayor debe ser mayor que este numero
	while True:
		menor = 10000000
		mayor = 99999999
		primo = random.randrange(menor, mayor) #rango en el que debe estar los numeros primos a generar
		if esPrimo(primo):
			auxiliar = (primo - 1) / 2
			if esPrimo(auxiliar):
				a = factorizar(primo - 1)
				lga = a[len(a) - 1]
				b = factorizar(primo + 1)
				lgb = b[len(b) - 1]
				if lga > minimo and lgb > minimo:
					break
	return primo
	
def esPrimo(n):
	if n == 1:
		return False
	elif n == 2:
		return True
	elif n % 2 == 0:
		return False
	else:
		raiz = int(math.sqrt(n)) + 1
		for i in xrange(3, raiz):
			if n % i == 0:
				return False
		return True
	
	
def generarN():
	#generar n y fn, regresa una tupla de ambos
	p = generarprimo()
	q = 1
	gcd_bool = True
	while (p is not q) and gcd_bool:
		q = generarprimo()
		auxiliar = gcd(p - 1, q - 1)
		if auxiliar < 10:
			gcd_bool = False
	n = p * q
	fn = (p - 1) * (q - 1)
	nfn = (n, fn)
	return nfn
	
def generarE(fn):
	menor = 11
	mayor = 99999
	e = random.randrange(menor, mayor) #rango en el que quiero que este el valor de e
	while gcd(e, fn) != 1: #un do-while improvisado, parece que python no lo implementa por su cuenta
		e = random.randrange(menor, mayor)
	return e
	
def generarD(efn):
	e = efn[0]
	fn = efn[1]
	resultados_egcd = egcd(e, fn)
	d = resultados_egcd[2]
	while d <= 0:
		d = d + fn
	return d
