from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route("/microservicio1", methods=["POST"])
def enviar_valor():
    print("funciona")
    valor = request.json.get("valor")
    print(valor)
    response = requests.post(
        "http://localhost:5001/microservicio2", json={"valor": valor}
    )
    return response.json()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
