import sqlite3
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__) 

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'supersecret')")
    conn.commit()
    return conn

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = db.execute(query).fetchone()
        message = "Welcome!" if user else "Invalid credentials."
    return render_template_string("""
        <form method="post">
          <input name="username" placeholder="Username">
          <input name="password" type="password" placeholder="Password">
          <button type="submit">Login</button>
        </form>
        <p>{{ message }}</p>
    """, message=message)

@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    return render_template_string(f"<h1>Hello, {name}!</h1>")

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return f"<pre>{output.decode()}</pre>"

@app.route("/file")
def read_file():
    filename = request.args.get("name", "")
    with open(f"/var/data/{filename}") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
