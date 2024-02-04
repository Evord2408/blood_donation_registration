# Blood Donation Registration
#### Video Demo:  <https://www.youtube.com/watch?v=qt1Rf3Jxk98&t=4s>
#### Description:
My name is Evord Riccie, and I am from Malaysia. I am a medical laboratory technologist. For my final project in CS50, I decided to create a web-based application using JavaScript, Python, and SQL, applying all the knowledge I have learned from this course. My final project is named "Blood Donation Registration." As a medical staff member working in the pathology department, I created this application to streamline the blood donation process by providing an online registration system. The goal is to replace traditional offline registration methods, such as paper forms, with a more efficient and accessible digital solution.

#### Features:
User Registration and log in
- Medical staff can register new users and manage their authentication.
- Secure login functionality ensures data privacy.

Profile
- Users can edit their profiles, providing up-to-date information.

Password
Change password functionality for improved account security.

Add Donor
- Medical staff can easily register new donors, capturing essential details such as name, ID number, contact number, blood group, and the number of blood bags donated on a particular day.

View and Search Donors
- Comprehensive views of all registered donors.
- Search functionality to find donors by name or ID number.

Edit and Delete Donors
- Medical staff can update or remove donor details as needed.

#### Technology Stack:
Backend: Python with Flask framework
Frontend: HTML, CSS with Bootstrap, and JavaScript
Database: SQLite
Development Environment: CS50 Codespaces

### Templates
register.html
- User registration form.

login.html
- User login form.

home.html
- Dashboard providing an overview of the application.
- search donor

profile.html
- User profile management.

change_password.html
- Form for changing the user's password.

add_donor.html
- Form for adding new donor information and save to database.

add_edit.html
- Common form for both adding and editing donor details.

search_results.html
- Display search results for donors.

### Static
custom.js
- JavaScript file for custom client-side functionalities.

logo.png
- Application logo.

style.css
- Cascading Style Sheets for styling the web pages.

### app.py
Routes
index(): Landing page.
- This code defines a Flask route for the home page ("/").
- When a user accesses the root URL, it redirects them to the "/home" page.

login(): User login route.
- This code defines a Flask route for user login ("/login").
- It checks if the user is already logged in and redirects them if so.
- In the case of a form submission (POST request), it validates the provided username and password.
- It queries the database for the user and, if found, checks the password.
- Successful login sets session data and redirects to "/home".
- Error messages are flashed for invalid input or credentials.

register(): User registration route.
- This code defines a Flask route for user registration ("/register").
- It handles both GET and POST requests.
- During a form submission (POST), it validates the provided user registration information, including username, email, position, and password.
- If the data is valid, it checks if the username already exists in the database.
- If not, it hashes the password, inserts the user into the database, and redirects to the login page.
- In case of validation errors, it renders the registration template with appropriate danger messages.

logout(): Logout route.
- This code defines a Flask route for user logout ("/logout").
- It clears the user's session and redirects them to the login page ("/login").

home(): Dashboard route.
- The first route, "/home", integrates search functionality. It handles both GET and POST requests.
- In a POST request, it retrieves a search term from the form and performs a search.
- The route then gathers data on blood donations for the current date, categorizes it by blood type, and displays the information on the home page.

profile(): User profile route.
- This Flask route ("/profile") requires user authentication and handles both GET and POST requests.
- In a POST request, it validates and updates the user's profile information, including username, email, position, and department.
- Danger messages are set for empty fields. If all fields are filled, it executes an SQL update query, retrieves the updated user information, and updates the session.
-Flash messages indicate the success or failure of the update.

change_password(): Route for changing the user's password.
- This Flask route ("/change_password") handles GET and POST requests for changing the user's password.
- If it's a POST request, it validates the current password, checks if the new passwords match, and updates the password in the database if all checks pass.
- Flash messages indicate the success or failure of the password change.
- The rendered template displays the change password form and associated danger messages.

search_results(): Display search results route.
- This Flask route ("/search_results") renders the "search_results.html" template.
- It ensures that only authenticated users can access this page by using the @login_required decorator.
- The template likely displays the results of a search query or provides a search interface.

search_donor(): Search donor route.
- This Flask route ("/search_donor") handles both GET and POST requests.
- For GET requests, it retrieves the search term from the query parameters.
- If a search term is present, it performs a search using the perform_search function and renders the "search_results.html" template with the search results.
- If no search term is provided, it redirects the user to the "/search_results" route.
- This route is protected, and only authenticated users can access it, as indicated by the @login_required decorator.

add_donor(): Add new donor route.
- This Flask route ("/add_donor") is responsible for handling both GET and POST requests related to adding a new donor.
- If the request method is POST, it retrieves the form data, validates the required fields, and checks for existing entries with the same ID number and registration date.
- If the data is valid and no duplicate entry is found, it inserts a new donor record into the database and redirects the user to the "/add_edit" route.

edit_donor(donor_id): Edit donor route.
- This Flask route ("/edit_donor/int:donor_id") manages both GET and POST requests for editing donor information.
- It requires authentication with the @login_required decorator.
- If the specified donor ID doesn't exist, it displays an error and redirects to "/add_edit".
- For a POST request, the route validates and updates donor information in the database.
- On success, it flashes a message and redirects to "/add_edit".
- The "edit_donor.html" template renders with current donor info and any validation or database error messages.

inject_datetime(): Helper function to inject current datetime.
- This Flask context processor injects the current datetime into all templates under the variable name 'current_datetime'.
- It allows templates to access the current datetime without explicitly passing it in each render call.

add_edit(): Common route for adding and editing donor details.
- This route renders the "add_edit.html" template, displaying information about donors fetched from the database.
- It requires the user to be logged in.

delete_donor(donor_id): Delete donor route.
- This route allows logged-in users to delete a donor with a specified ID.
- If successful, it returns a success message; otherwise, it returns an error message, including any exception details.
- It requires user authentication.

### helpers.py
Login Required Decorator
- login_required(f): Decorator to ensure that a user is logged in for certain routes.
Search Functionality
- perform_search(search_term): Helper function to perform donor search based on a given term.

### Database.db
database: SQL object for database operations.
Tables: users and donors.

### How to Run the Project:
To run the Blood Donation Registration application locally, follow these steps:

Prerequisites
Make sure you have the following installed on your machine:
- Python (version 3.7 or higher)
- Flask (a micro web framework for Python)
- SQLite (for the database)

Clone the Repository
Clone the repository to your local machine:
- git clone https://github.com/yourusername/your-repository.git
Navigate to the project directory:
- cd your-repository

Set Up Virtual Environment (Optional but recommended)
Create and activate a virtual environment to isolate your project dependencies:
- python -m venv venv
- source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

Install Dependencies
Install the required Python packages:
- pip install -r requirements.txt

Initialize the Database
Run the following command to set up the SQLite database:
- flask initdb

Run the Application
Start the Flask development server:
- flask run

Visit http://localhost:5000 in your web browser to access the Blood Donation Registration application.
