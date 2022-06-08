from os import name
from typing import List
from flask import Flask, render_template, request
from flask.wrappers import Response
import pickle
from matplotlib.pyplot import get
import pandas as pd
import random

HOST = ""

app = Flask(__name__)

'''Variables globales: '''

#Acá se van a guardar los datos recibidos: 
pasajero = {
        'Age': ['0'],
        'TravelAlone': ['0'],
        'Pclass_1': ['0'],
        'Pclass_2': ['0'],
        'Pclass_3': ['0'],
        'Embarked_C': ['0'],
        'Embarked_Q': ['0'],
        'Embarked_S': ['0'],
        'Sex_male': ['0'],
        'IsMinor': ['0']
    }

historia = ['edad','clase','sexo','puerto','compañía','supervivencia']
solo_flag = 0
sexo_flag = 0 
contador_historia = 0

historia_edad = [   # < 18 años
                'Regresas a tu camarote después de que un guardia te regañara por correr en el pasillo, cuando escuchas un estruendo. ',
                'Estás en el salón principal, oyendo a unos músicos que tu familia te obligó a ir a ver, cuando de repente todo se sacude. ',
                    # 19 - 79 años
                'Sentado en un pasillo del barco, miras al mar pensando si tu jefe creerá el telegrama que le mandaste diciendo que no irás mañana a trabajar por estar enfermo y no porque te escapaste a Nueva York, cuando escuchas un gran estruendo. ',
                'Estás disfrutando en el salón principal esta nueva música y rebelde música llamada "jazz" a todo volumen. Ojalá ningún reverendo acuse mañana en los periódicos de Nueva York que si algo malo nos pasó, fue por culpa de esta música. De repente, un gran estruendo sacude el barco. Oh no. ',
                'Eres vigía del Titanic, andas muy aburrido porque a un tal David Blair lo mandaron a otro barco y olvidó dejar las llaves del locker de los binoculares y ahora no puedes ver nada. Oh bueno, ojalá nada malo pase. Terminas de pensarlo y un estruendo recorre toda la nave. ',
                    # > 80 años
                'Estás en el restaurante del barco peleando porque no te quieren hacer descuento en tu filete con tu credencial del INSEN, cuando una gran sacudida recorre la nave. ',
                'Estás en tu camarote buscando tu dentadura postiza debajo de la cama, cuando un fuerte estruendo hace que pegues un brinco y te des contra la base de la cama. Auch, esto dolerá mañana. '
                ]

historia_clase =[  # Primera clase
                'Miras el reloj de oro en tu bolsillo mientras deseas que todos estos plebeyos no hubieran abordado el barco para no compartir bote salvavidas con la chusma. ',
                'Pensando en si las £88,000 que costó tu boleto cubrirán también botes salvavidas de lujo, sigues las indicaciones de los marineros a cargo. ',
                    # Segunda clase
                'Te preguntas si todo este alboroto es por uno de esos estorbosos icebergs. Un día de estos debería hacer una Policía Internacional de Icebergs con sitio web y toda la cosa. Eso les enseñará. Sigues caminando hacia los botes salvavidas. ',
                'Si esto va mal, al menos sabes que hay otro barco cerca, el Carpathia, que los puede venir a ayudar. Ojalá el jefe de telecomunicaciones del Titanic no haya mandado a dormir al otro operador de radio hace poquito porque le dijo que estaba haciendo demasiado ruido. Sigues avanzando por el pasillo. ',
                    # Tercera clase
                'Pensando en qué injusto y a la vez práctico es que en la tercera clase separen los adultos solteros en los extremos opuestos del barco para que no se eh... ¿conozcan? Sigues las indicaciones de los marineros a cargo. ',
                'Mientras guardas un pan extra en tu bolsillo pensando en que será un rico desayuno para mañana, avanzas por el pasillo. '
                ]

historia_sexo = [   # Hombre o Mujer (Historia vacía)
                '',
                    # Otro
                'Escuchas que gritan "mujeres y niños primero" y, mientras piensas que eso es muy retrógrada, sigues a todos hacia los botes salvavidas. '
                ]

