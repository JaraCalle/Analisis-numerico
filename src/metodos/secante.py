from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def secante_DC(X0, X1, DC, Niter, Fun, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  xn.append(x)
  fn0=eval(Fun)
  x=X1
  xn.append(x)
  fn.append(fn0)
  fn1=eval(Fun)
  fn.append(fn1)
  c=0
  Error=100
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X1, fn[c+1], "-"]

  while Error>Tol and fn[c+1]!=0 and c<Niter:
    x=xn[c+1]-(fn[c+1]*(xn[c+1]-xn[c])/(fn[c+1]-fn[c]))
    f=eval(Fun)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c+1]-xn[c])
    df.loc[len(df)] = [c, xn[c+1], fn[c+1], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"Secante: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Secante: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Secante: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def secante_CS(X0, X1, CS, Niter, Fun, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn=[]
  xn=[]
  E=[]
  N=[]
  x=X0
  xn.append(x)
  fn0=eval(Fun)
  x=X1
  xn.append(x)
  fn.append(fn0)
  fn1=eval(Fun)
  fn.append(fn1)
  c=0
  Error=100
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X1, fn[c+1], "-"]

  while Error>=Tol and fn[c+1]!=0 and c<Niter:
    x=xn[c+1]-(fn[c+1]*(xn[c+1]-xn[c])/(fn[c+1]-fn[c]))
    f=eval(Fun)
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c+1]-xn[c])/abs(xn[c+1])
    df.loc[len(df)] = [c, xn[c+1], fn[c+1], Error]
    N.append(c)
    E.append(Error)
  if f==0:
    s=x
    messages.success(request, f"Secante: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Secante: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Secante: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico