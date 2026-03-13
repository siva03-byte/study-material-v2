from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.secret_key = "secret123"

# MySQL Connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root123",
    database="study_material_db",
    cursorclass=pymysql.cursors.DictCursor
)

# HOME PAGE
@app.route("/")
def index():

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) AS total_notes FROM notes")
    notes = cursor.fetchone()["total_notes"]

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT SUM(downloads) AS total_downloads FROM notes")
    result = cursor.fetchone()
    downloads = result["total_downloads"] if result["total_downloads"] else 0

    return render_template(
        "index.html",
        notes=notes,
        users=users,
        downloads=downloads
    )


# CATEGORY PAGE
@app.route("/category")
def category():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM departments")

    departments = cursor.fetchall()

    return render_template(
        "category.html",
        departments=departments
    )


# SUBJECT PAGE
@app.route("/subject/<int:dept_id>")
def subject(dept_id):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM subjects WHERE department_id=%s",
        (dept_id,)
    )

    subjects = cursor.fetchall()

    return render_template(
        "subject.html",
        subjects=subjects
    )


# DISCRETE MATHEMATICS PAGE
@app.route("/discrete")
def discrete():
    return render_template("discrete.html")


# DIGITAL ELECTRONICS PAGE
@app.route("/digital")
def digital():
    return render_template("digital.html")


# DATA STRUCTURES PAGE
@app.route("/ds")
def ds():
    return render_template("ds.html")


# OPERATING SYSTEMS PAGE
@app.route("/os")
def os_page():
    return render_template("os.html")


# TABLE OF CONTENTS PAGE
@app.route("/toc")
def toc():
    return render_template("toc.html")


# OOPS PAGE
@app.route("/oops")
def oops():
    return render_template("oops.html")


# SEARCH PAGE
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip().lower()
    if not query:
        return redirect("/")

    # Simple keyword-based redirects
    if "discrete" in query or "mathematics" in query:
        return redirect("/discrete")
    elif "digital" in query or "electronics" in query:
        return redirect("/digital")
    elif "oops" in query or "object oriented" in query or "java" in query:
        return redirect("/oops")
    elif "data structures" in query or "ds" in query:
        return redirect("/ds")
    elif "operating system" in query or "os" in query:
        return redirect("/os")
    elif "theory of computation" in query or "toc" in query or "automata" in query:
        return redirect("/toc")
    else:
        # If no match, show no results page
        return render_template("search.html", results=[], query=query)


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )

        user = cursor.fetchone()

        if user:
            session["user"] = user["name"]
            session["role"] = user["role"]
            return redirect("/")

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
            (name,email,password,role)
        )

        db.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)