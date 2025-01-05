$(function() {

    function isEmpty(camp) {
        return camp.val().trim() === ""; 
    }

    function isFileInputEmpty(inputElement) {
        return inputElement[0].files.length === 0;
    }

    function showAlert(message) {
        return `
        <div class="alert alert-danger" role="alert">
          ${message}
        </div>`;
    }

    function isSafeInput(input) {
        const regex = /^[a-zA-Z0-9_\-.@ ]*$/;
        return regex.test(input);
    }

    $('#form').on('submit', function(event) {

        let withErrors = false;
        $('#box-errors').empty();

        if (isFileInputEmpty( $('#file'))) {
            $('#file').addClass('is-invalid');
            $('#box-errors').append(showAlert('Por favor, selecciona un archivo para firmar.'));
            withErrors = true;
        } else {
            $('#file').removeClass('is-invalid');
        }

        if (isEmpty($('#passwd'))) {
            $('#passwd').addClass('is-invalid');
            $('#box-errors').append(showAlert('Por favor, ingresa una contraseña.'));
            withErrors = true;
        } else {
            $('#passwd').removeClass('is-invalid');
        }

        if (withErrors) {
            event.preventDefault();
        }
    });

});
