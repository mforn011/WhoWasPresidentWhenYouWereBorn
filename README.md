# Who Was President When You Were Born?

A web application created with HTML, CSS, and Python using the Flask framework, which allows users to enter their date of birth, and returns with the president at the time of their birth and a short description of that president's time in office. Upon running the application, the user is first treated to the index.html web page, which contains different fields displaying the month, day, and year. After entering this information, the application determines who the president was from the information provided in the date fields, using the who_was_president() method, and returns the web page corresponding to that president. However, the date only goes as far back as 1982, so older people, you're out of luck.

Note that HTML files containing code for your web pages must be in a folder named "templates", or else Flask's render_template() method won't work. Also make sure you specify that the app.route uses both GET and POST methods, or else your page won't display and you'll get an error.

UPDATE:
Added a new username and password feature using MongoDB. The index.html page is now a log-in screen, which asks the user for their username and password. If they have no account, they can click on the "create account" button, and enter a unique username and password (which is hashed using the scrypt algorithm), which is then stored in a MongoDB collection. They can then enter this username and password from the log-in screen.
