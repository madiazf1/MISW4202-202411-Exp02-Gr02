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

@app.route("/microservicio2-T2", methods=["POST"])
def generar_jwt_T2():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  2. Genero token, envío api gateway [Autorizador:5001]\n")
    valor = request.json.get("valor")
    token = jwt.encode({"valor": valor}, clave_secreta, algorithm="HS256")
    response = requests.post(
        "http://localhost:5000/microservicio1-1-T2", json={"valor": valor, "token": token}
    )
    return response.json()

@app.route("/microservicio2-T3", methods=["POST"])
def generar_jwt_T3():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  2. Genero token, envío api gateway [Autorizador:5001]\n")
    valor = request.json.get("valor")
    usuario_autorizado = request.json.get("usuario_autorizado")
    token = jwt.encode({"valor": valor}, clave_secreta, algorithm="HS256")
    response = requests.post(
        "http://localhost:5000/microservicio1-1-T3", json={"valor": valor, "token": token, "usuario_autorizado": usuario_autorizado}
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
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  WARNING [Recibo json, decode jwt]: Token Inválido [Autorizador:5001]\n")
        return jsonify({"error": "Token inválido"}), 401

@app.route("/microservicio2-1-T3", methods=["POST"])
def decode_jwt_T3():
    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  5. Recibo json, decode jwt [Autorizador:5001]\n")
    valor = request.json.get("valor")
    token = request.json.get("token")
    usuario_autorizado = request.json.get("usuario_autorizado")
    try:
        payload = jwt.decode(token, clave_secreta, algorithms=["HS256"])
        if payload["valor"] == valor:
            if usuario_autorizado == "S":
                response = requests.post("http://localhost:5002/microservicio3-1", json={"operacion": 1})
            else:
                response = requests.post("http://localhost:5002/microservicio3-1", json={"operacion": 0})
            return response.json()
        else:
            return jsonify({"error": "Valor no valido"}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "  WARNING [Recibo json, decode jwt]: Token Inválido [Autorizador:5001]\n")
        return jsonify({"error": "Token inválido"}), 401

if __name__ == "__main__":
    app.run(port=5001, debug=True)
