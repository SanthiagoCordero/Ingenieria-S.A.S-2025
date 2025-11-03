import sqlite3
import os

# Crear carpeta 'db' si no existe
if not os.path.exists("db"):
    os.makedirs("db")

def inicializar_base():
    conn = sqlite3.connect("db/interacciones.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta_cliente TEXT,
            respuesta_bot TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def guardar_interaccion(pregunta, respuesta):
    inicializar_base()
    conn = sqlite3.connect("db/interacciones.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interacciones (pregunta_cliente, respuesta_bot) VALUES (?, ?)",
        (pregunta, respuesta)
    )
    conn.commit()
    conn.close()
