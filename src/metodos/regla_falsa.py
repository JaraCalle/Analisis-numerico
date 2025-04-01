import pandas as pd
import numpy as np
import math

def regula_falsi_dc(a, b, fx, dc, niter):
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
    print(s,"es raiz de f(x)")
  elif E<tol:
    s=xm
    print(s,"es una aproximacion de un raiz de f(x) con una tolerancia", tol)
  else:
    s=xm
    print("Fracaso en ",niter, " iteraciones ")

  return df

def regula_falsi_cs(a, b, fx, cs, niter):
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
    print(s,"es raiz de f(x)")
  elif E<tol:
    s=xm
    print(s,"es una aproximacion de un raiz de f(x) con una tolerancia", tol)
  else:
    s=xm
    print("Fracaso en ",niter, " iteraciones ")

  return df