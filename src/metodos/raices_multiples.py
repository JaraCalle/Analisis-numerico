from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def newton_m2_DC(X0, DC, Niter, Fun, derivada_fx1, derivada_fx2, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  derivada1=eval(derivada_fx1)
  derivada2=eval(derivada_fx2)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  denominador = derivada1**2 - (f*derivada2)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>Tol and f!=0 and denominador!=0 and c<Niter:
    x=x-((f*derivada1)/denominador)
    derivada1=eval(derivada_fx1)
    derivada2=eval(derivada_fx2)
    f=eval(Fun)
    denominador = derivada1**2 - (f*derivada2)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Raíces Múltiples: Fracaso en {Niter} iteraciones.")

  messages.success(request, "Raíces Múltiples: Se ejecuto el método de raíces múltiples correctamente")

  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def newton_m2_CS(X0, CS, Niter, Fun, derivada_fx1, derivada_fx2, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  derivada1=eval(derivada_fx1)
  derivada2=eval(derivada_fx2)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  denominador = derivada1**2 - (f*derivada2)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>=Tol and f!=0 and denominador!=0 and c<Niter:
    x=x-((f*derivada1)/denominador)
    derivada1=eval(derivada_fx1)
    derivada2=eval(derivada_fx2)
    f=eval(Fun)
    denominador = derivada1**2 - (f*derivada2)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(xn[c])
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Raíces Múltiples: Fracaso en {Niter} iteraciones.")

  messages.success(request, "Raíces Múltiples: Se ejecuto el método de raíces múltiples correctamente")

  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun, x_solucion)
  return df, grafico