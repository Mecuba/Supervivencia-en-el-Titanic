$(document).ready(function () {

    $('#Submit').click(function(){
        edad = $('#edad').val()
        clase = $('#clase').val()
        viaja_solo = $('#viaje').val()
        puerto = $('#puerto').val()
        sexo = $("#sexo").val()

        //Convierte edad a num entero 
        edad = parseInt(edad)

        //Mostrar en pantalla: 
        console.log(edad)
        console.log(clase)
        console.log(viaja_solo)
        console.log(puerto)
        console.log(sexo)
        
        //Condiciones de edad: 

        if (edad < 0 ){ 
            window.alert('a')
        }
        //Muy joven
        if (edad < 9 && viaja_solo == '1'){
            window.alert('*Lo detienen en la entrad* ')
        }
        //Demasiado viejo
        else if(edad > 122){
            window.alert('Eres el man más viejo del mundo, el viaje es muy duro para tí :c')
        }
        
        else{
            //Envio de datos: 
            data_list = [edad, clase, viaja_solo, puerto, sexo]
            $.ajax({
                type: "POST",
                url: "/prediccion",
                data: {
                    data: data_list
                },
                success: function (response) {
                    console.log('ok')
                }
            });
        }
    })  

    

});
