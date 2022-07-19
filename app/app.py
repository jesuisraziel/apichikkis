from flask import Flask, abort, jsonify, request
from conexiones import conexion_clientes, conexion_pedidos
from utils import config, validador_clientes, validador_pedidos
import psycopg2
import datetime

app = Flask(__name__)

@app.route("/home")
def route():
    return "<h1>Ayo</h1>"

# Servicio para listar los clientes. (Verbo: GET, URL: /customers).
@app.route("/customers")
def get_clientes():
    cc = conexion_clientes.ConexionCliente()
    tupla_clientes = cc.listar_clientes() #Obtiene los clientes
    clientes = []
    if tupla_clientes != None:
        #Formatea el json de salida con cada cliente
        for tc in tupla_clientes:
            telefono_con_simbolo = "+" + tc[3]
            diccionario_cliente = {"cedula":tc[0],"name":tc[1],"email":tc[2],"whatsapp":telefono_con_simbolo}
            clientes.append(diccionario_cliente)
    return jsonify(clientes),200

# Servicio para crear un cliente. Verbo: POST, URL: /customers
@app.route("/customers", methods = ["POST"])
def post_cliente():
    dict_cliente = request.get_json()
    # Parsea y verifica que esten los campos requeridos
    if {'cedula','name','email','whatsapp'} <= set(dict_cliente):
        # Verifica que los campos del JSON de entrada respeten el tamaño
        if(not validador_clientes.validar_diccionario_clientes(dict_cliente)):
            print("Datos de JSON no validos.")
            abort(400)
        # Se procede a insertar los datos
        cc = conexion_clientes.ConexionCliente()
        whatsapp = dict_cliente["whatsapp"][1:]
        cc.insertar_cliente(dict_cliente["cedula"],dict_cliente["name"],dict_cliente["email"],whatsapp)
        return dict_cliente,201
    else:
        print("Error en JSON de entrada")
        abort(400)

# Servicio para editar un cliente (La cédula no se edita). (Verbo PUT, URL: /customers/<cédula>).
@app.route("/customers/<cedula>",methods = ["PUT"])
def put_cliente(cedula):
    dict_cliente = request.get_json()
    cc = conexion_clientes.ConexionCliente()
    # Se aborta si el cliente no existe
    if (cc.obtener_cliente(cedula) == None):
        print("No existe el cliente")
        abort(404)
    # Verifica que esten los campos requeridos
    if {'name','email','whatsapp'} <= set(dict_cliente):
        # Verifica que los campos del JSON de entrada respeten el tamaño
        if(not validador_clientes.validar_cambio_cliente(dict_cliente)):
            print("Datos de JSON no validos.")
            abort(400)
        # Se procede a cambiar los datos del cliente
        whatsapp = dict_cliente["whatsapp"][1:]
        cc.modificar_cliente(cedula,dict_cliente["name"],whatsapp,dict_cliente["email"])
        return '', 200
    else:
        print("Error en JSON de entrada")
        abort(400)

# Servicio para crear un pedido. (Verbo: POST, URL: /orders). 
@app.route("/orders",methods=["POST"])
def post_pedido():
   dict_no = request.get_json()
   # Verifica que este los campos requeridos
   if {'quantity','payment_method','remarks','city','municipality','cedula'} <= set(dict_no):
       cc = conexion_clientes.ConexionCliente()
       # El cliente al que se le esta haciendo la orden debe existir
       if (cc.obtener_cliente(dict_no['cedula']) == None):
           print("No existe el cliente")
           abort(404)
       # Verifica que los campos del JSON de entrada respeten el tamaño
       if(not validador_pedidos.validar_diccionario_pedidos(dict_no)):
            print("Datos de JSON no validos.")
            abort(400)
       # Se procede a crear el pedido
       if dict_no['municipality'].lower() != 'maneiro':
           monto_envio = 2.00 # Si no es de maneiro paga 2$
       else:
           monto_envio = 0    # De lo contrario el envio es gratis
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

# Servicio para cambiar el estado de un pedido. (Verbo: PATCH, URL: /orders/<id>/status).
# Los estados disponibles son "pending", "in_progress", "dispatched" y "completed"
@app.route("/orders/<id>/status", methods = ["PATCH"])
def patch_estado_pedido(id):
    dict_estado = request.get_json()
    # Verifica que el estado del pedido sea uno de los 4 antemencionados
    if(not validador_pedidos.validar_estado(dict_estado)):
        print("Datos de JSON no validos.")
        abort(400)
    conexion = conexion_pedidos.ConexionPedido()
    #Se verifica que exista el pedido a modificar
    if (conexion.buscar_pedido(id) == []):
        print("No existe el pedido")
        abort(404)    
    conexion.modificar_estado(id,dict_estado['status'])
    return '', 200

