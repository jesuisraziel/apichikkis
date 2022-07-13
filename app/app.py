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
    if tupla_clientes != None:
        for tc in tupla_clientes:
            telefono_con_simbolo = "+" + tc[3]
            diccionario_cliente = {"cedula":tc[0],"name":tc[1],"email":tc[2],"whatsapp":telefono_con_simbolo}
            clientes.append(diccionario_cliente)
    return jsonify(clientes),200

@app.route("/customers", methods = ["POST"])
def post_cliente():
    dict_cliente = request.get_json()
    if {'cedula','cliente','email','whatsapp'} <= set(dict_cliente):
        cc = conexion_clientes.ConexionCliente()
        whatsapp = dict_cliente["whatsapp"][1:]
        cc.insertar_cliente(dict_cliente["cedula"],dict_cliente["name"],dict_cliente["email"],whatsapp)
        return '',201
    else
        print("Error en JSON de entrada")
        abort(400)

@app.route("/customers/<cedula>",methods = ["PUT"])
def put_cliente(cedula):
    dict_cliente = request.get_json()
    cc = conexion_clientes.ConexionCliente()
    whatsapp = dict_cliente["whatsapp"][1:]
    cc.modificar_cliente(cedula,dict_cliente["name"],whatsapp,dict_cliente["email"])
    return '', 200

def pagina_no_encontrada(error):
    return "<h1>Error 404<h2><h2>Página no encontrada</h2>"

if __name__=="__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.config.from_object(config['development'])
    app.run()
