from cs50 import SQL
from flask import redirect, session
from functools import wraps

# Create a reusable instance of the SQL class for database operations
db = SQL("sqlite:///database.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def perform_search(search_term):
    """
    Perform a search based on the provided search term.

    If the search term is numeric (ID number), search for matching ID numbers.
    If the search term is not numeric (name), search for matching names.

    Args:
    - search_term (str): The search term to be used.

    Returns:
    - search_results (list): A list of matching search results.
    """
    if search_term.isnumeric():
        search_results = db.execute("SELECT * FROM donors WHERE idnumber = :term", term=search_term)
    else:
        search_results = db.execute("SELECT * FROM donors WHERE name LIKE :term", term=f"%{search_term}%")

    return search_results
