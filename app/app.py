from flask import Flask, abort, jsonify, request
from conexiones import conexion_clientes, conexion_pedidos
from utils import config, validador_clientes
import psycopg2
import datetime

app = Flask(__name__)

@app.route("/")
def route():
    return "Hey y'all, Scott here."

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
        if(not validador_clientes.validar_diccionario_clientes(dict_cliente)):
            print("Datos de JSON no validos.")
            abort(400)
        cc = conexion_clientes.ConexionCliente()
        whatsapp = dict_cliente["whatsapp"][1:]
        cc.insertar_cliente(dict_cliente["cedula"],dict_cliente["name"],dict_cliente["email"],whatsapp)
        return dict_cliente,201
    else:
        print("Error en JSON de entrada")
        abort(400)

@app.route("/customers/<cedula>",methods = ["PUT"])
def put_cliente(cedula):
    dict_cliente = request.get_json()
    cc = conexion_clientes.ConexionCliente()
    whatsapp = dict_cliente["whatsapp"][1:]
    cc.modificar_cliente(cedula,dict_cliente["name"],whatsapp,dict_cliente["email"])
    return '', 200

@app.route("/orders",methods=["POST"])
def post_pedido():
   dict_no = request.get_json()
   if {'quantity','payment_method','remarks','city','municipality','cedula'} <= set(dict_no):
       if dict_no['municipality'].lower() != 'maneiro':
           monto_envio = 2.00
       else:
           monto_envio = 0
       n_hamburguesas = int(dict_no['quantity'])
       monto_t = (n_hamburguesas*5) + monto_envio
       fecha = datetime.datetime.now()
       estado_d = 'pending'
       conexion = conexion_pedidos.ConexionPedido()
       conexion.insertar_pedido(dict_no['municipality'], dict_no['city'], n_hamburguesas, monto_envio, monto_t, dict_no['payment_method'],estado_d,fecha,dict_no['cedula'], dict_no['remarks'])
       return '', 201
   else:
       print("Error en JSON de entrada")
       abort(400)

@app.route("/orders/<id>/status", methods = ["PATCH"])
def patch_estado_pedido(id):
    dict_estado = request.get_json()
    conexion = conexion_pedidos.ConexionPedido()
    conexion.modificar_estado(id,dict_estado['status'])
    return '', 200

@app.route("/orders/<id>/payment-screenshot", methods = ["POST"])
def post_screenshot_pedido(id):
    archivo = request.files['screenshot']
    bytes_imagen = archivo.read()
    conexion = conexion_pedidos.ConexionPedido()
    conexion.modificar_screenshot(id,bytes_imagen)
    return '',201
    
@app.route("/orders")
def get_pedidos():
    conexion = conexion_pedidos.ConexionPedido()
    if (request.args.to_dict == {}):
        lista_tuplas = conexion.listar_pedidos()
    else:
        lista_tuplas = [] #Aquí la logica de filtrado, se hace con la clase psycopg2.sql
    #Aqui utilizar un proceso similar al get de clientes para convertir la lista de tuplas
    #en una lista de diccionarios. Se guardará en retornable.
    retornable = []
    return jsonify(retornable), 200
    

def pagina_no_encontrada(error):
    return "<h1>Error 404<h2><h2>Página no encontrada</h2>"

if __name__=="__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.config.from_object(config.config['development'])
    app.run()
