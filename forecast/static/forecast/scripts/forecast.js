/* Forecast module */

class Forecast {
    constructor(id) {
        this.id = id;
    }
    get_id() {
        return this.id;
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
            url: "/forecast/update_forecast/",
            dataType: "json",
            data:{
                //csrfmiddlewaretoken: '{{ csrf_token }}',
                id: this.id,
                lat: latitude,
                lon: longitude
            },
            success: function(data) 
            {
                console.log('Success of ajax call for forecast-' + this.id + '!')
                /*
                $('#lat-' + this.id).html(data.latitude);
                $('#lon-' + this.id).html(data.longitude);
                */
                $('#city-' + this.id).html(data.city);
                $('#country-' + this.id).html(data.country);
                $('#time-start-' + this.id).html(data.time_start);
                $('#time-end-' + this.id).html(data.time_end);

                // Create forecasts
                var forecasts = [];
                for (i in data.forecasts) {
                    var w = data.forecasts[i]
                    forecasts.push(
                        '<div class="col">' +
                        '<div class="row">' +
                        '<div class="col time-forecast">' + w.time + 
                        '</div></div>' +
                        '<div class="row">' +
                        '<div class="col">' +
                        '<div class="row">' +
                        '<div class="col weather-icon-forecast">' +
                        '<i class="wi wi-owm-' + w.time_of_day + '-' + w.code + '"></i>' +
                        '</div></div>' +
                        '<div class="row">' +
                        '<div class="col temp-forecast">' + w.temp.temp + '&#176; F' +
                        '</div></div>' +
                        '</div></div>'
                    );
                    //'Temp: ' + w.temp.temp + ' F (' + w.temp.temp_min + ' - ' + w.temp.temp_max + ')<br/>' +
                    //'Status: ' + w.status + '<br/>' +
                }
                $('#forecasts-' + this.id).html(forecasts)
            }.bind(this)
        })
    }
}

$(document).ready(function() {
    forecasts = [];
    $('div').each(function() {
        if (this.id.match(/id-forecast-\d+/)) {
            forecast = new Forecast(this.id.split('-')[2])
            console.log('forecast id: '+this.id);
            forecasts.push(forecast);
        }
    });
    for (var i in forecasts) {
        console.log('Getting location of forecast-' + forecasts[i].get_id())
        forecasts[i].getLocation();
    }
});