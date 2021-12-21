from os import name
from typing import List
from flask import Flask, render_template, request, jsonify
from flask.wrappers import Response
import pickle

HOST = ""

app = Flask(__name__)

'''Variables globales: '''
#Aca se va a guardar los datos recibidos : 
data_storage = {
    'edad': 30, 
    'pasajero': ['0','0','0'], 
    'viaja_solo': '0', 
    'puerto': ['0','0','0'],
    'sexo': '0', 
}

LISTA_VALORES = ['edad', 'pasajero', 'viaja_solo', 'puerto', 'sexo']

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/llegada_datos', methods=['POST'])
def llegada_datos():
    #Llegada de datos
    valores = request.form.getlist('data[]')
    guardar_variables_diccionario(valores)
    print(f'data_storage: {data_storage.items()}')

    return Response(status=200)


'''
¿Para realizar la predicción sería en una "pestaña" aparte?

@app.route('/predecir', methods=[ 'POST'])
def predecir():
    jugador = ['Age']
    filename = 'RegLog_model.sav'
    pickle_in = open(filename, 'rb')
    loaded_model = pickle.load(pickle_in)
    Selected_features = ['Age', 'TravelAlone', 'Pclass_1', 'Pclass_2', 
                    'Embarked_C','Embarked_S', 'Sex_male', 'IsMinor']
    jugador['Survived'] = loaded_model.predict(jugador[Selected_features])
    
    return
'''

'''Funciones '''
def guardar_variables_diccionario(valores): 
        #Guardar las variables
        for val, key in zip(valores, LISTA_VALORES): 
            val = int(val)
            #Guarda el valor de la edad: 
            if key == 'edad' or key == 'sexo' or key == 'viaja_solo': 
                data_storage[key] = val

            #Guarda las demas variables: 
            else: 
                for x in range(0,len(data_storage[key])): 
                    print(f'x: {x}')
                    print(f'val:{val}')
                    if x == val: 
                        data_storage[key][x] = '1'
                    else: 
                        data_storage[key][x] = '0'

if __name__ == '__main__': 
    app.run(debug = True, host = HOST)


