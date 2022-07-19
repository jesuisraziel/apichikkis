#Procedimiento para validar los campos de un pedido
def validar_diccionario_pedidos(dict_pd):
    # La cantidad de hamburguesas debe ser un numero
    try:
        int(dict_pd['quantity'])
    except:
        return False
    # El tamaño del metodo de pago no es superior a 10
    largo_prueba = len(dict_pd['payment_method'])
    if largo_prueba == 0 or largo_prueba > 10:
        return False
    # Las observaciones no deben tener mas de 80 caracteres
    largo_prueba = len(dict_pd['remarks'])
    if largo_prueba == 0 or largo_prueba > 80:
        return False
    # La ciudad no es superior a 140 caracteres
    largo_prueba = len(dict_pd['city'])
    if largo_prueba == 0 or largo_prueba > 140:
        return False
    # El municipio no tiene mas de 80 caracteres
    largo_prueba = len(dict_pd['municipality'])
    if largo_prueba == 0 or largo_prueba > 80:
        return False
    # La cedula tiene hasta 12 digitos
    largo_prueba = len(dict_pd['cedula'])
    if largo_prueba == 0 or largo_prueba > 12:
        return False
    # Tambien debe ser un numero
    try:
        int(dict_pd['cedula'])
    except:
        return False
    #Si pasa todas las pruebas entonces es verdadero
    return True

# Procedimiento para validar que el estado del pedido sea el indicado
def validar_estado(dict_status):
    #Se evalua el estado del pedido
    status = dict_status['status']
    if(status == 'pending' or status == 'in_progress' or status == 'dispatched' or status == 'completed'):
        return True
    else:
        return False
