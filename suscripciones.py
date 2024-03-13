from flask import Flask, request, jsonify
import jwt


app = Flask(__name__)
clave_secreta = "clave_secreta"


@app.route("/microservicio3", methods=["POST"])
def procesar_valor():
    valor = request.json.get("valor")
    token = request.json.get("token")
    try:
        payload = jwt.decode(token, clave_secreta, algorithms=["HS256"])
        if payload["valor"] == valor:
            return jsonify({"mensaje": "Proceso correcto"})
        else:
            return jsonify({"error": "Valor no valido"}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalido"}), 401


if __name__ == "__main__":
    app.run(port=5002, debug=True)
