from flask import Flask, jsonify, request
import pickle

#curl -d "{'Age':[22],'TravelAlone':[1],'Pclass_1':[1],'Pclass_2':[0],'Pclass_3':[0],'Embarked_C':[1],'Embarked_Q':[0],'Embarked_S':[0],'Sex_male':[0],'IsMinor':[0],'PassengerId':[1001]}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/predecir
#curl -d "{\"Age\":[[22]]}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/predecir
 
app = Flask(__name__)

@app.route("/")
def home():
    return 'Dogglos'

@app.route('/predecir', methods=["POST"])
def predecir():
   json=request.get_json(force=True)
   jugador = json['Age']
   #filename = 'RegLog_model.sav'
   #pickle_in = open(filename, 'rb')
   #loaded_model = pickle.load(pickle_in)
   #Selected_features = ['Age', 'TravelAlone', 'Pclass_1', 'Pclass_2', 
   #                 'Embarked_C','Embarked_S', 'Sex_male', 'IsMinor']
   #jugador['Survived'] = loaded_model.predict(jugador[Selected_features])
   if int(jugador['Age'][0]) <= 16:
       respuesta = 'Menor de edad'
   else:
       respuesta = 'Mayor de edad'
       
   return '¿Sobrevivirías al accidente del Titanic? {0}'.format(respuesta)

if __name__ == '__main__':
    app.run()