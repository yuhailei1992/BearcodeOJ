$(document).ready(function() {
    var textarea = $('textarea[name="editor"]');
    textarea.hide();
    var editor = ace.edit("editor_div");
    editor.setTheme("ace/theme/default");
    editor.getSession().setMode("ace/mode/java");
    $('#submitbtn').on('click', function() {
        submitCode(editor.getValue());
    });

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});

function submitCode(code_content){
    var problemid = $("#problemid").val();
    var submit_url = "/trysubmit";
    var textarea = $('textarea[name="editor"]');
    textarea.hide();
    var editor = ace.edit("editor_div");
    var language = $('#default_lang').val();
    console.log("url is:"+submit_url+", problem id is:"+problemid);
    console.log("submitted content is:"+code_content);

    $.ajax({
        url : submit_url,
        dataType: "json",
        method: "POST",
        data: {problemid:problemid,codecontent:code_content,language:language}
    })
    .done(function(result) {
        console.log("successfully submitted, get result"+result.status);
        var resultstatus = result.status;
        var statusPanel = $("#status")
        var msgPanel = $("#message")
        if(resultstatus=="Accepted"){
            statusPanel.css("color","green");
            statusPanel.text(result.status);
        }
        else{
            statusPanel.css("color","red");
            statusPanel.text(result.status);
            msgPanel.text(result.message);
        }
    });
}