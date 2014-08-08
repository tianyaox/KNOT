function search(){
	var context = {};
	var conditions = ['range'];
	// modify the input into the right format and store the value in context
	context['range'] = 'strangers';
	var name = $("#bSearchName")[0].value;
	context['name'] =name;
	if (name!==null && name!==""){conditions.push('name');}
	var gender = $(".gender")[1].children[1].firstChild.innerHTML;
	var age = $(".age")[1].children[1].firstChild.innerHTML;


	var currentCity = $("#bCurrentCity")[0].value;
	context['currentCity'] =currentCity;
	if (currentCity!==null && currentCity!==""){conditions.push('currentCity');}

	var mutualFriendStr = $(".mutualFriend")[0].value;
	var mutualFriends = [];
	var p1=0;
	var p2=0;
	var ageMin="";
	var ageMax="";
	if (mutualFriendStr!==""){
		for (var i=0;i<mutualFriendStr.length;i++){
			if (mutualFriendStr[i]===","){
				p2 = i;
				mutualFriends.push(mutualFriendStr.substring(p1,p2));
				p1 = p2+1;
			}
		}
		mutualFriends.push(mutualFriendStr.substring(p1,mutualFriendStr.length));
	}	

	if (gender === "Female"){ gender="F"; }
	else if (gender==="Male"){ gender="M"; }
	else {gender="";}
	context['gender']=gender;
	if (gender!==""){conditions.push('gender');}


	if (age.indexOf("~")!==-1){
		ageMin = age.substring(0,age.indexOf("~"));
		ageMax = age.substring(age.indexOf("~")+1,age.length);
		conditions.push("age");
	}
	else if(age.indexOf("+")!==-1){
		ageMin = age.substring(0,age.indexOf("+"));
		ageMax = "100";
		conditions.push("age");
	}

	context['ageMax']=ageMax;
	context['ageMin']=ageMin;



	for (var i=0;i<mutualFriends.length;i++){
		var j = i+1;
		var newLable = "mutualFriend"+j;
		context[newLable] = mutualFriends[i];
	}

	if ("mutualFriend1" in context){ conditions.push('mutualFriend'); }
	context['conditions'] = conditions;


	$.post('/search/',context,function(data){
		// use ajax, update the entire html in .xSearchPage
		var a=$(data).find(".xSearchPage");
		$(".xSearchPage").replaceWith(a);
			$(".addButton").click(function(){
		var friendId = $(this)[0].id;
		$(".addConfirm").css("display","block");
		$(".confirmAdd").click(function(){
			addFriendRequest(friendId);
		})
	});
		},'html');


}

// send a friend request. triggered when clicking ok in the pop up window.
function addFriendRequest(id){
	context = {};
	context['friendID'] = id;
	$.post('/addFriendRequest/',context,function(data){
		window.location.href = "/search/";

		$(".addConfirmAfter").css('display','block');
	})

}


$(document).ready(function(){
	$('.tagsinput').tagsInput();
	$("select").selectpicker({style: 'btn', menuStyle: 'dropdown-inverse'});
	$('.search').click(function(){
		search();
	})
	$(".addButton").click(function(){
		var friendId = $(this)[0].id;
		$(".addConfirm").css("display","block");
		$(".confirmAdd").click(function(){
			addFriendRequest(friendId);
		})
	})
	$(".closeAddConfirm").click(function(){
		$(".addConfirm").css("display","none");
	})
	$(".closeAddConfirmAfter").click(function(){
		$(".addConfirmAfter").css("display","none");
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


// used for city name auto fill
function initialize() {
           var options = {
               types:['(cities)']
           };

            var input = document.getElementById("bCurrentCity");
            var autocomplete = new google.maps.places.Autocomplete(input,options);
            var input2 = document.getElementById("bSearchCity");
            var autocomplete2 = new google.maps.places.Autocomplete(input2,options);
        }

google.maps.event.addDomListener(window, 'load', initialize);

