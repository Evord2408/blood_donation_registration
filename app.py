import os
from datetime import datetime
from flask import (
    Flask, flash, redirect, render_template, request, session, url_for, jsonify, g
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, perform_search
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Load user before each request
@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)[0]

# Utility function to fetch today's date
def get_today_date():
    return datetime.now().strftime('%Y-%m-%d')

# Home route
@app.route("/")
def index():
    return redirect("/index")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect("/index")

    message = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            message = "Must provide username and password"
        else:
            users = db.execute("SELECT * FROM users WHERE username = :username", username=username)

            if not users:
                message = "Invalid username and/or password"
            else:
                user = users[0]
                if not check_password_hash(user["hash"], password):
                    message = "Invalid username and/or password"
                else:
                    session["user_id"] = user["id"]
                    session["user"] = user
                    flash(f"Welcome, {user['username']}!", "success")
                    return redirect("/index")

    return render_template("login.html", message=message)

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    danger_message = None

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        position = request.form.get("position")
        department = request.form.get("department")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validate the form data
        if not all([username, email, position, department, password, confirm_password]):
            danger_message = "Please fill in all fields"
        elif password != confirm_password:
            danger_message = "Passwords do not match"
        else:
            # Check if the username already exists
            if db.execute("SELECT * FROM users WHERE username = :username", username=username):
                danger_message = "Username already exists. Please choose a different one."
            else:
                # Register the user
                hashed_password = generate_password_hash(password)
                db.execute("INSERT INTO users (username, email, position, department, hash) VALUES (:username, :email, :position, :department, :hash)",
                           username=username, email=email, position=position, department=department, hash=hashed_password)

                flash("Registration successful. You can now log in.", 'success')
                return redirect("/login")

    return render_template("register.html", danger_message=danger_message)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Home route with search functionality
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    search_results = []

    if request.method == "POST":
        search_term = request.form.get("search_term")

        if search_term:
            # Perform the search based on the provided search term
            search_results = perform_search(search_term)

    today_date = get_today_date()
    blood_collection_data = db.execute(
        "SELECT bloodtype, SUM(donate) as total FROM donors WHERE date_registered = :today_date GROUP BY bloodtype",
        today_date=today_date
    )

    blood_collection = {}
    total_collection = 0

    for row in blood_collection_data:
        blood_group = row["bloodtype"]
        total_donations = row["total"]
        blood_collection[blood_group] = total_donations
        total_collection += total_donations

    all_blood_types = ['A', 'B', 'AB', 'O']
    for blood_type in all_blood_types:
        if blood_type not in blood_collection:
            blood_collection[blood_type] = 0

    return render_template("index.html", search_results=search_results, blood_collection=blood_collection, total_collection=total_collection)

# Profile route
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    danger_messages = {
        "username": None,
        "email": None,
        "position": None,
        "department": None,
    }

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_position = request.form['position']
        new_department = request.form['department']

        if not new_username:
            danger_messages["username"] = "Please fill in your username"
        if not new_email:
            danger_messages["email"] = "Please fill in your email"
        if not new_position:
            danger_messages["position"] = "Please fill in your position"
        if not new_department:
            danger_messages["department"] = "Please fill in your department"

        if all(danger_messages[field] is None for field in danger_messages):
            user_id = session["user_id"]

            update_query = """
            UPDATE users
            SET username = :new_username, email = :new_email, position = :new_position, department = :new_department
            WHERE id = :user_id
            """
            db.execute(update_query, new_username=new_username, new_email=new_email, new_position=new_position, new_department=new_department, user_id=user_id)

            select_query = "SELECT * FROM users WHERE id = :user_id"
            updated_user = db.execute(select_query, user_id=user_id)

            if updated_user:
                session["user"] = updated_user[0]
                flash("Profile updated successfully", "success")
            else:
                flash("Failed to update profile", "danger")

    user = session["user"]
    return render_template('profile.html', user=g.user, danger_messages=danger_messages)

