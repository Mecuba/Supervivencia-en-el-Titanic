# Supervivencia en el Titanic
Aquí se encuentran los datasets de entrenamiento y prueba de la IA "Supervivencia en el Titanic", así como los archivos de la aplicación web diseñada para probar la acertividad del modelo entrenado.

## Entrenamiento del modelo predictivo en Goggle Colab
Para obtener un modelo predictivo lo suficientemente robusto, pero cuyo código de entrenamiento fuera fácil de manipular decidimos basarnos en un cuaderno de [Kaggle](https://www.kaggle.com/mnassrib/titanic-logistic-regression-with-python?select=test.csv). El entrenamiento del modelo está basado en regresión logística.

Los datasets originalmente fueron descargados de una competencia en Kaggle: [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic/data), pero han sido guardados aquí para facilitar y controlar la exportación a nuestro cuaderno en [Google Colaboratory](https://colab.research.google.com/drive/1Ww9WhgC7N0oYPHkDCjy0ZAHjhRPCOL9E?usp=sharing), el cual ha sido traducido y complementado con algunas descripciones útiles correspondientes a la sintaxis de Python.

## Creación de un entorno virtual para el proyecto
Suele ser común necesitar versiones específicas de ciertas librerías para que un proyecto de Python funcione correctamente. Estas pueden no ser las mismas que se tienen instaladas de forma global en la computadora o las que necesita algún otro proyecto, por lo que resulta una buena práctica trabajar dentro de entornos virtuales, donde se pueden instalar librerías con versiones particulares que solo impactarán al comportamiento del proyecto dentro del entorno virtual, quedando instaladas de manera independiente a Python global.

La creación de un entorno virtual o *venv* se sugiere como uno de los primeros pasos en el desarrollo de un proyecto, pero no hay problema con crearlo cuando ya se va a mitad de camino. Estos es aplicable independientemente del editor de código o IDE que se utilice. Lo primero es instalar la herramienta de entornos virtuales con el comando:

```
pip install virtualenv
```

Tras terminar la instalación se procede a crear el entorno virtual dirigiéndose a la carpeta donde se ubica el proyecto y se ejecuta el comando:

```
unidad\carpeta\de\proyecto>python -m venv my-venv
```

Donde *my-venv* es el nombre del entorno virtual. Con ello se estaría creado el entorno virtual pero aún queda activarlo para poder empezar a trabajar en él. Para esto se ejecuta:

```
source my-venv/Scripts/activate
```

Un último paso, al menos usando Visual Studio Code, es que se debe seleccionar el intérprete de Python pero que está dentro del entorno virtual y no el que está instalado de manera global.

Si deseas más información al respecto no dudes en escribirnos a: contacto.mecuba@gmail.com
