/* Weather module */

class Weather {
    constructor(id) {
        this.id = id;
    }
    get_id() {
        return this.id;
    }
    processForm(e) {
        if (e.preventDefault) e.preventDefault();

        var latitude = $('#lat-in-' + this.id).val();
        var longitude = $('#lon-in-' + this.id).val();

        console.log("New latitude: " + latitude + "\nNew longitude: " + longitude)

        this.setPosition(latitude, longitude);

        // You must return false to prevent the default form behavior
        return false;
    }

    getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                // Success function
                this.setGeoPosition.bind(this), 
                // Error function
                null, 
                // Options. See MDN for details.
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                });
        } else { 
            //x.innerHTML = "Geolocation is not supported by this browser.";
        }
    }

    setGeoPosition(position) {
        this.setPosition(position.coords.latitude, position.coords.longitude)
    }

    setPosition(latitude, longitude) {
        $.ajax(
        {
            type:"GET",
            url: "/weather/update_weather/",
            dataType: "json",
            data:{
                //csrfmiddlewaretoken: '{{ csrf_token }}',
                id: this.id,
                lat: latitude,
                lon: longitude
            },
            success: function(data) 
            {
                console.log('Success of ajax call for weather-' + this.id + '!')
                $('#lat-' + this.id).html(data.latitude);
                $('#lon-' + this.id).html(data.longitude);
                $('#city-' + this.id).html(data.city);
                $('#country-' + this.id).html(data.country);
                $('#wind_speed-' + this.id).html(data.wind.speed);
                $('#wind_deg-' + this.id).html(data.wind.deg);
                $('#wind_deg-icon-' + this.id).removeAttr('class');
                $('#wind_deg-icon-' + this.id).addClass('wi wi-wind towards-' + data.wind.deg + '-deg');
                $('#humidity-' + this.id).html(data.humidity);
                $('#temp-' + this.id).html(data.temperature.temp);
                $('#temp_min-' + this.id).html(data.temperature.temp_min);
                $('#temp_max-' + this.id).html(data.temperature.temp_max);
                var re = new RegExp('temp-unit-' + this.id + '.*');
                $('span').each(function() {
                    if (this.id.match(re)) {
                        $(this).html(data.unit);
                    }
                });
                $('#status-' + this.id).html(data.status);
                $('#details-' + this.id).html(data.details);
                $('#code-' + this.id).html(data.code);
                $('#weather-icon-' + this.id).removeAttr('class');
                $('#weather-icon-' + this.id).addClass('wi wi-owm-' + data.time_of_day + '-' + data.code);
    
                if ($('#forecasts-' + this.id).length != 0) {
                    var forecasts = [];
                    // Create forecasts
                    for (i in data.forecasts) {
                        var w = data.forecasts[i]
                        forecasts.push('<p>' +
                            '<strong>Time: ' + w.time + '</strong><br/>' + 
                            'Temp: ' + w.temp.temp + ' F (' + w.temp.temp_min + ' - ' + w.temp.temp_max + ')<br/>' +
                            'Status: ' + w.status + '<br/>' +
                            'Code: ' + w.code + '<br/>' +
                            'Time of day: ' + w.time_of_day + '<br/>' +
                            'Icon: <i class="wi wi-owm-' + w.time_of_day + '-' + w.code + '"></i>' +
                            '</p>' 
                        );
                    }
                    $('#forecasts-' + this.id).html(forecasts)
                }
            }.bind(this)
        })
        /*x.innerHTML="Latitude: " + position.coords.latitude + 
            "<br>Longitude: " + position.coords.longitude;  
    
        // Display on a map
        var latlon = position.coords.latitude + "," + position.coords.longitude;
    
        var img_url = "http://maps.googleapis.com/maps/api/staticmap?center=" + latlon + "&zoom=14&size=400x300&sensor=false";
    
        document.getElementById("mapholder").innerHTML = "<img src='" + img_url + "'>";
        */
    }
}

