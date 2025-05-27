from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def newton_DC(X0, DC, Niter, Fun, derivada_fx, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de f(x) y f'(x) en X0
  x=X0
  f=eval(Fun)
  derivada=eval(derivada_fx)

  # Inicialización del contador de iter y error inicial
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
    x=x-f/derivada # Aplicación de la fórmula de Newton
    derivada=eval(derivada_fx) # Evaluación de la derivada el nuevo x
    f=eval(Fun) # Evaluación de la función en el nuevo x
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1]) # Error absoluto
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
  if f==0:
    s=x
    messages.success(request, f"Newton: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Newton: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Newton: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def newton_CS(X0, CS, Niter, Fun, derivada_fx, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de f(x) y f'(x) en X0
  x=X0
  f=eval(Fun)
  derivada=eval(derivada_fx)

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

  while Error>=Tol and f!=0 and derivada!=0  and c<Niter:
    x=x-f/derivada # Aplicación de la fórmula de Newton
    derivada=eval(derivada_fx) # Evaluación de la derivada en el nuevo x
    f=eval(Fun) # Evaluación de la función en el nuevo x
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(x) # Error relativo
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
  if f==0:
    s=x
    messages.success(request, f"Newton: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Newton: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Newton: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico