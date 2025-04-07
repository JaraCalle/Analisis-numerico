from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def newton_DC(X0, DC, Niter, Fun, derivada_fx, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  derivada=eval(derivada_fx)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>Tol and f!=0 and derivada!=0  and c<Niter:
    x=x-f/derivada
    derivada=eval(derivada_fx)
    f=eval(Fun)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"{s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Fracaso en {Niter} iteraciones.")

  messages.success(request, "Se ejecuto el método de newton correctamente")
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun)
  return df, grafico

def newton_CS(X0, CS, Niter, Fun, derivada_fx, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  derivada=eval(derivada_fx)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>=Tol and f!=0 and derivada!=0  and c<Niter:
    x=x-f/derivada
    derivada=eval(derivada_fx)
    f=eval(Fun)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(x)
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"{s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Fracaso en {Niter} iteraciones.")

  messages.success(request, "Se ejecuto el método de newton correctamente")
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun)
  return df, grafico