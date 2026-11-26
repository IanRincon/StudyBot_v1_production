"""Aplicación Flask local: ejecutar con `python app.py`."""
import math

import pandas as pd
from flask import Flask, render_template, request

from predecir_knn import cargar_modelo, predecir

app = Flask(__name__)

# Se cargan una sola vez al iniciar; no se entrena ni se necesita el CSV.
MODELOS = {}
for nombre in ('sklearn', 'personalizado'):
    MODELOS[nombre], COLUMNAS = cargar_modelo(nombre)

ETIQUETAS = {
    'silencio': 'Silencio',
    'sombra': 'Sombra',
    'aire_acondicionado': 'Aire acondicionado',
    'soporte_para_trabajar': 'Soporte para trabajar',
    'asientos': 'Asientos',
    'asientos_comodos': 'Asientos cómodos',
    'enchufes': 'Enchufes',
    'flujo_personas': 'Flujo de personas',
    'banos_cerca': 'Baños cerca',
    'cafeteria_cerca': 'Cafetería cerca',
    'internet_wifi': 'Internet Wi-Fi',
}

# Interpretación asumida de Target; cambiar aquí si la codificación es otra.
CLASES = {0: 'No apto', 1: 'Apto'}


@app.route('/', methods=['GET', 'POST'])
def inicio():
    """Valida el formulario y reutiliza la función de predicción existente."""
    valores = {columna: request.form.get(columna, '') for columna in COLUMNAS}
    nombre_modelo = request.form.get('modelo', 'sklearn')
    errores = {}
    resultado = None

    if request.method == 'POST':
        if nombre_modelo not in MODELOS:
            errores['modelo'] = 'Selecciona un modelo válido.'
        fila = {}
        for columna in COLUMNAS:
            try:
                numero = float(valores[columna])
                # El dataset original utiliza exclusivamente 0 y 1.
                if not math.isfinite(numero) or numero not in (0, 1):
                    raise ValueError
                fila[columna] = numero
            except (ValueError, OverflowError):
                errores[columna] = 'Ingresa un número: 0 o 1.'

        if not errores:
            datos = pd.DataFrame([fila], columns=COLUMNAS)
            clase = int(predecir(MODELOS[nombre_modelo], datos, COLUMNAS)[0])
            resultado = {'texto': CLASES[clase], 'clase': clase}

    return render_template(
        'index.html', columnas=COLUMNAS, etiquetas=ETIQUETAS,
        valores=valores, modelo=nombre_modelo, errores=errores,
        resultado=resultado,
    ), (400 if errores else 200)


if __name__ == '__main__':
    # Disponible solamente en este equipo.
    app.run(host='127.0.0.1', port=5000, debug=False)
