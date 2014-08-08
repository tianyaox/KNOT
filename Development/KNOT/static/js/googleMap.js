$(document).ready(function(){

    $(".bGetAddress").click(function(){
        $("#bAddressContent").show();
        $(".container").css("opacity","0.1");
        getMap();
    })

    $(".bAddressClose").click(function(){
        $("#bAddressContent").hide();
        $(".container").css("opacity","1");
    })

})

function getMap() {
            var userLocations = document.getElementsByClassName("address1");
            var userLocation = userLocations[0].lastChild.textContent;
            console.log(typeof userLocation);
            var pointOfView = { heading:120, pitch:0, zoom:1};

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode(
                    {'address': userLocation},
                    function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            // Prepare to draw street map
                            var mapOptions = {
                                zoom: 15,
                                center: results[0].geometry.location,
                                mapTypeId: google.maps.MapTypeId.ROADMAP
                            };
                                    // place a street map at map-main
                                    var map = new google.maps.Map(document.getElementById("bAddressMap"),mapOptions);
                                    new google.maps.Marker({
                                        position: results[0].geometry.location,
                                        map: map,
                                        title:'Your Location'
                                    });
                        }
                        else {
                            var map = document.getElementById("bAddressMap");
                            map.innerHTML = "Geocode failed. Reason: " + status;
                        }
                    }
            );
        }