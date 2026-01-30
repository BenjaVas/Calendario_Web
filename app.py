from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "database.db" 


# ================== BASE DE DATOS ==================
def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        fecha_fin TEXT NOT NULL,
        color TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        fecha_fin TEXT NOT NULL,
        proyecto_id INTEGER NOT NULL,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
    )
    """)

    conn.commit()
    conn.close()


# (Se usará luego para calendario y gantt)
def dias_entre(f1, f2):
    d1 = datetime.fromisoformat(f1)
    d2 = datetime.fromisoformat(f2)
    return (d2 - d1).days


# ================== RUTAS ==================
@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()

    # ---------- PROYECTOS ----------
    cursor.execute("""
        SELECT id, nombre, fecha_inicio, fecha_fin, color
        FROM proyectos
        ORDER BY fecha_inicio
    """)
    proyectos_raw = cursor.fetchall()

    proyectos = []
    for p in proyectos_raw:
        proyectos.append({
            "id": p[0],
            "nombre": p[1],
            "inicio": p[2],
            "fin": p[3],
            "color": p[4]
        })

    # ---------- TAREAS ----------
    cursor.execute("""
        SELECT id, nombre, fecha_inicio, fecha_fin, proyecto_id
        FROM tareas
        ORDER BY fecha_inicio
    """)
    tareas_raw = cursor.fetchall()

    tareas = []
    for t in tareas_raw:
        tareas.append({
            "id": t[0],
            "nombre": t[1],
            "inicio": t[2],
            "fin": t[3],
            "proyecto_id": t[4]
        })

    conn.close()

    return render_template(
        "index.html",
        proyectos=proyectos,
        tareas=tareas
    )


# ================== PROYECTOS ==================
@app.route("/crear_proyecto", methods=["POST"])
def crear_proyecto():
    nombre = request.form["nombre"]
    inicio = request.form["inicio"]
    fin = request.form["fin"]
    color = request.form["color"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO proyectos (nombre, fecha_inicio, fecha_fin, color)
        VALUES (?, ?, ?, ?)
    """, (nombre, inicio, fin, color))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/editar_proyecto/<int:proyecto_id>", methods=["GET", "POST"])
def editar_proyecto(proyecto_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE proyectos
            SET nombre=?, fecha_inicio=?, fecha_fin=?, color=?
            WHERE id=?
        """, (
            request.form["nombre"],
            request.form["inicio"],
            request.form["fin"],
            request.form["color"],
            proyecto_id
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM proyectos WHERE id=?", (proyecto_id,))
    proyecto = cursor.fetchone()
    conn.close()

    return render_template("editar_proyecto.html", proyecto=proyecto)


@app.route("/eliminar_proyecto/<int:proyecto_id>", methods=["POST"])
def eliminar_proyecto(proyecto_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tareas WHERE proyecto_id=?", (proyecto_id,))
    cursor.execute("DELETE FROM proyectos WHERE id=?", (proyecto_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# ================== TAREAS ==================
@app.route("/crear_tarea", methods=["POST"])
def crear_tarea():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tareas (nombre, fecha_inicio, fecha_fin, proyecto_id)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["nombre"],
        request.form["inicio"],
        request.form["fin"],
        request.form["proyecto_id"]
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/editar_tarea/<int:tarea_id>", methods=["GET", "POST"])
def editar_tarea(tarea_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("""
            UPDATE tareas
            SET nombre=?, fecha_inicio=?, fecha_fin=?, proyecto_id=?
            WHERE id=?
        """, (
            request.form["nombre"],
            request.form["inicio"],
            request.form["fin"],
            request.form["proyecto_id"],
            tarea_id
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM tareas WHERE id=?", (tarea_id,))
    tarea = cursor.fetchone()

    cursor.execute("SELECT id, nombre FROM proyectos")
    proyectos = cursor.fetchall()

    conn.close()

    return render_template(
        "editar_tarea.html",
        tarea=tarea,
        proyectos=proyectos
    )


@app.route("/eliminar_tarea/<int:tarea_id>", methods=["POST"])
def eliminar_tarea(tarea_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# ================== MAIN ==================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
