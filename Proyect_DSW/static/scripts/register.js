$(document).ready(function() {
    function es_campo_vacio(campo) {
        return campo.trim() == "";
    }
    function generar_html_lista_errores(lista) {
        let res = "";
        for (let elemento of lista) {
            res += `<li>${elemento}</li>`;
        }
        return res;
    }
    $("#formulario").on("submit", function(event) {
        let listaErrores = new Array();
        let con_errores = false;
        const n = $("#name").val();
        const ni = $("#nick").val();
        const p = $("#passwd").val();
        const cp = $("#confirmPasswd").val();
        const m = $("#mail").val();
        if (es_campo_vacio(n)) {
                listaErrores.push("No pasaste USUARIO");
                con_errores = true;
        }
        if (es_campo_vacio(ni)) {
                listaErrores.push("No pasaste NICK DE USUARIO");
                con_errores = true;
        }
	if (es_campo_vacio(p)) {
                listaErrores.push("No pasaste CONTRASEÑA");
                con_errores = true;
        }
        if (es_campo_vacio(cp)) {
                listaErrores.push("No pasaste VERIFICASTE CONTRASEÑA");
                con_errores = true;
        }
        if (es_campo_vacio(m)) {
                listaErrores.push("No pasaste CORREO ELECTRONICO");
                con_errores = true;
        }
	if (p != cp) {
                listaErrores.push("LAS CONTRASEÑAS NO HACEN MATCH");
                con_errores = true;	
	}
        if (con_errores) {
                let listado_errores = generar_html_lista_errores(listaErrores);
                $("#lista_errores").html(listado_errores);
                $("#mistakes").fadeIn(3000).fadeOut(5000);
                event.preventDefault();
        }
    });
});

