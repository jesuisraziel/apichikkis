from conexiones.conexion import Conexion
import psycopg2

# Clase que se encarga de conectarse a la tabla Pedido de la base de datos 
class ConexionPedido(Conexion):
        def insertar_pedido(self, municipio, ciudad, n_hamburg, monto_deliv, monto_t, metodo_p, estado_d, fecha, cedula,remarks):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            try: # Trata de insertar un cliente
                cursor.execute("INSERT INTO Pedido (municipio, ciudad, n_hamburguesas, monto_delivery, monto_total, metodo_pago, estado_delivery, fecha, cedula,remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(municipio, ciudad, n_hamburg, monto_deliv, monto_t, metodo_p, estado_d, fecha, cedula,remarks))
                self.conexion_activa.commit()
                cursor.close()
                self.desconectar()
                print("Insercion exitosa")
            except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al insertar un pedido en la base de datos")      

        def modificar_estado(self, id, estado):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            try: # Trata de modificar el estado de un cliente
                cursor.execute("UPDATE Pedido SET estado_delivery = %s WHERE id = %s;", (estado, id))
                self.conexion_activa.commit()
                cursor.close()
                self.desconectar()
                print(f"Estado del pedido {id} se ha cambiado a {estado}")
            except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al modificar el estado de un pedido en la base de datos") 
            
        def modificar_screenshot(self, id, bytes_imagen):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            try: # Trata de añadir la screenshot
                cursor.execute("UPDATE Pedido SET screenshot = %s WHERE id = %s",(bytes_imagen, id))
                self.conexion_activa.commit()
                cursor.close()
                self.desconectar()
                print(f"Se ha subido una screenshot de pago para el pedido {id}")
            except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al mandar la screenshot a la base de datos") 
            
        def listar_pedidos(self):
           self.conectar()
           cursor = self.conexion_activa.cursor()
           try: # Trata de listar los pedidos
                cursor.execute("SELECT * FROM Pedido")
                self.conexion_activa.commit()
                retornable = cursor.fetchall()
                cursor.close()
                self.desconectar()
                return retornable
           except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al solicitar los pedidos a la base de datos") 
       
        def realizar_query_preconstruida(self, query_sql):
            self.conectar()
            cursor = self.conexion_activa.cursor()
            try: # Trata de hacer la query preconstruida
                cursor.execute(query_sql)
                self.conexion_activa.commit()
                retornable = cursor.fetchall()
                cursor.close()
                self.desconectar()
                return retornable
            except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al solicitar la query preconstruida a la base de datos") 

        def buscar_pedido(self, id):
           self.conectar()
           cursor = self.conexion_activa.cursor()
           try: # Trata de buscar un pedido por id
                cursor.execute("SELECT * FROM Pedido WHERE id = %s;",(id,))
                self.conexion_activa.commit()
                retornable = cursor.fetchall()
                cursor.close()
                self.desconectar()
                return retornable
           except:
                cursor.close()
                self.desconectar()
                raise Exception("Error al buscar un pedido en la base de datos")   
