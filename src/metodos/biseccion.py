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
		messages.error(request, "Bisección: La función no tiene raíces en el intervalo.")
		return None, None

	Tol = float(f'0.5E-{DC}')
	fm=[]
	E=[]
	x=Xi
	fi=eval(Fun)
	x=Xs
	fs=eval(Fun)

	columnas = ["iter", "Xm", "f(Xm)", "E"]
	df = pd.DataFrame(columns=columnas)

	if fi==0:
		s=Xi
		E=0
		print(Xi, "es raiz de f(x)")
	elif fs==0:
		s=Xs
		E=0
		print(Xs, "es raiz de f(x)")
	elif fs*fi<0:
		c=0
		Xm=(Xi+Xs)/2
		x=Xm
		fe=eval(Fun)
		fm.append(fe)
		E.append(100)
		N = 1

		while E[c]>Tol and fe!=0 and c<Niter:
			if fi*fe<0:
				Xs=Xm
				x=Xs
				fs=eval(Fun)
				if c == 0:
					Error = abs(Xi-Xs)
					df.loc[len(df)] = [N, Xm, fe, Error]
			else:
				Xi=Xm
				x=Xi
				fs=eval(Fun)
				if c == 0:
					Error = abs(Xi-Xs)
					df.loc[len(df)] = [N, Xm, fe, Error]
			Xa=Xm
			Xm=(Xi+Xs)/2
			x=Xm
			fe=eval(Fun)
			fm.append(fe)
			Error=abs(Xm-Xa)
			E.append(Error)
			c=c+1
			N+=1

			df.loc[len(df)] = [N, Xm, fe, Error]
		if fe==0:
				s=x
				messages.success(request, f"Bisección: {s} es raiz de f(x).")
		elif Error<Tol:
				s=x
				messages.success(request, f"Bisección: {s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
		else:
				s=x
				messages.error(request, f"Bisección: Fracaso en {Niter} iteraciones.")
	else:
		messages.error(request, "Bisección: El intervalo es inadecuado")

	messages.success(request, "Bisección: Se ejecuto el método de la bisección correctamente")

	x_solucion = df.iloc[-1, 1]
	df = df.to_html(classes='table table-striped', index=False)
	grafico = graficar(Fun, x_solucion)
	return df, grafico

def biseccion_CS(Xi, Xs, CS, Niter, Fun, request):
	continuidad = verificar_continuidad(Fun, Xi, Xs)
	raiz = verificar_existencia_raiz(Fun, Xi, Xs)

	if not continuidad:
		messages.error(request, "Bisección: La función no es continua en el intervalo.")
		return None, None
	
	if not raiz:
		messages.error(request, "Bisección: La función no tiene raíces en el intervalo.")
		return None, None

	Tol = float(f'5E-{CS}')
	fm=[]
	E=[]
	x=Xi
	fi=eval(Fun)
	x=Xs
	fs=eval(Fun)

	columnas = ["iter", "Xm", "f(Xm)", "ℇ"]
	df = pd.DataFrame(columns=columnas)

	if fi==0:
		s=Xi
		E=0
		print(Xi, "es raiz de f(x)")
	elif fs==0:
		s=Xs
		E=0
		print(Xs, "es raiz de f(x)")
	elif fs*fi<0:
		c=0
		Xm=(Xi+Xs)/2
		x=Xm
		fe=eval(Fun)
		fm.append(fe)
		E.append(100)
		N = 1

		while E[c]>=Tol and fe!=0 and c<Niter:
			if fi*fe<0:
				Xs=Xm
				x=Xs
				fs=eval(Fun)
				if c==0:
					Error = abs(Xi-Xs)/abs(Xm)
					df.loc[len(df)] = [N, Xm, fe, Error]
			else:
				Xi=Xm
				x=Xi
				fs=eval(Fun)
				if c==0:
					Error = abs(Xi-Xs)/abs(Xm)
					df.loc[len(df)] = [N, Xm, fe, Error]
			Xa=Xm
			Xm=(Xi+Xs)/2
			x=Xm
			fe=eval(Fun)
			fm.append(fe)
			Error=abs(Xm-Xa)/abs(Xm)
			E.append(Error)
			c=c+1
			N+=1

			df.loc[len(df)] = [N, Xm, fe, Error]
		if fe==0:
				s=x
				messages.success(request, f"Bisección: {s} es raiz de f(x).")
		elif Error<Tol:
				s=x
				messages.success(request, f"Bisección: {s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
		else:
				s=x
				messages.error(request, f"Bisección: Fracaso en {Niter} iteraciones.")
	else:
		messages.error(request, "Bisección: El intervalo es inadecuado")

	messages.success(request, "Bisección: Se ejecuto el método de la bisección correctamente")

	x_solucion = df.iloc[-1, 1]
	df = df.to_html(classes='table table-striped', index=False)
	grafico = graficar(Fun, x_solucion)
	return df, grafico