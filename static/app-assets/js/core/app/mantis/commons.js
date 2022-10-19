/**
 * Mostrar el bloqueo de pantalla
 * @param $elemento: componente html para mostrar bloqueo
 * @param mensaje: mensaje del bloqueo
 */
function mostrar_bloqueo($elemento, mensaje) {
    $elemento.block({
        message: '<i class="icon-spinner spinner"></i> <br> ' + mensaje,
        overlayCSS: {
            backgroundColor: '#1B2024',
            opacity: 0.85,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'none',
            color: '#fff'
        }
    });
}


/**
 * Muestra una alerta simple
 * @param mensaje
 * @param tipo
 */
function mostrarAlertaSwal(mensaje, tipo) {
    swal({
        type: tipo,
        title: mensaje,
        closeOnConfirm: true
    })
}


/**
 * FUNCIONES COMUNES PARA COMPONENTES HANDSONTABLE
 */

/**
 * Convertir una matriz de handsontable en diccionario
 * @param changes
 * @returns {{row: *, prop: *, prev: *, current: *}}
 */
function cambios_a_dict(changes) {
    return {
        'row': changes[0][0], 'prop': changes[0][1],
        'prev': changes[0][2], 'current': changes[0][3]
    };
}


/**
 * Revierte los cambios al retornar un error en las validaciones
 * @param grid_handsontable
 * @param cambios
 */
function revertirCambios(grid_handsontable, cambios) {
    grid_handsontable.setDataAtRowProp(cambios['row'], cambios['prop'], cambios['prev'], 'program');
}


/**
 * Renderiza en plugin select2 con "key" "value"
 * @param instance
 * @param td
 * @param row
 * @param col
 * @param prop
 * @param value
 * @param cellProperties
 * @returns {*}
 */
function formatearDropdownSelect2(instance, td, row, col, prop, value, cellProperties) {
    var selectedId;
    var optionsList = cellProperties.select2Options.data;

    if (isNaN(value)) {
        Handsontable.TextCell.renderer(instance, td, row, col, prop, value, cellProperties);
        return td
    }

    if (typeof optionsList === "undefined" || typeof optionsList.length === "undefined" || !optionsList.length) {
        Handsontable.TextCell.renderer(instance, td, row, col, prop, value, cellProperties);
        return td;
    }

    var values = (value + "").split(",");
    value = [];
    for (var index = 0; index < optionsList.length; index++) {

        if (values.indexOf(optionsList[index].id + "") > -1) {
            selectedId = optionsList[index].id;
            value.push(optionsList[index].text);
        }
    }
    value = value.join(", ");

    Handsontable.TextCell.renderer(instance, td, row, col, prop, value, cellProperties);
    return td;
}


/**
 * Actualizar los datos de la celda cuando el tipo de edicion es select2
 * @param cell_prop
 * @param data
 * @param grid_handsontable
 */
function updateCellSelect2(cell_prop, data, grid_handsontable) {
    var settings = grid_handsontable.getSettings();
    var indexProp = null;
    settings.columns.some(function (item, i) {
        return item.data === cell_prop ? (indexProp = i, true) : false;
    });
    if (indexProp != null) {
        settings.columns[indexProp]['select2Options']['data'] = data;
    }
}




$(".solo-numeros").keydown(function(event) {
    // Allow: backspace, delete, tab, escape, and enter
    if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
        // Allow: Ctrl+A
        (event.keyCode == 65 && event.ctrlKey === true) ||
        // Allow: home, end, left, right
        (event.keyCode >= 35 && event.keyCode <= 39)) {
        // let it happen, don't do anything
        return;
    } else {
        // Ensure that it is a number and stop the keypress
        if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105)) {
            event.preventDefault();
        }
    }
});

