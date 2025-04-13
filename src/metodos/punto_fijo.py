from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def punto_fijo_DC(X0, g, DC, Niter, Fun, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>Tol and f!=0 and c<Niter:
    x=eval(g)
    fe=eval(Fun)
    fn.append(fe)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])
    df.loc[len(df)] = [c, xn[c], fe, Error]
    N.append(c)
    E.append(Error)

  if fe==0:
    s=x
    messages.success(request, f"{s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Fracaso en {Niter} iteraciones.")

  messages.success(request, "Se ejecuto el método de punto fijo correctamente")

  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def punto_fijo_CS(X0, g, CS, Niter, Fun, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  f=eval(Fun)
  c=0
  Error=100
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>=Tol and f!=0 and c<Niter:
    x=eval(g)
    fe=eval(Fun)
    fn.append(fe)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(x)
    df.loc[len(df)] = [c, xn[c], fe, Error]
    N.append(c)
    E.append(Error)

  if fe==0:
    s=x
    messages.success(request, f"{s} es raiz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Fracaso en {Niter} iteraciones.")

  messages.success(request, "Se ejecuto el método de punto fijo correctamente")
  
  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(Fun, x_solucion)
  return df, grafico
