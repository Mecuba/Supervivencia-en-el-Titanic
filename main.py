from os import name
from typing import List
from flask import Flask, render_template, request
from flask.wrappers import Response

HOST = ""

app = Flask(__name__)

'''Variables globales: '''
#Aca se va a guardar los datos recividos: 
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

@app.route('/llegada_datos', methods=['POST'])
def llegada_datos():

    #Llegada de datos
    valores = request.form.getlist('data[]')
    #Guarda ls valores en un diccionario: 
    guardar_variables_diccionario(valores)

    #Los datos se guardan en datos juegos: 
    datos_juegos = save_data_juegos()
    print(datos_juegos)

    
    return Response(status=200)

    

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

def save_data_juegos(): #Datos para enviar :
    if (data_storage['edad'] < 16): 
        is_minor = '1' 
    else: 
        is_minor = '0'

    datos_juegos = {
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
        'PassengerId': [1001]
    }
    return datos_juegos 

if __name__ == '__main__': 
    app.run(debug = True, host = HOST)


