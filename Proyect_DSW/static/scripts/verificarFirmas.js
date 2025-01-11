$(function() {

    function isEmpty(input) {
        return input.val().trim() === "";
    }

    function isSafeInput(input) {
        const regex = /^[A-Za-z0-9_\.\-@]*$/;
        return regex.test(input.val());
    }

    function showAlert(message) {
        return `
        <div class="alert alert-danger" role="alert">
          ${message}
        </div>`;
    }

    $('#formulario').on('submit', function(event) {
        let withErrors = false;
        $('#box-errors').empty();

        if (isEmpty($('#archivo'))) {
            $('#archivo').addClass('is-invalid');
            $('#box-errors').append(showAlert('Campo archivo vacio.'));
            withErrors = true;
        } else {
            $('#archivo').removeClass('is-invalid');
        }

        if (isEmpty($('#firma'))) {
            $('#firma').addClass('is-invalid');
            $('#box-errors').append(showAlert('Campo firma vacio.'));
            withErrors = true;
        } else {
            $('#firma').removeClass('is-invalid');
        }

        if (isEmpty($('#user'))) {
            $('#user').addClass('is-invalid');
            $('#box-errors').append(showAlert('Campo usuario vacio.'));
            withErrors = true;
        } else if (!isSafeInput($('#user'))) {
            $('#user').addClass('is-invalid');
            $('#box-errors').append(showAlert('El usuario no existe.'));
            withErrors = true;
        } else {
            $('#user').removeClass('is-invalid');
        }

        if (withErrors) {
            event.preventDefault();
        }
    });

});
