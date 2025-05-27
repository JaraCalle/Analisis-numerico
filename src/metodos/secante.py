from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def secante_DC(X0, X1, DC, Niter, Fun, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)

  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de la función en X0
  x=X0
  xn.append(x)
  fn0=eval(Fun)
  fn.append(fn0)

  # Evaluación inicial de la función en X1
  x=X1
  xn.append(x)
  fn1=eval(Fun)
  fn.append(fn1)

  # Inicialización del contador de iter y error inicial
  c=0
  Error=100
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X1, fn[c+1], "-"]

  while Error>Tol and fn[c+1]!=0 and c<Niter:
    x=xn[c+1]-(fn[c+1]*(xn[c+1]-xn[c])/(fn[c+1]-fn[c])) # Aplicación de la fórmula de la secante
    f=eval(Fun) # Evaluación de la función en el nuevo x
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c+1]-xn[c]) # Error absoluto
    df.loc[len(df)] = [c, xn[c+1], fn[c+1], Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
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

  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de la función en X0
  x=X0
  xn.append(x)
  fn0=eval(Fun)
  fn.append(fn0)

  # Evaluación inicial de la función en X1
  x=X1
  xn.append(x)
  fn1=eval(Fun)
  fn.append(fn1)

  # Inicialización del contador de iter y error inicial
  c=0
  Error=100
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X1, fn[c+1], "-"]

  while Error>=Tol and fn[c+1]!=0 and c<Niter:
    x=xn[c+1]-(fn[c+1]*(xn[c+1]-xn[c])/(fn[c+1]-fn[c])) # Aplicación de la fórmula de la secante
    f=eval(Fun) # Evaluación de la función en el nuevo x
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c+1]-xn[c])/abs(xn[c+1]) # Error relativo
    df.loc[len(df)] = [c, xn[c+1], fn[c+1], Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
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