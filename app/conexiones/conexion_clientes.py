from conexiones.conexion import Conexion
import psycopg2

# Es EL que se encarga de conectar con la tabla de Cliente de la BD de Postgres
class ConexionCliente(Conexion):
    def listar_clientes(self):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        try: # Trata de obtener todos los clientes
            cursor.execute("SELECT * FROM Cliente;")
            self.conexion_activa.commit()
            usuarios = cursor.fetchall()
            cursor.close()
            self.desconectar()
            return usuarios  
        except: # Si no lo logra cierra la conexion y lanza una excepcion
            cursor.close()
            self.desconectar()
            raise Exception("Error al acceder a base de datos.")                        
        
    def obtener_cliente(self,cedula):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        try: # Trata de obtener los datos de un cliente
            cursor.execute("SELECT * FROM Cliente WHERE cedula=%s",(cedula,))
            self.conexion_activa.commit()
            usuario = cursor.fetchone()
            cursor.close()
            self.desconectar()
            return usuario
        except: # Si no lo logra lanza una excepcion
            cursor.close()
            self.desconectar()
            raise Exception("Error al obtener los datos de un cliente en la base de datos.")  

    def insertar_cliente(self, cedula, nombre_completo, email, whatsapp):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        try: # Trata de insertar el cliente
            cursor.execute("INSERT INTO Cliente VALUES (%s,%s,%s,%s);",(cedula, nombre_completo,email,whatsapp))
            self.conexion_activa.commit()
            cursor.close()
            self.desconectar()
            print("Insercion exitosa.")
        except: # Si no lo logra muestra una excepcion (Como se verifico previamente, lo mas probable es que sea una cedula repetida)
            cursor.close()
            self.desconectar()
            print("Insercion fallida.")
            raise Exception("Error al insertar el cliente en la base de datos, verifique que la cedula de un cliente no se repita")     
        

    def borrar_cliente(self,cedula):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        try: # Trata de eliminar un cliente
            cursor.execute("DELETE FROM Cliente WHERE cedula = %s;",(cedula,))
            self.conexion_activa.commit()
            cursor.close()
            self.desconectar()
            print("Borrado exitoso")
        except: # Si falla cierra la conexion y muestra una excepcion
            cursor.close()
            self.desconectar()
            print("Borrado fallido.")
            raise Exception("Error al borrar el cliente en la base de datos")     

    def modificar_cliente(self, cedula, nuevo_nombre, nuevo_whatsapp, nuevo_email):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        try: # Trata de modificar el usuario
            cursor.execute("UPDATE Cliente SET nombre_completo = %s, whatsapp = %s, email = %s WHERE cedula = %s",(nuevo_nombre, nuevo_whatsapp, nuevo_email, cedula))
            self.conexion_activa.commit()
            cursor.close()
            self.desconectar()
            print("Actualizacion exitosa.")
        except: # Si no lo logra lanza una excepcion
            cursor.close()
            self.desconectar()
            print("Actualizacion fallida.")
            raise Exception("Error al actualizar el cliente en la base de datos")     
