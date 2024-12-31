$(function() {

    function generar_listado_errores(errores) {
	let lista = "";
	for(let error of errores) {
	    lista += "<li>" + error + "</li>";
	}
	return lista;
    }

    function politica_pass(passw){
        exRegular = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$/;
        if (exRegular.test(passw)){
            return false;
        } else {
            return true;
        }
    }

    function es_campo_vacio(campo) {
        return campo.value.trim() == "";	
    }

    $(document).ready(function(){
        $("#formulario").on("submit", function(evento) {
            let errores = new Array();
            
            if(es_campo_vacio($("#name").val())) {		
                errores.push("No pasaste el nombre");
            }
            if(es_campo_vacio($("#nick").val())) {		
                errores.push("No pasaste el nick");
            }
            if(es_campo_vacio($("#passwd").val())) {		
                errores.push("No pasaste la contraseña");
            }
            if(es_campo_vacio($("#confirmPasswd").val())) {		
                errores.push("No pasaste la verificacion de contraseña");	
            }
            if(es_campo_vacio($("#mail").val())) {		
                errores.push("No pasaste el correo");	
            }

            if(politica_pass($("#passwd").val())) {
                errores.push("La contraseña debe tener al menos 12 caracteres, una mayúscula, un número y un caracter especial.");    
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