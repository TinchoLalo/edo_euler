import re
from sympy import symbols, lambdify, sin, cos, exp
from sympy.parsing.sympy_parser import parse_expr, TokenError, standard_transformations
import numpy as np

edo = "5xy*cos(x)"

# Preprocesamiento de la EDO
edo_preprocesado = re.sub(r'(?<=[0-9a-zA-Z])(?=[a-zA-Z])', '*', edo)
print(f"Expresión preprocesada: {edo_preprocesado}")

# Definición de símbolos
x, y = symbols('x y')

# Diccionario de símbolos locales
local_dict = {'x': x, 'y': y, 'cos': cos, 'sin': sin, 'exp': exp, 'log': np.log, 'abs': np.abs}
print(f"Diccionario local: {local_dict}")

# Transformaciones para manejar funciones trigonométricas
transformations = standard_transformations
print(f"Transformaciones: {transformations}")

# Conversión a expresión de sympy
try:
    expr = parse_expr(edo_preprocesado, local_dict=local_dict, transformations=transformations)
    print(f"Expresión de sympy: {expr}")
    f = lambdify((x, y), expr, modules=["numpy"])
    print("Función lambdify creada correctamente")

except TokenError as e:
    print(f"Error al analizar la expresión: {str(e)}")

except Exception as e:
    print(f"Ocurrió un error inesperado: {str(e)}")