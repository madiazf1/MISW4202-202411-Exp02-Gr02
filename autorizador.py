from flask import Flask, request, jsonify
from datetime import datetime
import jwt
import logging
import requests

app = Flask(__name__)
clave_secreta = "clave_secreta"
logging.basicConfig(filename="debug.log", level=logging.INFO)

@app.route("/microservicio2", methods=["POST"])
def generar_jwt():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  2. Genero token, envío api gateway [Autorizador:5001]\n")
    valor = request.json.get("valor")
    token = jwt.encode({"valor": valor}, clave_secreta, algorithm="HS256")
    response = requests.post(
        "http://localhost:5000/microservicio1-1", json={"valor": valor, "token": token}
    )
    return response.json()

@app.route("/microservicio2-1", methods=["POST"])
def decode_jwt():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  5. Recibo json, decode jwt [Autorizador:5001]\n")
    valor = request.json.get("valor")
    token = request.json.get("token")
    try:
        payload = jwt.decode(token, clave_secreta, algorithms=["HS256"])
        if payload["valor"] == valor:
            response = requests.post("http://localhost:5002/microservicio3-1", json={"operacion": 1})
            return response.json()
        else:
            return jsonify({"error": "Valor no valido"}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalido"}), 401

if __name__ == "__main__":
    app.run(port=5001, debug=True)
