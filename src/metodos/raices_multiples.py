from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .graficas import graficar

def newton_m2_DC(X0, DC, Niter, Fun, derivada_fx1, derivada_fx2, request):
  Tol = "0.5E-"
  Tol += DC
  Tol = float(Tol)
  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de f(x), f'(x) y f''(x) en X0
  x=X0
  f=eval(Fun)
  derivada1=eval(derivada_fx1)
  derivada2=eval(derivada_fx2)

  # Inicialización del contador de iter y error inicial
  c=0
  Error=100

  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  # Se calcula el denominador del método Newton m2
  denominador = derivada1**2 - (f*derivada2)

  columnas = ["i", "Xi", "f(Xi)", "E"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>Tol and f!=0 and denominador!=0 and c<Niter:
    x=x-((f*derivada1)/denominador) # Aplicación de la fórmula de Newton m2
    derivada1=eval(derivada_fx1) # Se evalúa f'(x) en el nuevo x
    derivada2=eval(derivada_fx2) # Se evalúa f''(x) en el nuevo x
    f=eval(Fun) # Se evalúa f(x) en el nuevo x
    denominador = derivada1**2 - (f*derivada2) # Se calcula el nuevo denominador
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
    messages.success(request, f"Raíces Múltiples: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Raíces Múltiples: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico

def newton_m2_CS(X0, CS, Niter, Fun, derivada_fx1, derivada_fx2, request):
  Tol = "5E-"
  Tol += CS
  Tol = float(Tol)
  fn = []  # Lista de f(x) en cada iteración
  xn = []  # Lista de valores x en cada iteración
  E = []   # Lista de errores
  N = []   # Lista de número de iteraciones

  # Evaluación inicial de f(x), f'(x) y f''(x) en X0
  x=X0
  f=eval(Fun)
  derivada1=eval(derivada_fx1)
  derivada2=eval(derivada_fx2)

  # Inicialización del contador de iter y error inicial
  c=0
  Error=100

  fn.append(f)
  xn.append(x)
  E.append(Error)
  N.append(c)

  # Se calcula el denominador del método Newton m2
  denominador = derivada1**2 - (f*derivada2)

  columnas = ["i", "Xi", "f(Xi)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  df.loc[len(df)] = [c, X0, fn[c], "-"]

  while Error>=Tol and f!=0 and denominador!=0 and c<Niter:
    x=x-((f*derivada1)/denominador) # Aplicación de la fórmula de Newton m2
    derivada1=eval(derivada_fx1) # Se evalúa f'(x) en el nuevo x
    derivada2=eval(derivada_fx2) # Se evalúa f''(x) en el nuevo x
    f=eval(Fun) # Se evalúa f(x) en el nuevo x
    denominador = derivada1**2 - (f*derivada2) # Se calcula el nuevo denominador
    fn.append(f)
    xn.append(x)
    c=c+1
    Error=abs(xn[c]-xn[c-1])/abs(xn[c]) # Error relativo
    df.loc[len(df)] = [c, xn[c], fn[c], Error]
    N.append(c)
    E.append(Error)

  # Condiciones de parada
  if f==0:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es raíz de f(x).")
  elif Error<Tol:
    s=x
    messages.success(request, f"Raíces Múltiples: {s} es una aproximación de un raíz de f(x) con una tolerancia {Tol}.")
  else:
    s=x
    messages.error(request, f"Raíces Múltiples: Fracasó en {Niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(Fun, x_solucion)
  return df, grafico