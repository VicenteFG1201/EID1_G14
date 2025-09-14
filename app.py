# Analizador de funciones matemáticas
# Proyecto EID 
# Integrante 1: Vicente Flores Guzman
# Integrante 2: Wladimir Peñeipil Soto
# Integrante 3: Lucas Nuñez Pinilla


# ------------------ LIBRERÍAS ------------------ 
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import math

# ------------------ CONFIG INICIAL ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

x = sp.Symbol("x")
transformaciones = (standard_transformations + (implicit_multiplication_application,))


# ------------------ F MATS ------------------

def calcular_dominio(expr_str):
    try:
        f = parse_expr(expr_str, transformations=transformaciones)
        dominio = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
        return f, dominio
    except Exception as e:
        return None, f"Error dominio: {e}"

def calcular_recorrido(expr_str):
  
    try:
        f = parse_expr(expr_str, transformations=transformaciones)
        dominio = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)

        # Intentar cálculo simbólico
        try:
            recorrido = sp.calculus.util.function_range(f, x, dominio)
            return recorrido
        except Exception:
            # Si falla, calcular recorrido numérico aproximado
            x_vals = [i * 0.1 for i in range(-100, 101)]
            y_vals = []
            for val in x_vals:
                try:
                    y = float(f.subs(x, val))
                    if math.isfinite(y):
                        y_vals.append(y)
                except Exception:
                    continue
            if y_vals:
                return sp.Interval(min(y_vals), max(y_vals))
            else:
                return "No se pudo calcular el recorrido"
    except Exception as e:
        return f"Error recorrido: {e}"

def encontrar_intersecciones(expr_str):
    try:
        f = parse_expr(expr_str, transformations=transformaciones)
        # Intersección con eje Y (f(0))
        try:
            interseccion_y = f.subs(x, 0)
            if not interseccion_y.is_real:
                interseccion_y = "No existe"
        except Exception:
            interseccion_y = "No existe"
        # Intersección con eje X (raíces)
        interseccion_x = []
        soluciones = sp.solve(f, x)
        for s in soluciones:
            try:
                if s.is_real:
                    interseccion_x.append(float(s))
            except Exception:
                continue
        return interseccion_x, interseccion_y
    except Exception as e:
        return f"Error intersecciones: {e}", None

def evaluar_punto(expr_str, valor_x):
    try:
        f = parse_expr(expr_str, transformations=transformaciones)
        mensaje = f"Evaluación paso a paso de f({valor_x}):\n"
        mensaje += f"1. Reemplazamos x por {valor_x} en f(x):\n"
        mensaje += f"   f(x) = {f}\n"
        paso = f.subs(x, valor_x)
        mensaje += f"2. f({valor_x}) = {paso}\n"
        # Validar dominio / resultados no definidos
        if paso.has(sp.zoo, sp.oo, sp.nan) or paso.is_real is False:
            mensaje += "3. El punto está fuera del dominio (resultado no definido o no real).\n"
            return None, mensaje
        resultado = float(paso)
        mensaje += f"3. Resultado final: f({valor_x}) = {resultado}\n"
        return (valor_x, resultado), mensaje
    except Exception as e:
        return None, f"Error en evaluación: {e}"
def sombrear_dominio(ax, dominio):
    try:
        if isinstance(dominio, sp.Interval):
            start = float(dominio.start) if dominio.start.is_finite else -100
            end = float(dominio.end) if dominio.end.is_finite else 100
            ax.axvspan(start, end, color='cyan', alpha=0.1, label="Dominio")
        elif isinstance(dominio, sp.Union):
            for intervalo in dominio.args:
                if isinstance(intervalo, sp.Interval):
                    start = float(intervalo.start) if intervalo.start.is_finite else -100
                    end = float(intervalo.end) if intervalo.end.is_finite else 100
                    ax.axvspan(start, end, color='cyan', alpha=0.1)
    except Exception:
        pass

def sombrear_recorrido(ax, recorrido):
    try:
        if isinstance(recorrido, sp.Interval):
            start = float(recorrido.start) if recorrido.start.is_finite else -100
            end = float(recorrido.end) if recorrido.end.is_finite else 100
            ax.axhspan(start, end, color='magenta', alpha=0.1, label="Recorrido")
        elif isinstance(recorrido, sp.Union):
            for intervalo in recorrido.args:
                if isinstance(intervalo, sp.Interval):
                    start = float(intervalo.start) if intervalo.start.is_finite else -100
                    end = float(intervalo.end) if intervalo.end.is_finite else 100
                    ax.axhspan(start, end, color='magenta', alpha=0.1)
    except Exception:
        pass

