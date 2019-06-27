'use strict';
$(function () {
    $.validate({
        form: '#login-form',
        errorMessagePosition: 'top',
        onError: function () {
            $('#login-form h3').hide();
        },
        onSuccess: function () {
            $('#login-form h3').show();
        },
    });
});
