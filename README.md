# Supervivencia en el Titanic
Aquí se encuentran los datasets de entrenamiento y prueba de la IA "Supervivencia en el Titanic", así como los archivos de la aplicación web diseñada para probar la acertividad del modelo entrenado.

Con el propósito de que este proyecto sirva de referencia para el mundo, también se han realizado algunas notas importantes sobre las técnicas o herramientas de programación, cuyo desconocimiento al inicio de este proyecto derivó en una serie de errores y tropiezos un tanto desafiantes para nosotros como principiantes en el diseño de aplicaciones web.

## Entrenamiento del modelo predictivo en Goggle Colab
Para obtener un modelo predictivo lo suficientemente robusto, pero cuyo código de entrenamiento fuera fácil de manipular decidimos basarnos en un cuaderno de [Kaggle](https://www.kaggle.com/mnassrib/titanic-logistic-regression-with-python?select=test.csv). El entrenamiento del modelo está basado en regresión logística.

Los datasets originalmente fueron descargados de una competencia en Kaggle: [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic/data), pero han sido guardados aquí para facilitar y controlar la exportación a nuestro cuaderno en [Google Colaboratory](https://colab.research.google.com/drive/1Ww9WhgC7N0oYPHkDCjy0ZAHjhRPCOL9E?usp=sharing), el cual ha sido traducido y complementado con algunas descripciones útiles correspondientes a la sintaxis de Python.

## Creación de un entorno virtual para el proyecto
Suele ser común necesitar versiones específicas de ciertas librerías para que un proyecto de Python funcione correctamente. Estas pueden no ser las mismas que se tienen instaladas de forma global en la computadora o las que necesita algún otro proyecto, por lo que resulta una buena práctica trabajar dentro de **entornos virtuales**, donde se pueden instalar librerías con versiones particulares que solo impactarán al comportamiento del proyecto dentro del entorno virtual, quedando instaladas de manera independiente a Python global.

La creación de un entorno virtual o *venv* se sugiere como uno de los primeros pasos en el desarrollo de un proyecto, pero no hay problema con crearlo cuando ya se va a mitad de camino. Estos es aplicable independientemente del editor de código o IDE que se utilice. Lo primero es instalar la herramienta de entornos virtuales con el comando:

```
pip install virtualenv
```

Tras terminar la instalación se procede a crear el entorno virtual dirigiéndose a la carpeta donde se ubica el proyecto y se ejecuta el comando:

```
\carpeta\de\proyecto>python -m venv my-venv
```

Donde `my-venv` es el nombre del entorno virtual. Con ello se estaría creado el entorno virtual pero aún queda activarlo para poder empezar a trabajar en él. Para esto se ejecuta:

```
source my-venv/Scripts/activate
```

> No usar un entorno virtual para el proyecto que sea que se esté desarrollando, puede desembocar en errores por las versiones de las librerías que se requieren en el proyecto, pero no indicarán directamente un problema con el entorno de Python en el que se está trabajando.

Un último paso, al menos usando **Visual Studio Code** y si es que no se realiza en automático, es la selección del intérprete de Python que está dentro del entorno virtual, no el que está instalado de manera global. Para esto, en la paleta de comandos (`Ctrl+Shift+P`) se debe usar la instrucción `Python: Select Interpreter` la cual desplegará una lista de intérpretes y deberá seleccionarse aquel dentro del entorno virtual. Según el editor de código o IDE que se esté utilizando esto puede cambiar, por lo que estos pasos solo son aplicables en [Visual Studio Code](https://code.visualstudio.com/docs/python/environments), en cuyo link se describe más a detalle la creación de entornos virtuales.

> Una buena práctica también es crear un archivo `.gitignore` que incluya la carpeta con todos los archivos del entorno virtual, cuya intención es evitar que estos archivos se suban innecesariamente a un repositorio si se trabaja con Git.

## Uso de Flask para crear una aplicación web
Flask es un marco de trabajo web para crear aplicaciones web con Python, y descrito como minimalista porque no requiere de otras librerías para funcionar, por lo que la creación de un app web se reduce a un plantilla como la siguiente:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```
Sin embargo, prescindir de otras librerías para funcionar no significa que no pueda complementarse con otras más para extender sus funcionalidades, y queda demostrado en este mismo proyecto.

> Dentro de `@app.route('/')` es posible *retornar* desde simple texto hasta una página completa de **HTML**. Para esto se requiere importar algunas otras funcionalidades de *Flask*, como `render_template`: `from flask import Flask, render_template, request`. Usando la función correspondiente, se puede renderizar una página de HTML cuyo código se encuentre dentro de la carpeta del proyecto, `index.html` es un ejemplo.

> Debido a *Flask*, es posible pasar variables de Python, directamente a HTML. Esto significa que, por ejemplo, se puede *postear* información a través de algún formulario, que esta sea procesada por el código Python y finalmente se puedan mostrar los resultados en HTML insertando las variables entre dos llaves `{{ variable }}`:
> ```html
> <html>
>     <head>
>         <title>{{ title }} </title>
>     </head>
>     <body>
>         <h1>Hello {{ username }}</h1>
>     </body>
> </html>
> ```
>
> Desde el código de Python, es importante agregar un argumento para **pasar** las variables en la función de *flask* que renderiza la página para que el código de HTML entienda de dónde provienen esas variables: `return render_template('pageName.html', variable = variable)`.


## Importación del modelo predictivo
Dentro de este repositorio se puede encontrar el modelo predictivo, el cual anteriormente fue exportado desde nuestro [cuaderno](https://colab.research.google.com/drive/1Ww9WhgC7N0oYPHkDCjy0ZAHjhRPCOL9E?usp=sharing), lleva por nombre `RegLog_model.sav` y ahora se ocupa para que la aplicación web pueda realizar las predicciones. Esto se logra importándolo con unas cuantas líneas, pero primero se debe importar la librería `pickle`, si no se encuentra instalada, se logra escribiendo `pip install pickle` en la terminal dentro de la carpeta del proyecto con el entorno virtual activo. Con la paquetería ya en el entorno, se manda a llamar dentro del archivo Python con `import pickle`.

```
filename = 'modelName.extension'
pickle_input = open(filename, 'rb')
model = pickle.load(pickle_input)
```

De este modo se logra importar el modelo si se encuentra en la raíz del proyecto. De encontrarse en algún subfolder, es importante especificar la dirección: `filename = 'Carpeta/NombreDelModelo.extension'`.

> Uno de los errores que se presentaron al tratar de usar `pickle` fue:
> ```
> UserWarning: Trying to unpickle estimator ( ) from version 1.0.1 when using version 1.0.2
> ```
> Pero fue corregido reinstalando `scikit learn` con la `versión 1.0.1` para que pudiera extraer correctamente el modelo predictivo.

> Es importante reconcoer la forma en que el modelo logra la predicción: el tipo de datos que necesita de entrada para evaluar y el tipo de datos que regresa. Por ejemplo, en este caso el modelo necesita que los datos estén organizados en un dataFrame de Pandas, así que basta con importar la librería: `import pandas as pd`.

## Servidor para la App Web: Heroku
Se seleccionó [Heroku](https://www.heroku.com/platform) como servidor para que esta App Web estuviera disponible en internet. Antes de subir el proyecto a esta plataforma (siendo similar a subirlo a Github), se deben crear algunos archivos como el `requirements.txt`:

```
pip freeze > requirements.txt
```

Donde se especificarán cada una de las librerías y versiones correspondientes que se encuentran instaladas en el entorno virtual y que se está ocupando actualmente en el proyecto.

> Algunas de estas librerías pueden no ser declaradas explícitamente en el código Python causando confusión sobre si son necesarias o no, pero muchas de ellas son librerías que se requieren para que otras puedan trabajar correctamente. Como sucede con `itsdangerous`,`Jinja2` y `Werkzeug`, que son librerías fundamentales para `Flask`.

`Procfile` es un archivo donde básicamente se le indica a Heroku cómo debe correr el proyecto. En Visual Studio Code puede resultar bastante fácil crearlo: basta con añadir un nuevo archivo a la carpeta del proyecto, nombrarlo exactamente como `Procfile` y en él escribir la siguiente línea:

```
web: gunicorn AppName:app
```

> Es importante haber instalado gunicorn en el entorno virtual: `pip install gunicorn` y que haya quedado declarado en `requirements.txt`, de otro modo, al intentar subir el proyecto a Heroku arrojará un error: `bash gunicorn command not found`.

Con estos archivos preparados, es posible comezar con la subida a Heroku, primero creando una cuenta en la plataforma y luego ejecutando los siguientes comandos (puede ser desde el CMD):

1. `heroku login` desde el directorio por default cuando se abre CMD
2. Dirigirse a la ubicación de la App, con `cd carpeta\donde\se\encuentra\la\App`
3. Si no se ha inicializado un repositorio, ejecutar `git init`
4. Ejecutar `heroku git:remote -a nombre-de-app`, donde `nombre-de-app` es el nombre de la aplicación asignado desde Heroku.
5. Ejecutar `git add .` para agregar los cambios en el repositorio
6. `git commit -m "Update App"` para definir el nombre del cambio
7. Ejecutar `git push heroku main`.

> El **comando 7** hace referencia al *branch* en el que la aplicación debe estar completamente actualizada (si es que se está trabajando en repositorios de Github con múltiples *branches*), pero puede suceder que la versión más reciente del proyecto esté en un *branch* diferente. Así que es preferible actualizar el *branch main* (o en dado caso el *branch master*) para que Heroku pueda aceptar el *push*, si se hace desde el *branch* con nombre distinto a *main* o *master*, Heroku va a ignorar la construcción subiendo únicamente los archivos a un *branch* nuevo, de modo que la app no existirá.
    
Si deseas más información al respecto no dudes en escribirnos a: contacto.mecuba@gmail.com
 