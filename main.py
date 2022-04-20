from os import name
from typing import List
from flask import Flask, render_template, request
from flask.wrappers import Response
import pickle
import pandas as pd
import random

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

historia_edad = [   # < 18 años
                'Regresas a tu camarote después de que un guardia te regañara por correr en el pasillo,cuando escuchas un estruendo.',
                'Estás en el salón principal, oyendo a unos músicos que tu familia te obligó a ir a ver, cuando de repente todo se sacude.',
                    # 19 - 79 años
                'Sentado en un pasillo del barco, miras al mar pensando si tu jefe creerá el telegrama que le mandaste diciendo que no irás mañana a trabajar por estar enfermo y no porque te escapaste a Nueva York, cuando escuchas un gran estruendo.',
                'Estás disfrutando en el salón principal esta nueva música y rebelde música llamada "jazz" a todo volumen. Ojalá ningún reverendo acuse mañana en los periódicos de Nueva York que si algo malo nos pasó, fue por culpa de esta música. De repente, un gran estruendo sacude el barco. Oh no.',
                'Eres vigía del Titanic, andas muy aburrido porque a un tal David Blair lo mandaron a otro barco y olvidó dejar las llaves del locker de los binoculares y ahora no puedes ver nada. Oh bueno, ojalá nada malo pase. Terminas de pensarlo y un estruendo recorre toda la nave.',
                    # > 80 años
                'Estás en el restaurante del barco peleando porque no te quieren hacer descuento en tu filete con tu credencial del INSEN, cuando una gran sacudida recorre la nave.',
                'Estás en tu camarote buscando tu dentadura postiza debajo de la cama, cuando un fuerte estruendo hace que pegues un brinco y te des contra la base de la cama. Auch, esto dolerá mañana.'
                ]

historia_clase =[  # Primera clase
                'Miras el reloj de oro en tu mano mientras deseas que todos estos plebeyos no hubieran abordado el barco para no compartir bote salvavidas con la chusma.',
                'Pensando en si las £88,000 que pagaste cubrirán también botes salvavidas de lujo, sigues las indicaciones de los marineros a cargo.',
                    # Segunda clase
                'Te preguntas si todo este alboroto es por uno de esos estorbosos icebergs. Un día de estos debería hacer una Policía Internacional de Icebergs con sitio web y toda la cosa. Eso les enseñará. Sigues caminando hacia los botes salvavidas.',
                'Si esto va mal, al menos sabes que hay otro barco cerca, el Carpathia, que los puede venir a ayudar. Ojalá el jefe de telecomunicaciones del Titanic no haya mandado a dormir al otro operador de radio hace poquito porque le dijo que estaba haciendo demasiado ruido. Sigues avanzando por el pasillo.',
                    # Tercera clase
                'Pensando en qué injusto y a la vez práctico es que en la tercera clase separen los adultos solteros en los extremos opuestos del barco para que no se eh... ¿conozcan? Sigues las indicaciones de los marineros a cargo',
                'Mientras guardas un pan extra en tu bolsillo pensando en que será un rico desayuno para mañana, avanzas por el pasillo.'
                ]

historia_sexo = ['Escuchas que gritan "mujeres y niños primero" y, mientras piensas que eso es muy retrógrada, sigues a todos hacia los botes salvavidas.',
                    '--Dogglo vacío--']

historia_puerto = ['--Dogglo vacío--','--Dogglo vacío--']

historia_solo = ['--Dogglo vacío--','--Dogglo vacío--']

historia_supervivencia = ['--Dogglo vacío--','--Dogglo vacío--']

LISTA_VALORES = ['edad', 'pasajero', 'viaja_solo', 'puerto', 'sexo']

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/prediccion', methods=['POST'])
def prediccion():

    #Llegada de datos
    valores = request.form.getlist('data[]')

    #Importanción del modelo predictivo
    filename = 'RegLog_model.sav'
    pickle_in = open(filename, 'rb')
    modelo_Titanic = pickle.load(pickle_in)

    #Guarda los valores en un diccionario: 
    guardar_variables_web(valores)

    #Los datos se reasignan para ser compatibles con el modelo predictivo: 
    pasajero = guardar_datos_pasajero()
    
    #Se predice la supervivencia según los datos recolectados
    pasajero['Survived'] = predecir_supervivencia(pasajero, modelo_Titanic)
    
    #Se redacta una historia según los datos que se ingresan al predictor y su resultado
    historia = redactar_historia(pasajero)
    
    return render_template("prediccion.html", historia = historia)

