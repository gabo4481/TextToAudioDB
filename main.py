import dearpygui.dearpygui as dpg
import pyttsx3
import time
import psycopg
from BD_control import BD_controler

BD_controler = BD_controler()

# Inicialización de pyttsx3
engine = pyttsx3.init()
contenido = ""
voices = engine.getProperty('voices')
opciones_voices = {index: voice.name for index, voice in enumerate(voices)}

# Funciones de base de datos


def actualizar_historial():
    if dpg.does_item_exist("tabla_historial"):
        dpg.delete_item("tabla_historial")

    with dpg.table(header_row=True,parent="historial", tag="tabla_historial"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Nombre")
        dpg.add_table_column(label="Audio")
        dpg.add_table_column(label="Caracteres")
        dpg.add_table_column(label="Palabras")
        dpg.add_table_column(label="Fecha")
        dpg.add_table_column(label="Acciones")
        
        registros = BD_controler.leer_historial()
        for registro in registros:
            with dpg.table_row():
                dpg.add_text(registro[0])
                dpg.add_text(registro[1])
                dpg.add_button(label="Reproducir", callback=create_reproducir_callback(registro[0]))
                dpg.add_text(registro[4])
                dpg.add_text(registro[5])
                dpg.add_text(registro[9])
                with dpg.group():
                    dpg.add_button(label="Actualizar", callback=create_actualizar_callback(registro[0]))
                    dpg.bind_item_theme(dpg.last_item(), "tema_boton_azul")
                    dpg.add_button(label="Eliminar", callback=create_eliminar_callback(registro[0]))
                    dpg.bind_item_theme(dpg.last_item(), "tema_boton_rojo")
                    
def create_reproducir_callback(registro_id):
    def reproducir_audio():
        registro = BD_controler.buscar_audio(registro_id)
        print(registro_id,"e")
        audio = registro[0]
        velocidad = registro[1]
        volumen = registro[2]
        contenido = registro[3]
        engine.setProperty('rate', velocidad)
        engine.setProperty('volume', volumen)
        # Usar pyttsx3 para reproducir el texto
        engine.say(contenido)
        engine.runAndWait()
        print(f"Reproduciendo audio para ID: {registro_id}")
    return reproducir_audio

def create_actualizar_callback(registro_id):
    def abrir_actualizacion():
        dpg.configure_item("actualizacion", show=True)
        
        # Cargar valores específicos del registro seleccionado
        registro = BD_controler.buscar_registro_especifico(registro_id)
        print(registro[0])
        dpg.set_value("id", registro[0])
        dpg.set_value("nombre", registro[1])
        dpg.set_value("contenido", registro[2])
        dpg.set_value("caracteres", registro[4])
        dpg.set_value("palabras", registro[5])
        dpg.set_value("Tiempo", registro[6])
        dpg.set_value("vel_update", registro[7])
        dpg.set_value("vol_update", registro[8])
        print(f"Actualizando registro para ID: {registro_id}")
    return abrir_actualizacion

def create_eliminar_callback(registro_id):
    def eliminar_historial():
        BD_controler.eliminar_conversion(registro_id)
        actualizar_historial()
        print(f"Eliminando registro para ID: {registro_id}")
    return eliminar_historial
                    

def confirmar_actualizacion():
    id = dpg.get_value("id")
    nombre_conversion = dpg.get_value("nombre")
    contenido = dpg.get_value("contenido")
    cantidad_caracteres = dpg.get_value("caracteres")
    cantidad_palabras = dpg.get_value("palabras")
    tiempo_conversion = dpg.get_value("Tiempo")
    binario_archivo = psycopg.Binary(open(f"{nombre_conversion}.mp3", "rb").read())
    velocidad = dpg.get_value("vel_update")
    volumen = dpg.get_value("vol_update")
    
    datos_conversion = {
        "nombre": nombre_conversion,
        "contenido": contenido,
        "archivo": binario_archivo,
        "cantidad_caracteres": cantidad_caracteres,
        "cantidad_palabras": cantidad_palabras,
        "tiempo_conversion": tiempo_conversion,
        "velocidad": velocidad,
        "volumen": volumen
    }
    BD_controler.actualizar_registro(id, datos_conversion)
    actualizar_historial()
    
    # Limpiar valores de los campos
    dpg.set_value("id", "")
    dpg.set_value("nombre", "")
    dpg.set_value("contenido", "")
    dpg.set_value("caracteres", 0)
    dpg.set_value("palabras", 0)
    dpg.set_value("tiempo", 0)
    dpg.set_value("vel_update", 125)
    dpg.set_value("vol_update", 0.8)
    
    dpg.configure_item("actualizacion",show=False)

def guardar_conversion():
    nombre_conversion = dpg.get_value("nombre_conversion")
    contenido = dpg.get_value("texto_archivo")
    cantidad_caracteres = dpg.get_value("cantidad_caracteres")
    cantidad_palabras = dpg.get_value("cantidad_palabras")  
    tiempo_conversion = dpg.get_value("Tiempo_conversion")
    binario_archivo = psycopg.Binary(open(f"{nombre_conversion}.mp3","rb").read())
    velocidad = dpg.get_value("slider_velocidad")
    volumen = dpg.get_value("slider_volumen")
    datos_conversion = {
            "nombre" : nombre_conversion,
            "contenido": contenido,
            "archivo" : binario_archivo,
            "cantidad_caracteres": cantidad_caracteres,
            "cantidad_palabras": cantidad_palabras,
            "tiempo_conversion": tiempo_conversion,
            "velocidad":velocidad,
            "volumen":volumen
        }
    BD_controler.crear_conversion(datos_conversion)
    actualizar_historial()
    

#Funciones de texto a voz    
def leer_archivo(sender, app_data):
    ruta_archivo = app_data['file_path_name']
    try:
        with open(ruta_archivo, 'r') as file:
            contenido = file.read()
            dpg.set_value("texto_archivo", contenido)
            dpg.set_value("cantidad_caracteres",len(contenido))
            dpg.set_value("cantidad_palabras",len(contenido.split()))
    except Exception as e:
        print("Error al abrir el archivo:", e)
        

def texto_voz():
    contenido = dpg.get_value("texto_archivo")
    velocidad = dpg.get_value("slider_velocidad")
    volumen = dpg.get_value("slider_volumen")
    nombre_archivo = dpg.get_value("nombre_conversion")
    
    # Obtener el índice de la voz seleccionada en el combo box
    voz_seleccionada = dpg.get_value("combo_voces")
    voz_index = next((index for index, voice in opciones_voices.items() if voice == voz_seleccionada), None)
    
    if len(contenido) > 0 and voz_index is not None:
        # Configuración de velocidad, volumen y voz
        engine.setProperty('rate', velocidad)
        engine.setProperty('volume', volumen)
        engine.setProperty('voice', voices[voz_index].id)  
        
        star_time = time.time()
        
        # Guardar en archivo y reproducir
        engine.save_to_file(contenido, f"{nombre_archivo}.mp3")
        engine.runAndWait()
        
        end_time = time.time()
        
        time_conversion = round(end_time - star_time,2)
        
        # Mostrar popup de éxito
        dpg.set_value("texto_popup", f"Conversion realizada con exito. Tardo {time_conversion}seg")
        dpg.configure_item("popup_id", show=True)
        dpg.set_value("Tiempo_conversion",f"{time_conversion}")
        
        
    else:
        dpg.set_value("texto_popup", "Por favor carga un archivo de texto y elige una voz.")
        dpg.configure_item("popup_id", show=True)
        
def generar_mp3():
    contenido = dpg.get_value("contenido")
    dpg.set_value("caracteres",len(contenido))
    dpg.set_value("palabras",len(contenido.split()))
    velocidad = dpg.get_value("vel_update")
    volumen = dpg.get_value("vol_update")
    nombre_archivo = dpg.get_value("nombre")
    
    # Obtener el índice de la voz seleccionada en el combo box
    voz_seleccionada = dpg.get_value("combo_box02")
    voz_index = next((index for index, voice in opciones_voices.items() if voice == voz_seleccionada), None)
    
    if len(contenido) > 0 and voz_index is not None:
        # Configuración de velocidad, volumen y voz
        engine.setProperty('rate', velocidad)
        engine.setProperty('volume', volumen)
        engine.setProperty('voice', voices[voz_index].id)  
        star_time = time.time()
        
        # Guardar en archivo y reproducir
        engine.save_to_file(contenido, f"{nombre_archivo}.mp3")
        engine.runAndWait()
        
        end_time = time.time()
        
        time_conversion = round(end_time - star_time,2)
        
        # Mostrar popup de éxito
        dpg.set_value("texto_popup", f"operacion realizada con exito. Tardo {time_conversion}seg")
        dpg.configure_item("popup_id", show=True)
        dpg.configure_item("popup_id", modal=True)
        dpg.set_value("Tiempo",f"{time_conversion}")
    else:
        dpg.set_value("texto_popup", "ingresa contenido o elige una voz.")
        dpg.configure_item("popup_id", modal=True)
        dpg.configure_item("popup_id", show=True)

def prueba_voz(sender, app_data):
    # Obtencion de valores velocidad, volumen y voz
    voz_seleccionada = dpg.get_value("combo_voces")
    velocidad = dpg.get_value("slider_velocidad")
    volumen = dpg.get_value("slider_volumen")
    voz_index = next((index for index, voice in opciones_voices.items() if voice == voz_seleccionada), None)
    
    if voz_index is not None:
        # Configuración de velocidad, volumen y voz
        engine.setProperty('rate', velocidad)
        engine.setProperty('volume', volumen)  
        engine.setProperty('voice', voices[voz_index].id)  # Usar el ID de la voz seleccionada
        engine.say(dpg.get_value("texto_archivo"))
        engine.runAndWait()
    else:
        dpg.set_value("texto_popup","Voz no encontrada en la lista...")
        dpg.configure_item("popup_id", show=True)
        

# Configuración de interfaz de DearPyGui
dpg.create_context()
with dpg.theme(tag="tema_sliders"):
    with dpg.theme_component(dpg.mvSliderInt):
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))  # Color del grab
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (138, 43, 226))  # Color del grab activo
    with dpg.theme_component(dpg.mvSliderFloat):
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))  # Color del grab
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (138, 43, 226))  # Color del grab activo
        
