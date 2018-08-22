///THIS FILE MUST BE IMPORTED BEFORE THE "main" FILE.
/**
  Executes a search for colors containing a substring.
 */
var myeventsSearch = function()  {
  //The key-press listener is no longer attached

  //Get and trim the search text.
  var username = $('#username').val().trim();

  if(username.length < 3)  {
    //Too short. Ignore the submission, and erase any current results.
    $('#miseventos').html("");

  }  else  {
    //There are at least two characters. Execute the search.

    var processServerResponse = function(sersverResponse_data, textStatus_ignored,
                        jqXHR_ignored)  {
      //alert("sersverResponse_data='" + sersverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "'");
      $('#miseventos').html(sersverResponse_data);
    }

    var config = {
      /*
        Using GET allows you to directly call the search page in
        the browser:

        http://the.url/search/?color_search_text=bl

        Also, GET-s do not require the csrf_token
       */
      type: "GET",
      url: SEARCH_MIS_EVENTOS_URL,
      data: {
        'username' : username,
      },
      dataType: 'html',
      success: processServerResponse
    };
    $.ajax(config);
  }
};
