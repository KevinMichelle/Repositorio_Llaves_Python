import math
import random

def sd(m):
	s = 1
	d = 0
	while True:
		d = int(m / math.pow(2, s))
		if d % 2 == 0: # Hay que evaluar si el numero que multiplica es par o impar
			s += 1
		else:
			break
	return (s, d)


def miller(n):
# Return true if n is probably prime, otherwise false
	probable = False
	if n > 3 and n % 2 != 0: # n debe ser mayor que 11 y ser impar
		m = n - 1
		s_d = sd(m) # Hay que expresar n - 1 como una potencia de 2 multiplicado por un numero impar: (2 ^ s) * d
		s = s_d[0]
		d = s_d[1]
		for i in xrange(1, 100):
			a = random.randrange(2, n)
			probable = False
			x = pow(a, d, n) # Si x = 1 o x = n - 1 pasar
			if s > 1 and (x != 1 or x != n - 1):
				for r in xrange(1, s): # de r = 1 hasta s - 1
					temporal = int(math.pow(2, r) * d) # temporal = (2 ^ r) * d
					x = pow(a, temporal, n) # x = (a ^ temporal) mod n
					# x = {a ^ [(2 ^ r) * d]} mod n
					if x == 1 or x == n - 1: # Si al menos uno es igual a esos, entonces es posible que sea primo, rompe el ciclo secundario
						probable = True
						break
			elif x == 1 or x == n - 1: # Si s es igual a 1 y x igual a esos valores entonces es primo, rompe el ciclo principal
				probable = True
				break
			if not probable: # Rompe el ciclo principal
				break
	if n == 1:
		probable = False
	elif n == 2 or n == 3:
		probable = True
	return probable
	
def generarprimo():
	contador = 0
	while True:
		candidato = random.randrange(1, 999999999)
		contador += 1
		if miller(candidato):
			auxiliar = (candidato - 1) / 2
			if miller(auxiliar):
				print auxiliar
				break
	return candidato
