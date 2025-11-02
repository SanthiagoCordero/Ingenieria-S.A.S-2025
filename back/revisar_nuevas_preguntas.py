import sqlite3, json
from datetime import datetime

# Cargar dataset actual
with open("dataset_ingenierias.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Mostrar nuevas preguntas recientes
def revisar_nuevas_preguntas():
    conn = sqlite3.connect("db/interacciones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta_cliente FROM interacciones ORDER BY fecha DESC LIMIT 20")
    nuevas = cursor.fetchall()
    conn.close()

    print("📊 Nuevas preguntas de los clientes:\n")
    for p in nuevas:
        print("-", p[0])

# Agregar manualmente nuevas preguntas al dataset
def agregar_pregunta_respuesta(pregunta, respuesta):
    nueva = {"pregunta": pregunta, "respuesta": respuesta}
    dataset.append(nueva)
    with open("dataset_ingenierias.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print("✅ Pregunta agregada exitosamente al dataset.")

# Ejemplo de uso:
if __name__ == "__main__":
    revisar_nuevas_preguntas()
    # agregar_pregunta_respuesta("Cuál es el horario de atención?", "Atendemos de lunes a viernes de 8:00 a 6:00 p.m.")
