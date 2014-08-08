// Global used for iterating all the needed fileds
var cardItemList = ["firstName","lastName",
"gender","title","birthday","citizenship",
"address1","address2","address3","address4","address5",
"city1","city2","city3","city4","city5",
"phone1","phone2","phone3","phone4","phone5",
"email1","email2","email3","email4","email5",
"blog"];




// Change the friend's group
function changeGroup(){
	var selection = $(".changeGroupSelect")[0];
	var permissionName = "";
	var url = $(location).attr('href');
	var friendID = url.substring(url.lastIndexOf("/")+1,url.length);
	// Ignore "#" in the url
	if (friendID.indexOf("#")!==-1){
		friendID = friendID.slice(0,friendID.indexOf("#"));
	}
	// Get selected value
	for (var i=0;i<selection.children.length;i++){
		if (selection.children[i].selected===true){
			permissionName = selection.children[i].text;
		}
	}
	$.post("/updateFriendPermission/",{'permissionName':permissionName,'friendID':friendID},function(json){

		var delimiter = '/',
		    start = "3",
		    tokens = url.split(delimiter).slice(start),
		    result = tokens.join(delimiter); // those.that
		url = url.slice(0,url.indexOf("#"));
		window.location.href = url;
	})


}
// Show detail profile animation 

function showProfile(element){
	var $this = $(element).parent().parent();

	// Basic info (name, title...)
	if (element.indexOf("old1")!==-1){


	 	$(".xShowAddress").fadeOut(function(){
	  		$(this).parent().parent().css({"display":"none"});
	  	});

		$(".xShowInfoNew").fadeOut(function(){
	  		$(this).parent().parent().css({"display":"none"});
	  	});
	  	$(".xShowSSN").fadeOut();

	  	$this.animate(
	    	{height:'203%',
	    	width:'203%'},
	    	750, "swing",function(){
	  			$(".old1").css({"display":"none"});
	    		$(".new1").css({"display":"block"});
	    	}
	  	);
	}
	// Contact info (address, phone...)
	else if (element.indexOf("old2")!==-1){

     	$(".xShowProfile").fadeOut();
     	$(".xShowSSN").fadeOut();

      	$this.animate(
        	{

        	width:'201%',
        	left:'-102%'},
        	750, "swing",function(){
				$(".old2").css({"display":"none"});
	    		$(".new2").css({"display":"block"});
        	}
        );
	}

	else if (element.indexOf("old3")!==-1){
		$(".xShowAddress").parent().parent().css({"display":"none"});

		$(".xShowAddress").fadeOut(function(){
        });
        $(".xShowProfile").fadeOut();
        $this.animate(
            {height:'330px',
            width:'645px',
            left:'-328px',
            top:'0px'},
            750, "swing",function(){
				$(".old3").css({"display":"none"});
	    		$(".new3").css({"display":"block"});
	    		// $(this).css({"top":"0"});
            }
        );
	}
}

// Hide detail profile animation 
function hideProfile(element){
	// Basic info (name, title...)

	if (element.indexOf("new1")!==-1){
		$(element).parent().parent().animate(
			{height:'100%',
		    width:'100%'},
		    750, "linear",function(){
		  		$(".old1").css({"display":"block","height":"100%","width":"100%"});
		    	$(".new1").css({"display":"none"});
		        $(".xShowSSN").fadeIn();
		        $(".xShowInfoNew").parent().parent().css({"display":"block"});
				$(".xShowInfoNew").fadeIn();
		});
	}
	// Contact info (address, phone...)

	else if (element.indexOf("new2")!==-1){
		$(element).parent().parent().animate(
            {height:'100%',
            width:'100%',
            left:'0px'},
            750, "swing",function(){
            	$(".old2").css({"display":"block","height":"100%","width":"100%"});
		    	$(".new2").css({"display":"none"});
	            $(".xShowProfile").fadeIn();
	            // $(".xShowInfo").parent().parent().css({"display":"block"});
	            // $(".xShowInfo").fadeIn();
	            $(".xShowSSN").fadeIn();
            }
        );
	}

	else if (element.indexOf("new3")!==-1){
		$(element).parent().parent().animate(
		   	{height:'100%',
            width:'100%',
            left:'0px',
            top:'0px'},
            750, "swing",function(){
            	$(".old3").css({"display":"block","height":"100%","width":"100%"});
		    	$(".new3").css({"display":"none"});
              	$(".xShowProfile").fadeIn();
              	$(".xShowAddress").parent().parent().css({"display":"block"});
              	$(".xShowAddress").fadeIn();
            });
	}

}