# Change password route
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    danger_message = None
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        user_id = session.get("user_id")
        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)

        if not rows:
            danger_message = "User not found"
        else:
            current_hash = rows[0]["hash"]
            if not check_password_hash(current_hash, current_password):
                danger_message = "Current password is incorrect"
            elif new_password != confirm_password:
                danger_message = "New passwords do not match"
            else:
                new_hash = generate_password_hash(new_password)
                db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id", new_hash=new_hash, user_id=user_id)
                flash("Password changed successfully", "success")
                return redirect("/change_password")

    return render_template("change_password.html", danger_message=danger_message)

# Search results route
@app.route("/search_results")
@login_required
def search_results():
    return render_template("search_results.html")

# Search donor route
@app.route("/search_donor", methods=["GET", "POST"])
@login_required
def search_donor():
    search_term = request.args.get("search_term")

    if search_term:
        search_results = perform_search(search_term)
        return render_template("search_results.html", search_results=search_results)

    return redirect("/search_results")

# Add donor route
@app.route('/add_donor', methods=['GET', 'POST'])
@login_required
def add_donor():
    danger_message = None

    if request.method == 'POST':
        idnumber = request.form.get('idnumber')
        name = request.form.get('name')
        contact = request.form.get('contact')
        bloodtype = request.form.get('bloodtype')
        donate = request.form.get('donate')

        if not all([idnumber, name, bloodtype, donate]):
            danger_message = "Please fill in all required fields."
        else:
            try:
                today_date = get_today_date()
                existing_entry = db.execute("SELECT * FROM donors WHERE idnumber = :idnumber AND date_registered = :today_date",
                                            idnumber=idnumber, today_date=today_date)

                if existing_entry:
                    danger_message = "ID number has already been registered on the same date"
                    flash(danger_message, "danger")
                    return redirect("/add_donor")

                db.execute("INSERT INTO donors (user_id, name, idnumber, contact, bloodtype, donate, date_registered) VALUES (:user_id, :name, :idnumber, :contact, :bloodtype, :donate, :date_registered)",
                           user_id=session["user_id"], name=name, idnumber=idnumber, contact=contact, bloodtype=bloodtype, donate=donate, date_registered=today_date)

                flash("Donor added successfully.", "success")
                return redirect("/add_edit")
            except Exception as e:
                danger_message = f"An error occurred: {str(e)}"

    return render_template("add_donor.html", danger_message=danger_message)

# Edit donor route
@app.route('/edit_donor/<int:donor_id>', methods=['GET', 'POST'])
@login_required
def edit_donor(donor_id):
    danger_message = None

    donor = db.execute("SELECT * FROM donors WHERE id = :donor_id", donor_id=donor_id)

    if not donor:
        flash("Donor not found.", "danger")
        return redirect("/add_edit")

    donor = donor[0]

    if request.method == 'POST':
        idnumber = request.form.get('idnumber')
        name = request.form.get('name')
        contact = request.form.get('contact')
        bloodtype = request.form.get('bloodtype')
        donate = request.form.get('donate')

        if not idnumber or not name or not bloodtype or not donate:
            danger_message = "Please fill in all required fields."
        else:
            db.execute("UPDATE donors SET name = :name, idnumber = :idnumber, contact = :contact, bloodtype = :bloodtype, donate = :donate WHERE id = :donor_id",
                       name=name, idnumber=idnumber, contact=contact, bloodtype=bloodtype, donate=donate, donor_id=donor_id)
            flash("Donor information updated successfully.", "success")
            return redirect("/add_edit")

    return render_template('edit_donor.html', donor=donor, danger_message=danger_message)

# Inject current datetime into templates
@app.context_processor
def inject_datetime():
    return {'current_datetime': datetime.now()}

# Add/Edit route
@app.route('/add_edit')
@login_required
def add_edit():
    donors = db.execute("SELECT * FROM donors")
    return render_template("add_edit.html", donors=donors)

# Delete donor route
@app.route('/delete_donor/<int:donor_id>', methods=['POST'])
@login_required
def delete_donor(donor_id):
    try:
        donor = db.execute("SELECT * FROM donors WHERE id = :donor_id", donor_id=donor_id)

        if not donor:
            return jsonify(success=False, message="Donor not found")

        db.execute("DELETE FROM donors WHERE id = :donor_id", donor_id=donor_id)

        flash("Donor deleted successfully.", "success")
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))

# Run the app
if __name__ == "__main__":
    app.run()