def graficar_funcion(expr_str, frame, valor_x=None):
    f = parse_expr(expr_str, transformations=transformaciones)
    intersecciones_x, interseccion_y = encontrar_intersecciones(expr_str)
    # Limpiar gráfico previo
    for widget in frame.winfo_children():
        widget.pack_forget()
        widget.destroy()
    # Generar valores de x y calcular y, filtrando los no válidos
    x_vals = [i * 0.1 for i in range(-100, 101)]
    y_vals = []
    for val in x_vals:
        try:
            y = float(f.subs(x, val))
            if math.isfinite(y):
                y_vals.append(y)
            else:
                y_vals.append(None)
        except Exception:
            y_vals.append(None)
    # Filtrar solo los puntos válidos
    x_plot = [x_vals[i] for i in range(len(y_vals)) if y_vals[i] is not None]
    y_plot = [y for y in y_vals if y is not None]
    # Crear figura
    fig, ax = plt.subplots(figsize=(5,4))
    ax.plot(x_plot, y_plot, color="blue", label="f(x)")
    ax.axhline(0, color="black")
    ax.axvline(0, color="black")
    ax.set_title("Gráfica de la función")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    # Resaltar intersecciones eje X (rojo)
    if isinstance(intersecciones_x, list):
        for i, r in enumerate(intersecciones_x):
            label = "Intersección eje X" if i == 0 else ""
            ax.plot(r, 0, "ro", markersize=8, label=label)
    # Resaltar intersección eje Y (verde)
    try:
        if isinstance(interseccion_y, (int, float)):
            ax.plot(0, float(interseccion_y), "go", markersize=8, label="Intersección eje Y")
    except Exception:
        pass
    # Punto evaluado (amarillo)
    if valor_x is not None:
        punto_eval, _ = evaluar_punto(expr_str, valor_x)
        if punto_eval:
            ax.plot(punto_eval[0], punto_eval[1], "yo", markersize=10, label=f"f({punto_eval[0]})")
            
    # Sombrear dominio y recorrido
    _, dominio = calcular_dominio(expr_str)
    sombrear_dominio(ax, dominio)

    recorrido = calcular_recorrido(expr_str)
    sombrear_recorrido(ax, recorrido)

    # Eliminar etiquetas duplicadas en la leyenda
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys())
    ax.grid(True)
    plt.tight_layout()
    # Mostrar en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ------------------ F PRINCIPAL DE ANÁLISIS ------------------

def analizar_funcion():
    entrada_funcion = entry_funcion.get()
    entrada_valor = entry_valor.get()
    # Dominio
    f, dominio = calcular_dominio(entrada_funcion)
    txt_dominio = f"Dominio: {dominio}"
    # Recorrido
    recorrido = calcular_recorrido(entrada_funcion)
    txt_recorrido = f"Recorrido: {recorrido}"
    # Intersecciones
    intersecciones_x, interseccion_y = encontrar_intersecciones(entrada_funcion)
    txt_intersecciones = f"Intersecciones eje X: {intersecciones_x}\nIntersección eje Y: {interseccion_y}"
    # Evaluación punto
    pasos = ""
    valor_x = None
    if entrada_valor.strip() != "":
        try:
            valor_x = float(entrada_valor)
            _, pasos = evaluar_punto(entrada_funcion, valor_x)
        except Exception:
            pasos = "Valor de x inválido. No se realizó evaluación."
    # Mostrar resultados en el textbox
    text_resultado.configure(state="normal")
    text_resultado.delete("1.0", "end")
    text_resultado.insert("end", txt_dominio + "\n")
    text_resultado.insert("end", txt_recorrido + "\n")
    text_resultado.insert("end", txt_intersecciones + "\n")
    text_resultado.insert("end", pasos)
    text_resultado.configure(state="disabled")
    # Mostrar gráfica
    graficar_funcion(entrada_funcion, frame_grafico, valor_x)

# ------------------ INTERFAZ ------------------ #
root = ctk.CTk()
root.title("Analizador de Funciones")
root.geometry("900x700")

# Frame superior para entradas
frame_superior = ctk.CTkFrame(root)
frame_superior.pack(pady=10)

# Entrada de función
label_funcion = ctk.CTkLabel(frame_superior, text="Ingrese función f(x):")
label_funcion.grid(row=0, column=0, padx=5, pady=5)
entry_funcion = ctk.CTkEntry(frame_superior, width=200)
entry_funcion.grid(row=0, column=1, padx=5, pady=5)

# Entrada de valor de x
label_valor = ctk.CTkLabel(frame_superior, text="Valor de x (opcional):")
label_valor.grid(row=1, column=0, padx=5, pady=5)
entry_valor = ctk.CTkEntry(frame_superior, width=200)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

# Botón para analizar
btn_analizar = ctk.CTkButton(frame_superior, text="Analizar", command=analizar_funcion)
btn_analizar.grid(row=2, column=0, columnspan=2, pady=10)

# Cuadro de texto para mostrar resultados
text_resultado = ctk.CTkTextbox(root, height=200, width=600)
text_resultado.pack(pady=10)

# Frame para el gráfico
frame_grafico = ctk.CTkFrame(root)
frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

# Ejecutar la interfaz
root.mainloop()
