from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def punto_fijo_DC(X0, g, DC, Niter, Fun, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn=[] # Lista de f(x) en cada iteración
  xn=[] # Lista de valores de x en cada iteración
  E=[] # Lista de errores
  N=[] # Lista de índices de iteración

  # Evaluamos f(x) en el punto inicial
  x=X0
  f=eval(Fun)

  # Inicialización del contador de iter y error inicial
  c=0
  Error=100

  # Guardamos los valores iniciales
  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>Tol and f!=0 and c<Niter:
    x=eval(g) # Evaluamos g(x) para obtener el nuevo valor de x
    fe=eval(Fun) # Evaluamos f(x) con el nuevo x
    fn.append(fe)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1]) # Error absoluto
    df.loc[len(df)] = [c, xn[c], fe, Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
  if fe==0:
    s=x
    messages.success(request, f"Punto Fijo: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Punto Fijo: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Punto Fijo: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def punto_fijo_CS(X0, g, CS, Niter, Fun, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn=[] # Lista de f(x) en cada iteración
  xn=[] # Lista de valores de x en cada iteración
  E=[] # Lista de errores
  N=[] # Lista de índices de iteración

  # Evaluamos f(x) en el punto inicial
  x=X0
  f=eval(Fun)

  # Inicialización del contador de iter y error inicial
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
    x=eval(g) # Evaluamos g(x) para obtener el nuevo valor de x
    fe=eval(Fun) # Evaluamos f(x) con el nuevo x
    fn.append(fe)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(x) # Error relativo
    df.loc[len(df)] = [c, xn[c], fe, Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
  if fe==0:
    s=x
    messages.success(request, f"Punto Fijo: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Punto Fijo: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Punto Fijo: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico
