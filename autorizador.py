from flask import Flask, request, jsonify
import jwt
import requests

app = Flask(__name__)
clave_secreta = "clave_secreta"


@app.route("/microservicio2", methods=["POST"])
def generar_jwt():
    valor = request.json.get("valor")
    token = jwt.encode({"valor": valor}, clave_secreta, algorithm="HS256")
    response = requests.post(
        "http://localhost:5002/microservicio3", json={"valor": valor, "token": token}
    )
    return response.json()


if __name__ == "__main__":
    app.run(port=5001, debug=True)
