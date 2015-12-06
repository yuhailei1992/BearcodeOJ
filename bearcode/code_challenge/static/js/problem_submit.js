$(document).ready(function() {
    $("#loading").html("");
    var java_default = $("#java_default").val();
    var python_default = $("#python_default").val();
    var default_lang = $("#default_lang");
    var editor = ace.edit("editor_div");

    console.log("java:");
    console.log(java_default);
    console.log("python");
    console.log(python_default);
    var editor_div = $("editor_div");
    $("#language").on("change", function() {
        console.log(this.value);
        var choice = this.value;
        switch (choice) {
            case "Java":
                console.log("You choose java!");
                default_lang.val("Java");
                //editor_div.text(java_default);
                editor.setValue(java_default,1);
                editor.getSession().setMode("ace/mode/java");
                break;
            case "Python":
                console.log("You choose python!");
                default_lang.val("Python");
                //editor_div.text(python_default);
                editor.setValue(python_default,1);
                editor.getSession().setMode("ace/mode/python");
                break;
        }
    });

    $("#restore").on("click", function(){
        var default_lang = $("#default_lang").val();
        if(default_lang=='Java'){
            editor.setValue(java_default,1);
            editor.getSession().setMode("ace/mode/java");
        }
        else{
            editor.setValue(python_default,1);
            editor.getSession().setMode("ace/mode/python");
        }
    });

    var textarea = $('textarea[name="editor"]');
    textarea.hide();
    var editor = ace.edit("editor_div");
    editor.setTheme("ace/theme/default");
    editor.getSession().setMode("ace/mode/java");
    $('#submitbtn').on('click', function() {
        $("#loading").html("<img src='/static/loading-gif.gif' width='36' height='36' alt='Loading...'>");
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
    var statusPanel = $("#status");
    var msgPanel = $("#message");
    statusPanel.text("");
    msgPanel.text("");
    var problemid = $("#problemid").val();
    var submit_url = $("#submit_mode").val();
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

        if(resultstatus=="Accepted"){
            statusPanel.css("color","green");
            statusPanel.text(result.status);
        }
        else{
            statusPanel.css("color","red");
            statusPanel.text(result.status);
            msgPanel.html("<pre>"+result.message+"</pre>");
        }

        $("#loading").html("");
    });
}