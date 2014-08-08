$(function() {
        
        function runEffect() {
        
        var options = {};
        $( "#bRegister" ).hide( "slide", options, 500, callback );
        };
 
        // callback function to bring a hidden box back
        function callback() {
        setTimeout(function() {
            $( "#bLogin" ).removeAttr( "style" ).hide().fadeIn();
        }, 0 );
        };
 
        $( "#bLoginSlide" ).click(function() {
            // preventDefault();
            runEffect();
            return false;
        });
    });

$(function() {
        
        function runEffect() {
        
        var options = {};
        $( "#bLogin" ).hide( "slide", options, 500, callback );
        };
 
        // callback function to bring a hidden box back
        function callback() {
        setTimeout(function() {
            $( "#bRegister" ).removeAttr( "style" ).hide().fadeIn();
        }, 0 );
        };
 
        $( "#bRegisterSlide" ).click(function() {
            runEffect();
            return false;
        });
        $(".bRegisterSlide").click(function(){
            runEffect();
            return false;
        })

    });        


$(".bRegisterButton").click(function(){

        var thisElement = $(this);
        var username = $(".busername").val();
        var email = $(".bemail").val();
        var password1 = $(".bpassword1").val();
        var password2 = $(".bpassword2").val();

        $.post("/register/",{username:username, email:email, password1:password1, password2:password2}, function(result){
            console.log(result)
            
            var divEl = $("#bRegister");
            
            $("#bRegister li").remove();

            if (result["errors"] != undefined){
                var errors = result["errors"];

                var size = errors.length;
                for (var i = 0; i < size; i++){
                    var errorEl = document.createElement("li");
                    errorEl.setAttribute("class","bRegisterError");
                    errorEl.innerHTML = errors[i];
                    divEl.append(errorEl);
                }
            }
            else{
                var message = result["message"];
                $(".bSuccess").html(message);
                console.log("message is" + message);
                divEl.hide();
            }
        })

    })





// ============ CSRF TOKEN ======================

$(document).ajaxSend(function(event, xhr, settings) {  
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
    function sameOrigin(url) {  
        // url could be relative or scheme relative or absolute  
        var host = document.location.host; // host + port  
        var protocol = document.location.protocol;  
        var sr_origin = '//' + host;  
        var origin = protocol + sr_origin;  
        // Allow absolute or scheme relative URLs to same origin  
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||  
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||  
            // or any other URL that isn't scheme relative or absolute i.e relative.  
            !(/^(\/\/|http:|https:).*/.test(url));  
    }  
    function safeMethod(method) {  
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));  
    }  
  
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {  
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));  
    }  
});

