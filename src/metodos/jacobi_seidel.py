"""
MatJacobiSeid: Calcula la solución del sistema Ax=b con base en una condición
inicial x0,mediante el método de Jacobi o de Gauss Seidel (Matricial), depende
del método elegido, se elige 0 o 1 en metodo respectivamente
"""

from django.contrib import messages
import pandas as pd
import numpy as np
from .condiciones import radio_espectral

def MatJacobiSeid_DC(A, b, x0, DC, niter, metodo, request):
  iteracion = 0 # Contador de iteraciones
  tol = float(f'0.5E-{DC}')
  error = 1 # Error inicial
  n = len(A) # Tamaño matriz A
  b = np.array(b).T
  x0 = np.array(x0).T

  columnas = ["i"]
  for i in range(n):
    columnas.append(f'X{i+1}')
  columnas.append("E")
  df = pd.DataFrame(columns=columnas)

  fila = {"i":iteracion}
  for i in range(len(x0)):
    fila[f'X{i+1}'] = x0[i]

  fila['E'] = '-'

  df.loc[len(df)] = fila

  # Descomposición de la matriz A en D, L y U
  D = np.diag(np.diagonal(A))
  L = -np.tril(A, -1)
  U = -np.triu(A, 1)

  while error > tol and iteracion < niter:
    if metodo == 0: # Método de Jacobi
      T = np.linalg.inv(D) @ (L + U) # Matriz de transición
      C = np.linalg.inv(D) @ b
      x1 = T @ x0 + C # Se calcula la nueva x
    elif metodo == 1: # Método de Gauss-Seidel
      T = np.linalg.inv(D - L) @ U # Matriz de transición
      C = np.linalg.inv(D - L) @ b
      x1 = T @ x0 + C # Se calcula la nueva x

    error = np.linalg.norm(x1 - x0, np.inf) # Error absoluto con norma infinita
    x0 = x1
    iteracion += 1

    fila = {"i":iteracion}
    for i in range(len(x0)):
      fila[f'X{i+1}'] = x0[i]

    fila['E'] = error

    df.loc[len(df)] = fila

  # Verificación de convergencia
  if error < tol:
    solucion = x0
    if metodo == 0:
      messages.success(request, f"Jacobi matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")
    else:
      messages.success(request, f"Gauss-Seidel matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")

  else:
    if metodo == 0:
      messages.error(request, f"Jacobi matricial: Fracasó en {niter} iteraciones.")
    else:
      messages.error(request, f"Gauss-Seidel matricial: Fracasó en {niter} iteraciones.")
    
  ro = radio_espectral(T)

  return df, ro

def MatJacobiSeid_CS1(A, b, x0, CS1, niter, metodo, request):
  iteracion = 0 # Contador de iteraciones
  tol = float(f'5E-{CS1}')
  error = 1 # Error inicial
  n = len(A) # Tamaño matriz A
  b = np.array(b).T
  x0 = np.array(x0).T

  columnas = ["i"]
  for i in range(n):
    columnas.append(f'X{i+1}')
  columnas.append("ℇ1")
  df = pd.DataFrame(columns=columnas)

  fila = {"i":iteracion}
  for i in range(len(x0)):
    fila[f'X{i+1}'] = x0[i]

  fila['ℇ1'] = '-'

  df.loc[len(df)] = fila

  # Descomposición de la matriz A en D, L y U
  D = np.diag(np.diagonal(A))
  L = -np.tril(A, -1)
  U = -np.triu(A, 1)

  while error > tol and iteracion < niter:
    if metodo == 0: # Método de Jacobi
      T = np.linalg.inv(D) @ (L + U) # Matriz de transición
      C = np.linalg.inv(D) @ b
      x1 = T @ x0 + C # Se calcula la nueva x
    elif metodo == 1: # Método de Gauss-Seidel
      T = np.linalg.inv(D - L) @ U # Matriz de transición
      C = np.linalg.inv(D - L) @ b
      x1 = T @ x0 + C # Se calcula la nueva x

    error= np.linalg.norm((x1-x0)/x1, np.inf) # Error relatico con división punto
    x0 = x1
    iteracion += 1

    fila = {"i":iteracion}
    for i in range(len(x0)):
      fila[f'X{i+1}'] = x0[i]

    fila['ℇ1'] = error

    df.loc[len(df)] = fila

  # Verificación de convergencia
  if error < tol:
    solucion = x0
    if metodo == 0:
      messages.success(request, f"Jacobi matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")
    else:
      messages.success(request, f"Gauss-Seidel matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")

  else:
    if metodo == 0:
      messages.error(request, f"Jacobi matricial: Fracasó en {niter} iteraciones.")
    else:
      messages.error(request, f"Gauss-Seidel matricial: Fracasó en {niter} iteraciones.")

  ro = radio_espectral(T)

  return df, ro

def MatJacobiSeid_CS2(A, b, x0, CS2, niter, metodo, request):
  iteracion = 0 # Contador de iteraciones
  tol = float(f'5E-{CS2}')
  error = 1 # Error inicial
  n = len(A) # Tamaño matriz A
  b = np.array(b).T
  x0 = np.array(x0).T

  columnas = ["i"]
  for i in range(n):
    columnas.append(f'X{i+1}')
  columnas.append("ℇ2")
  df = pd.DataFrame(columns=columnas)

  fila = {"i":iteracion}
  for i in range(len(x0)):
    fila[f'X{i+1}'] = x0[i]

  fila['ℇ2'] = '-'

  df.loc[len(df)] = fila

  # Descomposición de la matriz A en D, L y U
  D = np.diag(np.diagonal(A))
  L = -np.tril(A, -1)
  U = -np.triu(A, 1)

  while error > tol and iteracion < niter:
    if metodo == 0: # Método de Jacobi
      T = np.linalg.inv(D) @ (L + U) # Matriz de transición
      C = np.linalg.inv(D) @ b
      x1 = T @ x0 + C # Se calcula la nueva x
    elif metodo == 1: # Método de Gauss-Seidel
      T = np.linalg.inv(D - L) @ U # Matriz de transición
      C = np.linalg.inv(D - L) @ b
      x1 = T @ x0 + C # Se calcula la nueva x

    error= np.linalg.norm(x1-x0, np.inf)/np.linalg.norm(x1, np.inf) # Error relativo con división de normas infinitas
    x0 = x1
    iteracion += 1

    fila = {"i":iteracion}
    for i in range(len(x0)):
      fila[f'X{i+1}'] = x0[i]

    fila['ℇ2'] = error

    df.loc[len(df)] = fila

  # Verificación de convergencia
  if error < tol:
    solucion = x0
    if metodo == 0:
      messages.success(request, f"Jacobi matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")
    else:
      messages.success(request, f"Gauss-Seidel matricial: {solucion} es una aproximación de un raiz de f(x) con una tolerancia {tol}.")

  else:
    if metodo == 0:
      messages.error(request, f"Jacobi matricial: Fracasó en {niter} iteraciones.")
    else:
      messages.error(request, f"Gauss-Seidel matricial: Fracasó en {niter} iteraciones.")

  ro = radio_espectral(T)

  return df, ro
