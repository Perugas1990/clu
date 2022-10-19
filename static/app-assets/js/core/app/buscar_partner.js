const ModalDiagnostico = new Vue({
    el: '#modal_diagnostico',
    delimiters: ['[[', ']]'], 
    data: {
        clientes: [],
        criteriaD: '',
        inner_selector_cliente: null
   
    },
    methods: {
        searchDiagnosticos: function () {            
            const url = '/api/ventas/buscar-cliente/?criteriaD=' + this.criteriaD;
            this.$http.get(url).then(
                response => {
                    if (response.status === 200 && response.body instanceof Array) {
                        this.clientes = response.body;
                    }
                },
                response => {
                    console.error(response);
                }
            ).catch(error => {
                console.error(error);
            });
        },
        
        selectDiagnostico: function (cliente) {
            this.clientes = [];
            this.criteriaD = '';
            
            if($id_partner.length > 1){
                agregar_opcion_a_select(this.inner_selector_cliente, cliente.id, cliente.razon_social_comprador, true);
            }
            else{
                agregar_opcion_a_select($id_partner, cliente.id,  cliente.razon_social_comprador, true);
            }
            $('#modal_diagnostico').modal('hide');
        }        
    },   
    mounted: function () {
        $('#input-criteriaD').focus();
        let this_app = this;
        $(document).on('hidden.bs.modal', '#modal_diagnostico', function(e){
            this_app.clientes = [];
            this_app.criteriaD = '';
        });
       
    }
        
});


// const ModalDiagnostico = new Vue({
//     el: '#modal_diagnostico',
//     delimiters: ['[[', ']]'], 
//     data: {
//         diagnosticos: [],
//         criteriaD: '',
//         inner_selector_diagnostico: null       
//     },
//     methods: {
//         searchDiagnosticos: function () {            
//             const url = '/api/his/buscar-diagnostico/?criteriaD=' + this.criteriaD;
//             this.$http.get(url).then(
//                 response => {
//                     if (response.status === 200 && response.body instanceof Array) {
//                         this.diagnosticos = response.body;
//                     }
//                 },
//                 response => {
//                     console.error(response);
//                 }
//             ).catch(error => {
//                 console.error(error);
//             });
//         },
        
//         selectDiagnostico: function (diagnostico) {
//             this.diagnosticos = [];
//             this.criteriaD = '';
            
//             if($diagnostico_temporal.length > 1){
//                 agregar_opcion_a_select(this.inner_selector_diagnostico, diagnostico.id, diagnostico.codigo + " - "+ diganostico.nombre, true);
//             }
//             else{
//                 agregar_opcion_a_select($diagnostico_temporal, diagnostico.id, diagnostico.codigo + " - "+ diagnostico.nombre, true);
//             }
//             $('#modal_diagnostico').modal('hide');
//         }        
//     },   
//     mounted: function () {
//         $('#input-criteriaD').focus();
//         let this_app = this;
//         $(document).on('hidden.bs.modal', '#modal_diagnostico', function(e){
//             this_app.diagnosticos = [];
//             this_app.criteriaD = '';
//         });
       
//     }
        
// });