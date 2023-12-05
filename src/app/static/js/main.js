window.onload = () => {
    'use strict';

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register('./../static/sw.js').then(function (registration) {
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            },

        function(error) {
            console.log('ServiceWorker registration failed: ', error);
        });
    }
}
//TODO - organize in a different file
$(document).ready(function () {
    $('#card-profile-edit').hide();
    $('#toggleEdit').click(function () {
        $('#card-profile').toggle();
        $('#card-profile-edit').toggle();

    });

    $("#submitFormBtn").click(function () {
        $.ajax({
            url: $("#profileForm").attr("action"),
            method: "POST",
            data: $("#profileForm").serialize(),
            success: function (response) {
                console.log(response);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

});