import json
import os
import re
from difflib import SequenceMatcher
from database import guardar_interaccion

# Ruta correcta al dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset_ingenierias.json")

# Cargar dataset
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

def limpiar_texto(texto: str) -> str:
    """Normaliza el texto quitando signos y minúsculas."""
    return re.sub(r"[^a-zA-Záéíóúüñ0-9\s]", "", texto.lower().strip())

def similitud(a: str, b: str) -> float:
    """Calcula similitud entre dos strings (0 a 1)."""
    return SequenceMatcher(None, a, b).ratio()

def responder_usuario(pregunta_usuario: str) -> str:
    pregunta = limpiar_texto(pregunta_usuario)
    mejor_respuesta = "Lo siento, no tengo una respuesta exacta, pero puedo conectarte con un asesor humano."
    mejor_score = 0.0

    # Respuestas creativas para palabras clave específicas
    if "programar una cita" in pregunta:
        mejor_respuesta = (
            "¡Genial! Si deseas programar una cita, solo haz clic en el siguiente enlace y en el mensaje "
            "escribe 'Quiero programar una cita': "
            "<a href='https://wa.me/+573203685345?text=Quiero%20programar%20una%20cita' target='_blank'>Programar cita</a>"
        )
    elif "cotizar una propuesta" in pregunta:
        mejor_respuesta = (
            "¡Perfecto! Si deseas cotizar una propuesta, haz clic en el enlace a continuación y en el mensaje "
            "escribe 'Quiero cotizar una propuesta': "
            "<a href='https://wa.me/+573203685345?text=Quiero%20cotizar%20una%20propuesta' target='_blank'>Cotizar propuesta</a>"
        )
    elif "consultar un servicio" in pregunta:
        mejor_respuesta = (
            "¡Por supuesto! Para consultar nuestros servicios, dirijete a nuestra sección de servicios. "
            "Cada uno tiene un botón de WhatsApp para que puedas contactarnos directamente:\n\n"
            "En cada servicio, encontrarás un botón de WhatsApp para conectarte con nosotros."
        )
    elif "hablar con un asesor" in pregunta:
        mejor_respuesta = (
            "¡Claro! Si deseas hablar con un asesor, simplemente haz clic en el siguiente enlace y estarás "
            "en contacto con uno de nuestros expertos: "
            "<a href='https://wa.me/+573203685345' target='_blank'>Hablar con asesor</a>"
        )
    else:
        # Si no coincide con las palabras clave específicas, busca la mejor coincidencia en el dataset
        for item in dataset:
            if "pregunta" not in item or "respuesta" not in item:
                continue

            pregunta_base = limpiar_texto(item["pregunta"])

            # 1️⃣ Coincidencia exacta o contenida
            if pregunta_base in pregunta or pregunta in pregunta_base:
                mejor_respuesta = item["respuesta"]
                break

            # 2️⃣ Coincidencia parcial por palabras clave
            palabras_usuario = set(pregunta.split())
            palabras_base = set(pregunta_base.split())
            palabras_comunes = palabras_usuario.intersection(palabras_base)
            score_palabras = len(palabras_comunes) / max(len(palabras_base), 1)

            # 3️⃣ Similitud semántica simple
            score_similitud = similitud(pregunta, pregunta_base)

            # 4️⃣ Score total ponderado
            score_total = (score_palabras * 0.6) + (score_similitud * 0.4)

            if score_total > mejor_score:
                mejor_score = score_total
                mejor_respuesta = item["respuesta"]

    # Agregar siempre el mensaje de WhatsApp al final
    mejor_respuesta += (
        "<br><br>Para más información, conéctate a nuestro canal de WhatsApp: "
        "<a href='https://wa.me/+573203685345' target='_blank'>Contactar Asesor</a>"
    )

    guardar_interaccion(pregunta_usuario, mejor_respuesta)
    return mejor_respuesta
