def gcd(a, b):
	auxiliar = (a, b)
	a = max(auxiliar)
	b = min(auxiliar)
	while a % b != 0:
		c = a % b
		a = b
		b = c
	resultado = b
	return resultado
	
def egcd(a, b):
	auxiliar = (a, b)
	a = max(auxiliar)
	b = min(auxiliar)
	x = (1, 0)
	y = (0, 1)
	while a % b != 0:
		q = a / b
		c = a % b
		nx = x[0] - (x[1] * q)
		ny = y[0] - (y[1] * q)
		x = (x[1], nx)
		y = (y[1], ny)
		a = b
		b = c
	resultado = (b, x[1], y[1])
	return resultado
