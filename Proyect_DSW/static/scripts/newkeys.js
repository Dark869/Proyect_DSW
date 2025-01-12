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

        if (isEmpty($('#passwd'))) {
            $('#passwd').addClass('is-invalid');
            $('#box-errors').append(showAlert('No pasaste la contraseña.'));
            withErrors = true;
        } else if (!isSafeInput($('#passwd'))) {
            $('#passwd').addClass('is-invalid');
            $('#box-errors').append(showAlert('Contraseña incorrecta.'));
            withErrors = true;
        } else {
            $('#passwd').removeClass('is-invalid');
        }

        if (withErrors) {
            event.preventDefault();
        }
    });

});

