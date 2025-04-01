import pandas as pd
import numpy as np
import math

def biseccion_DC(Xi, Xs, DC, Niter, Fun):
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
				print(s,"es raiz de f(x)")
		elif Error<Tol:
				s=x
				print(s,"es una aproximacion de un raiz de f(x) con una tolerancia", Tol)
				print("Fm",fm)
				print("Error",fm)
		else:
				s=x
				print("Fracaso en ",Niter, " iteraciones ")
	else:
		print("El intervalo es inadecuado")

	return df

def biseccion_CS(Xi, Xs, CS, Niter, Fun):
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
				print(s,"es raiz de f(x)")
		elif Error<Tol:
				s=x
				print(s,"es una aproximacion de un raiz de f(x) con una tolerancia", Tol)
				print("Fm",fm)
				print("Error",fm)
		else:
				s=x
				print("Fracaso en ",Niter, " iteraciones ")
	else:
		print("El intervalo es inadecuado")

	return df