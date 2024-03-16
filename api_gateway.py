from flask import Flask, request, jsonify
from datetime import datetime
import logging
import requests

app = Flask(__name__)
logging.basicConfig(filename="debug.log", level=logging.INFO)

@app.route("/microservicio1", methods=["POST"])
def enviar_valor_autorizador():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  1. Envío autorizador [API_Gateway:5000]\n")
    valor = request.json.get("valor")
    response = requests.post(
        "http://localhost:5001/microservicio2", json={"valor": valor}
    )
    return response.json()

@app.route("/microservicio1-1", methods=["POST"])
def recibir_jwt_enviar_suscripciones():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  3. Recibo token, envío suscripciones [API_Gateway:5000]\n")
    valor = request.json.get("valor")
    token =  request.json.get("token")
    response = requests.post(
        "http://localhost:5002/microservicio3", json={"valor": valor, "token": token}
    )
    return response.json()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
