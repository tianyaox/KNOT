var video = document.querySelector('video');
var canvas = document.querySelector('canvas');
var ctx = canvas.getContext('2d');
var localMediaStream = null;
var recorder = null;
var audio = document.querySelector('audio');
var counter = 10;
var counterForUpload = 5;

$(document).ready(function(){
	$("#snapShotButton").click(snapshot);
	$("#startVideoButton").click(startVideo);
	$("#uploadImageButton").click(uploadImage);
	$("#startRecordButton").click(startRecord);
	$("#stopRecordButton").click(stopRecord);
	$("#upLoadAudioButton").click(function(){
		$(".overlay").css('display','block');
		uploadAudio();
		
		setInterval(function(){
			counterForUpload-=1;
			if( counterForUpload === 0 ){

				$(".overlay").css('display','none');
				$(".recordStatus3").css('display','block');
				$(".recordStatus3").css('visibility','visible');
				$(".recordStatus1").css('display','none');
				$(".recordStatus2").css('display','none');
				$(".recordStatus1").css('visibility','hidden');
				$(".recordStatus2").css('visibility','hidden');
				window.location.href = "/myCard/";
				clearInterval();
				counterForUpload = 5;
			}
		},1000);


	});
	$(".closeRecordWindow").click(function(){
		$(".record").css("display","none");
	})
	$(".closePhotoWindow").click(function(){
		$(".takePhoto").css("display","none");
	})

	// var cam:Camera = Camera.getCamera();
	// if (cam != null)
	// {
	//     cam.addEventListener(StatusEvent.STATUS, statusHandler);
	//     var vid:Video = new Video();
	//     vid.attachCamera(cam);
	//     addChild(vid);
	// }



})

// function statusHandler(event:StatusEvent):void
// 	{
// 	    // This event gets dispatched when the user clicks the "Allow" or "Deny"
// 	    // button in the Flash Player Settings dialog box.
// 	    if (cam.muted)
// 	    {
// 	        trace("User clicked Deny.");
// 	    }
// 	    else
// 	    {
// 	        trace("User clicked Accept.");
// 	    }
// 	}


function snapshot() {
	if (localMediaStream) {
	  	ctx.drawImage(video, 0, 0);
	  	// "image/webp" works in Chrome.
	  	// Other browsers will fall back to image/png.
	  	document.querySelector('img').src = canvas.toDataURL('image/webp');
	}
}

function uploadImage(){

  	var snapShot = canvas.toDataURL('image/jpeg').replace("data:image/jpeg;base64,", "");
	$(".overlay").css('display','block');
  	
  	$.ajax({
  		type:"POST",
  		url:"/uploadImageFromCamera/",
  		data:{image:snapShot}
  	}).done(function(json){
  		console.log(json['status']);
		$(".overlay").css('display','none');
		window.location.href = "/myCard/";


  	})
}

function hasGetUserMedia() {
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function startVideo(){
	if (hasGetUserMedia()) {
	  // Not showing vendor prefixes.
	  // get user media


		navigator.getUserMedia  = navigator.getUserMedia ||
		                          navigator.webkitGetUserMedia ||
		                          navigator.mozGetUserMedia ||
		                          navigator.msGetUserMedia;
		var vgaConstraints = {
		  video: {
		    mandatory: {
		      maxWidth: 640,
		      maxHeight: 480
		    }
		  }
		};


		// video.addEventListener('click', snapshot, false);

		navigator.getUserMedia(vgaConstraints, function(stream) {
		    video.src = window.URL.createObjectURL(stream);
		    localMediaStream = stream;
		})
	}
	else {
		alert('HTML5 feature is not supported in your browser');
	}
}


function startRecord(){
	if (hasGetUserMedia()) {
		// alert("Start Recorder")
		navigator.getUserMedia  = navigator.getUserMedia ||
		                          navigator.webkitGetUserMedia ||
		                          navigator.mozGetUserMedia ||
		                          navigator.msGetUserMedia;

		navigator.getUserMedia({audio: true}, function(stream){
	        var context = new webkitAudioContext();
	        var mediaStreamSource = context.createMediaStreamSource(stream);
	        recorder = new Recorder(mediaStreamSource);
	        recorder.record();
		});
		$(".recordCounter").html(counter);
		setInterval(function(){
			counter-=1;
			$(".recordCounter").html(counter);
			if( counter === 0 ){
				stopRecord();
				clearInterval();
				counter = 10;
				$(".recordCounter").html();
			}
		},1000);
		$(".recordStatus2").css("display","none");
		$(".recordStatus3").css("display","none");
		$(".recordStatus2").css("visibility","hidden");
		$(".recordStatus3").css('display','hidden');

		$(".recordStatus1").css("display","block");
		$(".recordStatus1").css("visibility","visible");
	}
	else {
		alert('HTML5 feature is not supported in your browser');
	}
}

function stopRecord(){
	if(recorder){
        recorder.stop();
        recorder.exportWAV(function(stream) {
          audio.src = window.URL.createObjectURL(stream);
        });
		$(".recordStatus1").css("display","none");
		$(".recordStatus3").css("display","none");
		$(".recordStatus1").css("visibility","hidden");
		$(".recordStatus3").css("visibility","hidden");

		$(".recordStatus2").css("display","block");
		$(".recordStatus2").css("visibility","visible");

	}
}

function uploadAudio(){
	if(recorder){
		recorder.exportWAV(function(blob){
			var form = new FormData();
			form.append("audio",blob);
			$.ajax({
		  		type:"POST",
		  		url:"/uploadAudio/",
		  		data: form,
		  		processData: false,
		  		contentType: false,
		  	}).done(function(json){
		  		console.log(json);
		  	})
		})
	}
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


