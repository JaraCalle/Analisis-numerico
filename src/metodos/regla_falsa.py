from django.contrib import messages
import pandas as pd
import numpy as np
import math
from .condiciones import verificar_continuidad, verificar_existencia_raiz
from .graficas import graficar

def regla_falsa_DC(a, b, dc, niter, fx, request):
  continuidad = verificar_continuidad(fx, a, b)
  raiz = verificar_existencia_raiz(fx, a, b)

  if not continuidad:
    messages.error(request, "Regla Falsa: La función no es continua en el intervalo.")
    return None, None

  if not raiz:
    messages.error(request, "Regla Falsa: La función no tiene raíces en el intervalo.")
    return None, None
     
  i = 1
  tol = "0.5E-"
  tol += dc
  tol = float(tol)
  E = 1
  xm_ant = a

  columnas = ["iter", "Xm", "f(Xm)", "E"]
  df = pd.DataFrame(columns=columnas)

  while E > tol and i <= niter:
    q0 = eval(fx, {'x': a, 'math': math})
    q1 = eval(fx, {'x': b,'math': math})
    xm = b - ((q1 * (b - a)) / (q1 - q0))
    E = abs(xm - xm_ant)
    fe = eval(fx, {'x': xm, 'math': math})
    df.loc[len(df)] = [i, xm, fe, E]
    xm_ant = xm
    i += 1
    if fe * q1 < 0:
      a = xm
    else:
      b = xm

  if fe==0:
    s=xm
    messages.success(request, f"Regla Falsa: {s} es raiz de f(x).")
  elif E<tol:
    s=xm
    messages.success(request, f"Regla Falsa: {s} es una aproximacion de un raiz de f(x) con una tolerancia {tol}.")
  else:
    s=xm
    messages.error(request, f"Regla Falsa: Fracaso en {niter} iteraciones.")

  messages.success(request, "Regla Falsa: Se ejecuto el método de la regla falsa correctamente")

  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(fx, x_solucion)
  return df, grafico

def regla_falsa_CS(a, b, cs, niter, fx, request):
  continuidad = verificar_continuidad(fx, a, b)
  raiz = verificar_existencia_raiz(fx, a, b)

  if not continuidad:
    messages.error(request, "La función no es continua en el intervalo.")
    return None, None

  if not raiz:
    messages.error(request, "La función no tiene raíces en el intervalo.")
    return None, None

  i = 1
  tol = "5E-"
  tol += cs
  tol = float(tol)
  E = 1
  xm_ant = a

  columnas = ["iter", "Xm", "f(Xm)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  while E >= tol and i <= niter:
    q0 = eval(fx, {'x': a, 'math': math})
    q1 = eval(fx, {'x': b,'math': math})
    xm = b - ((q1 * (b - a)) / (q1 - q0))
    E = abs(xm - xm_ant)/abs(xm)
    fe = eval(fx, {'x': xm, 'math': math})
    df.loc[len(df)] = [i, xm, fe, E]
    xm_ant = xm
    i += 1
    if fe * q1 < 0:
      a = xm
    else:
      b = xm

  if fe==0:
    s=xm
    messages.success(request, f"{s} es raiz de f(x).")
  elif E<tol:
    s=xm
    messages.success(request, f"{s} es una aproximacion de un raiz de f(x) con una tolerancia {tol}.")
  else:
    s=xm
    messages.error(request, f"Fracaso en {niter} iteraciones.")

  messages.success(request, "Se ejecuto el método de la regla falsa correctamente")

  x_solucion = df.iloc[-1, 1]
  df = df.to_html(classes='table table-striped', index=False)
  grafico = graficar(fx, x_solucion)
  return df, grafico