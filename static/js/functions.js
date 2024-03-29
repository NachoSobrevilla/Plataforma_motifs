    var dataReturn = {};
    var textseqs = 0;
    //Carga de la pagina 
    window.addEventListener('load', init, false)

     //Lectura de archivo Fasta al subirlo a la plataforma
    var inputFile = document.getElementById("inputFile");
    if (inputFile != null) {
        inputFile.addEventListener("change", function () {
            var file = this.files[0]; //toma el archivo contenido 
            var reader = new FileReader(); //crea un lector de archivos
            var offset = 0;
            var chunkSize = assingChunck(); //tamaño del bloque de lectura
            console.log("Leyendo archivo");
            //Lectura de archivo Fasta
            reader.onload = function () {
                console.log("Entra al onload");
                var view = new Uint8Array(reader.result);
                for (let index = 0; index < view.length; index++) {
                    if (String.fromCharCode(view[index]) == ">" ){
                        textseqs++;
                        console.log(textseqs);
                    }
                }
                
                offset += chunkSize;
                seek();
            }
            reader.onerror = function () { console.log("error"); };
            seek();
            function seek() {
                var end = offset + chunkSize;
                if (end <= file.size) {
                    var slice = file.slice(offset, end);
                    console.log(end);
                    reader.readAsArrayBuffer(slice);                    
                }else {
                    document.getElementById("sendSequenceFile").style.display = "block"; //muestra el boton de enviar
                    showConfigAlgorithm("file"); //mostrar el formulario de configuracion
                    return;
                }
                
            }
            function assingChunck(){
                if (file.size <= 1024){
                    return file.size
                }else if(file.size > 1024 && file.size <= 64*1024){
                    return 1024
                }else if(file.size > 64*1024 && file.size <= 256*1024){
                    return 64*1024
                }else if(file.size > 256*1024 && file.size <= 1024*1024){
                    return 256*1024
                }else if(file.size > 1024*1024 && file.size <= 64*1024*1024){
                    return 1024*1024
                }else if(file.size > 64*1024*1024 && file.size <= 256*1024*1024){
                    return 64*1024*1024
                }else{
                    return 256*1024*1024
                }
            }
        });
        } else {
            console.log("No se pudo mostrar el archivo");
            alert("No se pudo mostrar el archivo");
        }
    
    //Es la primera funcion 
    function init() {
        document.getElementById("formControlInputSelect").selectedIndex = -1;
        // document.getElementById("selectAlgorithm").selectedIndex = -1;
        // document.getElementById("minSup").value = '';
        limpiarCampoConfig();
        // document.getElementById("sendSequenceTxt").style.display = "none";
        // document.getElementById("sendSequenceFile").style.display = "none";
        // document.getElementById("resultForm").style.display = "none";
        // document.getElementById("principalFormFile").style.display = "none";
        // document.getElementById("principalFormTxt").style.display = "none";
        hideElements();
        // cargadorResultados();
        mostrarArchivos();
        // paginacionArchivos();

    
                // reader.onload = function (progressEvent) {
                //     // Entire file
                //     // console.log(this.result);
                //     // By lines
                //     textseqs = 0;
                //     var lines = this.result.split('\n'); //separa el archivo por lineas

                //     document.getElementById("previsualSequenceAnalisisFile").value = ''; //limpia el campo de texto
                //     console.log('cargando datos de archivo');
                //     for (var line = 0; line < lines.length; line++) { //recorre las lineas
                //         // document.getElementById("previsualSequenceAnalisisFile").value += lines[line] + "\n"; //agrega las lineas al campo de texto
                //         // if (lines[line].search('>') != -1) { //si la linea contiene una secuencia de fasta
                //         //     textseqs += 1; //cuenta las keys de la secuencia
                //         // }
                //         if(lines[line][0] == '>'){
                //             textseqs += 1;
                //         }else{
                //             continue;
                //         }

                //     }
                //     // document.getElementById("sendSequenceFile").style.display = "block"; //muestra el boton de enviar
                //     showConfigAlgorithm("file"); //mostrar el formulario de configuracion
                // };
                // reader.readAsText(file);
            
        //lectura de contenido de archivo
        // function readFile(evt){
        //     var file = evt.target.files[0];
        //     reader.readAsText(file);
        //     reader.onload = function(event){
        //         var txt = event.target.result.split("\n");
        //         document.getElementById("previsualSequenceAnalisisFile").value = txt;
        //     }
        // }
        ///////////////////////////////////

    }

    document.addEventListener("DOMContentLoaded", cargadorResultados);

    function cargadorResultados() {
        // var x = document.getElementById("cargaResultado");
        var y = document.getElementById("cargaResultadoChil");
        if (y.style.display === 'block' || y.style.display === '') { //Si el proceso de analsis fue iniciado
            y.style.display = 'none';
        } else {
            y.style.display = 'block';
            $("#resultados").empty();


        }
    }
    // function cargadorConfig(status = 0){
    //     if(status == 1){//Si el proceso de analsis fue iniciado
    //         document.getElementById("cargaresultados").style.display = "block";
    //     }      
    //     else{
    //         document.getElementById("cargaresultados").style.display = "none";
    //     }

    // }

    // function cargadorArch(status = 0){
    //     if(status == 1){//Si el proceso de analsis fue iniciado
    //         document.getElementById("cargaresultados").style.display = "block";
    //     }      
    //     else{
    //         document.getElementById("cargaresultados").style.display = "none";
    //     }

    // }


    function mostrarArchivos() {
        $.ajax({
            contentType: 'application/json',
            url: "/mostrarArchivos",
            type: 'POST',
            processData: false,
            contentType: false,
            statusCode: {
                404: function () {
                    console.log('El sitio que quiere acceder no existe')
                },
                200: function () {
                    console.log('Sitio encontrado, solicitud en proceso')
                },
                500: function () {
                    console.log('Error en el servidor, proceso cancelado')
                }
            },
            processData: false,
            success: function (response) {
                console.log(response);
                $archivos = $('#mostrarArchivos');
                $archivos.empty()

                $tabla = $('<table id="experimentos" class="table table-striped table-bordered table-responsive table-sm small"></table>');
                $tabla.empty();
                $tabla.append('<thead class="thead-light text-justify"> <tr>' +
                    '<th valing="middle" class="">#</th>' +
                    '<th valing="middle" class="">Nombre archivo</th>' +
                    '<th valing="middle" class="">Peso archivo (MB)</th>' +
                    '<th valing="middle" class="">Num Aprox bp</th>' +
                    '<th valing="middle" class="">Num Secuencias</th>' +
                    '<th valing="middle" class="">Secuencias</th>' +
                    '<th valing="middle" class="">Longitud de la(s) secuencia(s)</th>' +
                    '<th valing="middle" class="">Tipo entrada</th>' +
                    '<th valing="middle" class="">Algoritmo</th>' +
                    '<th valing="middle" class="">Min sup</th>' +
                    '<th valing="middle" class="">Tolerancia delante</th>' +
                    '<th valing="middle" class="">Tolerancia detras</th>' +
                    '<th valing="middle" class="">Longitud minima</th>' +
                    '<th valing="middle" class="">Impresion logo</th>' +
                    '<th valing="middle" class="">Num Patrones</th>' +
                    '<th valing="middle" class="">Longitud max patrones</th>' +
                    '<th valing="middle" class="">Num motifs</th>' +
                    '<th valing="middle" class="">Longitud max motifs</th>' +
                    '<th valing="middle" class="">Inicio</th>' +
                    '<th valing="middle" class="">Fin</th>' +
                    '<th valing="middle" class="">Duración</th>' +
                    '<th valing="middle" class="text-center">  JSON (Patrones Frecuentes) </th>' +
                    '<th valing="middle" class="text-center">  CVS (Patrones Frecuentes)  </th>' +
                    '<th valing="middle" class="text-center">  JSON (Motifs) </th>' +
                    '<th valing="middle" class="text-center">  XLSX (Motifs) </th>' +
                    // '<th>Archivo</th>'+
                    '</tr> </thead>');

                    "Nombre_Resultados"
                    // '<th> Descarga </th>'+                                    
                    // '<th> CVS </th>'+                                    
                $tablabody = $('<tbody></tbody>')
                for (var i = 0; i < response.length; i++) {
                    // archivo = response[i].split("_");
                    // console.log(response[i]);

                    $fila = $('<tr></tr>');

                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + i + '</td>');
                    for (var j = 0; j < response[i].length; j++) {
                        if (j == response[i].length - 1 ) {
                            $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/JSON/' + String(response[i][j]) + '/"' + '>' + 'Descargar JSON PF' + '</a></td>');
                            $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/CSV/' + String(response[i][j]) + '/"' + '>' + 'Descargar CSV' + '</a></td>');
                            $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/JSONMotif/' + String(response[i][j]) + '/"' + '>' + 'Descargar JSON M' + '</a></td>');
                            $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/XLSX/' + String(response[i][j]) + '/"' + '>' + 'Descargar XLSX' + '</a></td>');
                        }else{
                            $fila.append('<td class="text-center" align="center" valign="middle" >' + String(response[i][j]) + '</td>');
                        }
                    }
                    
                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[2] + '</td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[3] + '</td>');

                    


                    // // $fila.append('<td class="text-center" align="center" valign="middle">'+'<a '+ "onclick= mostrarArchivoAct('"+response[i]+"')"+' >'+response[i]+'</a></td>');
                    // // $fila.append('<td class="text-center" align="center" valign="middle" >'+$a.innerHTML()+'</td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  >' + 'Ver Archivo' + '</a></td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/JSON/' + String(response[i]) + '.json/"' + '>' + 'Descargar JSON' + '</a></td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/CSV/' + String(response[i]) + '.csv/"' + '>' + 'Descargar CSV' + '</a></td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >'+'<a class="btn btn-warning btn-sm my-2" href = "'+'"{{ url_for("getExpetimento"), filetype = "JSON", filename = "'+String(response[i])+'") }}'+'" target="_blank">'+'Descargar JSON'+'</a></td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >'+'<a class="btn btn-info form-control btn-lg my-2" href="{{ url_for('+'getExpetimento'+', filetype = '+'JSON'+', filename = '+response[i]+') }}>Descargar JSON</a> </td>');
                    // $fila.append('<td class="text-center">'+'<a onclick=descargarArchivos('+response[i]+",'JSON')>"+response[i]+'</a></td>');
                    // $fila.append('<td class="text-center">'+'<button type="button" class="btn btn-default" onclick=descargarArchivos('+response[i]+",'JSON')>"+' descargar archivo </button>'+'</td>');
                    // $fila.append('<td >'+'<button type="button" class="btn btn-default"> CVS </button>'+'</td>');

                    $tablabody.append($fila);
                }
                $tabla.append($tablabody);

                $archivos.append($tabla);
                // $archivos.append('<div class="text-center justify-content-center>' +
                //     '<ui class="pagination pager" id="paginas_exp">' + '</ui>' +
                //     '</div>'); //paginacion de la tabla de experimentos
                    
                $(document).ready(function () {
                    $('#experimentos').DataTable();
                    $('.dataTables_length').addClass('bs-select');
                });

                // $('#experimentos').paging({limit:5});
                // $('#paginas_exp').pagination({
                //     dataSource: response,
                //     pageSize: 10,
                //     autoHidePrevious: true,
                //     autoHideNext: true,
                //      function(data, pagination) {
                //         // template method of yourself
                //         var html = template(data);
                //         $('#tabla_exp').html(html);
                //     }
                // });

                // $("#experimentos").pageMe({
                //     pagerSelector:"#paginas_exp",
                //     activeColor: "#007bff",
                //     prevText: "Anterior",
                //     nextText: "Siguiente",
                //     showPrevNext: true,
                //     hidePageNumbers: false,
                //     perPage: 5
                // });


                console.log('Success: Experimentos');
            },
            error: function (error) {
                console.log('Error ' + error);
            }
        });
    }

    // function paginacionArchivos() {
    //     $("#experimentos").pageMe({
    //         pagerSelector:"#paginas_exp",
    //         activeColor: "#007bff",
    //         prevText: "Anterior",
    //         nextText: "Siguiente",
    //         showPrevNext: true,
    //         hidePageNumbers: false,
    //         perPage: 5
    //     });
    // }

    function mostrarArchivoAct(filename = '') {
        filename += '.json';
        console.log(filename);
        $.ajax({
            dataType: 'json',
            contentType: 'application/json',
            url: "/mostrarArchivoExp",
            data: JSON.stringify({
                'filename': filename
            }),
            type: 'POST',
            processData: false,
            statusCode: {
                404: function () {
                    console.log('El sitio que quiere acceder no existe')
                    alert('El archivo no existe')
                },
                200: function () {
                    console.log('Sitio encontrado, solicitud en proceso')
                    alert('El archivo encontrado')

                },
                500: function () {
                    console.log('Error en el servidor, proceso cancelado')
                    alert('Error en el servidor, proceso cancelado')
                }
            },
            processData: false,
            success: function (response) {
                $modal = $('#pmodalFile-body');
                // $modal.empty();



                $preModal = $('#premodalFile');
                $titeModal = $('#titleModalFile');

                $titeModal.empty();
                $titeModal.innerHTML = filename
                // $titeModal.append('<h5 class="modal-title" id="exampleModalLabel">'+filename+'</h5>');

                $preModal.empty();
                // $preModal.append('<pre>'+response+'</pre>');
                $preModal.innerHTML = response;
                $('#PatternsModalFiles').modal('show');

                // $archivos = $('#mostrarArchivoAct');
                // $archivos.empty()

                // $tabla = $('<table class="table table-bordered"></table>');
                // $tabla.append('<thead class="thead-light"> <tr>'+
                //                     '<th>#</th>'+
                //                     '<th>Archivo</th>'+
                //                     '<th> Descarga </th>'+                                    
                //                     '<th> CVS </th>'+                                    
                //                 '</tr> </thead>');
                // $tablabody = $('<tbody></tbody>')
                // for(var i=0; i < response.length; i++){
                //     $fila = $('<tr></tr>');
                //     $a = $('<a>Descargar JSON</a>');
                //     $fila.append('<td class="text-center" align="center" valign="middle" >'+i+'</td>');
                //     $fila.append('<td class="text-center" align="center" valign="middle" >'+'<a>'+response[i]+'</a></td>');
                //     // $fila.append('<td class="text-center" align="center" valign="middle" >'+$a.innerHTML()+'</td>');
                //     $fila.append	
                // }
            }
        })
    }

    function hideElements() {
        limpiarCamposFile();
        limpiarCamposTxt();


        document.getElementById("btnSentSeqText").style.display = "none";
        document.getElementById("btnSentSeqFile").style.display = "none";
        document.getElementById("principalFormFile").style.display = "none";

        // document.getElementById("resultForm").style.display = "none";
    }

    document.addEventListener("DOMContentLoaded", hideForms);

    //Funcion para esconder las formas principales de cada entrada
    function hideForms() {
        document.getElementById("principalFormFile").style.display = "none";
        document.getElementById("principalFormTxt").style.display = "none";
        document.getElementById("configAlgorithm").style.display = "none";
        document.getElementById("principalFormGenBank").style.display = "none";
        $("#resultados").empty();
        // document.getElementById("resultForm").style.display = "none";

    }
    //funcion para la limpiar los campos de entrada de texto
    function limpiarCamposTxt() {
        textseqs = 0;
        document.getElementById("inputManualADNText").value = '';
        document.getElementById("previsualSequenceAnalisis").value = '';
        document.getElementById("previsualSequenceAnalisis").rows = 1;
    }

    //funcion para limpiar los campos de la entrada de archivo
    function limpiarCamposFile() {
        document.getElementById("inputFile").value = '';
        // document.getElementById("previsualSequenceAnalisisFile").value = '';
    }

    //funcion para limpiar los campos 
    function limpiarCamposGenbank(){
        document.getElementById("infoGenBank").value = "";
        document.getElementById("infoGenBank").rows = 1;   
    }
    //funcion para limpiar los campos de configuración
    function limpiarCampoConfig() {
        document.getElementById("minSup").value = '';
        document.getElementById("LMC").value = '';
        document.getElementById("tolerancia_delante").value = '';
        document.getElementById("tolerancia_atras").value = '';
        
        document.getElementById("infoMinSup").title = 'Ingrese una secuencia de ADN para comenzar';
        document.getElementById("selectAlgorithm").selectedIndex = -1;
        document.getElementById("selectAlgorithm").children[0].style.display = "none";
        document.getElementById("selectAlgorithm").children[1].style.display = "none";
        document.getElementById("selectAlgorithm").children[2].style.display = "none";
        document.getElementById("infoAlgoritmo").title = 'Ingrese una secuencia de ADN para comenzar';
        document.getElementById("btnSentSeqText").display = "none";
        document.getElementById("btnSentSeqFile").display = "none";
        // document.getElementById("formControlInputSelect").selectedIndex = -1;
    }

    function selectProcess() {
        var item_selected = document.getElementById("formControlInputSelect");
        textseqs = 0;
        limpiarCampoConfig()
        document.getElementById("btnSentSeqFile").style.display = "none";
        document.getElementById("btnSentSeqText").style.display = "none";
        document.getElementById("btnSentGenBank").style.display = "none";
        document.getElementById("configAlgorithm").style.display = "none";
        switch (item_selected.options[item_selected.selectedIndex].value) {

            case "inputManual":
                limpiarCamposTxt();
                document.getElementById("principalFormTxt").style.display = "block";
                document.getElementById("principalFormFile").style.display = "none";
                document.getElementById("principalFormGenBank").style.display = "none";
                // document.getElementById("sendSequenceTxt").style.display = "none";
                break;

            case "inputFile":
                limpiarCamposFile();
                document.getElementById("principalFormFile").style.display = "block";
                document.getElementById("btnSentSeqFile").style.display = "none";
                document.getElementById("principalFormTxt").style.display = "none";
                break;

            case "inputGenBank":
                limpiarCamposGenbank();
                document.getElementById("principalFormGenBank").style.display = "block";
                document.getElementById("principalFormTxt").style.display = "none";
                document.getElementById("principalFormFile").style.display = "none";
                break;

                
            default:
                hideElements();
                break;
        }
    }

    function addStringSequences() {
        // alert("\n"+document.getElementById("inputManualADNText").value.toUpperCase());  
        if (document.getElementById("inputManualADNText").value.length != 0) {
            let n = 'ACTG';
            let pos = 0;
            let sequence = document.getElementById("inputManualADNText").value.trim().toUpperCase();
            sequence = sequence.replace(/ /g, "");
            console.log(sequence);
            let flag = false;
            for (i = 0; i < sequence.length; i++) {
                if (n.indexOf(sequence[i]) != -1) {
                    flag = true;
                } else {
                    flag = false;
                    pos = i + 1
                    break;
                }
            }
            if (flag == false) {
                // document.getElementById("inputManualADNText").value = '';
                alert("La sequencia no valida, error hallado en la posición " + pos + " de la sequencia");
            } else {
                document.getElementById("previsualSequenceAnalisis").value += (textseqs += 1) + ".-" + sequence + "\n";
                document.getElementById("previsualSequenceAnalisis").rows += 1;
                document.getElementById("inputManualADNText").value = '';
                // document.getElementById("sendSequenceTxt").style.display = "block"; 
                showConfigAlgorithm("txt"); //mostrar el formulario de configuracion

            }

        } else {
            alert("Ingrese una secuencia de ADN para su análisis")
        }
    }

    function infoSelectAlgorithm() {
        /*"Funcion para mostrar la informacion de los algoritmos y umbral(min_sup)"*/
        switch (document.getElementById("selectAlgorithm").options[document.getElementById("selectAlgorithm").selectedIndex].value) {
            case "bi":
                document.getElementById("infoMinSup").title = "El minimo soporte es el número minimo de apariciones de una subsecuencia dentro de una cadena de ADN para que pueda ser considerada un patrón frecuente.";
                document.getElementById("infoAlgoritmo").title = "Basado en indices es el algoritmo ideal para una secuencia de ADN y hallar sus patrones frecuentes de forma rápida.";
                document.getElementById("minSup").max = '';
                break;
            
            case "bi+":
                document.getElementById("infoMinSup").title = "El minimo soporte es el número minimo de apariciones de una subsecuencia dentro de un grupo secuencia del ADN para que pueda ser considerada un patrón frecuente";
                document.getElementById("infoAlgoritmo").title = "Basado en indices en multiples secuencias es un algoritmo que trabaja con grupos de secuencias para hallar sus patrones frecuentes de forma rápida.";
                document.getElementById("minSup").max = textseqs;
                break;
            
            case "gsp":
                document.getElementById("infoMinSup").title = "El minimo soporte es el número minimo de apariciones de una subsecuencia dentro de un grupo secuencia del ADN para que pueda ser considerada un patrón frecuente";
                document.getElementById("infoAlgoritmo").title =  "GSP es un algoritmo que trabaja con grupos de secuencias para hallar sus patrones frecuentes de forma rápida.";
                document.getElementById("minSup").max = textseqs;
                break;

            default:
                document.getElementById("infoMinSup").title = "Ingrese una secuencia de ADN para comenzar";
                document.getElementById("infoAlgoritmo").title = "Ingrese una secuencia de ADN para comenzar";
                document.getElementById("minSup").max = '';
                break;
        }
        
    }

    function cleanStringSequences() {
        var mensaje = confirm("¿Está seguro que desea limpiar la lista de secuencias?");
        if (mensaje == true) {
            limpiarCamposTxt();
            document.getElementById("configAlgorithm").style.display = "none";
            alert("Se han limpiado los campos");
        }
    }

    function newProcess() {
        var mensaje = confirm("¿Está seguro que desea iniciar un nuevo proceso?");
        if (mensaje == true) {
            textseqs = 0;
            dataReturn = {};
            hideForms();
            hideElements();
            limpiarCamposFile();
            limpiarCamposTxt();
            limpiarCampoConfig();
            mostrarArchivos();
            document.getElementById("formControlInputSelect").selectedIndex = -1;
            alert("Se han limpiado los campos")
        }
    }

    function showConfigAlgorithm(process) {
        limpiarCampoConfig()
        btntxt  =document.getElementById("btnSentSeqText");
        btnfile =document.getElementById("btnSentSeqFile");

        if (textseqs < 2) {
            document.getElementById("selectAlgorithm").children[0].style.display = "block";
            document.getElementById("selectAlgorithm").children[1].style.display = "none";
            document.getElementById("selectAlgorithm").children[2].style.display = "none";

        } else {
            document.getElementById("selectAlgorithm").children[0].style.display = "none";
            document.getElementById("selectAlgorithm").children[1].style.display = "block";
            document.getElementById("selectAlgorithm").children[2].style.display = "block";
        }

        if ((process == "txt"  || btnfile.style.display == "block")) {
            btnfile.style.display = "none";
            btntxt.style.display = "block";
            // if (btnfile.style.display == "block"){ btnfile.style.display = "none"; }
            
        } else if (process == "file" || btntxt.style.display == "block") {
            btntxt.style.display = "none";
            btnfile.style.display = "block";
            // if (btntxt.style.display == "block"){ btntxt.style.display = "none"; 
            // if(btntxt.style.display == "block"){ btntxt.style.display = "none"; }
              
        }

        document.getElementById("configAlgorithm").style.display = "block";
        // document.getElementById("formControlInputSelect").selectedIndex = -1;
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

    function formateoTxt() {
        var txt = document.getElementById("previsualSequenceAnalisis").value;
        // var lines = txt.split('\n').map(line => line.split('.- ',2));
        const listSequence = txt.split("\n").map(line => line.split('.-', 2));
        listSequence.pop();
        console.log(listSequence);
        return listSequence;
    }

    function mostrarDatosJSON(p, tipo) {
        // var pos = dataReturn.Patrones[p].Posiciones;
        if (tipo == 1) {
            var pos = dataReturn.Patrones_Frecuentes.Patrones[p].Posiciones;
        } else if (tipo == 0) {
            var pos = dataReturn.Motifs.Alineaciones[p].alineamientos;
        }
        
        console.log(pos);

        var table = document.createElement('table');
        var thead = document.createElement('thead');
        var tbody = document.createElement('tbody');
        var th = document.createElement('th');
        var td = document.createElement('td');
        td.style.alignContent = "center";
        var tr = document.createElement('tr');

        table.style.width = "100%";
        table.classList.add("table");
        table.classList.add("table-striped");

        table.classList.add("table-responsive-sm");


        table.appendChild(thead);
        table.appendChild(tbody);
        th.classList.add("text-center");

        if (tipo == 0) {
            th.innerHTML = 'Alineamiento';
            tr.appendChild(th);
        }

        th = document.createElement('th');
        th.innerHTML = 'Secuencia';
        tr.appendChild(th);
        
        th = document.createElement('th');
        th.innerHTML = 'Posicion';
        tr.appendChild(th);

        

        thead.appendChild(tr);


        for (var i = 0; i < pos.length; i++) {
            tr = document.createElement('tr');
            var td = document.createElement('td');

            // td.style.alignContent = "center";
            if (tipo == 0) {
                td.classList.add("text-center");
                td.align = "center";
                td.vAlign = "middle";
                td.innerHTML = pos[i].alineamiento;
                tr.appendChild(td);
            }

            td = document.createElement('td');
            td.classList.add("text-center");
            td.align = "center";
            td.vAlign = "middle";
            td.innerHTML = pos[i].secuencia;
            td.style.alignContent = "center";
            tr.appendChild(td);

            td = document.createElement('td');
            td.classList.add("text-center");
            td.align = "center";
            td.vAlign = "middle";
            td.innerHTML = pos[i].posicion;
            td.style.alignContent = "center";
            tr.appendChild(td);

            

            tbody.appendChild(tr);
        }
        // document.getElementById("resultado").appendChild(table);

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
    $(document).ready(function () {
        $("#sendSequenceTxt").click(function () {
            if (verificarValores("text") == true) {
                cargadorResultados();
                var sequences = formateoTxt();
                var k = [];
                var s = [];
                sequences.forEach(function (element) {
                    k.push(element[0]);
                    s.push(element[1]);
                });

                console.log(k);
                console.log(s);
                var sendData = [{
                    "algoritmo": $('#selectAlgorithm').val(),
                    "min_sup": $('#minSup').val(),
                    "keys_sequences": k,
                    "sequence": s,
                    "input": "Manual",
                    "longtud_minina": $('#LMC').val(),
                    "tolerancia_delante":$('#tolerancia_delante').val(),
                    "tolerancia_atras":$('#tolerancia_atras').val(),
                    "imprimir_logo":$('#checkLogo').is(':checked')
                }];
                console.log(sendData);
                $.ajax({
                    dataType: "json",
                    contentType: 'application/json',
                    url: "/analisisText",
                    data: JSON.stringify(sendData),
                    type: 'POST',
                    statusCode: {
                        404: function () {
                            cargadorResultados();
                            console.log('El sitio que quiere acceder no existe')
                            alert('El sitio que quiere acceder no existe')
                        },
                        200: function () {
                            console.log('Sitio encontrado, solicitud en proceso')
                            alert('Ejecución finiliza con éxito')
                        },
                        500: function () {
                            cargadorResultados();
                            console.log('Error en el servidor, proceso cancelado')
                            alert('Error en el servidor, proceso cancelado')
                        }
                    },
                    processData: false,
                    success: function (data_response) {
                        // console.log('regreso:', data_response);
                        // console.log('longitud respose: ', data_response.length);
                        // console.log('longitud return: ', dataReturn.length);
                        console.log(data_response);
                        // console.log(data_response2);
                        if (dataReturn.length > 0) {
                            dataReturn.empty();
                        }
                        dataReturn = data_response;
                        cargadorResultados();
                        despliegeResultados(data_response);
                        // console.log(data_response);
                        // console.log(data_response.Patrones.length);
                        // $patrones = $('#resultados');
                        // $patrones.empty()

                        // $tabla = $('<table class="table table-bordered"></table>');
                        // $tabla.append('<thead class="thead-light"> <tr>'+
                        //                     '<th>Patron</th>'+
                        //                     '<th>Longitud</th>'+
                        //                     '<th>No. de ocurrencias</th>'+
                        //                     '<th>Posiciones</th>');

                        // $tablabody = $('<tbody></tbody>')
                        // for(var i=0; i < data_response.Patrones.length; i++){
                        //     $fila = $("<tr></tr>");

                        //     $fila.append('<td>'+data_response.Patrones[i].Patron+'</td>');
                        //     $fila.append('<td>'+data_response.Patrones[i].Longitud+'</td>');
                        //     $fila.append('<td>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        //     $fila.append('<td>'+'<button type="button" class="alert"'+"onClick=mostrarDatosJSON("+i+")>"+"Posiciones"+'</button>'+'</td>');

                        //     $tablabody.append($fila);
                        // }
                        // $tabla.append($tablabody);
                        // $patrones.append($tabla);

                        console.log('Success');
                    },
                    error: function (error) {
                        console.log('Error ' + error);
                    }
                });
            }
        });
    });
    //-------------------------------------------

    ////-------------------Para archivos -------------------------------------
    $(document).ready(function () {
        $("#sendSequenceFile").click(function () {
            // var dato_archivo = $('#inputFile').prop("files")[0];
            // var dato_algo = $('#selectAlgorithm').val();
            // var dato_minsup = $('#minSup').val(); 
            if (verificarValores("file") == true) {
                cargadorResultados();
                console.log($('#inputFile').prop("files")[0]);
                console.log($('#formControlInputSelect').val());

                var form_data = new FormData();
                console.log($('#tolerancia_delante').val());
                console.log($('#tolerancia_atras').val());
                console.log($('#LMC').val());
                console.log($('#checkLogo').is(':checked'));

                form_data.append('Algoritmo', $('#selectAlgorithm').val());
                form_data.append('min_sup', $('#minSup').val());
                form_data.append('file', $('#inputFile').prop("files")[0]);
                form_data.append('input', 'Archivo');
                form_data.append('longtud_minina', $('#LMC').val());
                form_data.append('tolerancia_delante', $('#tolerancia_delante').val());
                form_data.append('tolerancia_atras', $('#tolerancia_atras').val());
                form_data.append('imprimir_logo', $('#checkLogo').is(':checked'));
                // form_data.append('input', $('#formControlInputSelect').val());

                $.ajax({
                    url: '/analisisFile',
                    data: form_data,
                    type: 'POST',
                    processData: false,
                    contentType: false,
                    statusCode: {
                        404: function () {
                            cargadorResultados();
                            console.log('El sitio que quiere acceder no existe');
                            alert('El sitio que quiere acceder no existe');

                        },
                        200: function () {
                            console.log('Sitio encontrado, solicitud en proceso');
                            alert('Ejecución finiliza con éxito');

                        },
                        500: function () {
                            cargadorResultados();
                            console.log('Error en el servidor, proceso cancelado');
                            alert('Error en el servidor, proceso cancelado');
                        }
                    },
                    // processData: false, 
                    success: function (data_response) {
                        // mostrarDatos(response, 'file');
                        // console.log('longitud respose: ', data_response.length);
                        // console.log('longitud return: ', dataReturn.length);
                        console.log(data_response);


                        if (dataReturn.length > 0) {
                            dataReturn.empty();
                        }

                        dataReturn = data_response;
                        cargadorResultados();
                        despliegeResultados(data_response);
                        // $patrones = $('#resultados');
                        // $patrones.empty()

                        // $tabla = $('<table class="table table-bordered"></table>');
                        // $tabla.append('<thead class="thead-light"> <tr>'+
                        //                     '<th >Patron</th>'+
                        //                     '<th >Longitud</th>'+
                        //                     '<th >Ocurrencias</th>'+
                        //                     '<th>Posiciones</th>'+
                        //                 '</tr>');
                        // $tablabody = $('<tbody></tbody>')
                        // for(var i=0; i < data_response.Patrones.length; i++){
                        //     $fila = $("<tr onClick=mostrarDatosJSON("+i+") data-toggle='modal' data-target='#PatternsModal'></tr>");

                        //     $fila.append('<td>'+data_response.Patrones[i].Patron+'</td>');
                        //     $fila.append('<td>'+data_response.Patrones[i].Longitud+'</td>');
                        //     $fila.append('<td>'+data_response.Patrones[i].Ocurrencias+'</td>');
                        //     $fila.append('<td>'+'<button type="button" class="alert"'+"onClick=mostrarDatosJSON("+i+")>"+"Posiciones"+'</button>'+'</td>');

                        //     $tablabody.append($fila);
                        // }
                        // $tabla.append($tablabody);
                        // $patrones.append($tabla);
                        console.log('Success');
                    },
                    error: function (error) {
                        console.log('Error ' + error);
                    }
                });
            }
        });
    });


    //-------------------------------------------

    function despliegeResultados(data) {
        console.log(data);
        $patrones = $('#resultados');
        $patrones.empty()

        $tabs = $('<ul class="nav nav-tabs nav-justified"></ul>');
        $tabs.append('<li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#tabMotifs">Motifs</a></li>');
        $tabs.append('<li class="nav-item"><a class="nav-link" data-toggle="tab" href="#tabPatrones">Patrones</a></li>');
        $divContenedor = $('<div class="tab-content"></div>');
        $divContenedorMotif = $('<div id="tabMotifs" class="tab-pane fade show active table-responsive"></div>');
        $divContenedorPatrones = $('<div id="tabPatrones" class="tab-pane fade table-responsive"></div>');
        

        $tabla = $('<table id="resultadoMotifs" class="table table-striped table-bordered table-sm small" cellpadding="4" ></table>');
        $tabla.empty();
        $tabla.append('<thead class="thead-light text-center " align = "center"> <tr>' +
            '<th>#</th>' +
            '<th>Patron</th>' +
            '<th>Motif</th>' +
            '<th>Expresión Regular</th>' +
            '<th>Ocurrencias del Patron</th>' +
            '<th>Longitud del motif </th>' +
            '<th>Traducciona a aminoáciodos </th>' +
            '<th>Posiciones Especificas</th>' +

            // '<th>Patron</th>' +
            // '<th>Longitud</th>' +
            // '<th>Ocurrencias</th>' +
            // '<th>Posiciones</th>' +
            '</tr> </thead>');
        $tablabody = $('<tbody></tbody>');
        for (var i = 0; i < data.Motifs.Alineaciones.length; i++) {
        // for (var i = 0; i < data.Patrones.length; i++) {
            // $fila = $("<tr data-toggle='modal' data-target='#PatternsModal'></tr>");
            $fila = $("<tr></tr>");
            // console.log(data.Alineaciones[i]);
            // $fila = $("<tr data-toggle='modal' data-target='#MotifsModal'></tr>");
            $fila.append('<td>' + (i + 1) + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].patron + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].motif + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].expresion_regular + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].ocurrencias_patron + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].longitud_motif + '</td>');
            $fila.append('<td>' + data.Motifs.Alineaciones[i].traduccion_aminoacido + '</td>');
            // $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Patron + '</td>');
            // $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Longitud + '</td>');
            // $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Ocurrencias + '</td>');
            // $fila.append('<td class="text-center" align="center" valign="middle" >' + '<button type="button" class="btn  btn-warning"' + "onClick=mostrarDatosJSON(" + i + ")>" + "Posiciones" + '</button>' + '</td>');
            $fila.append('<td class="text-center" align="center" valign="middle"'+"data-toggle='modal' data-target='#PatternsModal'"+'>'+ '<button type="button" class="btn  btn-warning"' + "onClick=mostrarDatosJSON(" + i + ","+0+")>" + "Detalles" + '</button>' + '</td>');

            $tablabody.append($fila);
        }

        // $patrones.classList.add('border border-primary');
        $patrones.append('<h3 class="h5 text-info text-center p-2 m-2">Resultados</h3>');
        $patrones.append($tabs);
        
        $divContenedorMotif.append(document.createElement('br'));
        $tabla.append($tablabody);
        $divContenedorMotif.append($tabla);


        $tabla2 = $('<table id="resultadoPatrones" class="table table-striped  table-bordered " cellpadding="5" ></table>');
        $tabla2.empty();
        $tabla2.append('<thead class="thead-light text-center " align = "center"> <tr>' +
            '<th>#</th>' +
            '<th>Patron</th>' +
            '<th>Longitud</th>' +
            '<th>Ocurrencias</th>' +
            '<th>Posiciones</th>' +
            '</tr> </thead>');
        $tablabody2 = $('<tbody></tbody>');
        for (var i = 0; i < data.Patrones_Frecuentes.Patrones.length; i++) {
        // for (var i = 0; i < data.Patrones.length; i++) {
            // $fila = $("<tr onClick=mostrarDatosJSON("+i+") data-toggle='modal' data-target='#PatternsModal'></tr>");
            // console.log(data.Alineaciones[i]);
            $fila2 = $("<tr></tr>");
            $fila2.append('<td>' + (i + 1) + '</td>');
            $fila2.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones_Frecuentes.Patrones[i].Patron + '</td>');
            $fila2.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones_Frecuentes.Patrones[i].Longitud + '</td>');
            $fila2.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones_Frecuentes.Patrones[i].Ocurrencias + '</td>');
            $fila2.append('<td class="text-center" align="center" valign="middle"'+"data-toggle='modal' data-target='#PatternsModal'"+'>' + '<button type="button" class="btn  btn-warning"' + "onClick=mostrarDatosJSON(" + i + ","+1+")>" + "Detalles" + '</button>' + '</td>');
           

            $tablabody2.append($fila2);
        }

        $divContenedorPatrones.append(document.createElement('br'));
        $tabla2.append($tablabody2);
        $divContenedorPatrones.append($tabla2);

        $divContenedor.append($divContenedorMotif);
        $divContenedor.append($divContenedorPatrones);

        $patrones.append($divContenedor);
        $patrones.append("<br>");

        var bttdiv = document.createElement('div');
        bttdiv.id = 'bttnFilesDownload';
        bttdiv.classList.add("form-group");
        bttdiv.classList.add("form-row");
        bttdiv.classList.add("m-2");



        // var a = document.createElement('a');
        // a.href = 'data:application/vnd.ms-excel,'+ encodeURIComponent($tabla); 
        // a.download = 'Patrones.xls';
        // a.innerHTML = 'Descargar Tabla';

        // boton de decarga de archivo json
        var aJSON = document.createElement('a');
        aJSON.id = "downCurrentFileJSON";
        aJSON.href = "/descarga/experimentos/currentJSON/" //"{{ url_for('getExpetimento', filetype = 'currentJSON') }}";
        aJSON.target = "_blank";
        aJSON.classList.add("btn");
        aJSON.classList.add("btn-info");
        aJSON.classList.add("form-control");
        aJSON.classList.add("btn-lg");
        aJSON.classList.add("my-2");
        aJSON.title = "Descarga los resultados en un archivo CSV";
        aJSON.innerHTML = "Descargar JSON Patrones frecuentes";

        // $patrones.appendChild(a)
        //$patrones.append(a);
        // $patrones.append(aJSON);
        bttdiv.append(aJSON);
        bttdiv.append(document.createElement('br'));
        // $patrones.append("<br>");

        //boton de descarga de archivo csv
        var aCSV = document.createElement('a');
        aCSV.id = "downCurrentFileCSV";
        aCSV.href = "/descarga/experimentos/currentCSV/" //"{{ url_for('getExpetimento', filetype = 'currentJSON') }}";
        aCSV.target = "_blank";
        aCSV.classList.add("btn");
        aCSV.classList.add("btn-info");
        aCSV.classList.add("form-control");
        aCSV.classList.add("btn-lg");
        aCSV.classList.add("my-2");
        aCSV.title = "Descarga los resultados en un archivo CSV";
        aCSV.innerHTML = "Descargar CSV Patrones frecuentes";

        bttdiv.append(aCSV);
        bttdiv.append(document.createElement('br'));

        //boton de descarga de archivo xlsx motifs
        var aXLS = document.createElement('a');
        aXLS.id = "downCurrentFileXLS";
        aXLS.href = "/descarga/experimentos/currentXLSX/" //"{{ url_for('getExpetimento', filetype = 'currentJSON') }}";
        aXLS.target = "_blank";
        aXLS.classList.add("btn");
        aXLS.classList.add("btn-info");
        aXLS.classList.add("form-control");
        aXLS.classList.add("btn-lg");
        aXLS.classList.add("my-2");
        aXLS.title = "Descarga los resultados en un archivo xls de los motifs hallados";
        aXLS.innerHTML = "Descargar XLSX Motifs";

        bttdiv.append(aXLS);
        bttdiv.append(document.createElement('br'));

        //boton de descarga de archivo xlsx motifs
        var aJSONm = document.createElement('a');
        aJSONm.id = "downCurrentFileJSONm";
        aJSONm.href = "/descarga/experimentos/currentJSONMotif/" //"{{ url_for('getExpetimento', filetype = 'currentJSON') }}";
        aJSONm.target = "_blank";
        aJSONm.classList.add("btn");
        aJSONm.classList.add("btn-info");
        aJSONm.classList.add("form-control");
        aJSONm.classList.add("btn-lg");
        aJSONm.classList.add("my-2");
        aJSONm.title = "Descarga los resultados en un archivo JSON de los motifs hallados";
        aJSONm.innerHTML = "Descargar JSON Motifs";

        bttdiv.append(aJSONm);
        bttdiv.append(document.createElement('br'));

        //boton de nuevo proceso
        var newprocess = document.createElement('button');
        newprocess.id = "newprocess";
        newprocess.classList.add("btn");
        newprocess.classList.add("btn-danger");
        newprocess.classList.add("form-control");
        newprocess.classList.add("btn-lg");
        newprocess.classList.add("my-2");
        newprocess.onclick = function () {
            newProcess()
        };
        // newprocess.addEventListener("click",newProcess);
        newprocess.title = "Inicia un nueva ejecución";
        newprocess.innerHTML = "Nueva ejecución";

        bttdiv.append(newprocess);
        // $patrones.appendChild(a)
        //$patrones.append(a);
        $patrones.append(bttdiv);

        $(document).ready(function () {
            $('#resultadoMotifs').DataTable();
            $('#resultadoPatrones').DataTable();
            $('.dataTables_length').addClass('bs-select');

        });

    }

    function descargarArchivos(name = "x", type = "currentJSON") {
        // var a = document.createElement("a");
        // var file = new Blob([dataReturn], {type: type});
        // a.href = URL.createObjectURL(file);
        // a.download = name;
        // a.click();
        var data = [{
            "filename": name,
            "filetype": type
        }];
        console.log(data);
        $.ajax({
            dataType: "json",
            contentType: 'application/json',
            url: '/descargaArchivo',
            data: JSON.stringify(data),
            type: 'POST',
            statusCode: {
                404: function () {
                    console.log('El sitio que quiere acceder no existe')
                    alert('El sitio que quiere acceder no existe')
                },
                200: function () {
                    console.log('Sitio encontrado, solicitud en proceso')
                    // alert('El archivo no existe')
                },
                500: function () {
                    console.log('Error en el servidor, proceso cancelado')
                    alert('Error en el servidor, proceso cancelado')
                }
            },
            // processData: false, 
            success: function (dataresponse) {

                console.log('Success');
                console.log(dataresponse);
                var a = document.createElement("a");
                var file = new Blob(dataresponse, {
                    type: "text/json"
                });
                a.href = URL.createObjectURL(file);
                a.download = name;
                a.click();

            },
            error: function (error) {
                console.log('Error ' + error.responseText);
            }
        });
    }

    function verificarValores(typeprocess) {
        if (typeprocess == 'file') {
            if ($('#inputFile').val() == '') {
                alert('Debe seleccionar un archivo FASTA');
                return false;
            } else if ($('#minSup').val() == '') {
                alert('Debe ingresar un valor para umbral');
                return false;
            } else if ($('#LMC').val() == '') {
                alert('Debe ingresar un valor para la longitud minima');
                return false;
            } else if ($('#tolerancia_atras').val() == '') {
                alert('Debe ingresar un valor para tolerancia detras');
                return false;
            } else if ($('#tolerancia_delante').val() == '') {
                alert('Debe ingresar un valor para tolerancia delante');
                return false;
            } else if ($('#selectAlgorithm').val() == -1) {
                alert('Debe seleccionar un algoritmo');
                return false;
            } else {
                return true;
            }
        } else if (typeprocess == 'text') {
            if ($('#previsualSequenceAnalisist').val() == '') {
                alert('Debe ingresar las secuencias de ADN para su analisis');
                return false;
            } else if ($('#minSup').val() == '') {
                alert('Debe ingresar un valor del umbral');
                return false;
            } else if ($('#LMC').val() == '') {
                alert('Debe ingresar un valor para la longitud minima');
                return false;
            } else if ($('#tolerancia_atras').val() == '') {
                alert('Debe ingresar un valor para tolerancia detras');
                return false;
            } else if ($('#tolerancia_delante').val() == '') {
                alert('Debe ingresar un valor para tolerancia delante');
                return false;
            } else if ($('#selectAlgorithm').val() == -1) {
                alert('Debe seleccionar un algoritmo');
                return false;
            } else {
                return true;
            }
        }
    }

    // $(document).ready(function(){
    //     $("#experimentos").pageMe({
    //         pagerSelector:"#paginas_exp",
    //         activeColor: "#007bff",
    //         prevText: "Anterior",
    //         nextText: "Siguiente",
    //         showPrevNext: true,
    //         hidePageNumbers: false,
    //         perPage: 5
    //     });
    // });