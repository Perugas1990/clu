initAdmision();

function initAdmision() {
    
    $(document).on('ready', function () {
        console.log('llegaaaaaaaaaaaaaaaaa')



        var $id_cliente = $('#id_partner');
        $id_cliente.select2({});


        // detectando el evento show del modal para agregar el focus al primer input
        $('body').on('shown.bs.modal', '#modal_diagnostico', function () {
            $('input:visible:enabled:first', this).focus();
        });


        let $cliente = $('#id_partner');
        $diagnostico_temporal = $cliente;
        $diagnostico_temporal.on('change', function (e) {
            buscar_diagnostico($(this));
        });

        // // SELECT DE DIAGNOSTICOS
        // let $diagnostico_ingreso = $('#id_partner');
        // $diagnostico_temporal = $diagnostico_ingreso;
        // $diagnostico_temporal.on('change', function (e) {
        //     buscar_diagnostico($(this));
        // });   

        // $id_cliente = $("#id_seguro_titular");
        // let FIND_MORE_OPTION = $('<option>', { value: 'buscar_mas', text: 'BUSCAR MÁS' });

        // $id_cliente.append(FIND_MORE_OPTION.clone());
        // $id_cliente.on('change', function() {
        //     let opcion_seleccionada = $(this).val();
        //     if (opcion_seleccionada === 'buscar_mas') {
        //         $(this).val('');
        //         $(this).trigger('change');
        //         $('#modal_clientes').modal('show');
        //     }
        // });

        // $id_medico_tratante = $("#id_partner");       
        // $id_medico_tratante.on('change', function() {
        //     let opcion_seleccionada = $(this).val();
        //     if (opcion_seleccionada === 'buscar_mas') {
        //         $(this).val('');
        //         $(this).trigger('change');
        //         $('#modal_diagnostico').modal('show');
        //     }
        // });



    function buscar_diagnostico($element) {
        let opcion_seleccionada = $($element).val();
        $diagnostico_temporal = $($element);
        ModalDiagnostico.inner_selector_cliente = $(this);
        if (opcion_seleccionada === 'buscar_mas') {
            $diagnostico_temporal.val('');
            $diagnostico_temporal.trigger('change');
            $('#modal_diagnostico').modal('show')
        }
    }


})
   
}
