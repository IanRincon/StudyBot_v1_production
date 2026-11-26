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
| `exportar_knn.py` | Reproducción del entrenamiento y exportación. |
| `test_app.py` | Pruebas de la aplicación. |
| `PROCESO_KNN.md` | Documentación de la exportación con joblib. |
| `APLICACION_FLASK.md` | Detalles de la aplicación local. |

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

## Predecir desde un CSV (opcional)

El CSV debe incluir encabezados con las 11 características. Puede contener
también `Lugar` y `Target`; estas columnas no se usan como entradas.

```powershell
python predecir_knn.py "C:\ruta\nuevos_datos.csv" --pruebas
python predecir_knn.py "C:\ruta\nuevos_datos.csv" --modelo personalizado --pruebas
```

Se muestran las filas con una columna `Prediccion`. El parámetro `--pruebas`
es opcional. Comparar con etiquetas de filas usadas en entrenamiento no
sustituye una evaluación en datos independientes.

## Desplegar en Render

1. Subir el código, la carpeta `templates`, los modelos y los metadatos a un
   repositorio de GitHub. No es necesario subir el dataset ni el entorno `.venv`.
2. Agregar `gunicorn` a `requirements-flask.txt` si todavía no está incluido.
3. En Render, crear un **Web Service** conectado al repositorio y elegir el
   plan **Free**, si está disponible para la cuenta.
4. Configurar:

   | Campo | Valor |
   |---|---|
   | Build Command | `pip install -r requirements-flask.txt` |
   | Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |

5. Definir `PYTHON_VERSION` con la versión completa de Python compatible con
   las dependencias del proyecto, preferiblemente la misma del entorno local
   (`python --version`).
6. Desplegar y abrir el enlace público proporcionado por Render.

El comando de Gunicorn es para el entorno Linux de Render; para ejecutar en
Windows localmente, usar `python app.py`. Gunicorn importa la aplicación y
no ejecuta el bloque `app.run()` del archivo.

El plan gratuito puede suspender el servicio tras periodos de inactividad y
tardar en responder a la siguiente visita. El enlace es público y no limita
el acceso a las personas con quienes se comparta.

Referencias: [Flask en Render](https://render.com/docs/deploy-flask),
[versión de Python](https://render.com/docs/python-version) y
[límites del plan gratuito](https://render.com/docs/free).

## Problemas frecuentes

- **`ModuleNotFoundError`:** instalar las dependencias con el mismo Python que
  se usa para iniciar el programa.
- **No se encuentra un modelo o los metadatos:** comprobar que los archivos
  estén junto a `app.py`. Para el KNN propio también se necesita
  `knn_personalizado.py`.
- **Puerto 5000 ocupado:** detener otra ejecución de la aplicación o usar
  `python -m flask --app app run --port 5001` y abrir el puerto correspondiente.
- **El navegador no conecta:** comprobar que el proceso siga ejecutándose y
  que se esté abriendo `http://127.0.0.1:5000`.
- **Error de compatibilidad al cargar un modelo:** utilizar las versiones de
  las dependencias registradas en `requirements.txt` y `metadatos_knn.json`.

Cargar únicamente archivos joblib de confianza: su deserialización puede
ejecutar código Python.
