from os import name
from typing import List
from flask import Flask, render_template, request
from flask.wrappers import Response
import pickle
import pandas as pd

HOST = ""

app = Flask(__name__)

'''Variables globales: '''
#Acá se va a guardar los datos recibidos: 
data_storage = {
    'edad': 30, 
    'pasajero': ['0','0','0'], 
    'viaja_solo': '0', #0 -> no 
    'puerto': ['0','0','0'],
    'sexo': '0', #0 -> Mujer
}


LISTA_VALORES = ['edad', 'pasajero', 'viaja_solo', 'puerto', 'sexo']

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/prediccion', methods=['POST'])
def prediccion():
    global sobrevives
    #Llegada de datos
    valores = request.form.getlist('data[]')
    #Guarda los valores en un diccionario: 
    guardar_variables_diccionario(valores)

   
    #Los datos se reasignan para ser compatibles con el modelo predictivo: 
    jugador = guardar_datos_jugador()
    print(jugador)
    print('--------------------------------------------------------------------------')
    jugador_pd = pd.DataFrame(jugador)
    
    #Se predice la supervivencia según los datos recolectados
    jugador_pd['Survived'] = predecir_supervivencia(jugador_pd)
    
    if jugador_pd['Survived'][0] == 1:
        sobrevives = 'Sí'
        print('Sobrevives')
    else:
        sobrevives = 'No'
        print('No sobrevives')
    
    #return Response(status=200) 
    return render_template("prediccion.html", sobrevives = sobrevives)
    # The HTTP Status 200 (OK) status code indicates that the request has been
    # processed successfully on the server.
    # return '¿Sobrevivirías al accidente del Titanic? {0}'.format(supervivencia)

'''Funciones '''
def guardar_variables_diccionario(valores): 
        #Guardar las variables
        for val, key in zip(valores, LISTA_VALORES): 
            val = int(val)
            #Guarda el valor de la edad: 
            if key == 'edad' or key == 'sexo' or key == 'viaja_solo': 
                data_storage[key] = val

            #Guarda las demás variables: 
            else: 
                for x in range(0,len(data_storage[key])): 
                    #print(f'x: {x}')
                    #print(f'val:{val}')
                    if x == val: 
                        data_storage[key][x] = 1
                    else: 
                        data_storage[key][x] = 0

def guardar_datos_jugador():
    #Datos para enviar :
    if (data_storage['edad'] <= 16): 
        is_minor = 1 
    else: 
        is_minor = 0

    jugador = {
        'Age': [data_storage['edad']],
        'TravelAlone': [data_storage['viaja_solo']],
        'Pclass_1': [data_storage['pasajero'][0]],
        'Pclass_2': [data_storage['pasajero'][1]],
        'Pclass_3': [data_storage['pasajero'][2]],
        'Embarked_C': [data_storage['puerto'][0]],
        'Embarked_Q': [data_storage['puerto'][1]],
        'Embarked_S': [data_storage['puerto'][2]],
        'Sex_male': [data_storage['sexo']],
        'IsMinor': [is_minor],
    }
    return jugador

def predecir_supervivencia(jugador_pd):
    filename = 'RegLog_model.sav'
    pickle_in = open(filename, 'rb')
    loaded_model = pickle.load(pickle_in)
    Selected_features = ['Age', 'TravelAlone', 'Pclass_1', 'Pclass_2', 
                    'Embarked_C','Embarked_S', 'Sex_male', 'IsMinor']
    jugador_pd['Survived'] = loaded_model.predict(jugador_pd[Selected_features])

    #return Selected_features
    return jugador_pd['Survived']

if __name__ == '__main__': 
    app.run(host = HOST)


