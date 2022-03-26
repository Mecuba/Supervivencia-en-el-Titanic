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
    'viaja_solo': '0', #0 = No
    'puerto': ['0','0','0'],
    'sexo': '0', #0 = Mujer
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
    
    #Se redacta una historia según los datos que se ingresan al predictor y su resultado
    historia = redactar_historia(jugador_pd)
    
    return render_template("prediccion.html", historia = historia)

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

def redactar_historia(jugador_pd):
    historia = ['supervivencia','edad','sexo','compañía','puerto','clase']
#-- ¿Sobreviviste?
    if jugador_pd['Survived'][0] == 1:
        historia[0] = '¡Qué suerte, has sobrevivido!'
#------- ¿Cómo influyó tu edad?
        if jugador_pd['Age'][0] < 16:
            historia[1] = 'Quizá el terror a pasado ahora que descansas en el bote pero ¿cómo será posible olvidar todos esos gritos?'
        elif jugador_pd['Age'][0] < 40:
            historia[1] = 'Con la fuerza de tu edad sí que has logrado salir airoso de tremendo lío.'
        elif jugador_pd['Age'][0] < 70:
            historia[1] = 'Algo de experiencia en situaciones de riesgo te ha salvado esta ocasión.'
        else:
            historia[1] = 'Demasiada suerte para ser un anciano. Quizá esas caminatas por la tarde han ayudado de algo.'
#------- ¿Cómo influyó el sexo?
        if jugador_pd['Sex_male'][0] == 1:
            historia[2] = '¿Te has colado al bote salvavidas? ¿en serio? Qué suerte, eh.'
        else:
            historia[2] = 'Has luchado bien contra ese oportunista y recuperado el bote para todas esas madres y niños, que no digan que eres el sexo débil'
#------- ¿Cómo influyó ir acompañado o no?
        if jugador_pd['TravelAlone'][0] == 1:
            historia[3] = 'Es bien sabido que estando solo resulta más fácil moverse, estás por tu cuenta y no debes preocuparte por nadie.'
        else:
            historia[3] = 'La compañía siempre es buena, sobretodo cuando se queda atascada la puerta del dormitorio y alguien va a salvarte porque recordó que estabas ahí.'
#------- ¿Cómo influyó el puerto de embarcación?
        if jugador_pd['Embarked_C'][0] == 1:
            historia[4] = 'Oh'
        elif jugador_pd['Embarked_S'][0] == 1:
            historia[4] = 'Ahhh'
        else:
            historia[4] = 'Perro'
#------- ¿Cómo influyó la clase de pasajero?
        if jugador_pd['Pclass_1'][0] == 1:
            historia[5] = 'Oh'
        elif jugador_pd['Pclass_2'][0] == 1:
            historia[5] = 'Ahhh'
        else:
            historia[5] = 'Perro'
#-- ¿Sobreviviste?
    else:
        historia[0] = 'Ahora tu cadáver yace en el fondo del mar...'
#------- ¿Cómo influyó tu edad?
        if jugador_pd['Age'][0] < 16:
            historia[1] = 'Tan pequeño, un mundo inmenso que ya no alcanzarás a conocer.'
        elif jugador_pd['Age'][0] < 40:
            historia[1] = 'La muerte toma a aquellos que quizá menos se lo merecen.'
        elif jugador_pd['Age'][0] < 70:
            historia[1] = 'Una persona que al menos ya había disfrutado su vida'
        else:
            historia[1] = 'Bueno... ¿qué podría esperarse de un anciano?'
#------- ¿Cómo influyó el sexo?
        historia[2] = 'De un modo u otro estarás en la memoria de aquellos que lograste ayudar a escapar, tienes merecido un descanso eterno'
#------- ¿Cómo influyó ir acompañado o no?
        if jugador_pd['TravelAlone'][0] == 1:
            historia[3] = 'Pero es triste ¿no? Que nadie sepa que quedaste atrapado en el baño luego, que nadie te salve...'
        else:
            historia[3] = 'Descansa, tu familia está a salvo gracias a ti. Es un sacrificio que vale la pena y tus amados le recordarán.'
#------- ¿Cómo influyó el puerto de embarcación?
        if jugador_pd['Embarked_C'][0] == 1:
            historia[4] = 'Oh'
        elif jugador_pd['Embarked_S'][0] == 1:
            historia[4] = 'Ahhh'
        else:
            historia[4] = 'Perro'
#------- ¿Cómo influyó la clase de pasajero?
        if jugador_pd['Pclass_1'][0] == 1:
            historia[5] = 'Oh'
        elif jugador_pd['Pclass_2'][0] == 1:
            historia[5] = 'Ahhh'
        else:
            historia[5] = 'Perro'
    return historia

if __name__ == '__main__': 
    app.run(host = HOST)


