from flask import Flask, jsonify, request
import psycopg2
from utils.config import config

app = Flask(__name__)

@app.route("/")
def route():
    return "<h1>Hello, y'all!<h1>"

@app.route("/customers")
def get_clientes():
    pass

def pagina_no_encontrada(error):
    return "<h1>Error 404<h2><h2>Página no encontrada</h2>"

if __name__=="__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.config.from_object(config['development'])
    app.run()
