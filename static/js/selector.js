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
            window.alert('Los bebés no nacidos no se cuentan como pasajeros :)')
        }
        //Muy joven
        if (edad < 16 && viaja_solo == '0'){
            window.alert('Niño, eres muy pequeño para viajar sin acompañante')
        }
        //Demasiado viejo
        else if(edad > 122){
            window.alert('Vaya, sí que eres viejo, el viaje será muy duro para ti :(')
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

    var myCarousel = document.querySelector('#myCarousel')
    var carousel = new bootstrap.Carousel(myCarousel, {
    interval: 2000,
    wrap: false
    })

    carousel.next()
    

});
