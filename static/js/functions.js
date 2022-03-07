    var dataReturn = {};
    var textseqs = 0;
    window.addEventListener('load', init, false)

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

        //Lectura de archivo Fasta al subirlo a la plataforma
        var inputFile = document.getElementById("inputFile");
        if (inputFile != null) {
            inputFile.addEventListener("change", function () {
                var file = this.files[0]; //toma el archivo contenido 
                var reader = new FileReader(); //crea un lector de archivos
                reader.onload = function (progressEvent) {
                    // Entire file
                    // console.log(this.result);
                    // By lines
                    textseqs = 0;
                    var lines = this.result.split('\n'); //separa el archivo por lineas

                    document.getElementById("previsualSequenceAnalisisFile").value = ''; //limpia el campo de texto
                    console.log('cargando datos de archivo');
                    for (var line = 0; line < lines.length; line++) { //recorre las lineas
                        // document.getElementById("previsualSequenceAnalisisFile").value += lines[line] + "\n"; //agrega las lineas al campo de texto
                        // if (lines[line].search('>') != -1) { //si la linea contiene una secuencia de fasta
                        //     textseqs += 1; //cuenta las keys de la secuencia
                        // }
                        if(lines[line][0] == '>'){
                            textseqs += 1;
                        }else{
                            continue;
                        }

                    }
                    // document.getElementById("sendSequenceFile").style.display = "block"; //muestra el boton de enviar
                    showConfigAlgorithm("file"); //mostrar el formulario de configuracion
                };
                reader.readAsText(file);
            });
        } else {
            console.log("No se pudo mostrar el archivo");
        }
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
            $("#patronesHallados").empty();


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

                $tabla = $('<table id="experimentos" class="table  table-striped table-bordered table-sm small"></table>');
                $tabla.empty();
                $tabla.append('<thead class="thead-light text-justify"> <tr>' +
                    '<th valing="middle" class="">#</th>' +
                    '<th valing="middle" class="">Algoritmo</th>' +
                    '<th valing="middle" class="">Umbral</th>' +
                    '<th valing="middle" class="">Tipo de entrada</th>' +
                    '<th valing="middle" class="">Nombre <br><small>(archivo fasta o manual)</small> </th>' +
                    '<th valing="middle" class="">Num. de secuencias analizadas</th>' +
                    '<th valing="middle" class="">Num. de patrones hallados</th>' +
                    '<th valing="middle" class="">Fecha y Hora del Análisis</th>' +
                    '<th valing="middle" class="">Duración del Análisis <small>(segundos)</small></th>' +
                    '<th valing="middle" class="text-center"> Ver </th>' +
                    '<th valing="middle" class="text-center"> JSON </th>' +
                    '<th valing="middle" class="text-center"> CVS </th>' +
                    // '<th>Archivo</th>'+
                    // '<th> Descarga </th>'+                                    
                    // '<th> CVS </th>'+                                    
                    '</tr> </thead>');
                $tablabody = $('<tbody></tbody>')
                for (var i = 0; i < response.length; i++) {
                    archivo = response[i].split("_");
                    console.log(response[i]);
                    $fila = $('<tr></tr>');

                    $fila.append('<td class="text-center" align="center" valign="middle" >' + i + '</td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[1] + '</td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[2] + '</td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[3] + '</td>');

                    if (archivo[3] == "Archivo") {
                        $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[4].replace('-', '_') + '.fasta' + '</td>');
                    } else {
                        $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[4] + '</td>');
                    }
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[5] + '</td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + archivo[6] + '</td>');
                    fh = archivo[7]
                    fh = fh.replaceAll('&', ' ');
                    fh = fh.replaceAll('d', '/');
                    fh = fh.replaceAll('-', ':');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + fh + '</td>');
                    d = archivo[8]
                    d = d.replace('D-', '');
                    d = d.replace('&', '.');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + d + '</td>');


                    // $fila.append('<td class="text-center" align="center" valign="middle">'+'<a '+ "onclick= mostrarArchivoAct('"+response[i]+"')"+' >'+response[i]+'</a></td>');
                    // $fila.append('<td class="text-center" align="center" valign="middle" >'+$a.innerHTML()+'</td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  >' + 'Ver Archivo' + '</a></td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/JSON/' + String(response[i]) + '.json/"' + '>' + 'Descargar JSON' + '</a></td>');
                    $fila.append('<td class="text-center" align="center" valign="middle" >' + '<a class="btn btn-warning btn-sm my-2" target="_blank"  href="/descarga/experimentos/CSV/' + String(response[i]) + '.csv/"' + '>' + 'Descargar CSV' + '</a></td>');
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
                //     callback: function(data, pagination) {
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


        document.getElementById("sendSequenceTxt").style.display = "none";
        document.getElementById("sendSequenceFile").style.display = "none";
        document.getElementById("principalFormFile").style.display = "none";

        // document.getElementById("resultForm").style.display = "none";
    }

    document.addEventListener("DOMContentLoaded", hideForms);

    function hideForms() {
        document.getElementById("principalFormFile").style.display = "none";
        document.getElementById("principalFormTxt").style.display = "none";
        document.getElementById("configAlgorithm").style.display = "none";
        $("#patronesHallados").empty();
        // document.getElementById("resultForm").style.display = "none";
    }

    function limpiarCamposTxt() {
        textseqs = 0;
        document.getElementById("inputManualADNText").value = '';
        document.getElementById("previsualSequenceAnalisis").value = '';
        document.getElementById("previsualSequenceAnalisis").rows = 1;
    }

    function limpiarCamposFile() {
        document.getElementById("inputFile").value = '';
        document.getElementById("previsualSequenceAnalisisFile").value = '';
    }

    function limpiarCampoConfig() {
        document.getElementById("minSup").value = '';
        document.getElementById("infoMinSup").title = 'Ingrese una secuencia de ADN para comenzar';
        document.getElementById("selectAlgorithm").selectedIndex = -1;
        document.getElementById("selectAlgorithm").children[0].style.display = "none";
        document.getElementById("selectAlgorithm").children[1].style.display = "none";
        document.getElementById("selectAlgorithm").children[2].style.display = "none";
        document.getElementById("infoAlgoritmo").title = 'Ingrese una secuencia de ADN para comenzar';


        // document.getElementById("formControlInputSelect").selectedIndex = -1;
    }

    function selectProccess() {
        var item_selected = document.getElementById("formControlInputSelect");
        textseqs = 0;
        limpiarCampoConfig()
        switch (item_selected.options[item_selected.selectedIndex].value) {

            case "inputManual":
                limpiarCamposTxt();
                document.getElementById("principalFormTxt").style.display = "block";
                document.getElementById("principalFormFile").style.display = "none";
                // document.getElementById("sendSequenceTxt").style.display = "none";
                break;

            case "inputFile":
                limpiarCamposFile();
                document.getElementById("principalFormFile").style.display = "block";
                document.getElementById("sendSequenceFile").style.display = "none";
                document.getElementById("principalFormTxt").style.display = "none";

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
            alert("Se han limpiado los campos");



        }
    }

    function showConfigAlgorithm(process) {
        limpiarCampoConfig()

        if (textseqs < 2) {
            document.getElementById("selectAlgorithm").children[0].style.display = "block";
            document.getElementById("selectAlgorithm").children[1].style.display = "none";
            document.getElementById("selectAlgorithm").children[2].style.display = "none";

        } else {
            document.getElementById("selectAlgorithm").children[0].style.display = "none";
            document.getElementById("selectAlgorithm").children[1].style.display = "block";
            document.getElementById("selectAlgorithm").children[2].style.display = "block";
        }

        if (process == "txt") {
            document.getElementById("sendSequenceTxt").style.display = "block";
            document.getElementById("sendSequenceFile").style.display = "none";
        } else if (process == "file") {
            document.getElementById("sendSequenceTxt").style.display = "none";
            document.getElementById("sendSequenceFile").style.display = "block";
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

    function mostrarDatosJSON(p) {
        var pos = dataReturn.Patrones[p].Posiciones;
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


        table.appendChild(thead);
        table.appendChild(tbody);
        th.classList.add("text-center");

        th.innerHTML = 'Sequencia';
        tr.appendChild(th);
        th = document.createElement('th');
        th.innerHTML = 'Posicion';

        tr.appendChild(th);
        thead.appendChild(tr);


        for (var i = 0; i < pos.length; i++) {
            tr = document.createElement('tr');

            var td = document.createElement('td');

            // td.style.alignContent = "center";
            td.classList.add("text-center");
            td.align = "center";
            td.vAlign = "middle";
            td.innerHTML = pos[i].sequencia;
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
                    "input": "Manual"
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
                        if (dataReturn.length > 0) {
                            dataReturn.empty();
                        }
                        dataReturn = data_response;
                        cargadorResultados();
                        despliegePatrones(data_response);
                        // console.log(data_response);
                        // console.log(data_response.Patrones.length);
                        // $patrones = $('#patronesHallados');
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

                form_data.append('Algoritmo', $('#selectAlgorithm').val());
                form_data.append('min_sup', $('#minSup').val());
                form_data.append('file', $('#inputFile').prop("files")[0]);
                form_data.append('input', 'Archivo');
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

                        if (dataReturn.length > 0) {
                            dataReturn.empty();
                        }

                        dataReturn = data_response;
                        cargadorResultados();
                        despliegePatrones(data_response);
                        // $patrones = $('#patronesHallados');
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

    function despliegePatrones(data) {
        console.log(data);
        $patrones = $('#patronesHallados');
        $patrones.empty()

        $tabla = $('<table id="resultadoPatrones" class="table table-bordered " cellpadding="5" ></table>');
        $tabla.empty();
        $tabla.append('<thead class="thead-light text-center " align = "center"> <tr>' +
            '<th>Patron</th>' +
            '<th>Longitud</th>' +
            '<th>Ocurrencias</th>' +
            '<th>Posiciones</th>' +
            '</tr>');
        $tablabody = $('<tbody></tbody>');
        for (var i = 0; i < data.Patrones.length; i++) {
            // $fila = $("<tr onClick=mostrarDatosJSON("+i+") data-toggle='modal' data-target='#PatternsModal'></tr>");
            $fila = $("<tr data-toggle='modal' data-target='#PatternsModal'></tr>");

            $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Patron + '</td>');
            $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Longitud + '</td>');
            $fila.append('<td class="text-center" align="center" valign="middle" >' + data.Patrones[i].Ocurrencias + '</td>');
            $fila.append('<td class="text-center" align="center" valign="middle" >' + '<button type="button" class="btn  btn-warning"' + "onClick=mostrarDatosJSON(" + i + ")>" + "Posiciones" + '</button>' + '</td>');

            $tablabody.append($fila);
        }

        $patrones.append('<h3 class="h5 text-info text-center p-2 m-2">Resultados</h3>');
        $tabla.append($tablabody);
        $patrones.append($tabla);
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
        aJSON.innerHTML = "Descargar JSON";

        // $patrones.appendChild(a)
        //$patrones.append(a);
        // $patrones.append(aJSON);
        bttdiv.append(aJSON);
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
        aCSV.innerHTML = "Descargar CSV";

        bttdiv.append(aCSV);

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
                alert('Debe ingresar un valor del umbral');
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