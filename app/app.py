from flask import Flask, jsonify, request
import psycopg2
from utils.config import config
from conexiones import conexion_clientes
app = Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello, y'all!<h1>"

@app.route("/customers")
def get_clientes():
    cc = conexion_clientes.ConexionCliente()
    tupla_clientes = cc.listar_clientes()
    clientes = []
    for tc in tupla_clientes:
        telefono_con_simbolo = "+" + tc[3]
        diccionario_cliente = {"cedula":tc[0],"name":tc[1],"email":tc[2],"whatsapp":telefono_con_simbolo}
        clientes.append(diccionario_cliente)
    return jsonify(clientes),200

def pagina_no_encontrada(error):
    return "<h1>Error 404<h2><h2>Página no encontrada</h2>"

if __name__=="__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.config.from_object(config['development'])
    app.run()
