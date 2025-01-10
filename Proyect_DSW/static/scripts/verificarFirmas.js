$(function() {

    function generar_listado_errores(errores) {
        let lista = "";
        for(let error of errores) {
            lista += "<li>" + error + "</li>";
        }
        return lista;
    }

    function es_campo_vacio(campo) {
        return campo.value.trim() == "";
    }

    $(document).ready(function(){
        $("#formulario").on("submit", function(evento) {
            let errores = new Array();

            if(es_campo_vacio($("#archivo").val())) {
                errores.push("No pasaste el ARCHIVO");
                con_errores = true;
            }
            if(es_campo_vacio($("#firma").val())) {
                errores.push("No pasaste la FIRMA");
                con_errores = true;
            }
            if(es_campo_vacio($("#user").val())) {
                errores.push("No pasaste el USUARIO");
                con_errores = true;
            }
            if(errores.length != 0) {
                let lista_html = generar_listado_errores(errores);
                $("#lista-errors").html(lista_html);
                $("#errors").fadeIn(2000).fadeOut(5000);
                evento.preventDefault();
            }
        });
    });

});
~    
