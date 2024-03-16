from flask import Flask, request, jsonify
from datetime import datetime
import logging
import requests

app = Flask(__name__)
clave_secreta = "clave_secreta"
logging.basicConfig(filename="debug.log", level=logging.INFO)

@app.route("/microservicio3", methods=["POST"])
def recibir_json_enviar_autorizador():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  4. Recibo json, envío autorizador [Suscripciones:5002]\n")
    valor = request.json.get("valor")
    token =  request.json.get("token")
    response = requests.post(
        "http://localhost:5001/microservicio2-1", json={"valor": valor, "token": token}
    )
    return response.json()

@app.route("/microservicio3-1", methods=["POST"])
def ejecutar_operacion():
    operacion = request.json.get("operacion")
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  6. Recibo permisos de usuario [Suscripciones:5002]\n")
    if operacion == 1:
        print(operacion)
        return jsonify({"mensaje": "Proceso autorizado"})
    else:
        return jsonify({"mensaje": "Proceso no autorizado"})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