with dpg.theme(tag="tema_boton_rojo"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button,(255, 0, 0, 128))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(255, 0, 0,50))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 0, 0, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 24)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)  # gap
                dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5 )
                with dpg.theme(tag="tema_boton_azul"):
                    with dpg.theme_component(dpg.mvButton):
                        dpg.add_theme_color(dpg.mvThemeCol_Button, (10, 56, 113) )  # background-color
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (138, 43, 226) )  # hover background-color
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (138, 43, 226) )  # active background-color
                        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255) )  # color
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 24 )  # border-radius
                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3,3)  # padding
                        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)  # gap
                        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5 )  # text-align
                    with dpg.theme(tag="tema_boton_blanco"):
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button, (216, 223, 232))  # background-color
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (138, 43, 226))  # hover background-color
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (138, 43, 226))  # active background-color
                            dpg.add_theme_color(dpg.mvThemeCol_Text, (10, 56, 113))  # color
                            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 24)  # border-radius
                            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)  # padding
                            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)  # gap
                            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)  # text-align

with dpg.window(label="Convertir Texto a Voz",tag="principal", width=700, height=600,pos=(0,0)):
    dpg.add_separator(label="Ingresa el Nombre de la conversion")
    dpg.add_input_text(indent=20,tag="nombre_conversion")
    
    dpg.add_separator(label="Contenido del archivo")
    with dpg.group(width=645,indent=20):
        dpg.add_input_text(tag="texto_archivo", multiline=True,readonly=True, height=200)

    dpg.add_separator(label="Configuraciones de Voz")
    with dpg.group(indent=20):
        dpg.add_slider_int(tag="slider_velocidad", label="Velocidad", default_value=125, min_value=100, max_value=300)
        dpg.bind_item_theme(dpg.last_item(), "tema_sliders")
        dpg.add_slider_float(tag="slider_volumen", label="Volumen", default_value=0.8, min_value=0.0, max_value=1.0)
        dpg.bind_item_theme(dpg.last_item(), "tema_sliders")
        dpg.add_combo(items=list(opciones_voices.values()), label="Listado de Voces", tag="combo_voces")
    
    dpg.add_separator(label="Estadisticas")
    with dpg.group(label="Estadisticas",tag="Estadisticas",horizontal=True,horizontal_spacing=40,width=600,indent=20):    
        with dpg.group(horizontal=True):
            dpg.add_text("Cantidad De Caracteres: ")
            dpg.add_text(label="cantidad_caracteres",tag="cantidad_caracteres",default_value=0)
        with dpg.group( horizontal=True):
            dpg.add_text("Cantidad De Palabras:")
            dpg.add_text(label="cantidad_palabras",tag="cantidad_palabras",default_value=0)
        with dpg.group( horizontal=True):
            dpg.add_text("Tiempo de conversion:")
            dpg.add_text(label="Tiempo de conversion:",tag="Tiempo_conversion",default_value=0)

    dpg.add_separator(tag="Acciones_control",label="Acciones")
    with dpg.group(tag="Acciones",horizontal=True,horizontal_spacing=50,width=150,height=40,indent=50):
        dpg.add_button(label="Convertir Texto", callback=lambda:texto_voz())
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_blanco")
        dpg.add_button(label="Escuchar Texto", callback=prueba_voz)
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_azul")
        dpg.add_button(label="Cargar texto", callback=lambda: dpg.show_item("cargar_texto_id"))
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_rojo")
        
    dpg.add_separator(tag="Guardar_Registro",label="Guardar Registro")   
    with dpg.group(width=200,height=40,indent=50,tag="boton_guardar_conversion"):
        dpg.add_button(label="Guardar Conversion", callback=guardar_conversion)
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_blanco")
        
        
    
