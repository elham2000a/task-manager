from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        completed INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO tasks (title, completed) VALUES (?,0)", (data["title"],))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status":"deleted"})

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE tasks SET title=? WHERE id=?", (data["title"], id))
    conn.commit()
    conn.close()
    return jsonify({"status":"updated"})

@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def complete(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET completed = NOT completed WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status":"done"})

if __name__ == "__main__":
    app.run(debug=True)