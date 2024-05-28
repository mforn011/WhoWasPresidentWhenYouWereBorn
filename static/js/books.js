document.addEventListener('DOMContentLoaded', function () {
    var saveButtons = document.querySelectorAll('.save-button');
    var sessionUsername = document.getElementById('sessionUsername').value;
    var savedBooks = JSON.parse(document.getElementById('savedBooks').value);

    saveButtons.forEach(function (button) {
        var bookTitle = button.getAttribute('data-book-title');

        // Check if the book is already saved
        if (savedBooks.some(function(book) { return book.book_title === bookTitle; })) {
            button.disabled = true;
            button.value = 'Saved';
            button.style.backgroundColor = 'navy';
            button.style.color = 'white';
        }

        button.closest('form').addEventListener('submit', function (event) {
            if (sessionUsername) {
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
                        button.value = 'Saved';
                        button.style.backgroundColor = 'navy';
                        button.style.color = 'white';
                    } else {
                        // Handle errors
                        console.error('Failed to submit form');
                    }
                };
                xhr.send(new URLSearchParams(formData)); // Send form data as URL encoded string
            }
        });
    });
})

