// Do deleting friend
function deleteFriend(id){
	context = {};
	context['friendID'] = id;
	$.post('/deleteFriend/',context,function(data){
		window.location.href = "/contacts/all";
	})
}

// Submit search form (search contacts using name)
function searchContacts(){
    $('#searchContactForm').submit();
}


function getFriendMap(locations, friends) {
    var mapOptions = {
        zoom: 2,
        center:new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("bGoogleMap"),mapOptions);  

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent("<div style=\"width:150px;height:20px;\">"+ locations[i][0] + "<div>");
                infowindow.open(map, marker);
            }
        })(marker, i));
    }
}

function showLocation(){
    var mapOptions = {
        zoom: 2,
        center:new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("bGoogleMap"),mapOptions);
    $.post('/getFriendLocation/',function(data){

        getFriendMap(data['locations'], data['friends']);
    })
}




$(document).ready(function(){
	var url = $(location).attr('href');
	var lastUrl = url.substring(url.lastIndexOf("/")+1,url.length);
	var capitalFirstLastUrl = lastUrl.charAt(0).toUpperCase() + lastUrl.slice(1);
	var leftNavs = $(".leftNav");
    // Check left side bar and make the selected item active (looks like been selected in frontend)
	for (var i=0;i<leftNavs.length;i++){
		leftNav = leftNavs[i];
		leftNav.parentNode.className = "";
		if (leftNav.text.indexOf(lastUrl)!=-1 || leftNav.text.indexOf(capitalFirstLastUrl)!=-1){
			leftNav.parentNode.className = "active";
		}

	}
	$(".removeButton").click(function(){
		var friendId = $(this)[0].id;
        $(".removeConfirm").css('display','block');
        $(".confirmRemove").click(function(){
            deleteFriend(friendId);
        })
	})

    $(".closeRemoveConfirm").click(function(){
        $(".removeConfirm").css('display','none');
    })


    $(".xSearchContacts").click(searchContacts);

    $(".bLocation").click(function(){
        $("#bGoogleContent").show();
        $(".container").css("opacity","0.1");
        showLocation();
    })

    $(".bMapClose").click(function(){
        $("#bGoogleContent").hide();
        $(".container").css("opacity","1");
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


