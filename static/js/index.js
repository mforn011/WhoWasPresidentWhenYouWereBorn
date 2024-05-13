var monthField = document.getElementById('month')
var dayField = document.getElementById('day')

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

monthField.addEventListener('change', function() {
  var selectedMonth = monthField.value;
  var options = '';
  for (var i = 1; i <= daysInMonth[selectedMonth]; i++) {
    options += '<option value="' + i + '">' + i + '</option>';
  }
  dayField.innerHTML = options;
});

// Initially populate day field based on default selected month
var defaultSelectedMonth = monthField.value;
var options = '';
for (var i = 1; i <= daysInMonth[defaultSelectedMonth]; i++) {
  options += '<option value="' + i + '">' + i + '</option>';
}
dayField.innerHTML = options;