/**
 * Variables del componente upload Zip o XML
 */
 var numeroAutorizacion;
 var estado;
 var fechaAutorizacion;
 var fechaEmision;
 var dirEstablecimiento;
 var contribuyenteEspecial;
 var obligadoContabilidad;
 var tipoIdentificacionComprador;
 var razonSocialComprador;
 var identificacionComprador;
 var totalSinImpuestos;
 var totalDescuento;
 var totalConImpuestos;
 var importeTotal;
 //infoTributaria
 var infoTributaria;
 var detalles;
 var ambiente;
 var claveAcceso;
 var codDoc;
 var dirMatriz;
 var estab;
 var nombreComercial;
 var ptoEmi;
 var razonSocial;
 var ruc;
 var secuencial;
 var tipoEmision;
 //var endpoint = 'http://test.mantis.inprise.club/api/voucher-parser/';
 
 /**
  * Busca el tipo de identificación del partner
  * y pone le valor en el formulario.
  * @param {*} cod
  */
 function tipoIdentificacion(cod) {
     $.get('/api/tipo-identificacion/' + cod + '/')
         .done(function (data) {
             $("#proveedor_tipo").val(data['nombre']);
         })
         .fail(function (error) {
             console.error(error)
         })
 }
 
 /**
  * Busca el tipo de comprobante y pone valor en el formulario.
  * @param {*} cod
  */
 function tipoComprobante(cod) {
     $.get('/api/tipo-comprobante/' + cod + '/')
         .done(function (data) {
             $('#id_tipo_comprobante').val(data['id']).trigger('change');
         })
         .fail(function (error) {
             console.error(error)
         })
 }
 
 /**
  * Se obtiene los datos del partner dado la identificación
  * @param {*} ruc
  */
 function getProvider(ruc) {
     $.get('/api/partners/' + ruc + '/')
         .done(function (data) {
             // console.log('El proveedor pertenece a esta empresa');
             agregar_opcion_a_select($('#id_cliente'), data['id'], data['nombre'], true);
             $('#import-file').modal('hide');
             if (data['grupo_proveedor'] == null) {
                 console.warn('Este proveerdor no tiene definido un grupo');
             }
         })
         .fail(function (error) {
             // console.log('El proveedor de dicha factura no está registrado en esta empresa');
             //mostrar_notificacion('El proveedor de dicha factura no está registrado en esta empresa', 'warning');
             $('#zip-component').hide();
             $('#messages').show();
             $('#nombre-proveedor').text(razonSocial);
 
         })
         .always(function () {
             // console.log("The request are done !!!");
         });
 }
 
 
 /**
  * retorna un diccionario con los parametros que existen en la URL
  * ej: localhost?a=1&b=2 -> {a=1, b=2}
  * @param url : url de la pagina actual
  * @returns {diccionario}
  */
 function getURLParameters(url) {
     var result = {};
     var searchIndex = url.indexOf("?");
     if (searchIndex == -1) return result;
     var sPageURL = url.substring(searchIndex + 1);
     var sURLVariables = sPageURL.split('&');
     for (var i = 0; i < sURLVariables.length; i++) {
         var sParameterName = sURLVariables[i].split('=');
         result[sParameterName[0]] = sParameterName[1];
     }
     return result;
 }
 
 
 /**
  * Cambia la url en el browser sin tener que recargar la pagina
  * @param page_history_title
  * @param page_history_value
  */
 function change_url_parameters(page_history_title, page_history_value) {
     var stateObj = {s: ""};
     history.pushState(stateObj, page_history_title, page_history_value);
 }
 
 
 /**
  * Verifica si una cadena termina con determinado caracter
  * @param pattern : caracter para verificar
  * @returns {boolean}
  */
 String.prototype.endsWith = function (pattern) {
     var d = this.length - pattern.length;
     return d >= 0 && this.lastIndexOf(pattern) === d;
 };
 
 
 /**
  * Mostrar la notificacion flotante con la lib PNotify
  * @param texto: Texto a mostrar en la notificacion
  * @param tipo: tipo de mensaje a mostrar
  */
 function mostrar_notificacion(texto, tipo) {
     var clase = 'bg-primary';
     if (tipo === "success") {
         clase = "bg-success"
     } else if (tipo === "error") {
         clase = "bg-danger"
     } else if (tipo === "info") {
         clase = "bg-info"
     } else if (tipo === "warning") {
         clase = "bg-warning"
     }
     new PNotify({
         text: texto,
         addclass: clase,
         delay: 4000
     });
 }
 
 /**
  * completar una cadena con ceros a la izquierda ej: 0002
  * @param numero: valor ingresado por el usuario
  * @param longitud: longitud de caracteres de la cadena
  * @param caracter: caracter a rellenar
  * @returns {*}
  */
 function zfill(numero, longitud, caracter) {
     caracter = caracter || '0';
     numero = numero + '';
     return numero.length >= longitud ? numero : new Array(longitud - numero.length + 1).join(caracter) + numero;
 }
 
 // /**
 //  * agregar a la cadena ceros al input
 //  * @param $elemento: componente html para asignar el valor de la cadena
 //  * @param longitud: numero de caracteres de la cadena a generar
 //  */
 // function z_fill($elemento, longitud) {
 //     var valor = $elemento.val();
 //     if (valor) {
 //         var pad_numero = completar_cadena_con_ceros(valor, longitud);
 //         $elemento.val(pad_numero)
 //     }
 // }
 
 /**
  * funcion para validar el ingreso de solo numeros
  * @param e: event
  * @returns {boolean}
  */
 function solonumeros(e) {
     var keynum = window.event ? window.event.keyCode : e.which;
     if ((keynum == 8) || (keynum == 46) || (keynum == 0) || (keynum == 13))
         return true;
 
     return /\d/.test(String.fromCharCode(keynum));
 }
 
 /**
  * Detectando evento 'keydown' de los inputs y selects,
  * Verifica si la tecla presionada es ENTER para pasar al siguiente input
  */
 $('form input').keydown(function (event) {
     if (!$(this).hasClass("last")) {
         if (event.which == 13) {
             event.preventDefault();
             var $input = $('form input');
             $input.eq($input.index(this) + 1).focus();
         }
     }
 });
 
 $('.add-extra-option').append($('<option>', {
     value: 'buscar_mas',
     text: 'BUSCAR MÁS'
 }));
 
 $('.add_option_new_item').append($('<option>', {
     value: 'add_new_product',
     text: 'Agregar nuevo'
 }));
 
 
 // ****** detectando pausa al escribir en cuadro de busqueda ******
 
 function completar_la_busqueda($elemento) {
     var timeoutID;
 
     $elemento.on('keypress', function () {
         window.clearTimeout(timeoutID);
     });
 
     $elemento.on('keyup', function () {
         timeoutID = window.setTimeout(filtrarProveedores, 1000);
     });
 
     function filtrarProveedores() {
 
     }
 }
 
 /**
  * Agrega una nueva opción a un select, agrega la propiedad seleccionada
  * @param $select, componente 'select' html
  * @param id: valor id de la opcion
  * @param texto: valor a mostrar en la opcion
  * @param texto: valor a mostrar en la opcion
  * @param seleccionar: boleano para seleccionar la opcion agregada
  */
 function agregar_opcion_a_select($select, id, texto, seleccionar, lanzar_evento=true) {
     var valor_opcion = "option[value='" + id + "']";
 
     if (!$select.find(valor_opcion).length > 0) {
 
         // agregar antes de opcion "buscar mas"
         var index_add = -3;
         if ($select.find('option').length == 0) {
             $select.append($('<option>', {
                 value: id,
                 text: texto
             }));
         }
         else if ($select.find('option').length <= 5) {
 
             $select.find('option').eq(0).after($('<option>', {
                 value: id,
                 text: texto
             }));
         }
         else {
             $select.find('option').eq(index_add).after($('<option>', {
                 value: id,
                 text: texto
             }));
         }
     }
 
     if (seleccionar) {
         $select.find('option:selected').removeAttr("selected");
         $select.val(id);
         if(lanzar_evento)
             $select.trigger('change');
     }
 }
 
 
 // limpiando los modales
 // detectando el evento show del modal para agregar el focus al primer input
 $('body').on('shown.bs.modal', '#modal_clientes, #modal_productos', function () {
     $('input:visible:enabled:first', this).val('');
     $('input:visible:enabled:first', this).focus();
 });
 
 
 function formatDate(d) {
 
     let datestring = ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
     d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
 
     return datestring;
 }
 
 function esPlacaVehiculo(identificador){
     if(identificador == null || identificador == undefined){
         return ''
     }
 
     identificador = identificador.toUpperCase();
     if (((identificador.length == 7) && identificador.match("^[A-Z]{3}[0-9]{4}$"))) {
         return 'vehiculo';
     }
     //hh835c
     if (((identificador.length == 6) && identificador.match("^[A-Z]{2}[0-9]{3}[A-Z]{1}$"))) {
         return 'moto';
     }
 
     return '';
 }