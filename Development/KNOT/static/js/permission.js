// global used to store the current permission level
var oldName;


function addOrUpdatePermission(type){
	var context = {};

	var name = $(".permissionLevelName")[0].value;
	if (name===""){
		$(".errorMessage").html("Please enter a name.");
		return;
	}
	else{
		$(".errorMessage").html("");
	}
	context['name'] = name;
	var checkboxes = $(".checkbox");
	var sectionIndex = 1;
	// Store shared items in context by searching for checked checkboxes
	for (var i=0;i<checkboxes.length;i++){
		var checkbox = checkboxes[i];
		if (checkbox.className.indexOf("checked")!==-1){
			var section = $.trim(checkbox.textContent).toLowerCase();

			if (section==="name"){
				context["sharedSection"+sectionIndex] = "firstName";
				sectionIndex+=1;
				context["sharedSection"+sectionIndex] = "lastName";
				sectionIndex+=1;
			}
			else if (section==="google plus"){
				context["sharedSection"+sectionIndex] = "googlePlus";
				sectionIndex+=1;
			}
			else{
				var newKey = "sharedSection"+sectionIndex;
				sectionIndex+=1;
				context[newKey] = section;
			}
		}
	}

	if (type==="add"){


		$.post('/addPermissionTemplate/',context,function(json){

			if (json['status']==="Fail"){
				$('.errorMessage').html(json['errors']);
				$('.errorMessage').css('color','red');
			}
			else if (json['status']==="Success"){
				$('.errorMessage').html("New level added!");
				$('.errorMessage').css('color','green');
				var newName = json['name'];
				var newElement = "<li class=\'active\'><a class=\'leftNav\' href=\'/getPermissionTemplate/" + 
					name+ "\'>"+name+"</a></li>";

				$(newElement).insertBefore($(".addNewTemplateButton"));
				window.location.href = "/getPermissionTemplate/"+newName;

			}
		})
	}
	else if (type==="update"){
		context['templateID'] = $(".hiddenId")[0].innerText;


		$.post('/updatePermissionTemplate/',context,function(json){
			// callback
			if (json['status']==="Fail"){
				// fail. print errors.
				$('.errorMessage').html(json['errors']);
				$('.errorMessage').css('color','red');
			}

			else if (json['status']==="Success"){
				// success
				$('.errorMessage').html("Level updated!");
				$('.errorMessage').css('color','green');
				var newName = json['name'];

				// change name in sidebar by ajax
				var selector = "a[href=\'/getPermissionTemplate/"+oldName+"\']";



				var curElement = $(selector)[0];
				curElement.setAttribute("href","/getPermissionTemplate/"+newName);
				curElement.innerText = newName;				
			}
		})

	}
}

function deletePermission(){
	context = {};
	// get selected permission level id
	context['templateID'] = $(".hiddenId")[0].innerText;

	$.post('/deletePermissionTemplate/',context,function(data){
		//callback
		//directly reload the page
		window.location.href = "/getPermissionTemplate/default";
	})
}

$(document).ready(function(){
	oldName = $(".permissionLevelName")[0].value;

	$(".addNewTemplate").click(function(){
		addOrUpdatePermission("add");
	});
	$(".updateTemplate").click(function(){
		addOrUpdatePermission("update");
	})
	$(".deleteTemplate").click(function(){
		$(".deletePermissionModal").css("display","block");
	})

	$(".closeDeletePermission").click(function(){
		$(".deletePermissionModal").css("display","none");
	})
	$(".confirmDeletePermission").click(function(){deletePermission();});

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

