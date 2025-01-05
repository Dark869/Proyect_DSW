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

            if(es_campo_vacio($("#pass").val())) {		
                errores.push("No pasaste la contraseña");
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