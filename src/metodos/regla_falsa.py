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
    messages.error(request, "Regla falsa: No se encontraron raíces con el método seleccionado. Verifique con la gráfica.")
    return None, None
  
  i = 1 # Contador de iteraciones
  tol = "0.5E-"
  tol += dc
  tol = float(tol)
  E = 1 # Error inicial
  xm_ant = a # Valor anterior de la aproximación de la raíz

  columnas = ["iter", "Xm", "f(Xm)", "E"]
  df = pd.DataFrame(columns=columnas)

  while E > tol and i <= niter:
    # Evalúa f(a) y f(b)
    q0 = eval(fx, {'x': a, 'math': math})
    q1 = eval(fx, {'x': b,'math': math})
    xm = b - ((q1 * (b - a)) / (q1 - q0)) # Aplica la fórmula de la regla falsa para obtener el nuevo punto xm
    E = abs(xm - xm_ant) # Error absoluto
    fe = eval(fx, {'x': xm, 'math': math}) # Evalúa la función en el nuevo punto xm
    df.loc[len(df)] = [i, xm, fe, E]
    xm_ant = xm # Guarda xm como el valor anterior para la siguiente iteración
    i += 1
    if fe * q1 < 0: # La raíz está entre xm y b -> se actualiza a
      a = xm
    else: # La raíz está entre a y xm -> se actualiza b
      b = xm

  # Condiciones de parada
  if fe==0: # Se encontró una raíz exacta
    s=xm
    messages.success(request, f"Regla Falsa: {s} es raíz de f(x).")
  elif E<tol: # Se alcanzó la tolerancia -> raíz aproximada
    s=xm
    messages.success(request, f"Regla Falsa: {s} es una aproximación de un raíz de f(x) con una tolerancia {tol}.")
  else: # No se encontró solución en el número máximo de iteraciones
    s=xm
    messages.error(request, f"Regla Falsa: Fracasó en {niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(fx, x_solucion)
  return df, grafico

def regla_falsa_CS(a, b, cs, niter, fx, request):
  continuidad = verificar_continuidad(fx, a, b)
  raiz = verificar_existencia_raiz(fx, a, b)

  if not continuidad:
    messages.error(request, "Regla Falsa: La función no es continua en el intervalo.")
    return None, None

  if not raiz:
    messages.error(request, "Regla falsa: No se encontraron raíces con el método seleccionado. Verifique con la gráfica.")
    return None, None

  i = 1 # Contador de iteraciones
  tol = "5E-"
  tol += cs
  tol = float(tol)
  E = 1 # Error inicial
  xm_ant = a # Valor anterior de la aproximación de la raíz

  columnas = ["iter", "Xm", "f(Xm)", "ℇ"]
  df = pd.DataFrame(columns=columnas)

  while E >= tol and i <= niter:
    # Evalúa f(a) y f(b)
    q0 = eval(fx, {'x': a, 'math': math})
    q1 = eval(fx, {'x': b,'math': math})
    xm = b - ((q1 * (b - a)) / (q1 - q0)) # Aplica la fórmula de la regla falsa para obtener el nuevo punto xm
    E = abs(xm - xm_ant)/abs(xm) # Error relativo
    fe = eval(fx, {'x': xm, 'math': math}) # Evalúa la función en el nuevo punto xm
    df.loc[len(df)] = [i, xm, fe, E]
    xm_ant = xm # Guarda xm como el valor anterior para la siguiente iteración
    i += 1
    if fe * q1 < 0: # La raíz está entre xm y b -> actualiza a
      a = xm
    else: # La raíz está entre a y xm -> actualiza b
      b = xm

  # Condiciones de parada
  if fe==0:
    s=xm
    messages.success(request, f"{s} es raíz de f(x).")
  elif E<tol:
    s=xm
    messages.success(request, f"{s} es una aproximación de un raíz de f(x) con una tolerancia {tol}.")
  else:
    s=xm
    messages.error(request, f"Fracasó en {niter} iteraciones.")

  x_solucion = df.iloc[-1, 1]
  grafico = graficar(fx, x_solucion)
  return df, grafico