# Servicio para enviar el screenshot de un pedido. (Verbo: POST, URL: /orders/<id>/payment-screenshot). 
@app.route("/orders/<id>/payment-screenshot", methods = ["POST"])
def post_screenshot_pedido(id):
    archivo = request.files['screenshot']
    bytes_imagen = archivo.read()
    conexion = conexion_pedidos.ConexionPedido()
    # Se verifica que exista el pedido a modificar
    if (conexion.buscar_pedido(id) == []):
        print("No existe el pedido")
        abort(404)
    # Ahora se añade el screenshot
    conexion.modificar_screenshot(id,bytes_imagen)
    return '',201

# Servicio para listar pedidos con posibilidad de filtrar (Verbo: GET, URL: /orders?date=2022-06-28&status=pending&cedula).
@app.route("/orders")
def get_pedidos():
    conexion = conexion_pedidos.ConexionPedido()
    retornable = []
    # Si no se provee nada, se retorna todo
    if (request.args.to_dict() == {}):
        lista_tuplas = conexion.listar_pedidos()
    else:
        # Se obtiene los filtros
        dict_args = request.args.to_dict()
        segmento_where = ""
        # Se añade la cedula (si tiene)
        if 'cedula' in dict_args:
            discriminante = dict_args['cedula']
            segmento_where = segmento_where + "cedula = '" + discriminante + "' AND "
        # Se añade el estado (si tiene)
        if 'status' in dict_args:
            #identificador = psycopg2.sql.Identifier('estado_delivery')
            #identificadores.append(identificador)
            #identificadores.append('estado_delivery')
            discriminante = dict_args['status']
            segmento_where = segmento_where + "estado_delivery = '" + discriminante + "' AND "
        # Se añade la fecha (si tiene)
        if 'date' in dict_args:
            #identificador = psycopg2.sql.Identifier('fecha')
            #identificadores.append(identificador)
            #identificadores.append('fecha')
            discriminante = dict_args['date']
            segmento_where = segmento_where + "CAST(fecha AS date) = '" + discriminante + "' AND "
        # Al final el segmento se le remueve el ultimo AND y se añade el ; que llevan las queries
        segmento_where = segmento_where[:-5] + ";"
        # Se une y se realiza la query
        query = f"SELECT * FROM Pedido WHERE {segmento_where}"
        lista_tuplas = conexion.realizar_query_preconstruida(query)
    # Se parsea los resultados (si tiene)
    if lista_tuplas != []:
        for tup in lista_tuplas:
            dict_ped = {}
            dict_ped['id'] = tup[0]
            dict_ped['municipality'] = tup[1]
            dict_ped['city'] = tup[2]
            dict_ped['quantity'] = tup[3]
            dict_ped['delivery_amount'] = tup[4]
            dict_ped['total'] = tup[5]
            dict_ped['payment_method'] = tup[6]
            dict_ped['status'] = tup[7]
            screen = tup[8]
            if screen is not None:
                dict_ped['screenshot'] = screen.hex()
            else:
                dict_ped['screenshot'] = screen
            fecha = tup[9]
            dict_ped['datetime'] = parsear_fecha(fecha)
            dict_ped['cedula'] = tup[10]
            dict_ped['remark'] = tup[11]
            retornable.append(dict_ped)
    return jsonify(retornable), 200
    
# Metodo para construrir las fechas con los ceros a su lado
def parsear_fecha(fecha):
    string_fecha = ""
    string_fecha = string_fecha + str(fecha.year) + "-"
    if (fecha.month < 10):
        string_fecha = string_fecha + "0" + str(fecha.month) + "-"
    else:
        string_fecha = string_fecha + str(fecha.month) + "-"
    if (fecha.day < 10):
        string_fecha = string_fecha + "0" + str(fecha.day) + " "
    else:
        string_fecha = string_fecha + str(fecha.day) + " "
    if (fecha.hour < 10):
        string_fecha = string_fecha + "0" + str(fecha.hour) + ":"
    else:
        string_fecha = string_fecha + str(fecha.hour) + ":"
    if (fecha.minute < 10):
        string_fecha = string_fecha + "0" + str(fecha.minute) + ":"
    else:
        string_fecha = string_fecha + str(fecha.minute) + ":"
    if (fecha.second < 10):
        string_fecha = string_fecha + "0" + str(fecha.second)
    else:
        string_fecha = string_fecha + str(fecha.second)    
    return string_fecha

def pagina_no_encontrada(error):
    return "<h1>Error 404<h2><h2>Página no encontrada</h2>"

if __name__=="__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.config.from_object(config.config['development'])
    app.run()
