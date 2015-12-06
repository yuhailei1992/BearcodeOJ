$(document).ready(function(){
        var role_value = $("#role_value");
        $("#role").on("change", function() {
            console.log(this.value);
            var choice = this.value;
            switch (choice) {
                case "user":
                    console.log("You choose user!");
                    role_value.val("user");
                    break;
                case "admin":
                    console.log("You choose admin!");
                    role_value.val("admin");
                    break;
            }
        });
    });

    function perm_check(){
        var msgboard = $("#msgboard");
        msgboard.text("");
        var username = $("#id_username").val();
        var role = $("#role_value").val();
        if(username=="bearcode2015@gmail.com"){
            if(role!="admin"){
                msgboard.text("Administrator cannot log in as a normal user");
                return false;
            }
        }
        else{
            if(role=="admin"){
                msgboard.text("You are not a Administrator");
                return false;
            }
        }

        return true;
    }