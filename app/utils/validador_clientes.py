# Procedimiento para validar los campos de un cliente
def validar_diccionario_clientes(dict_cl):
    # El tamaño de la cedula es de hasta 12 digitos
    largo_prueba = len(dict_cl['cedula'])
    if largo_prueba == 0 or largo_prueba > 12:
        return False
    int(dict_cl['cedula'])
    # El nombre del cliente no debe contener mas de 240 caracteres
    largo_prueba = len(dict_cl['name'])
    if largo_prueba == 0 or largo_prueba > 240:
        return False
    # El email no contiene mas de 140 caracteres
    largo_prueba = len(dict_cl['email'])
    if largo_prueba == 0 or largo_prueba > 140:
        return False
    # El numero de Whatsapp no es superior a 15
    largo_prueba = len(dict_cl['whatsapp'])
    if largo_prueba == 0 or largo_prueba > 15:
        return False
    #Tambien, la cedula debe ser un numero
    try:
        int(dict_cl['cedula'])
    except:
        return False
    #Si pasa todo eso entonces es verdadero
    return True        

# Procedimiento para validar los campos PARA ACTUALIZAR un cliente
# La unica diferencia con validar_diccionario_cliente es que no se suministra la cedula
def validar_cambio_cliente(dict_cl):
    # El nombre del cliente no debe contener mas de 240 caracteres
    largo_prueba = len(dict_cl['name'])
    if largo_prueba == 0 or largo_prueba > 240:
        return False
    # El email no contiene mas de 140 caracteres
    largo_prueba = len(dict_cl['email'])
    if largo_prueba == 0 or largo_prueba > 140:
        return False
    # El numero de Whatsapp no es superior a 15
    largo_prueba = len(dict_cl['whatsapp'])
    if largo_prueba == 0 or largo_prueba > 15:
        return False
    #Si pasa todo eso entonces es verdadero
    return True 
