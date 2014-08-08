$(document).ready(function(){
	$("#bAccountSuc").html("");
	$("#bAccountChangeError").html("");
	$(".bAccountChange").hide();
	$(".bPasswordChange").show();

	$(".bPasswordLink").click(function(){
		$("#bAccountSuc").html("");
		$("#bAccountChangeError").html("");
		$(".bAccountChange").hide();
		$(".bPasswordChange").show();
	})

	$(".bAccountLink").click(function(){
		$("#bAccountSuc").html("");
		$("#bAccountChangeError").html("");
		$.get('/account/1',function(data){
			console.log("abc");
			$(".bAccountChange").show();
			$(".bPasswordChange").hide();
		})
	})

	$("#bEmailChange").click(function(){
		$.ajax({
			type:"POST",
			url:"/account/2",
			data:{email:$(this).prev().val()},
			dataType:"json",
			async:true,
			success:function(result){
				if (result["errors2"] != undefined){
                    var errors = result["errors2"];

                    var errorDiv = $("#bAccountChangeError");
                    $("#bAccountChangeError li").remove();
                    var errorEl = document.createElement("li");
                    errorEl.setAttribute("class","bChangeError");
                    errorEl.innerHTML = errors[0];
                    errorDiv.append(errorEl);
                }
                else{
                	$("#bAccountChangeError li").remove();
                    var message = result["message"];
                    console.log("message is" + message);
                    $("input[name=email]").remove();
                    $("button[id=bEmailChange]").remove();
                    var alert = document.createElement("h6");
                    alert.setAttribute("class","bUpdateSuc");
                    alert.innerHTML = message;
                    var divEl = $(".bAccountSetting");
                    divEl.append(alert);

                }
			}
		})
		
	})
})