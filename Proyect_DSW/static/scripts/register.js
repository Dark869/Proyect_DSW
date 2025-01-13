$(function () {
    function showAlert(message) {
        return `
        <div class="alert alert-danger" role="alert">
          ${message}
        </div>`;
    }

    function isEmpty(input) {
        return input.val().trim() === "";
    }

    function isSafeInput(input) {
        const regex = /^[A-Za-z0-9_\.\-@]*$/;
        return regex.test(input.val());
    }

    function hasUpperCase(input) {
        const regex = /[A-Z]/;
        return regex.test(input.val());
    }

    function hasNumber(input) {
        const regex = /[0-9]/;
        return regex.test(input.val());
    }

    $('#formulario').on('submit', function (event) {
        let withErrors = false;
        $('#box-errors').empty();

        if (isEmpty($('#name'))) {
            $('#name').addClass('is-invalid');
            $('#box-errors').append(showAlert('El campo nombre completo no puede ir vacío.'));
            withErrors = true;
        } else {
            $('#name').removeClass('is-invalid');
        }

        if (isEmpty($('#nick'))) {
            $('#nick').addClass('is-invalid');
            $('#box-errors').append(showAlert('El campo nombre de usuario no puede ir vacío.'));
            withErrors = true;
        } else {
            $('#nick').removeClass('is-invalid');
        }

        if (isEmpty($('#mail'))) {
            $('#mail').addClass('is-invalid');
            $('#box-errors').append(showAlert('El campo correo electrónico no puede ir vacío.'));
            withErrors = true;
        } else {
            $('#mail').removeClass('is-invalid');
        }

        const passwd = $('#passwd');
        if (isEmpty(passwd)) {
            passwd.addClass('is-invalid');
            $('#box-errors').append(showAlert('El campo contraseña no puede ir vacío.'));
            withErrors = true;
        } else if (passwd.val().length < 12) {
            passwd.addClass('is-invalid');
            $('#box-errors').append(showAlert('La contraseña debe tener al menos 12 caracteres.'));
            withErrors = true;
        } else if (!hasUpperCase(passwd)) {
            passwd.addClass('is-invalid');
            $('#box-errors').append(showAlert('La contraseña debe tener al menos una letra mayúscula.'));
            withErrors = true;
        } else if (!hasNumber(passwd)) {
            passwd.addClass('is-invalid');
            $('#box-errors').append(showAlert('La contraseña debe tener al menos un número.'));
            withErrors = true;
        } else {
            passwd.removeClass('is-invalid');
        }

        if ($('#passwd').val() !== $('#confirmPasswd').val()) {
            $('#confirmPasswd').addClass('is-invalid');
            $('#box-errors').append(showAlert('Las contraseñas no coinciden.'));
            withErrors = true;
        } else {
            $('#confirmPasswd').removeClass('is-invalid');
        }

        if (!isSafeInput(passwd)) {
            passwd.addClass('is-invalid');
            $('#box-errors').append(showAlert('La contraseña solo puede contener los caracteres _, -, ., @.'));
            withErrors = true;
        }

        if (withErrors) {
            event.preventDefault();
        }
    });
});
