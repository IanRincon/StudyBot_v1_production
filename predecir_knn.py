"""Predicciones con los KNN exportados, sin volver a entrenarlos.

Ejemplos (desde la carpeta del programa):
    python predecir_knn.py "nuevos_datos.csv"
    python predecir_knn.py "nuevos_datos.csv" --modelo personalizado
    python predecir_knn.py "Dataset v1.0.csv" --pruebas

Requiere las dependencias de requirements.txt, metadatos_knn.json y el
archivo .joblib elegido junto a este programa. Para el modelo personalizado
también se necesita knn_personalizado.py. Cargar solo modelos de confianza.
"""

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

CARPETA = Path(__file__).resolve().parent


# 1. CARGADO DEL MODELO Y DE LOS DATOS
def cargar_modelo(nombre='sklearn'):
    """Carga uno de los objetos ya entrenados y el orden de sus columnas."""
    archivos = {
        'sklearn': 'modelo_knn.joblib',
        'personalizado': 'modelo_knn_personalizado.joblib',
    }
    if nombre not in archivos:
        raise ValueError('El modelo debe ser sklearn o personalizado.')
    modelo = joblib.load(CARPETA / archivos[nombre])
    metadata = json.loads(
        (CARPETA / 'metadatos_knn.json').read_text(encoding='utf-8')
    )
    return modelo, metadata['columnas_entrada_en_orden']


def cargar_datos(ruta_csv):
    """Lee un CSV con encabezados. Puede incluir Lugar y Target."""
    datos = pd.read_csv(ruta_csv)
    if datos.empty:
        raise ValueError('El CSV no contiene filas para predecir.')
    return datos


# 2. FUNCIÓN DE PREDICCIÓN
def predecir(modelo, datos, columnas):
    """Devuelve una clase por fila de un DataFrame.

    `modelo` es el objeto recuperado con joblib; `columnas` es la lista
    del archivo de metadatos. Se conserva el preprocesamiento original:
    conversión a float sin escalado. Las columnas adicionales se ignoran.
    """
    faltantes = [columna for columna in columnas if columna not in datos.columns]
    if faltantes:
        raise ValueError(f'Faltan columnas de entrada: {faltantes}')
    if datos.empty:
        raise ValueError('Se necesita al menos una fila para predecir.')
    X = datos[columnas].to_numpy(dtype=float)
    if not np.isfinite(X).all():
        raise ValueError('Las entradas deben ser números sin vacíos ni infinitos.')
    # scikit-learn usa predict; la implementación propia usa predicir.
    if hasattr(modelo, 'predict'):
        return modelo.predict(X)
    return modelo.predicir(X)


# 3. PRUEBAS OPCIONALES
def realizar_pruebas(modelo, datos, columnas):
    """Comprueba la función con las primeras filas del CSV suministrado.

    No compara ambos modelos entre sí: pueden resolver empates de distinta
    manera. Si hay Target, muestra coincidencias solo como comprobación;
    un CSV con filas de entrenamiento no mide generalización.
    """
    muestra = datos.head(3)
    resultado = predecir(modelo, muestra, columnas)
    assert len(resultado) == len(muestra), 'Debe haber una predicción por fila.'
    # Cambiar el orden del CSV no debe alterar las predicciones.
    reordenado = muestra.loc[:, list(reversed(muestra.columns))]
    np.testing.assert_array_equal(resultado, predecir(modelo, reordenado, columnas))
    try:
        predecir(modelo, muestra.drop(columns=[columnas[0]]), columnas)
    except ValueError:
        pass
    else:
        raise AssertionError('Se debía detectar la columna faltante.')
    print('Pruebas correctas: tamaño, orden de columnas y columna faltante.')
    print('Predicciones de ejemplo:', resultado)
    if 'Target' in muestra:
        reales = muestra['Target'].to_numpy(dtype=float)
        print(f'Coincidencias con Target en la muestra: {np.sum(resultado == reales)}/{len(reales)}')
        print('Esta comprobación no sustituye la evaluación en datos de prueba independientes.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', help='Ruta al CSV que se desea clasificar.')
    parser.add_argument('--modelo', choices=['sklearn', 'personalizado'], default='sklearn')
    parser.add_argument('--pruebas', action='store_true', help='Ejecuta las pruebas de ejemplo.')
    args = parser.parse_args()

    modelo, columnas = cargar_modelo(args.modelo)
    datos = cargar_datos(args.csv)
    predicciones = predecir(modelo, datos, columnas)

    # Conservar las columnas originales y agregar la clase predicha.
    resultado = datos.copy()
    resultado['Prediccion'] = predicciones
    print(resultado.to_string(index=False))
    if args.pruebas:
        realizar_pruebas(modelo, datos, columnas)


if __name__ == '__main__':
    main()
