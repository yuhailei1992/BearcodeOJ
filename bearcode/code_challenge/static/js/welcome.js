$(document).ready( function(){
    var codestr = "from django.shortcuts import render\n\n^1000"+
                "def welcome(request):^500\n"+
                "\tprint 'Welcome to Code Challenge!'^500\n"+
                "\tprint 'A platform to prepare for technical interviews'^500\n"+
                "\tprint 'We support Python and Java'^500\n"+
                "\tprint 'Try it NOW!'\n"+
                "\treturn render(request, 'code_challenge/welcome.html', {})"
    console.log(codestr);
    $("#title").typed({ strings: [codestr] });
});