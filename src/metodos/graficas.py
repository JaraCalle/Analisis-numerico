import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import math



def graficar(fx, x_solucion):
    x_values = np.linspace(x_solucion - 50, x_solucion + 50, 10000)

    funcion = [eval(fx, {'x': x, 'math': math}) for x in x_values]

    # Creamos la figura
    fig = go.Figure()

    # Añadimos el trazo de la función seno
    fig.add_trace(go.Scatter(x=x_values, y=funcion, mode='lines', line=dict(color='red', width=2), showlegend=False))

    # Se agrega un punto para que se vea la solución
    fig.add_trace(go.Scatter(
    x=[x_solucion], y=[0],
    mode='markers+text',
    marker=dict(color='lightblue', size=10, symbol='circle'),
    text=["Solución"],
    textposition="top right",
    name='Solución'
    ))

    # Establecemos los parámetros visuales para los ejes y la cuadrícula
    fig.update_layout(
        xaxis=dict(
            title="x",
            range=[x_solucion -10, x_solucion + 10],  # Rango fijo para el eje x
            gridcolor='lightgray',  # Color gris claro para la cuadrícula
            zeroline=True,  # Mostrar línea en x=0
            zerolinecolor='darkgray',  # Color gris oscuro para la línea en x=0
            zerolinewidth=2,  # Ancho de la línea en x=0
            showgrid=True,  # Mostrar la cuadrícula
            showline=True,  # Mostrar la línea del eje
            linewidth=2  # Ancho de la línea del eje x
        ),
        yaxis=dict(
            title="y",
            range=[-10, 10],  # Rango fijo para el eje y
            gridcolor='lightgray',  # Color gris claro para la cuadrícula
            zeroline=True,  # Mostrar línea en y=0
            zerolinecolor='darkgray',  # Color gris oscuro para la línea en y=0
            zerolinewidth=2,  # Ancho de la línea en y=0
            showgrid=True,  # Mostrar la cuadrícula
            showline=True,  # Mostrar la línea del eje
            linewidth=2  # Ancho de la línea del eje y
        ),
        plot_bgcolor='white',  # Color blanco para el fondo del área de trazado
        paper_bgcolor='white',  # Color blanco para el fondo fuera del área de trazado
        showlegend=True
    )

    graph_html = plot(fig, output_type='div', include_plotlyjs=True)
    
    return graph_html