from flask import Flask, request, jsonify
from flask_cors import CORS
from ia_model import responder_usuario

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    if not pregunta:
        return jsonify({"respuesta": "En este momento no puedo responder tu consulta, por favor realiza tu consulta por medio de nuestro canal de WhatsApp.(https://wa.me/+573203685345)"}), 400
    
    respuesta = responder_usuario(pregunta)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)
