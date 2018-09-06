$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:

    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("#form_participante").validate({
        // Specify validation rules
        rules: {
            // The key name on the left side is the name attribute
            // of an input field. Validation rules are defined
            // on the right side
            nombre: "required",
            apellido: "required",
            email: {
                required: true,
                // Specify that email should be validated
                // by the built-in "email" rule
                email: true
            },
            mensaje: "required",
            video: {
                required: false
            }
        },
        // Specify validation error messages
        messages: {
            nombre: "Ingrese su nombre",
            apellido: "Ingrese su apellido",
            email: "Ingrese correo valido",
            mensaje: "Ingrese mensaje"
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function (form) {
            debugger;
            form.submit();
        }
    });

    var uploadButton = $('<button/>')
        .addClass('btn btn-primary')
        .css(
            'width', '100%'
        )
        .prop('disabled', true)
        .text('Processing...')
        .on('click', function () {
            if ($("#form_participante").valid()) {
                var $this = $(this),
                    data = $this.data();

                debugger;


                $this
                    .off('click')
                    .text('Abort')
                    .on('click', function () {
                        $this.remove();
                        data.abort();
                    });


                data.submit().always(function () {
                    $this.remove();
                });
            }
        });

    $('[name="video"]').fileupload({
        url: upload_file_url,
        formData: function () {
            return [
                {name: "uid", value: uuid},
                {name: "csrfmiddlewaretoken", value: csrf_token},
                {name: "concurso_id", value: concurso_id},

                {name: "participante_nombre", value: $("#form_participante [name='nombre']").val()},
                {name: "participante_apellido", value: $("#form_participante [name='apellido']").val()},
                {name: "participante_email", value: $("#form_participante [name='email']").val()},
                {name: "participante_mensaje", value: $("#form_participante [name='mensaje']").val()},
            ]
        },
        dataType: 'json',
        autoUpload: false,
        uploadTemplateId: null,
        downloadTemplateId: null,
        maxNumberOfFiles: 1,
        acceptFileTypes: /^video\/(.+)$/i,
    }).on('fileuploadadd', function (e, data) {
        $(window).bind('beforeunload', function () {
            return 'Estas seguro de abandonar?';
        });
        $("#files").empty();
        $('#progress .progress-bar').css(
            'width', '0%'
        );
        data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            var node = $('<p/>').append($('<span/>').text(file.name));
            if (!index) {
                node.append('<br>').append(uploadButton.clone(true).data(data));
            }
            node.appendTo(data.context);
        });
    }).on('fileuploadprocessalways', function (e, data) {
        var index = data.index,
            file = data.files[index],
            node = $(data.context.children()[index]);
        if (file.preview) {
            node
                .prepend('<br>')
                .prepend(file.preview);
        }
        if (file.error) {
            node
                .append('<br>')
                .append($('<span class="text-danger"/>').text(file.error));
        }
        if (index + 1 === data.files.length) {
            data.context.find('button')
                .text('Cargar')
                .prop('disabled', !!data.files.error);
        }
    }).on('fileuploadprogressall', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progress .progress-bar').css(
            'width',
            progress + '%'
        );
    }).on('fileuploadstart', function (e, data) {
        debugger;
        $("#form_participante :input").prop("disabled", true);
    }).on('fileuploaddone', function (e, data) {
        $(window).unbind('beforeunload');
        $.each(data.result.files, function (index, file) {
            if (file.url) {
                var link = $('<a>')
                    .attr('target', '_blank')
                    .prop('href', file.url);
                $(data.context.children()[index])
                    .wrap(link);
            } else if (file.error) {
                var error = $('<span class="text-danger"/>').text(file.error);
                $(data.context.children()[index])
                    .append('<br>')
                    .append(error);
            }
        });
        alert("archivo cargado con exito, en unos minutos llegara un correo confirmandole el estado de su solicitud");
        window.location.href = base_concurso_url;
    }).on('fileuploadfail', function (e, data) {
        $.each(data.files, function (index) {
            var error = $('<span class="text-danger"/>').text('File upload failed.');
            $(data.context.children()[index])
                .append('<br>')
                .append(error);
        });
        alert("Error al cargar el archivo");
        $("#form_participante :input").prop("disabled", false);
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});