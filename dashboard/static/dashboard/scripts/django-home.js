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