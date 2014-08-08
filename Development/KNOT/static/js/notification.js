$(document).ready(function(){
	getNotification('all');

	$(".wNavigationAll").click(function(){
		getNotification('all');
	})
	$(".wNavigationConfirm").click(function(){
		getNotification('1');
	})
	$(".wNavigationReminder").click(function(){
		getNotification('2');
	})
	$(".wNavigationTag").click(function(){
		getNotification('3');
	})
	$(".wNavigationConRequest").click(function(){
		getNotification('4');
	})
})


function getNotification(type){
	$.post('/getNotification/',{'nType':type},function(json){
		var wNotificationList=$(".wNotificationList:last").clone(true,true);


		//delete old notification jump title and template 
		notificationSections = $(".wNotificationCenterContainer .wNotificationSectionContainer");
		for(var i=2; i<=notificationSections.length-1;i++){
			$(notificationSections.get(i)).remove();
		}


		for (var i=0;i<json.dates.length;i++){
			var newNotificationList = wNotificationList.clone(true,true);
			newNotificationList.find(".wListTitle").html(json.dates[i]);
			newNotificationList.find(":not('.wListTitle')").remove();
			for (var j=0;j<json[json.dates[i]].length;j++){
				var icon;
				var nType=json[json.dates[i]][j]['nType'];
				var fromUserID = json[json.dates[i]][j]["fromUserID"];
				// 1. friend request confirmation
				console.log("type:"+nType);
				if (nType==="1"){
					icon = "fa-check-square-o";
				}
				// 2. card information change
				else if (nType==="2"){
					icon = "fa-bullhorn";

				}
				// 3. tag name
				else if (nType==="3"){
					icon = "fa-bookmark-o";
				}
				// 4. friend request
				else if (nType==="4"){
					icon = "fa-group";
				}
				//add id
				var notificationIDHtml="<p class=\"wNotificationID\" style=\"display:none\">"+json[json.dates[i]][j]['id']+"</p>";

				if(nType!="4")
					newNotificationList.append("<li>"+notificationIDHtml+"<i class=\'fa "+ icon +" fa-fw\'></i><div class=\'wNotificationName\'><a href=\'/otherCard/"+ fromUserID +"\'>"+json[json.dates[i]][j]['fromUser']+"</a></div>"+json[json.dates[i]][j]['content']+"<button class=\"btn btn-info wNotificationCheckButton\">Check</button></li>");
				else
					newNotificationList.append("<li>"+notificationIDHtml+"<i class=\'fa "+ icon +" fa-fw\'></i><div class=\'wNotificationName\'><a href=\'/otherCard/"+ fromUserID +"\'>"+json[json.dates[i]][j]['fromUser']+"</a></div>"+json[json.dates[i]][j]['content']+"<button class=\"btn btn-success wNotificationAcceptButton\">Accept</button><button class=\"btn btn-inverse wNotificationDeclineButton\">Decline</button></li>");


			}
			var ul = $("<ul></ul>").addClass('wNotificationList').html(newNotificationList.html());
			var container = $("<div></div>").addClass("wNotificationSectionContainer").append(ul);
			$(".wNotificationCenterContainer").append(container);
		}

		//bind click event
		$(".wNotificationCheckButton").bind("click",checkNotification);
		$(".wNotificationDeclineButton").bind("click",checkNotification);
		$(".wNotificationAcceptButton").bind("click",confirmFriendRequest);
	})
}



function checkNotification(){
	var notificationID = $(this).parent().find('.wNotificationID').html();
	content={}
	content['notificationID']=notificationID
	var notification = $(this).parent()
	var notificationSection = notification.parent()
	$.post('/deleteNotification/',content, function(json){
		console.log(json);

		//no notification in today, remove notification section
		if(notification.parent().find("li:not(.wListTitle)").length>1)
			notification.remove();
		else
			notificationSection.remove();
	})
}

function confirmFriendRequest(){
	var notificationID = $(this).parent().find('.wNotificationID').html();
	content={}
	content['notificationID']=notificationID
	var notification = $(this).parent()
	var notificationSection = notification.parent()
	$.post('/addFriend/',content, function(json){
		console.log(json);

		//no notification in today, remove notification section
		if(notification.parent().find("li:not(.wListTitle)").length>1)
			notification.remove();
		else
			notificationSection.remove();
	})	
}

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