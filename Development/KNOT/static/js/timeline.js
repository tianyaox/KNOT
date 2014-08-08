$(document).ready(function(){


	//pin sidebar


	$(".wTimeLineMiddleLine").animate({
		display:"block",
		height: $(".wTimeLineContainer").height()+20,
	},2000,function(){
		$(".wLeftCardContainer").animate({opacity:"1"},2000);
		$(".wRightCardContainer").animate({opacity:"1"},2000);
	});


	//infinate scrolling
	// $(window).scroll(function(){
	// 	//pin sidebar
	// 	$(".wTimeLineSideBarContainer>ul").css("top",$(window).scrollTop().toString()+"px");


	// 	if(($(window).scrollTop() == ($(document).height() - $(window).height())) && !$(".wTimeLineLoadContainer").is(":animated")){

	// 		$leftContainers=$(".wTimeLineLeftContainer");
	// 		$rightContainers=$(".wTimeLineRightContainer");
	// 		$middleLineContainer=$(".wTimeLineMiddleLine");

	// 		//spin show 
	// 		$(".wTimeLineLoadContainer").slideDown(1000,function(){
	// 			$(this).delay(3000).slideUp(1000, function(){
	// 				//add left card
	// 				var leftCardTemplate = $($(".wLeftCardContainer").get(0)).clone();
	// 				var newLeftCard = $("<div></div>").addClass("wLeftCardContainer").html(leftCardTemplate.html());//.css("opacity","1");
	// 				var newClearFloat = $("<div></div>").addClass("wClearFloat");

	// 				$leftContainers.append(newLeftCard);
	// 				$leftContainers.append(newClearFloat);

	// 				//add right card
	// 				var rightCardTemplate = $($(".wRightCardContainer").get(0)).clone();
	// 				var newRightCard = $("<div></div>").addClass("wRightCardContainer").html(rightCardTemplate.html());//.css("opacity","1");
	// 				var newClearFloat1 = $("<div></div>").addClass("wClearFloat");

	// 				$rightContainers.append(newRightCard);
	// 				$rightContainers.append(newClearFloat1);					

	// 				//timeline expand
	// 				$(".wTimeLineMiddleLine").animate({height:$(".wTimeLineContainer").height()+20},500,function(){
	// 					$(".wLeftCardContainer").animate({opacity:"1"},2000);	
	// 					$(".wRightCardContainer").animate({opacity:"1"},2000);	
	// 				});
	// 				// $(".wTimeLineMiddleLine").height($(".wTimeLineContainer").height()+20);	
	// 				// $(".wLeftCardContainer").animate({opacity:"1"},2000);				
	// 			})
	// 		})
	// 		// alert(123);
	// 		// var leftContainer = $($(".wLeftCardContainer").get(0)).clone();
	// 		// var newLeftContainer = $("<div></div>").addClass("wLeftCardContainer").html(leftContainer.html()).css("opacity","1");
	// 		// var newClearFloat = $("<div></div>").addClass("wClearFloat");

	// 		// console.log($(".wTimeLineContainer").height());

	// 		// $(".wTimeLineLeftContainer").append(newLeftContainer);

	// 		// $(".wTimeLineLeftContainer").append(newLeftContainer);

	// 		// $(".wTimeLineLeftContainer").append(newLeftContainer);
	// 		// $(".wTimeLineLeftContainer").append(newClearFloat);


	// 		// $(".wTimeLineMiddleLine").height($(".wTimeLineContainer").height()+20);


	// 	}
	// })
});	

// function wAddCircleToMiddleLine(){
// 	var wLeftCardArrowTopOffset=30;
// 	var wRightCardArrowTopOffset=40;
// 	var wLeftCards =$(".wLeftCardContainer");
// 	var wTimeLineMiddleLine=$(".wTimeLineMiddleLine");
// 	var wTimeLineMiddleLinePosition=wTimeLineMiddleLine.offset();
// 	var wTimeLineMiddleLineWidth=wTimeLineMiddleLine.width();


// 	$(".wLeftCardContainer").each(function(index, value){
// 		wTimeLineMiddleLine.append("<i class=\"fa fa-circle-o\ wTimeLineMiddleLineIcon\"></i>");

// 		var wContainerPosition= $(this).offset();
// 		var wIconPosition = wContainerPosition;
// 		wIconPosition.left = wTimeLineMiddleLinePosition.left-wTimeLineMiddleLineWidth/2;
// 		wIconPosition.top = wContainerPosition.top+wLeftCardArrowTopOffset;

// 		$(".wTimeLineMiddleLineIcon").last().css(wIconPosition);
// 	})

// 	$(".wRightCardContainer").each(function(index, value){
// 		wTimeLineMiddleLine.append("<i class=\"fa fa-circle-o\ wTimeLineMiddleLineIcon\"></i>");

// 		var wContainerPosition= $(this).offset();
// 		var wIconPosition = wContainerPosition;
// 		wIconPosition.left = wTimeLineMiddleLinePosition.left-wTimeLineMiddleLineWidth/2;
// 		wIconPosition.top = wContainerPosition.top+wRightCardArrowTopOffset;

// 		$(".wTimeLineMiddleLineIcon").last().css(wIconPosition);
// 	})
// }