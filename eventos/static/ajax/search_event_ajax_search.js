///THIS FILE MUST BE IMPORTED BEFORE THE "main" FILE.
/**
  Executes a search for colors containing a substring.
 */
var eventSearch = function()  {
  //The key-press listener is no longer attached

  //Get and trim the search text.
// var id_event = $('#username').val().trim();
  var id_event = document.getElementById(this.id).getAttribute("id-event");
  var tipo_peticion = document.getElementById(this.id).getAttribute("data-event");
  //var tipo_peticion = this.data-event;

  console.log('ajax id_event', id_event);
  console.log('ajax tipo_peticion', tipo_peticion);

  if(id_event.length < 1)  {
    //Too short. Ignore the submission, and erase any current results.
    $('#myevento_view').html("");
    $('#myevento_edit').html("");
    $('#myevento_delete').html("");
    $('#myevento_videos').html("");

  }  else  {
    //There are at least two characters. Execute the search.

    var processServerResponse = function(sersverResponse_data, textStatus_ignored,
                        jqXHR_ignored)  {
      //alert("sersverResponse_data='" + sersverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "'");

      if(tipo_peticion == '1'){
        $('#myevento_view').html(sersverResponse_data);
      }else if (tipo_peticion == '2') {
        $('#myevento_edit').html(sersverResponse_data);
      }else if (tipo_peticion == '3') {
        $('#myevento_delete').html(sersverResponse_data);
      }else if (tipo_peticion == '4') {
        $('#myevento_videos').html(sersverResponse_data);
      }

    }

    var config = {
      /*
        Using GET allows you to directly call the search page in
        the browser:
        http://the.url/search/?color_search_text=bl
        Also, GET-s do not require the csrf_token
       */
      type: "GET",
      url: SEARCH_ID_EVENTO_URL,
      data: {
        'id_event' : id_event,
        'tipo_peticion': tipo_peticion,
      },
      dataType: 'html',
      success: processServerResponse
    };
    $.ajax(config);
  }
};
