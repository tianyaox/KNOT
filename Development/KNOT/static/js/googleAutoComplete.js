// For auto filling city fields

function initialize(){
    var options = {
        types:['(cities)']
    };

	var input = document.getElementById("cityInput1");

	var autocomplete = new google.maps.places.Autocomplete(input,options);

	var input2 = document.getElementById("cityInput2");

	var autocomplete2 = new google.maps.places.Autocomplete(input2,options);
	
	var input3 = document.getElementById("city3Auto");

	var autocomplete3 = new google.maps.places.Autocomplete(input3,options);
	
	var input4 = document.getElementById("city4Auto");

	var autocomplete4 = new google.maps.places.Autocomplete(input4,options);
	
	var input5 = document.getElementById("city5Auto");

	var autocomplete5 = new google.maps.places.Autocomplete(input5,options);


}

google.maps.event.addDomListener(window, 'load', initialize);

