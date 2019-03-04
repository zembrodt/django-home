/* Datetime module scripts */

// Function to pad leading zeros
Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
}

const seconds_inc = 1000;
const minutes_inc = seconds_inc * 60;
const hours_inc = minutes_inc * 60;
const month_names = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
];

class Datetime {
    constructor(id) { // other things?
        this.id = id;
        this.twenty_four_hours = parseInt($('#twenty_four_hours-' + id).val());
    }
    get_id() {
        return this.id;
    }
    is_twenty_four_hours() {
        return this.twenty_four_hours === 1;
    }
}

// TODO: do we want to move these functions into the Datetime class?

// Set the clock values
function set_seconds(datetime) {
    $('#second-' + datetime.get_id()).html((new Date().getSeconds()).pad(2));
}
function set_minutes(datetime) {
    $('#minute-' + datetime.get_id()).html((new Date().getMinutes()).pad(2));
}
function set_hours(datetime) {
    var date = new Date();
    var hour = date.getHours();
    if (!datetime.is_twenty_four_hours()) {
        var am_pm = 'AM';
        if (hour === 0) {
            hour = 12;
        }
        else if (hour === 12) {
            am_pm = 'PM';
        }
        else if (hour > 12) {
            hour -= 12;
            am_pm = 'PM';
        }
        $('#am-pm-' + datetime.get_id()).html(am_pm);
    }
    $('#hour-' + datetime.get_id()).html(hour.pad(2));
    $('#date-' + datetime.get_id()).html(month_names[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear());
    //temp
    $('#timezone-' + datetime.get_id()).html('EST');
}

// Starts the timers for each value
function start_clock(datetime) {
    // Re-initialize all the values
    set_seconds(datetime);
    set_minutes(datetime);
    set_hours(datetime);
    // Set timers
    setInterval(function() { return set_seconds(datetime); }, seconds_inc);
    setInterval(function() { return set_minutes(datetime); }, minutes_inc);
    setInterval(function() { return set_hours(datetime); }, hours_inc);
}

function init_clock(datetime) {
    console.log('Starting clock with id ' + datetime.get_id())
    // Initialize all the values
    set_seconds(datetime);
    set_minutes(datetime);
    set_hours(datetime);

    var seconds = new Date().getSeconds();
    var ticks = 60 - seconds;
    var secondsInterval = setInterval(function() {
        set_seconds(datetime);
        ticks--;
        if (ticks == 0) {
            window.clearInterval(secondsInterval);
            start_clock(datetime);
        }
    }, seconds_inc);
}

// Main code
datetimes = []
$('div').each(function() {
    if (this.id.match(/id-dt-\d+/)) {
        datetimes.push(new Datetime(this.id.split('-')[2]));
    }
});

for (var i in datetimes) {
    init_clock(datetimes[i]);
}