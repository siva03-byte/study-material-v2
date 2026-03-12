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