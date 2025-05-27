from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .condiciones import verificar_continuidad, verificar_existencia_raiz
from .graficas import graficar

def biseccion_DC(Xi, Xs, DC, Niter, Fun, request):
	continuidad = verificar_continuidad(Fun, Xi, Xs)
	raiz = verificar_existencia_raiz(Fun, Xi, Xs)

	if not continuidad:
		messages.error(request, "Bisección: La función no es continua en el intervalo.")
		return None, None
	
	if not raiz:
		messages.error(request, "Bisección: No se encontraron raíces con el método seleccionado. Verifique con la gráfica.")
		return None, None

	Tol = float(f'0.5E-{DC}')

	# Listas para guardar f(x) y errores en cada iteración
	fm=[]
	E=[]

	# Evalúa la función en los extremos del intervalo
	x=Xi
	fi=eval(Fun)
	x=Xs
	fs=eval(Fun)

	columnas = ["iter", "Xm", "f(Xm)", "E"]
	df = pd.DataFrame(columns=columnas)

	# Verifica si alguno de los extremos ya es una raíz exacta
	if fi==0:
		s=Xi
		E=0
		print(Xi, "es raiz de f(x)")
	elif fs==0:
		s=Xs
		E=0
		print(Xs, "es raiz de f(x)")
	elif fs*fi<0: # Existe una raíz entre Xi y Xs
		c=0 # Contador de iteraciones
		Xm=(Xi+Xs)/2 # Punto medio inicial
		x=Xm
		fe=eval(Fun) # f(Xm)
		fm.append(fe)
		E.append(100) # Primer error (grande)
		N = 1 # Numero de iter

		while E[c]>Tol and fe!=0 and c<Niter:
			if fi*fe<0: # La raíz está entre Xi y Xm
				Xs=Xm
				x=Xs
				fs=eval(Fun)
				if c == 0:
					Error = abs(Xi-Xs)
					df.loc[len(df)] = [N, Xm, fe, Error]
			else: # La raíz está entre Xm y Xs
				Xi=Xm
				x=Xi
				fs=eval(Fun)
				if c == 0:
					Error = abs(Xi-Xs)
					df.loc[len(df)] = [N, Xm, fe, Error]
			Xa=Xm # Guarda valor anterior
			Xm=(Xi+Xs)/2 # Nuevo punto medio
			x=Xm
			fe=eval(Fun) # f(Xm) nueva
			fm.append(fe)
			Error=abs(Xm-Xa) # Error absoluto
			E.append(Error)
			c=c+1
			N+=1

			df.loc[len(df)] = [N, Xm, fe, Error]
		
		# Condiciones de parada
		if fe==0: # Se encontró raíz exacta
				s=x
				messages.success(request, f"Bisección: {s} es raíz de f(x).")
		elif Error<Tol: # Se encontró una aproximación con tolerancia deseada
				s=x
				messages.success(request, f"Bisección: {s} es una aproximación de un raiz de f(x) con una tolerancia {Tol}.")
		else: # Fracaso por alcanzar el máximo de iteraciones
				s=x
				messages.error(request, f"Bisección: Fracasó en {Niter} iteraciones.")
	else:
		messages.error(request, "Bisección: El intervalo es inadecuado")

	x_solucion = df.iloc[-1, 1]
	grafico = graficar(Fun, x_solucion)
	return df, grafico

def biseccion_CS(Xi, Xs, CS, Niter, Fun, request):
	continuidad = verificar_continuidad(Fun, Xi, Xs)
	raiz = verificar_existencia_raiz(Fun, Xi, Xs)

	if not continuidad:
		messages.error(request, "Bisección: La función no es continua en el intervalo.")
		return None, None
	
	if not raiz:
		messages.error(request, "Bisección: No se encontraron raíces con el método seleccionado. Verifique con la gráfica.")
		return None, None

	Tol = float(f'5E-{CS}')
	
	# Listas para guardar f(x) y errores en cada iteración
	fm=[]
	E=[]

	# Evalúa la función en los extremos del intervalo
	x=Xi
	fi=eval(Fun)
	x=Xs
	fs=eval(Fun)

	columnas = ["iter", "Xm", "f(Xm)", "ℇ"]
	df = pd.DataFrame(columns=columnas)

	# Verifica si alguno de los extremos ya es una raíz exacta
	if fi==0:
		s=Xi
		E=0
		print(Xi, "es raiz de f(x)")
	elif fs==0:
		s=Xs
		E=0
		print(Xs, "es raiz de f(x)")
	elif fs*fi<0: # Existe una raíz entre Xi y Xs
		c=0 # Contador de iteraciones
		Xm=(Xi+Xs)/2 # Punto medio inicial
		x=Xm
		fe=eval(Fun) # f(Xm)
		fm.append(fe)
		E.append(100) # Primer error (grande)
		N = 1 # Numero de iter

		while E[c]>=Tol and fe!=0 and c<Niter:
			if fi*fe<0: # La raíz está entre Xi y Xm
				Xs=Xm
				x=Xs
				fs=eval(Fun)
				if c==0:
					Error = abs(Xi-Xs)/abs(Xm)
					df.loc[len(df)] = [N, Xm, fe, Error]
			else: # La raíz está entre Xm y Xs
				Xi=Xm
				x=Xi
				fs=eval(Fun)
				if c==0:
					Error = abs(Xi-Xs)/abs(Xm)
					df.loc[len(df)] = [N, Xm, fe, Error]
			Xa=Xm # Guarda valor anterior
			Xm=(Xi+Xs)/2 # Nuevo punto medio
			x=Xm
			fe=eval(Fun) # f(Xm) nueva
			fm.append(fe)
			Error=abs(Xm-Xa)/abs(Xm) # Error relativo
			E.append(Error)
			c=c+1
			N+=1

			df.loc[len(df)] = [N, Xm, fe, Error]

		# Condiciones de parada
		if fe==0: # Se encontró raíz exacta
				s=x
				messages.success(request, f"Bisección: {s} es raíz de f(x).")
		elif Error<Tol: # Se encontró una aproximación con tolerancia deseada
				s=x
				messages.success(request, f"Bisección: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
		else:  # Fracaso por alcanzar el máximo de iteraciones
				s=x
				messages.error(request, f"Bisección: Fracasó en {Niter} iteraciones.")
	else:
		messages.error(request, "Bisección: El intervalo es inadecuado")

	x_solucion = df.iloc[-1, 1]
	grafico = graficar(Fun, x_solucion)
	return df, grafico