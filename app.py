# Analizador de funciones matemáticas
# Proyecto EID 
# Integrante 1: Vicente Flores Guzman
# Integrante 2: (Completar)
# Integrante 3: (Completar)


import sympy as sp
import matplotlib.pyplot as plt

x = sp.Symbol('x')


def calcular_dominio(expr_str):
    """
    Calcula el dominio de una función matemática.
    (Integrante 1)
    """
    try:
        f = sp.sympify(expr_str)
        dominio = sp.calculus.util.function_domain(f, x, sp.S.Reals)
        print("\nDominio de la función:")
        print("f(x) =", f)
        print("Dominio:", dominio)
        return dominio
    except Exception as e:
        print("No se pudo calcular el dominio:", e)
        return None

def calcular_recorrido(expr_str):
    """
    Calcula el recorrido (rango) de una función matemática.
    (Integrante 2: Completar)
    """
    pass

def encontrar_intersecciones(expr_str):
    
    """
    Busca las intersecciones de la función con los ejes X e Y.
    (Integrante 3: Completar)
    """
    f = sp.sympify(expr_str)
    interseccion_y = f.subs(x,0)

    interseccion_x = sp.solve(f,x)

    print("La intersección en el eje x es: ",", ".join(str((xi,0)) for xi in interseccion_x)," y la intersección en el eje y es: ",(0,interseccion_y),sep="")

def evaluar_punto(expr_str, valor_x):
    """
    Evalúa la función en un punto específico y muestra el procedimiento.
    (Integrante 1: Hecho)
    Integrante 3: Agregar validación para puntos fuera del dominio.
    """
    try:
        f = sp.sympify(expr_str)
        print("\nEvaluación paso a paso:")
        print(f"1. Reemplazamos x por {valor_x} en f(x):")
        print(f"   f(x) = {f}")
        paso = f.subs(x, valor_x)
        print(f"2. f({valor_x}) = {paso}")
        resultado = float(paso)
        print(f"3. Resultado final: ({valor_x}, {resultado})")
        return (valor_x, resultado)
    except Exception as e:
        print("No se pudo evaluar el punto:", e)
        return None

def graficar_funcion(expr_str, valor_x=None):
    """
    Grafica la función y resalta puntos importantes.
    (Integrante 2: Completar)
    """
    pass

def main():
    print("=== Analizador de Funciones ===")
    print("Puedes ingresar funciones como: x**2+3*x, (x+2)/3, etc.")
    expr_str = input("Ingresa la función en x: ")

    opcion = input("¿Quieres evaluar un valor de x? (s/n): ")
    valor_x = None
    if opcion.lower() == "s":
        try:
            valor_x = float(input("Ingresa el valor de x: "))
        except:
            print("Valor de x inválido. Se omite evaluación de punto.")

    calcular_dominio(expr_str)
    calcular_recorrido(expr_str)
    encontrar_intersecciones(expr_str)
    if valor_x is not None:
        evaluar_punto(expr_str, valor_x)
    graficar_funcion(expr_str, valor_x)


if __name__ == "__main__":
    main()
