var logoutText = document.getElementById('logout-text')
var dots = '';
var interval = setInterval(function() {
    if (dots.length < 3) {
        dots += '.';
    } else {
        dots = '';
    }
    logoutText.innerText = 'Logging out' + dots;
}, 200); // Interval of 200 milliseconds

setTimeout(function() {
    clearInterval(interval)
    window.location.href = "{{ url_for('index') }}";
}, 3000); // 3000 milliseconds = 3 seconds