historia_puerto = [ # Francia
                'Oh là là, siendo francés piensas en que sería más fácil decidir quién sube a los botes salvavidas si tuvieran una guillatina a la mano. C´est dommage. Alzas tu puño y saltas a luchar por tu libertad. ',
                'Recordando el deseo de la liberté que corre por tu sangre francesa, tientas con la idea de luchar por tu lugar en el bote salvavidas en vez de esperar "civilizadamente" como el demás rebaño de ovejas hace. ',
                    # Inglaterra
                'Como buen inglés, piensas que este sería un buen momento para una taza de té. Mientras, sigues empujando para ver si logras subir a algún bote salvavidas. ',
                'Considerando el clima de tu amada Inglaterra, piensas en que el agua del mar podría no estar taaan fría, y consideras detenidamente en saltar en vez de esperar en la fila para un bote salvavidas. ',
                    # Irlanda
                'Ver a la gente empujándose para subir a los botes te recuerda al ambiente de las tabernas irlandesas. Oh hogar, dulce hogar. Piensas mientras golpeas a alguien e intentas lanzarte al bote más cercano. '
                ]

historia_solo = [   # Solo
                'Feliz de no haber viajado con acompañante, agarras doble chaleco salvavida. por si las moscas, claro. ',
                    # Acompañado
                'Mientras se hunde el barco, escoges con tu pareja sobre qué tabla de madera podrán flotar los dos, cuando otra pareja de una chica rica y un chico pobre y guapo se la agandallan. Oh bueno, ojalá la compartan justamente y no deje la chica congelarse al chico aún cuando se ve que claramente caben los dos ahí. ',
                'Mientras hacen piedra, papel o tijera por ver quién se lleva el último chaleco salvavidas, tú y tu grupo ven cómo bajan el último bote salvavidas. Oh bueno, seguro habrán muchas tablitas de madera tamaño-individual a las qué subirse. '
                ]

historia_supervivencia = [  # Final
                        'El barco se ha hundido, partido en dos y los músicos ya no suenan a lo lejos. Algunos abordaron a salvo el Carpathia y a otros no los dejaron subirse a tablitas de madera para sobrevivir. Salen los periódicos el día siguiente y en la lista de supervivientes... ',
                            # ¿Sobreviviste?
                        'No está tu nombre. :( Ahora tu cadáver yace en lo más profundo del océano... Esperemos que, si hacen una película de esto, al menos consigan a un buen extra que sepa hacer buenos soniditos de cubo de hielo para representarte. ',
                        '¡Está tu nombre! ¡Enhorabuena, sobreviviste al hundimiento del Titanic! Ahora esperemos que, si hacen una película de esto, al menos consigan a un buen extra para representarte. '
                        ]

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/prediccion', methods=['POST'])
def prediccion():
    global historia 

    #Llegada de datos
    edad = int(request.form.get("edad"))
    solo = int(request.form.get("solo"))
    sexo = int(request.form.get("sexo"))
    clase = int(request.form.get("clase"))
    puerto = int(request.form.get("puerto"))
    valores_web = [edad, solo, sexo, clase, puerto]

    #Importación del modelo predictivo
    filename = 'RegLog_model.sav'
    pickle_in = open(filename, 'rb')
    modelo_Titanic = pickle.load(pickle_in)

    #Guarda los valores en un diccionario: 
    print(f"Datos que vienen de la página web: {valores_web}")
 
    #Los datos se reasignan para ser compatibles con el modelo predictivo: 
    pasajero = guardar_datos_pasajero(valores_web)
    
    #Se predice la supervivencia según los datos recolectados
    pasajero['Survived'] = predecir_supervivencia(pasajero, modelo_Titanic)
    
    #Se redacta una historia según los datos que se ingresan al predictor y su resultado
    historia = redactar_historia(pasajero)
    
    return render_template("prediccion.html", historia = historia)

@app.route("/continuar_hist", methods = ["POST"])
def continuar_historia(): 
    global historia
    return render_template("continuar_historia.html", historia = historia)
  

    
