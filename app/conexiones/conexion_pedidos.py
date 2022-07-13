from conexiones.conexion import Conexion
import psycopg2

class ConexionPedido(Conexion):
        def insertar_pedido(self, municipio, ciudad, n_hamburg, monto_deliv, monto_t, metodo_p, estado_d, fecha, cedula,remarks):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            cursor.execute("INSERT INTO Pedido (municipio, ciudad, n_hamburguesas, monto_delivery, monto_total, metodo_pago, estado_delivery, fecha, cedula,remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(municipio, ciudad, n_hamburg, monto_deliv, monto_t, metodo_p, estado_d, fecha, cedula,remarks))
            self.conexion_activa.commit()
            cursor.close()
            self.desconectar()
            print("Insercion exitosa")

        def modificar_estado(self, id, estado):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            cursor.execute("UPDATE Pedido SET estado_delivery = %s WHERE id = %s;", (estado, id))
            self.conexion_activa.commit()
            cursor.close()
            self.desconectar()
            print(f"Estado del pedido {id} se ha cambiado a {estado}")