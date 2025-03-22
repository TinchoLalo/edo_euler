from flask import Flask, send_from_directory, request, jsonify # librerias necesarias para crear el servidor
from flask_cors import CORS # CORS

from sympy import symbols, lambdify, sin, cos, exp
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

from euler_method import euler_method # importamos la funcion para resolver EDOs
from preprocess_edo import preprocess_edo

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
port = 5000 # puerto donde va a correr el servidor

# Ruta principal donde cargamos el index.html (la página web)
@app.route("/")
def base():
    return send_from_directory('public', 'index.html')

# Nos permite cargar archivos estáticos (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('public', path)

# ========= EJERCICIO 1 =========
# Resolver la ecuación diferencial dy/dx = 0.2xy, con y(1) = 1, aproximando y(1.5) utilizando un paso de 0.1.
@app.route("/edo1/a", methods=['GET']) # definimos la ruta y el método
def edo1_a():
    # Funcion
    def f(x, y):
        return 0.2 * x * y 
    # Valores iniciales
    x0 = 1 # valor de x inicial
    y0 = 1 # valor de y en x0
    x = 1.5 # valor de x hasta donde se desea aproximar

    # Paso de 0.1
    h = 0.1
   

    # Resolver
    solution = euler_method(f, x0, y0, x, h )
    result = solution[-1][1]  # Aproximación de y(1.5) con paso de 0.1
    return jsonify({'result': result})


# ========= EJERCICIO 1B =========
@app.route("/edo1/b", methods=['GET'])
def edo1_b():
    # Funcion
    def f(x, y):
        return 0.2 * x * y
    
    # Valores iniciales
    x0 = 1
    y0 = 1
    x = 1.5

    # Paso de 0.05
    h = 0.05

    # Resolver
    solution = euler_method(f, x0, y0, x, h)
    result = solution[-1][1]  # Aproximación de y(1.5) con paso de 0.05
    return jsonify({'result': result})

# ========= EJERCICIO 2 =========
# Resolver la ecuación diferencial dI/dt = 15-3I, con I(0) = 0, aproximando I(0.5) utilizando un paso de 0.001
@app.route("/edo2/a", methods=['GET'])
def edo2_a():
    # Valores dados en el problema
    R = 12  # Resistencia (Ohmios)
    L = 4   # Inductancia (Henrios)
    V = 60  # Voltaje de la batería (Voltios)
    I0 = 0  # Corriente inicial (A)
    # Funcion
    def f(x, y):
        return 15 - 3 * I0
    
    # Valores iniciales
    t = 0 # I(0) = 0
    y0 = I0
    x = 0.5

    # Paso 
    h = 0.001 # paso del tiempo

    # Resolver
    solution = euler_method(f, t, y0, x, h)
    result = solution[-1][1]  
    return jsonify({'result': result})


# ========= CALCULADORA =========
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        edo = data['edo']
        x0 = float(data['x0'])
        y0 = float(data['y0'])
        xf = float(data['x'])
        h = float(data['stepSize'])
        
        edo_preprocesado = preprocess_edo(edo)
        print(f"EDO preprocesada: {edo_preprocesado}")

        # Definir símbolos
        x, y = symbols('x y')
        local_dict = {'x': x, 'y': y, 'cos': cos, 'sin': sin, 'exp': exp, 'log': np.log, 'abs': np.abs, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e}

        # Convertir la expresión a una función matemática
        expr = parse_expr(edo_preprocesado, local_dict=local_dict)
        print(f"Expresión de sympy: {expr}")
        f = lambdify((x, y), expr, modules=["numpy"])

        # Resolver usando el método de Euler
        solution = euler_method(f, x0, y0, xf, h)

        return jsonify({'result': solution})

    except Exception as e:
        return jsonify({'error': f"Ocurrió un error inesperado: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=port)
