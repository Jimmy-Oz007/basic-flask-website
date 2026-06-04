from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"


# DATABASE SETUP
def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")


# PROJECTS PAGE
@app.route("/projects")
def projects():
    return render_template("projects.html")


# CONTACT PAGE
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        flash("Message sent successfully!")

        return redirect("/contact")

    return render_template("contact.html")


# ADMIN PAGE
@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")

    messages = cursor.fetchall()

    conn.close()

    return render_template("admin.html", messages=messages)


# RUN APP
if __name__ == "__main__":

    init_db()

    app.run(debug=True)