$(document).ready(function() {
    weathers = [];
    $('div').each(function() {
        if (this.id.match(/id-weather-\d+/)) {
            weather = new Weather(this.id.split('-')[2])
            weathers.push(weather);
            /*
            var form = document.getElementById('#latlon-form-' + weather.get_id());
            if (form.attachEvent) {
                form.attachEvent("submit", weather.processForm.bind(weather) );
            } else {
                form.addEventListener("submit", weather.processForm.bind(weather));
            }
            */
        }
    });
    for (var i in weathers) {
        console.log('Getting location of weather-' + weathers[i].get_id())
        weathers[i].getLocation();
    }
});
/*
function processForm(e) {
    if (e.preventDefault) e.preventDefault();

    latitude = $("lat-in").value;
    longitude = $("lon-in").value;

    console.log("New latitude: " + latitude + "\nNew longitude: " + longitude)

    setPosition(latitude, longitude);

    // You must return false to prevent the default form behavior
    return false;
}
*/


//var x = document.getElementById("demo");
/*
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            // Success function
            setGeoPosition, 
            // Error function
            null, 
            // Options. See MDN for details.
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            });
    } else { 
        //x.innerHTML = "Geolocation is not supported by this browser.";
    }
}
*//*
function setGeoPosition(position) {
    setPosition(position.coords.latitude, position.coords.longitude)
}
*/
/*
function setPosition(latitude, longitude) {
    $.ajax(
    {
        type:"GET",
        url: "/update_weather",
        dataType: "json",
        data:{
                //csrfmiddlewaretoken: '{{ csrf_token }}',
                id: '{{ id }}',
                lat: latitude,
                lon: longitude
        },
        success: function(data) 
        {
            $('#lat-{{ id }}').html(data.latitude);
            $('#lon-{{ id }}').html(data.longitude);
            $('#city-{{ id }}').html(data.city);
            $('#country-{{ id }}').html(data.country);
            $('#wind_speed-{{ id }}').html(data.wind.speed);
            $('#wind_deg-{{ id }}').html(data.wind.deg);
            $('#wind_deg-icon-{{ id }}').removeAttr('class');
            $('#wind_deg-icon-{{ id }}').addClass('wi wi-wind towards-' + data.wind.deg + '-deg');
            $('#humidity-{{ id }}').html(data.humidity);
            $('#temp-{{ id }}').html(data.temperature.temp);
            $('#temp_min-{{ id }}').html(data.temperature.temp_min);
            $('#temp_max-{{ id }}').html(data.temperature.temp_max);
            $('#status-{{ id }}').html(data.status);
            $('#details-{{ id }}').html(data.details);
            $('#code-{{ id }}').html(data.code);
            $('#weather-icon-{{ id }}').removeAttr('class');
            $('#weather-icon-{{ id }}').addClass('wi wi-owm-' + data.time_of_day + '-' + data.code);

            if ($('#forecasts-{{ id }}').length != 0) {
                forecasts = [];
                // Create forecasts
                for (i in data.forecasts) {
                    w = data.forecasts[i]
                    forecasts.push('<p>' +
                        '<strong>Time: ' + w.time + '</strong><br/>' + 
                        'Temp: ' + w.temp.temp + ' F (' + w.temp.temp_min + ' - ' + w.temp.temp_max + ')<br/>' +
                        'Status: ' + w.status + '<br/>' +
                        'Code: ' + w.code + '<br/>' +
                        'Time of day: ' + w.time_of_day + '<br/>' +
                        'Icon: <i class="wi wi-owm-' + w.time_of_day + '-' + w.code + '"></i>' +
                        '</p>' 
                    );
                }
                $('#forecasts-{{ id }}').html(forecasts)
            }
        }
    })
    /*x.innerHTML="Latitude: " + position.coords.latitude + 
        "<br>Longitude: " + position.coords.longitude;  

    // Display on a map
    var latlon = position.coords.latitude + "," + position.coords.longitude;

    var img_url = "http://maps.googleapis.com/maps/api/staticmap?center=" + latlon + "&zoom=14&size=400x300&sensor=false";

    document.getElementById("mapholder").innerHTML = "<img src='" + img_url + "'>";
    */
//}*/

function showError(error) {
    /*switch(error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    }*/
}