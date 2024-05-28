document.addEventListener('DOMContentLoaded', function () {
    var removeButtons = document.querySelectorAll('.remove-button');

    removeButtons.forEach(function (button) {
        button.closest('form').addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Serialize form data
            var formData = new FormData(event.target);

            // Send an AJAX request to the server
            var xhr = new XMLHttpRequest();
            xhr.open('POST', event.target.action);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // Disable the button after successful submission
                    button.disabled = true;
                    button.value = 'Removed';
                    button.style.backgroundColor = 'navy';
                    button.style.color = 'white';
                } else {
                    // Handle errors
                    console.error('Failed to submit form');
                }
            }
            xhr.send(new URLSearchParams(formData)); // Send form data as URL encoded string
        })
    })
})