'''Funciones '''
def guardar_variables_web(valores): 
        #Guardar las variables
        for val, key in zip(valores, LISTA_VALORES): 
            val = int(val)
            #Guarda el valor de la edad: 
            if key == 'edad' or key == 'sexo' or key == 'viaja_solo': 
                data_storage[key] = val

            #Guarda las demás variables: 
            else: 
                for x in range(0,len(data_storage[key])): 
                    if x == val: 
                        data_storage[key][x] = 1
                    else: 
                        data_storage[key][x] = 0

def guardar_datos_pasajero():
    #Datos para enviar :
    if (data_storage['edad'] <= 16): 
        is_minor = 1 
    else: 
        is_minor = 0

    pasajero = {
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
    pasajero_pd = pd.DataFrame(pasajero)

    return pasajero_pd

def predecir_supervivencia(pasajero, modelo):
    Selected_features = ['Age', 'TravelAlone', 'Pclass_1', 'Pclass_2', 
                    'Embarked_C','Embarked_S', 'Sex_male', 'IsMinor']
    pasajero['Survived'] = modelo.predict(pasajero[Selected_features])

    return pasajero['Survived']

def redactar_historia(pasajero):
    pasajero_historia = ['edad','clase','sexo','compañía','puerto','supervivencia']

    # Easter Egg !!!
    if pasajero['Age'][0] == 33 and pasajero['Pclass_2'][0] == 1 and pasajero['Sex_male'][0] == 1 and pasajero['TravelAlone'][0] == 1 and pasajero['Embarked_S'][0] == 1 and pasajero['Survived'][0] == 0:
        pasajero_historia = ['---','---','---','---','---','No, mueres por feo xDxDxdxd --- --- --- --- ---']
    # Casos normales
    else:        
    #-- ¿Cómo influyó tu edad?
        if pasajero['Age'][0] < 18:
            pasajero_historia[0] = historia_edad[random.randint(0,1)]
        elif pasajero['Age'][0] < 79:
            pasajero_historia[0] = historia_edad[2 + random.randint(0,2)]
        else:
            pasajero_historia[0] = historia_edad[5 + random.randint(0,1)]

    #-- ¿Cómo influyó la clase de pasajero?
        if pasajero['Pclass_1'][0] == 1:
            pasajero_historia[1] = historia_clase[random.randint(0,1)]
        elif pasajero['Pclass_2'][0] == 1:
            pasajero_historia[1] = historia_clase[2 + random.randint(0,1)]
        else:
            pasajero_historia[1] = historia_clase[4 + random.randint(0,1)]

    #-- ¿Cómo influyó el sexo?
        if pasajero['Sex_male'][0] == 1:
            pasajero_historia[2] = historia_sexo[random.randint(0,1)]
        else:
            pasajero_historia[2] = historia_sexo[random.randint(0,1)]

    #-- ¿Cómo influyó ir acompañado o no?
        if pasajero['TravelAlone'][0] == 1:
            pasajero_historia[3] = historia_solo[random.randint(0,1)]
        else:
            pasajero_historia[3] = historia_solo[random.randint(0,1)]

    #-- ¿Cómo influyó el puerto de embarcación?
        if pasajero['Embarked_C'][0] == 1:
            pasajero_historia[4] = historia_puerto[random.randint(0,1)]
        elif pasajero['Embarked_S'][0] == 1:
            pasajero_historia[4] = historia_puerto[random.randint(0,1)]
        else:
            pasajero_historia[4] = historia_puerto[random.randint(0,1)]

    #-- ¿Sobreviviste?
        if pasajero['Survived'][0] == 1:
            pasajero_historia[5] = historia_supervivencia[random.randint(0,1)]
        else:
            pasajero_historia[5] = historia_supervivencia[random.randint(0,1)]

    return pasajero_historia

if __name__ == '__main__': 
    app.run(host = HOST, debug = True)