$(document).ready(function(){

	$("select").selectpicker({style: 'btn', menuStyle: 'dropdown-inverse'});

	if ($(".gender").html()==="M"){
		$(".gender").html("♂");
		$(".gender").css('color','blue');
	}
	else if ($(".gender").html()==="F"){
		
		$(".gender").html("♀");	
		$(".gender").css('color','pink');


	}	
	$(".xEditIcon").click(function(){
	  	syncInputValue();

	 	if($(this).parents(".flipcard").hasClass("flip")){
	      $(this).parents(".flipcard").removeClass("flip");
	    }
	    else{
	      $(this).parents(".flipcard").addClass("flip");
	    }
	});
	$(".xRecordIcon").click(function(){

		$(".record").fadeIn();
	});
	$(".xCameraIcon").click(function(){
		$(".takePhoto").fadeIn();
		startVideo();
	})

	$( ".xShowProfilePicture" ).hover(function(){
		$(".playRecordButton").css('display','block');
	},function(){
		$(".playRecordButton").css('display','none');

	});
	$(".closeInfoWindow").click(function(){
		$(".moreInfo").css("display","none");	
	});
	$(".closeShowInfoWindow").click(function(){
		$(".showMoreInfo").css("display","none");	
	});
	$(".closeChangeGroup").click(function(){
		$(".changeGroupModal").css("display","none");	
	});

	$(".addMore").click(function(){
		$(".moreInfo").css("display","block");
	})
	$(".xShowMoreInfo").click(function(){
		$(".showMoreInfo").css("display","block");
	})
	$(".editChangeGroup").click(function(){
		$(".changeGroupModal").css("display","block");
	})
	$(".changeGroupConfirm").click(changeGroup);

	$(".submitUploadPicButton").click(function(){

		$("#uploadPicForm").submit();
	});
	$(".xUploadPicture").click(function(){
		$(".uploadPicModal").css("display","block");
	})
	$(".closeUploadModal").click(function(){
		$(".uploadPicModal").css("display","none");
	})	
	$(".closeError").click(function(){
		$(".errorModal").css("display","none");

	})
})


// Used for syncing the input text box value when fliping the card and ajax update after submitting
function syncInputValue(){
	$.post('/getMyCard/',{},function(json){

		for (var i=0;i<cardItemList.length;i++){
			var item = cardItemList[i];
			if (item!=="gender"){
				$('[name=\"'+item+'\"]').val(json.card[item]);		
			}
		}
		var gender = json.card.gender;

		if (gender==="M"){
			$("span.filter-option.pull-left").text("Male");
			$("[rel='0']").addClass("selected");
			$("[rel='1']").removeClass("selected");

		}
		else if(gender==="F"){
			$("span.filter-option.pull-left").text("Female");
			$("[rel='1']").addClass("selected");
			$("[rel='0']").removeClass("selected");

		}
		for (var i=0;i<cardItemList.length;i++){
			if (cardItemList[i]!=="firstName" && cardItemList[i]!=="lastName")
			{
				$('.'+cardItemList[i]).html(json.card[cardItemList[i]]);
			}
		}
		$(".name").html(json.card['firstName']+" "+json.card['lastName']);
		var addressList = ["address1","address2","address3","address4","address5"]
		var cityList = ["city1","city2","city3","city4","city5"]
		for (var i=0;i<addressList.length;i++){
			if (json.card[addressList[i]]!=="" && json.card[cityList[i]]!==""){
				$("."+addressList[i]).html(json.card[addressList[i]]+", "+json.card[cityList[i]]);
			}
			else if (json.card[addressList[i]]==="" && json.card[cityList[i]]!==""){
				$("."+addressList[i]).html(json.card[cityList[i]]);	
			}
			else if (json.card[addressList[i]]!=="" && json.card[cityList[i]]===""){
				$("."+addressList[i]).html(json.card[addressList[i]]);

			}
			else if (json.card[addressList[i]]==="" && json.card[cityList[i]]===""){
				$("."+addressList[i]).html("");
			}
		}



		var gList = $(".gender");
		for (var i=0;i<gList.length;i++){
			var g = gList[i];
			if (g.textContent==="M"){
				g.textContent=" ♂";
				g.style.color="blue";
			}
			else if (g.textContent==="F"){
				g.textContent=" ♀";
				g.style.color="pink";
			}
		}
	})
}

// Do updating
function updateMyCard(){
	var context={};
	var phoneList = ["phone1","phone2","phone3","phone4","phone5"]
	var emailList = ["email1","email2","email3","email4","email5"]
	var errors = [];
	for (var i=0;i<cardItemList.length;i++){
		if (phoneList.indexOf(cardItemList[i])!==-1){
			var phone = $('[name=\"'+cardItemList[i]+'\"]').val();

			if (isNaN(phone)){
				errors.push(cardItemList[i]+ " should be only numbers.");
			}
		}
		if (emailList.indexOf(cardItemList[i])!==-1){
			var email = $('[name=\"'+cardItemList[i]+'\"]').val();

			if (email.indexOf("@")===-1 && email!==""){
				errors.push(cardItemList[i]+ " should be an email address.");
			}
		}
	}




	// The front error check is not used. The backend form error check is used instead.



	for (var i=0;i<cardItemList.length;i++){

		if (cardItemList[i]!=="gender"){
			context[cardItemList[i]]=$('[name=\"'+cardItemList[i]+'\"]').val();
		}
		else if (cardItemList[i]==="gender"){
			if ($("[selected='selected']").text()==="Female"){
				context[cardItemList[i]]="F";
			}
			else if ($("[selected='selected']").text()==="Male"){
				context[cardItemList[i]]="M";
			}
		}
	}


	$.post('/updateMyCard/',context,function(json){
		// console.log(context);
		console.log(json);
		if ('errors' in json){
			console.log(json.errors);
			var curErrors = json.errors;
			console.log(curErrors);

			$(".errorBody").html("");
			for(var i=0;i<curErrors.length;i++){
				$(".errorBody").append("<div style='color:red;'>"+curErrors[i]+"</div>");
			}
			$(".errorModal").css("display","block");
		}
		syncInputValue();
	})

}


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



