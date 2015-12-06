$(document).ready(function() {
    // to render bootstrapped html code
    $("div > select").attr("class","form-control");
    $("div > input").attr("class","form-control");
    $("div > textarea").attr("class","form-control");
    $("div > textarea").attr("rows","3");

    var java_default_div = $("div[data-idx=div_id_java_default]");
    java_default_div.text($("#id_java_default").text());
    java_default_div.attr("id","java_default");

    var java_tests_div = $("div[data-idx=div_id_java_tests]");
    java_tests_div.text($("#id_java_tests").text());
    java_tests_div.attr("id","java_tests");

    var python_default_div = $("div[data-idx=div_id_python_default]");
    python_default_div.text($("#id_python_default").text());
    python_default_div.attr("id","python_default");

    var python_tests_div = $("div[data-idx=div_id_python_tests]");
    python_tests_div.text($("#id_python_tests").text());
    python_tests_div.attr("id","python_tests");

    var java_default = ace.edit("java_default");
    var java_tests = ace.edit("java_tests");
    var python_default = ace.edit("python_default");
    var python_tests = ace.edit("python_tests");

    java_default.setTheme("ace/theme/default");
    java_tests.setTheme("ace/theme/default");
    python_default.setTheme("ace/theme/default");
    python_tests.setTheme("ace/theme/default");

    java_default.getSession().setMode("ace/mode/java");
    java_tests.getSession().setMode("ace/mode/java");
    python_default.getSession().setMode("ace/mode/python");
    python_tests.getSession().setMode("ace/mode/python");

    $("form").submit(function(){
        //alert(java_default.getValue());
        $("#java_default").append("<textarea id='id_java_default' name='java_default'>"+java_default.getValue()+"</textarea>");
        //alert(java_tests.getValue());
        $("#python_default").append("<textarea id='id_python_default' name='python_default'>"+python_default.getValue()+"</textarea>");
        //alert(python_default.getValue());
        $("#java_tests").append("<textarea id='id_java_tests' name='java_tests'>"+java_tests.getValue()+"</textarea>");
        //alert(python_tests.getValue());
        $("#python_tests").append("<textarea id='id_python_tests' name='python_tests'>"+python_tests.getValue()+"</textarea>");
    });
});