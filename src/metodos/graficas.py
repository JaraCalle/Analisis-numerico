import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import math
import numpy as np
import math
import plotly.graph_objs as go
from plotly.offline import plot

def graficar(fx, x_solucion=None):
    if x_solucion is not None:
        x_values = np.linspace(x_solucion - 50, x_solucion + 50, 10000)
    else:
        x_values = np.linspace(-50, 50, 10000)

    funcion = [eval(fx, {'x': x, 'math': math}) for x in x_values]

    fig = go.Figure()

    # Añadir la curva de la función
    fig.add_trace(go.Scatter(
        x=x_values,
        y=funcion,
        mode='lines',
        line=dict(color='#f5740c', width=2),
        showlegend=False
    ))

    # Si se proporciona una solución, añadirla al gráfico
    if x_solucion is not None:
        fig.add_trace(go.Scatter(
            x=[x_solucion], y=[0],
            mode='markers+text',
            marker=dict(color='#121212', size=10, symbol='circle'),
            text=["Solución"],
            textposition="top right",
            name='Solución'
        ))

    fig.update_layout(
        xaxis=dict(
            title="x",
            range=[x_solucion - 10, x_solucion + 10] if x_solucion is not None else [-10, 10],
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='darkgray',
            zerolinewidth=2,
            showgrid=True,
            showline=True,
            linewidth=2
        ),
        yaxis=dict(
            title="y",
            range=[-10, 10],
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='darkgray',
            zerolinewidth=2,
            showgrid=True,
            showline=True,
            linewidth=2
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )

    graph_html = plot(fig, output_type='div', include_plotlyjs=True)
    return graph_html


def graficar_interpolacion(x, y, a, x_real, y_real, titulo):
    x_vals = np.linspace(min(x) - 1, max(x) + 1, 500)
    y_vals = np.polyval(a, x_vals)

    fig = go.Figure()

    # Curva del polinomio
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name='Polinomio interpolante',
        line=dict(color='#f5740c')
    ))

    # Puntos originales
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Datos originales',
        marker=dict(color='#121212', size=8)
    ))

    # Punto adicional
    if x_real is not None and y_real is not None:
      fig.add_trace(go.Scatter(
        x=[x_real],
        y=[y_real],
        mode='markers',
        name='Punto adicional',
        marker=dict(color='green', size=10, symbol='x')
      ))

    fig.update_layout(
        title=f"Interpolación {titulo}",
        xaxis=dict(
            title="x",
            gridcolor='lightgray',  # Color gris claro para la cuadrícula
            zeroline=True,  # Mostrar línea en x=0
            zerolinecolor='darkgray',  # Color gris oscuro para la línea en x=0
            zerolinewidth=2,  # Ancho de la línea en x=0
            showgrid=True,  # Mostrar la cuadrícula
            showline=True,  # Mostrar la línea del eje
            linewidth=2  # Ancho de la línea del eje x
        ),
        yaxis=dict(
            title="P(x)",
            gridcolor='lightgray',  # Color gris claro para la cuadrícula
            zeroline=True,  # Mostrar línea en y=0
            zerolinecolor='darkgray',  # Color gris oscuro para la línea en y=0
            zerolinewidth=2,  # Ancho de la línea en y=0
            showgrid=True,  # Mostrar la cuadrícula
            showline=True,  # Mostrar la línea del eje
            linewidth=2  # Ancho de la línea del eje y
        ),
        legend=dict(x=0, y=1),
        width=700,
        height=500,
        plot_bgcolor='white',  # Color blanco para el fondo del área de trazado
        paper_bgcolor='white',  # Color blanco para el fondo fuera del área de trazado
    )

    graph_html = plot(fig, output_type='div', include_plotlyjs=True)
    
    return graph_html

def graficar_spline_general(x, y, tabla, d, x_real=None, y_real=None):
  if d == 1:
    titulo = "Spline Lineal"
  elif d == 3:
    titulo = "Spline Cúbico"

  fig = go.Figure()

  for i in range(len(x) - 1):
    xi = np.linspace(x[i], x[i+1], 100)
    coef = tabla[i]

    if d == 1:
      ai, bi = coef
      yi = ai * xi + bi

    elif d == 2:
      ai, bi, ci = coef
      yi = ai * xi**2 + bi * xi + ci

    elif d == 3:
      ai, bi, ci, di = coef
      yi = ai * xi**3 + bi * xi**2 + ci * xi + di

    else:
      raise ValueError("Solo se admiten splines de grado 1, 2 o 3")

    fig.add_trace(go.Scatter(
      x=xi,
      y=yi,
      mode='lines',
      name=f'Tramo {i+1}',
      line=dict(color='#f5740c')
    ))

  # Puntos originales
  fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    name='Datos originales',
    marker=dict(color='#121212', size=8)
  ))

  # Punto adicional
  if x_real is not None and y_real is not None:
    fig.add_trace(go.Scatter(
      x=[x_real],
      y=[y_real],
      mode='markers',
      name='Punto adicional',
      marker=dict(color='green', size=10, symbol='x')
    ))

  fig.update_layout(
    title=f"Interpolación {titulo}",
    xaxis=dict(
      title="x",
      gridcolor='lightgray',
      zeroline=True,
      zerolinecolor='darkgray',
      zerolinewidth=2,
      showgrid=True,
      showline=True,
      linewidth=2
      ),
    yaxis=dict(
      title="P(x)",
      gridcolor='lightgray',
      zeroline=True,
      zerolinecolor='darkgray',
      zerolinewidth=2,
      showgrid=True,
      showline=True,
      linewidth=2
    ),
    legend=dict(x=0, y=1),
    width=700,
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
  )

  graph_html = plot(fig, output_type='div', include_plotlyjs=True)
    
  return graph_html