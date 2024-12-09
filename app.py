from flask import Flask, render_template, redirect, url_for, request, session, Response
from werkzeug.security import generate_password_hash
import sqlite3
from helpers import validate_user_data, insert_user, validate_login_credentials, get_user_info_by_email, classify_user_profile, get_horse_id_by_name, get_times_and_competitors_for_horse, analyze_horse_performance, generate_report

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

@app.route("/")
def index():
    return render_template("index.html")
    
#Login page, just checks to see if the information is correct and currently on our db
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Extract form data
        email = request.form.get("email")
        password = request.form.get("password")
        # Validate login credentials using helper function
        error = validate_login_credentials(email, password)
        if error:
            # If validation fails, return the error message and clear fields
            return render_template("login.html", error=error)
        # If validation succeeds, redirect the user
        session["user"] = email  # Store the user's email in the session
        return redirect(url_for("check_horse_rider_match"))
    return render_template("login.html")  
    
#Adding the information of the user to the db of users in the application
@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        # Extract form data
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        sex = request.form.get("sex")
        age = request.form.get("age")
        experience = request.form.get("experience")
        # Validate data
        error = validate_user_data(email, password, name, sex, age, experience)
        if error:
            return render_template("create_account.html", error=error)
        # Hash password and insert user into the database
        hashed_password = generate_password_hash(password)
        error = insert_user(email, hashed_password, name, sex, int(age), int(experience))
        if error:
            return render_template("create_account.html", error=error)
        # Redirect to login with success message
        return redirect(url_for("login"))
    return render_template("create_account.html") 

#The main page of the website: checking the horse and the rider match. The loggic is to get data from our sources and compare them using the function we built
@app.route("/check-horse-rider-match", methods=["GET", "POST"])
def check_horse_rider_match():
    # Check if the user is logged in for both GET and POST requests
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        # Get data from the form
        horse_name = request.form.get("horse-name")
        desired_time = request.form.get("desired-time")
        rider_type = request.form.get("rider-type")
        # Check to see if the user is logged in
        if "user" not in session:
            return redirect(url_for("login"))
        # Get information on the user profile usign his email
        user_info = get_user_info_by_email(session["user"])
        if not user_info:
            # If don't find the user, redirect to login page
            return redirect(url_for("login"))
        # Classify user profile
        user_profile = classify_user_profile(user_info["experience"], rider_type)
        # Get horse_id
        horse_id = get_horse_id_by_name(horse_name)
        if horse_id is None:
            return render_template("check_horse_rider_match.html", error="Horse not found")
        # get times and competitors
        times, competitors = get_times_and_competitors_for_horse(horse_id)
        # Converter desired_time para float
        desired_time = float(desired_time) if desired_time else 0.0
        # Analise performance
        horse_analysis = analyze_horse_performance(times, competitors)
        # Generate report
        report = generate_report(user_profile, horse_analysis, desired_time)
        # Guardar na sessão e redirecionar
        session["analysis_report"] = report
        return redirect(url_for("report"))
    return render_template("check_horse_rider_match.html")

# Download the report 
@app.route("/download_report", methods=["POST"])
def download_report():
    if "analysis_report" not in session:
        return redirect(url_for("report"))
    report_text = session["analysis_report"]
    return Response(
        report_text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=analysis_report.txt"}
    )

# Retrieve the analysis report from the session
@app.route("/report")
def report():
    # Retrieve the analysis report from the session
    report_text = session.get("analysis_report", "No report found.")
    return render_template("report.html", report_text=report_text)

# Suggest horses name so that the user doesn't need to get ir right
@app.route("/suggest-horses")
def suggest_horses():
    query = request.args.get("query", "").strip()
    suggestions = []
    if len(query) >= 4:
        conn = sqlite3.connect("novabase.db")
        cursor = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT animal_name FROM horses WHERE animal_name LIKE ? LIMIT 10", (query + "%",))
        rows = cursor.fetchall()
        conn.close()
        suggestions = [row[0] for row in rows]
    # Return a response
    return {"suggestions": suggestions}


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
