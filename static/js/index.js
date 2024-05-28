var monthField = document.getElementById('month')
var dayField = document.getElementById('day')
var yearField = document.getElementById('year')

var daysInMonth = {
  'January': 31,
  'February': 28,
  'March': 31,
  'April': 30,
  'May': 31,
  'June': 30,
  'July': 31,
  'August': 31,
  'September': 30,
  'October': 31,
  'November': 30,
  'December': 31
};

monthField.addEventListener('change', updateDays)
yearField.addEventListener('change', updateDays)

function updateDays() {
  var selectedYear = parseInt(yearField.value)
  var selectedMonth = monthField.value
  var options = '';

  function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
  }

  var days = daysInMonth[selectedMonth];
  if (selectedMonth === 'February' && isLeapYear(selectedYear)) {
    days = 29;
  }

  for (var i = 1; i <= days; i++) {
    options += '<option value="' + i + '">' + i + '</option>';
  }

  dayField.innerHTML = options;
}

// Initially populate the day field based on the default selected month and year
function initializeDays() {
  var selectedYear = parseInt(yearField.value);
  var selectedMonth = monthField.value;
  var options = '';

  function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
  }

  var days = daysInMonth[selectedMonth];
  if (selectedMonth === 'February' && isLeapYear(selectedYear)) {
    days = 29;
  }

  for (var i = 1; i <= days; i++) {
    options += '<option value="' + i + '">' + i + '</option>';
  }

  dayField.innerHTML = options;
}

// Call the function to populate the day field on initial load
initializeDays();