#Actualizacion
with dpg.window(label="Actualizacion Registro",tag="actualizacion",modal=True,show=False, width=700, height=600,pos=(400,0)):
    dpg.add_input_text(tag="id")
    dpg.add_separator(label="Nombre de la conversion")
    dpg.add_input_text(indent=20,tag="nombre")
    
    dpg.add_separator(label="Contenido del archivo")
    with dpg.group(width=620,indent=20):
        dpg.add_input_text(tag="contenido", multiline=True,readonly=False, height=200)

    dpg.add_separator(label="Configuraciones de Voz")
    with dpg.group(indent=20):
        dpg.add_slider_int(tag="vel_update", label="velocidad", default_value=125, min_value=100, max_value=300)
        dpg.bind_item_theme(dpg.last_item(), "tema_sliders")
        dpg.add_slider_float(tag="vol_update", label="volumen", default_value=0.8, min_value=0.0, max_value=1.0)
        dpg.bind_item_theme(dpg.last_item(), "tema_sliders")
        dpg.add_combo(items=list(opciones_voices.values()), label="Listado de Voces", tag="combo_box02")
    
    dpg.add_separator(label="Estadisticas")
    with dpg.group(label="Estadisticas",tag="estadisticas_update",horizontal=True,horizontal_spacing=40,width=600,indent=20):    
        with dpg.group(horizontal=True):
            dpg.add_text("Cantidad De Caracteres: ")
            dpg.add_text(label="cantidad_caracteres",tag="caracteres",default_value=0)
        with dpg.group( horizontal=True):
            dpg.add_text("Cantidad De Palabras:")
            dpg.add_text(label="cantidad_palabras",tag="palabras",default_value=0)
        with dpg.group( horizontal=True):
            dpg.add_text("Tiempo de conversion:")
            dpg.add_text(label="Tiempo de conversion:",tag="Tiempo",default_value=0)
            
    dpg.add_separator(tag="Acciones_actualizacion",label="Acciones actualizar")
    with dpg.group(tag="Acciones_actualizar",horizontal=True,horizontal_spacing=40,width=200,height=40,indent=50):
        dpg.add_button(label="Confirmar Cambio",tag="boton_confirmacion",callback=confirmar_actualizacion)
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_blanco")
        dpg.add_button(label="Cerrar", callback=lambda: dpg.configure_item("actualizacion", show=False))
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_azul")
        dpg.add_button(label="Generar mp3", callback=lambda:generar_mp3())
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_rojo")

# Construcción inicial de la ventana y la tabla
with dpg.window(label="Historial de Conversiones", autosize=True, tag="historial", pos=(715, 0)):
    with dpg.table(header_row=True, tag="tabla_historial"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Nombre")
        dpg.add_table_column(label="Audio")
        dpg.add_table_column(label="Caracteres")
        dpg.add_table_column(label="Palabras")
        dpg.add_table_column(label="Fecha")
        dpg.add_table_column(label="Acciones")
        # Llamamos a actualizar_historial para llenar la tabla al inicio
        actualizar_historial()


with dpg.file_dialog(directory_selector=False, show=False, modal=True, callback=leer_archivo, tag="cargar_texto_id", width=600, height=400):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255))

with dpg.window(label="Estatus de Conversión", autosize=True, show=False, modal=True, tag="popup_id"):
    dpg.add_text(default_value="Conversión Completada con Éxito.",tag="texto_popup")
    dpg.add_button(label="Cerrar", callback=lambda: dpg.configure_item("popup_id", show=False))
        

# Configuración final
dpg.create_viewport(title="Conversor texto a voz",resizable=True,x_pos=0,y_pos=0)
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