'''Funciones '''
def guardar_datos_pasajero(valores):
    global solo_flag
    global sexo_flag
    # Guarda la Edad
    pasajero['Age'][0] = valores[0]
    
    # Determina si es menor de edad o no
    if valores[0] <= 16:
        pasajero['IsMinor'][0] = 1
    else:
        pasajero['IsMinor'][0] = 0
    
    # Guarda el valor de Solo
    solo_flag = int(valores[1])
    if valores[1] == 0:
        pasajero['TravelAlone'][0] = 1
    else:
        pasajero['TravelAlone'][0] = 0

    # Guarda el Sexo
    if valores[2] == 2:
        sexo_flag = 1
        pasajero['Sex_male'][0] = random.randint(0,1)
    else:
        sexo_flag = 0
        pasajero['Sex_male'][0] = valores[2]

    # Guarda la Clase
    if valores[3] == 0:
        pasajero['Pclass_1'][0] = 1
        pasajero['Pclass_2'][0] = 0
        pasajero['Pclass_3'][0] = 0
    elif valores[3] == 1:
        pasajero['Pclass_1'][0] = 0
        pasajero['Pclass_2'][0] = 1
        pasajero['Pclass_3'][0] = 0
    else:
        pasajero['Pclass_1'][0] = 0
        pasajero['Pclass_2'][0] = 0
        pasajero['Pclass_3'][0] = 1

    # Guarda el Puerto
    # print(range(pasajero['Embarked_C'], pasajero['Embarked_S']))
    if valores[4] == 0:
        pasajero['Embarked_C'][0] = 1
        pasajero['Embarked_Q'][0] = 0
        pasajero['Embarked_S'][0] = 0
    elif valores[4] == 1:
        pasajero['Embarked_C'][0] = 0
        pasajero['Embarked_Q'][0] = 1
        pasajero['Embarked_S'][0] = 0
    else:
        pasajero['Embarked_C'][0] = 0
        pasajero['Embarked_Q'][0] = 0
        pasajero['Embarked_S'][0] = 1

    pasajero_pd = pd.DataFrame(pasajero)

    return pasajero_pd

def predecir_supervivencia(pasajero, modelo):
    Selected_features = ['Age', 'TravelAlone', 'Pclass_1', 'Pclass_2', 
                    'Embarked_C','Embarked_S', 'Sex_male', 'IsMinor']
    pasajero['Survived'] = modelo.predict(pasajero[Selected_features])

    return pasajero['Survived']

def redactar_historia(pasajero):
    pasajero_historia = ['edad','clase','sexo','puerto','solo','supervivencia']

    # Easter Egg !!!
    if pasajero['Age'][0] == 33 and pasajero['Pclass_2'][0] == 1 and pasajero['Sex_male'][0] == 1 and pasajero['TravelAlone'][0] == 1 and pasajero['Embarked_S'][0] == 1:
        pasajero_historia = ['---','---','---','---','---','No, mueres por feo xDxDxdxd --- --- --- --- ---']
        
    # Casos normales
    else:        
    #-- ¿Cómo influyó tu edad?
        if pasajero['Age'][0] < 16:
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
        pasajero_historia[2] = historia_sexo[sexo_flag]

    #-- ¿Cómo influyó el puerto de embarcación?
        if pasajero['Embarked_C'][0] == 1:
            pasajero_historia[3] = historia_puerto[random.randint(0,1)]
        elif pasajero['Embarked_S'][0] == 1:
            pasajero_historia[3] = historia_puerto[2 + random.randint(0,1)]
        else:
            pasajero_historia[3] = historia_puerto[4]

    #-- ¿Cómo influyó ir acompañado o no?
        if pasajero['TravelAlone'][0] == 1:
            pasajero_historia[4] = historia_solo[0]
        else:
            pasajero_historia[4] = historia_solo[solo_flag]

    #-- ¿Sobreviviste?
        if pasajero['Survived'][0] == 0:
            pasajero_historia[5] = historia_supervivencia[0] + historia_supervivencia[1]
        else:
            pasajero_historia[5] = historia_supervivencia[0] + historia_supervivencia[2]

    return pasajero_historia

if __name__ == '__main__': 
    app.run(host = HOST, debug = True)