from conexiones.conexion import Conexion
import psycopg2

class ConexionCliente(Conexion):
    def listar_clientes(self):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        cursor.execute("SELECT * FROM Cliente;")
        self.conexion_activa.commit()
        usuarios = cursor.fetchall()
        cursor.close()
        self.desconectar()
        return usuarios

    def obtener_cliente(self,cedula):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE cedula=%s",(cedula,))
        self.conexion_activa.commit()
        usuario = cursor.fetchone()
        cursor.close()
        self.desconectar()
        return usuario

    def insertar_cliente(self, cedula, nombre_completo, email, whatsapp):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        cursor.execute("INSERT INTO Cliente VALUES (%s,%s,%s,%s);",(cedula, nombre_completo,email,whatsapp))
        self.conexion_activa.commit()
        cursor.close()
        self.desconectar()
        print("Insercion exitosa.")

    def borrar_cliente(self,cedula):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        cursor.execute("DELETE FROM Cliente WHERE cedula = %s;",(cedula,))
        self.conexion_activa.commit()
        cursor.close()
        self.desconectar()
        print("Borrado exitoso")

    def modificar_cliente(self, cedula, nuevo_nombre, nuevo_whatsapp, nuevo_email):
        self.conectar()
        cursor = self.conexion_activa.cursor()
        cursor.execute("UPDATE Cliente SET nombre_completo = %s, whatsapp = %s, email = %s WHERE cedula = %s",(nuevo_nombre, nuevo_whatsapp, nuevo_email, cedula))
        self.conexion_activa.commit()
        cursor.close()
        self.desconectar()
        print("Actualizacion exitosa.")