def validar_diccionario_clientes(dict_cl):
    largo_prueba = len(dict_cl['cedula'])
    if largo_prueba == 0 or largo_prueba > 12:
        return False
    int(dict_cl['cedula'])
    largo_prueba = len(dict_cl['name'])
    if largo_prueba == 0 or largo_prueba > 240:
        return False
    largo_prueba = len(dict_cl['email'])
    if largo_prueba == 0 or largo_prueba > 140:
        return False
    largo_prueba = len(dict_cl['whatsapp'])
    if largo_prueba == 0 or largo_prueba > 15:
        return False
    try:
        int(dict_cl['cedula'])
    except:
        return False

    return True        