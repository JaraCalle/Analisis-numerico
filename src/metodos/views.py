from django.shortcuts import render
from django.contrib import messages
from .biseccion import biseccion_CS, biseccion_DC
from .regla_falsa import regla_falsa_CS, regla_falsa_DC
from .punto_fijo import punto_fijo_CS, punto_fijo_DC
from .newton import newton_CS, newton_DC
from .secante import secante_CS, secante_DC
from .raices_multiples import newton_m2_CS, newton_m2_DC

def inicio(request):
    df = None
    grafico = None

    if request.method == "POST":
        metodo = request.POST.get("metodo")
        tipo_error = request.POST.get("tipo_error")  # 'DC' o 'CS'
        tolerancia = request.POST.get("tolerancia")
        fx = request.POST.get("funcion")
        iteraciones = int(request.POST.get("iteraciones"))

        # Nombre dinámico de la función, ej: biseccion_DC
        nombre_funcion = f"{metodo.lower().replace(' ', '_')}_{tipo_error}"
        print(nombre_funcion)

        # Obtener la función desde el módulo
        funcion_metodo = globals().get(nombre_funcion)

        if not funcion_metodo:
            messages.error(request, "Método no encontrado.")
            return render(request, 'inicio.html')

        try:
            if metodo in ["Biseccion", "Regla Falsa"]:
                a = float(request.POST.get("inferior"))
                b = float(request.POST.get("superior"))
                df, grafico = funcion_metodo(a, b, tolerancia, iteraciones, fx, request)

            elif metodo == "Punto Fijo":
                g = request.POST.get("g")
                x0 = float(request.POST.get("punto_inicial"))
                df, grafico = funcion_metodo(x0, g, tolerancia, iteraciones, fx, request)

            elif metodo == "Newton":
                df1 = request.POST.get("derivada")
                x0 = float(request.POST.get("punto_inicial"))
                df, grafico = funcion_metodo(x0, tolerancia, iteraciones, fx, df1, request)

            elif metodo == "Newton M2":
                df1 = request.POST.get("derivada")
                df2 = request.POST.get("segunda_derivada")
                x0 = float(request.POST.get("punto_inicial"))
                df, grafico = funcion_metodo(x0, tolerancia, iteraciones, fx, df1, df2, request)

            elif metodo == "Secante":
                x0 = float(request.POST.get("punto_inicial_1"))
                x1 = float(request.POST.get("punto_inicial_2"))
                df, grafico = funcion_metodo(x0, x1, tolerancia, iteraciones, fx, request)

        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return render(request, 'inicio.html')

    return render(request, 'inicio.html', {'tabla': df, 'grafico': grafico})