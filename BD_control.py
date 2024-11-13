import psycopg
class BD_controler():
    def conectar(self):
        try:
            conexion = psycopg.connect(
                host = "localhost",
                dbname = "texttoaudioDB",
                user = "postgres",
                password = "gabo4481"
            )
            print("Conexion Exitosa.")
            return conexion
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        
        
    def buscar_audio(self,id):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """SELECT audio_binario,velocidad,volumen,contenido FROM datos_conversion where id = %s""",(id,)
                    )
                    archivo_binario = cursor.fetchone()
                    if archivo_binario:
                        
                        return archivo_binario
                    else:
                        print(f"No se encontro audio del id {id}")
            except psycopg.Error as e:
                print(f"Error al buscar el archivo del id {id}: {e}")
            finally:
                conexion.close()
                
            
        
    def crear_conversion(self, datos):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO datos_conversion (nombre,contenido,audio_binario,cantidad_caracteres,cantidad_palabras,tiempo_conversion,velocidad,volumen)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(datos["nombre"],datos["contenido"],datos["archivo"],datos["cantidad_caracteres"],datos["cantidad_palabras"],datos["tiempo_conversion"],datos["velocidad"],datos["volumen"])
                    )
                    conexion.commit()
                    print("Registro creado exitosamente.")
            except psycopg.Error as e:
                print(f"Error al crear el registro: {e}")
            finally:
                conexion.close()
                
    def leer_historial(self):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """SELECT * FROM datos_conversion"""
                    )
                    registros = cursor.fetchall()
            except psycopg.Error as e:
                print(f"Error al intente leer los datos: {e}")
            finally:
                conexion.close()
                return registros
            
    def eliminar_conversion(self,id):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """ DELETE FROM datos_conversion where id =%s """,(id,)
                    )
                    conexion.commit()
                    if cursor.rowcount > 0:
                        print("Registro borrado exitosamnete.")
                    else:
                        print(f"No se encontro un registro con el id {id}")
            except psycopg.Error as e:
                print(f"Error al intentar borrar el registro: {e}")
            finally:
                conexion.close()
        
    def buscar_registro_especifico(self,id):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """SELECT * FROM datos_conversion where id = %s""",(id,)
                    )
                    registro = cursor.fetchone()
            except psycopg.Error as e:
                print(f"Error al buscar el registro con id {id}: {e}")
            finally:
                conexion.close()
                return registro
            
    def actualizar_registro(self, id, datos):
        conexion = self.conectar()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """UPDATE datos_conversion SET nombre = %s, contenido = %s, audio_binario = %s, cantidad_caracteres = %s,
                        cantidad_palabras = %s, tiempo_conversion = %s, velocidad = %s, volumen = %s WHERE id = %s""",
                        (datos["nombre"], datos["contenido"], datos["archivo"], datos["cantidad_caracteres"],
                        datos["cantidad_palabras"], datos["tiempo_conversion"], datos["velocidad"], datos["volumen"], id)
                    )
                    conexion.commit()
                    if cursor.rowcount > 0:
                        print("Registro actualizado con éxito.")
                    else:
                        print(f"No se encontró ningún registro para el ID {id}")
            except psycopg.Error as e:
                print(f"Error al actualizar el registro ID {id}: {e}")
            finally:
                conexion.close()
