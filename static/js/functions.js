    var dataReturn;
    window.addEventListener('load',init,false)
    function init(){
        document.getElementById("formControlInputSelect").selectedIndex =-1;
        document.getElementById("selectAlgorithm").selectedIndex = -1;
        document.getElementById("minSup").value = '';
        
        // document.getElementById("sendSequenceTxt").style.display = "none";
        // document.getElementById("sendSequenceFile").style.display = "none";
        // document.getElementById("resultForm").style.display = "none";
        // document.getElementById("principalFormFile").style.display = "none";
        // document.getElementById("principalFormTxt").style.display = "none";
        hideElements(); 
        mostrarArchivos();

    } 

    function mostrarArchivos(){
        $.ajax({
            contentType: 'application/json',
            url: "/mostrarArchivos",
            type: 'POST',
            processData: false, 
            contentType: false,  
            statusCode:{
                404:function(){
                    console.log('El sitio que quiere acceder no existe')
                },
                200: function(){
                    console.log('Sitio encontrado, solicitud en proceso')
                }, 
                500: function(){
                    console.log('Error en el servidor, proceso cancelado')
                }
            },
            processData: false, 
            success: function(response){
                $archivos = $('#mostrarArchivos');
                $archivos.empty()

                $tabla = $('<table class="table table-bordered"></table>');
                $tabla.append('<thead class="thead-light"> <tr>'+
                                    '<th>#</th>'+
                                    '<th>Archivo</th>'+
                                    '<th> CVS </th>'+                                    
                                '</tr> </thead>');
                $tablabody = $('<tbody></tbody>')
                for(var i=0; i < response.length; i++){
                    $fila = $('<tr></tr>');
                    
                    $fila.append('<td >'+i+'</td>');
                    $fila.append('<td >'+response[i]+'</td>');
                    $fila.append('<td >'+'<button type="button" class="btn btn-default"> CVS </button>'+'</td>');

                    $tablabody.append($fila);
                }
                $tabla.append($tablabody);
                $archivos.append($tabla);
                console.log('Success');
            }, error: function(error){
                console.log('Error '+error);
            }
        });
    }

    function hideElements(){
        limpiarCamposFile();
        limpiarCamposTxt();
        
        document.getElementById("sendSequenceTxt").style.display = "none";
        document.getElementById("sendSequenceFile").style.display = "none";
        // document.getElementById("resultForm").style.display = "none";
    }

    document.addEventListener("DOMContentLoaded", hideForms);
    function hideForms(){
        document.getElementById("principalFormFile").style.display = "none";
        document.getElementById("principalFormTxt").style.display = "none";
        // document.getElementById("resultForm").style.display = "none";
    }

    function limpiarCamposTxt(){
        document.getElementById("inputManualADNText").value = '';
        document.getElementById("previsualSequenceAnalisis").value = '';
    }

    function limpiarCamposFile(){
        document.getElementById("inputFile").value = '';
        document.getElementById("previsualSequenceAnalisis").value = '';
    }

    function selectProccess(){
        var item_selected = document.getElementById("formControlInputSelect");
        switch(item_selected.options[item_selected.selectedIndex].value){

            case "inputManual":
                limpiarCamposTxt();
                document.getElementById("principalFormTxt").style.display = "block";
                document.getElementById("principalFormFile").style.display = "none";
            break;

            case "inputFile":
                limpiarCamposFile();
                document.getElementById("principalFormFile").style.display = "block";
                document.getElementById("sendSequenceFile").style.display = "block";
                document.getElementById("principalFormTxt").style.display = "none";
                
            break;

            default:
                hideElements();
            break;
        }
    }    
    
    function addStringSequences(){  
        // alert("\n"+document.getElementById("inputManualADNText").value.toUpperCase());  
        if(document.getElementById("inputManualADNText").value.length != 0){
            document.getElementById("sendSequenceTxt").style.display = "block" ; 
            document.getElementById("previsualSequenceAnalisis").value += document.getElementById("inputManualADNText").value.toUpperCase() + "\n";
            document.getElementById("inputManualADNText").value = ''
        }
        else{
            alert("Ingrese una secuencia de ADN para su análisis")
        }  
    }

    

    function showbtnFile(){
        document.getElementById("sendSequenceFile").style.display = "block";
    }

    // function sendingSequence(){
    //     var item_selected = document.getElementById("formControlInputSelect");
    //     var sequence;
    //     switch(item_selected.options[item_selected.selectedIndex].value){

    //         case "inputManual":
    //             sequence = fomateoTxt();
    //         break;

    //         case "inputFile":
    //             var dato_archivo = $('#inputFile').prop("files")[0];
    //             var form_data = new FormData();
    //             sequence = form_data.append('file',dato_archivo);
    //         break;

    //         case "inputDB":

    //         break;
                
    //         default:
    //             sequence = null
    //         break;
    //     }

    //     return sequence
    // }  
    
    function formateoTxt(){
        var txt = document.getElementById("previsualSequenceAnalisis").value;
        const listSequence = txt.split("\n");
        listSequence.pop();
        console.log(listSequence);
        return listSequence;
    }
    
    function mostrarDatosJSON(p){
        var pos = dataReturn.Patrones[p].Posiciones;
        var table = document.createElement('table');
        var thead = document.createElement('thead');
        var tbody = document.createElement('tbody');
        var th = document.createElement('th');
        var td = document.createElement('td');
        var tr = document.createElement('tr');
        

        table.appendChild(thead);
        table.appendChild(tbody);

        
        th.innerHTML ='Sequencia';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML='Posicion';

        tr.appendChild(th);
        thead.appendChild(tr);
        

        for(var i =0;  i< pos.length; i++){
            tr = document.createElement('tr');
            var td = document.createElement('td');

            td.innerHTML=pos[i].sequencia;
            tr.appendChild(td);
            td = document.createElement('td');

            td.innerHTML=pos[i].posicion;
            tr.appendChild(td);

            tbody.appendChild(tr);
        }
        

        $("#pmodal-body").empty();
        $("#pmodal-body").append(table);

        

        // document.getElementById("resultForm").style.display = 'block';
        
        // console.log(datos);
        // if(tipo == 'file'){
        //     console.log(datos["Candidatos"]);
        //     document.getElementById("resultadoAnalisis").value += datos["Encabezados"];
        //     document.getElementById("resultadoAnalisis").value += "\n";
        //     document.getElementById("resultadoAnalisis").value += datos["Candidatos"];
            
        // }else if(tipo == 'txt'){
        //     document.getElementById("resultadoAnalisis").value = datos["Candidatos"];
        // }
        

    }

    //--- Para entrada de texto
    $(document).ready(function(){
        $("#sendSequenceTxt").click(function(){
            var sendData = [{
                            "algoritmo": $('#selectAlgorithm').val(),
                            "min_sup": $('#minSup').val(),
                            "sequence" :formateoTxt()
                            }];
            console.log(sendData);
            $.ajax({
                dataType: "json" ,
                contentType: 'application/json',
                url: "/analisisText",
                data: JSON.stringify(sendData),
                type: 'POST',
                statusCode:{
                    404:function(){
                        console.log('El sitio que quiere acceder no existe')
                    },
                    200: function(){
                        console.log('Sitio encontrado, solicitud en proceso')
                    }, 
                    500: function(){
                        console.log('Error en el servidor, proceso cancelado')
                    }
                },
                processData: false, 
                success: function(data_response){
                    dataReturn = data_response;
                    console.log(data_response);
                    
                    console.log(data_response.Patrones.length);
                    $patrones = $('#patronesHallados');
                    $patrones.empty()

                    $tabla = $('<table class="table table-bordered"></table>');
                    $tabla.append('<thead class="thead-light"> <tr>'+
                                        '<th>Patron</th>'+
                                        '<th>Longitud</th>'+
                                        '<th>No. de ocurrencias</th>'+
                                        '<th>Posiciones</th>');
                                    //     +
                                    //     '<th colspan = 2>Posciones</th>'+
                                    // '</tr>'+
                                    // '<tr>'+
                                    //     '<th>Secuencia</th>'+
                                    //     '<th>Posicion</th>'+
                                    // '</tr> </thead>');
                    $tablabody = $('<tbody></tbody>')
                    for(var i=0; i < data_response.Patrones.length; i++){
                        $fila = $("<tr></tr>");
                        
                        $fila.append('<td>'+data_response.Patrones[i].Patron+'</td>');
                        $fila.append('<td>'+data_response.Patrones[i].Longitud+'</td>');
                        $fila.append('<td>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        $fila.append('<td>'+'<button type="button" class="alert"'+"onClick=mostrarDatosJSON("+i+")>"+"Posiciones"+'</button>'+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Patron+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Longitud+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        // for(var j=0; j< data_response.Patrones[i].Posiciones.length; j++){
                        //     $fila_seq=$('<tr></tr>');
                        //     if(j == 0){
                        //         $fila.append('<td>'+data_response.Patrones[i].Posiciones[j].sequencia+'</td>');
                        //         $fila.append('<td>'+data_response.Patrones[i].Posiciones[j].posicion+'</td>');
                        //         $tablabody.append($fila);
                        //     } else{
                        //         $fila_seq.append('<td>'+data_response.Patrones[i].Posiciones[j].sequencia+'</td>');
                        //         $fila_seq.append('<td>'+data_response.Patrones[i].Posiciones[j].posicion+'</td>');
                        //         $tablabody.append($fila_seq);
                        //     }
                        // }
                        $tablabody.append($fila);
                    }
                    $tabla.append($tablabody);
                    $patrones.append($tabla);

                    console.log('Success');
                }, error: function(error){
                    console.log('Error '+error);
                }
            });
        });
    });
    //-------------------------------------------

    ////-------------------Para archivos -------------------------------------
    $(document).ready(function(){
        $("#sendSequenceFile").click(function(){
            // var dato_archivo = $('#inputFile').prop("files")[0];
            // var dato_algo = $('#selectAlgorithm').val();
            // var dato_minsup = $('#minSup').val();

            console.log($('#inputFile').prop("files")[0]);
            var form_data = new FormData();
            
            form_data.append('Algoritmo', $('#selectAlgorithm').val());
            form_data.append('min_sup', $('#minSup').val());
            form_data.append('file', $('#inputFile').prop("files")[0]);
            
            

            

            // var sendData = [{
            //                 "Algoritmo": $('#selectAlgorithm').val(),
            //                 "min_sup": $('#minSup').val(),
            //                 "sequence" :$('#inputFile').prop("files")[0]
            //                 }];
            // console.log(sendData);
            // $.ajax({
            //     dataType: "json" ,
            //     contentType: 'application/json',
            //     url: "/analisisFile",
            //     data: JSON.stringify(sendData),
            //     type: 'POST',
            //     statusCode:{
            //         404:function(){
            //             console.log('El sitio que quiere acceder no existe')
            //         },
            //         200: function(){
            //             console.log('Sitio encontrado, solicitud en proceso')
            //         }, 
            //         500: function(){
            //             console.log('Error en el servidor, solicitud no enviada')
            //         }
            //     },
            //     processData: false, 
            //     success: function(response){
            //         console.log('Success '+response);
            //     }, error: function(error){
            //         console.log('Error '+error);
            //     }
            // });

            $.ajax({
                url: '/analisisFile',
                data: form_data,
                type: 'POST',
                processData: false, 
                contentType: false,   
                statusCode:{
                    404:function(){
                        console.log('El sitio que quiere acceder no existe')
                    },
                    200: function(){
                        console.log('Sitio encontrado, solicitud en proceso')
                    }, 
                    500: function(){
                        console.log('Error en el servidor, proceso cancelado')
                    }
                },
                // processData: false, 
                success: function(data_response){
                    // mostrarDatos(response, 'file');
                    dataReturn = data_response;
                    console.log(data_response);
                    
                    console.log(data_response.Patrones.length);
                    $patrones = $('#patronesHallados');
                    $patrones.empty()

                    $tabla = $('<table class="table table-bordered"></table>');
                    $tabla.append('<thead class="thead-light"> <tr>'+
                                        '<th >Patron</th>'+
                                        '<th >Longitud</th>'+
                                        '<th >Ocurrencias</th>'+
                                        
                                    '</tr>');
                                    // '<th colspan = 2> Posciones</th>'++
                                    // '<tr>'+
                                    //     '<th>Secuencia</th>'+
                                    //     '<th>Posicion de inicio</th>'+
                                    // '</tr> </thead>');
                    $tablabody = $('<tbody></tbody>')
                    for(var i=0; i < data_response.Patrones.length; i++){
                        $fila = $("<tr onClick=mostrarDatosJSON("+i+") data-toggle='modal' data-target='#PatternsModal'></tr>");
                        
                        $fila.append('<td>'+data_response.Patrones[i].Patron+'</td>');
                        $fila.append('<td>'+data_response.Patrones[i].Longitud+'</td>');
                        $fila.append('<td>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Patron+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Longitud+'</td>');
                        // $fila.append('<td rowspan = '+data_response.Patrones[i].Posiciones.length+'>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        // for(var j=0; j< data_response.Patrones[i].Posiciones.length; j++){
                        //     $fila_seq=$('<tr></tr>');
                        //     if(j == 0){
                        //         $fila.append('<td>'+data_response.Patrones[i].Posiciones[j].sequencia+'</td>');
                        //         $fila.append('<td>'+data_response.Patrones[i].Posiciones[j].posicion+'</td>');
                        //         $tablabody.append($fila);
                        //     } else{
                        //         $fila_seq.append('<td>'+data_response.Patrones[i].Posiciones[j].sequencia+'</td>');
                        //         $fila_seq.append('<td>'+data_response.Patrones[i].Posiciones[j].posicion+'</td>');
                        //         $tablabody.append($fila_seq);
                        //     }
                        // }
                        $tablabody.append($fila);
                    }
                    $tabla.append($tablabody);
                    $patrones.append($tabla);
                    console.log('Success');
                }, error: function(error){
                    console.log('Error '+error);
                }
            });

        });
    });
    //-------------------------------------------


        