# Study Bot: evaluación de lugares con KNN

Aplicación sencilla en Flask para capturar las características de un lugar y
mostrar una predicción: **Apto** o **No apto**. Permite elegir entre un KNN de
scikit-learn y una implementación propia, ambos exportados con joblib.

## Requisitos

- Python y pip. Para reproducir el entorno original se utilizó Python 3.14.
- Las dependencias indicadas en `requirements.txt` y `requirements-flask.txt`.
- Los modelos exportados y sus metadatos incluidos en este proyecto.

## Ejecutar en local

Abrir una terminal en la carpeta del proyecto. En Windows PowerShell:

```powershell
cd "C:\Users\irinc\OneDrive\Documentos\ChatGPT\Study Bot"
```

Opcionalmente, crear un entorno virtual. Se puede usar su Python directamente
sin activar scripts de PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-flask.txt
.\.venv\Scripts\python.exe app.py
```

Si no se utiliza un entorno virtual:

```powershell
python -m pip install -r requirements-flask.txt
python app.py
```

Abrir [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.
Mantener la terminal abierta mientras se usa la aplicación. Para detenerla,
presionar **Ctrl+C**.

## Usar el formulario

1. Elegir el modelo KNN.
2. Completar las 11 características con valores numéricos **0 o 1**, siguiendo
   la misma codificación del dataset de entrenamiento.
3. Pulsar **Evaluar lugar**.
4. Consultar el resultado en la misma página.

Características requeridas, en el orden usado por el modelo:

```text
silencio, sombra, aire_acondicionado, soporte_para_trabajar,
asientos, asientos_comodos, enchufes, flujo_personas,
banos_cerca, cafeteria_cerca, internet_wifi
```

Se validan campos obligatorios y valores numéricos binarios tanto en el
navegador como en Flask. No se aceptan vacíos, texto, NaN ni infinitos.
Los modelos se cargan al iniciar: **no se necesita el dataset para ejecutar
la aplicación y no se vuelven a entrenar**. No hay base de datos.

La interpretación configurada es `Target=1`: **Apto**, `Target=0`: **No apto**.
Esta correspondencia es una suposición documentada porque el notebook no
define las etiquetas textuales. Puede modificarse en `CLASES` dentro de
`app.py`. Conservar la codificación original de las entradas, especialmente
`flujo_personas`; el CSV no incluye un diccionario de variables.

## Archivos del proyecto

| Archivo | Función |
|---|---|
| `app.py` | Aplicación Flask, carga de modelos y validación del formulario. |
| `templates/index.html` | Formulario y presentación del resultado. |
| `predecir_knn.py` | Función reutilizable de predicción y uso desde terminal. |
| `knn_personalizado.py` | Clase necesaria para cargar el modelo propio. |
| `modelo_knn.joblib` | Modelo entrenado de scikit-learn. |
| `modelo_knn_personalizado.joblib` | Modelo entrenado propio. |
| `metadatos_knn.json` | Orden de columnas, versiones y resultados de validación. |
| `requirements.txt` | Dependencias de los modelos. |
| `requirements-flask.txt` | Dependencias de la aplicación, incluyendo las anteriores. |


Mantener los modelos, los metadatos y los módulos Python junto a `app.py` y
conservar la carpeta `templates` con su estructura original.

## Ejecutar las pruebas

Desde la carpeta del proyecto, con las dependencias instaladas:

```powershell
python -m unittest test_app.py
```

Si se utiliza el entorno virtual sin activarlo:

```powershell
.\.venv\Scripts\python.exe -m unittest test_app.py
```

Las pruebas comprueban la carga del formulario, predicciones con ambos modelos,
las dos clases de salida y el rechazo de entradas inválidas.
