
// $(document).ready(function(){});  same as $(function(){});

$(function () {
    $('form').on('submit', function (event) {
    console.log("form submited")
        $.ajax({
            data: {
                textforspeech: $('#tts').val()
            },

            type: 'POST',
            url: '/converttospeech/'

        })
            .done(function (data) {

                $('#display').text(data.txt)
            });
        // Prevent default submit event
        event.preventDefault();

    });
});


