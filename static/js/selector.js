$(document).ready(function () {

    $('#Submit').click(function(){
        edad = $('#edad').val()
        clase = $('#clase').val()
        viaja_solo = $('#viaje').val()
        puerto = $('#puerto').val()
        sexo = $("#sexo").val()

        //Mostrar en pantalla: 
        console.log(edad)
        console.log(clase)
        console.log(viaja_solo)
        console.log(puerto)
        console.log(sexo)
        
        //Envio de datos: 
        data_list = [edad, clase, viaja_solo, puerto, sexo]
        $.ajax({
            type: "POST",
            url: "/llegada_datos",
            data: {
                data: data_list
            },
            success: function (response) {
                console.log('ok')
            }
        });
        
    })  
});
