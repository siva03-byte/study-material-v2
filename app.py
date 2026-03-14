from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY","secret123")

# PostgreSQL connection (Neon)
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Insert admin user if not exists
conn = get_db()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users(name,email,password,role)
VALUES('Admin','admin@gmail.com','admin123','admin')
ON CONFLICT (email) DO NOTHING
""")

conn.commit()
cursor.close()
conn.close()


# HOME PAGE
@app.route("/")
def index():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notes")
    notes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(downloads),0) FROM notes")
    downloads = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        notes=notes,
        users=users,
        downloads=downloads
    )


# CATEGORY PAGE
@app.route("/category")
def category():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("category.html", departments=departments)


# SUBJECT PAGE
@app.route("/subject/<int:dept_id>")
def subject(dept_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM subjects WHERE department_id=%s",
        (dept_id,)
    )

    subjects = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("subject.html", subjects=subjects)


# DIGITAL PAGE
@app.route("/digital")
def digital():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("digital.html", role=session.get("role"))


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,name,role FROM users WHERE email=%s AND password=%s",
            (email,password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user"] = user[1]
            session["role"] = user[2]

            return redirect("/")

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        role = request.form["role"]

        if password != password_confirm:
            return "Passwords do not match", 400

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
            (username,email,password,role)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# UPDATE NOTES
@app.route("/update/<subject>", methods=["GET","POST"])
def update(subject):

    if session.get("role") != "admin":
        return "Access denied", 403

    topic = request.args.get("topic","")

    if request.method == "POST":

        file = request.files["file"]

        if file:

            upload_dir = os.path.join("static","uploads",subject)
            os.makedirs(upload_dir, exist_ok=True)

            filepath = os.path.join(upload_dir, file.filename)
            file.save(filepath)

            return redirect("/" + subject)

    return render_template("update.html", subject=subject, topic=topic)


# Vercel entry
app = app