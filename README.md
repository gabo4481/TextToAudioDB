# TextToAudioDB
# Aplicación de Conversión de Texto a Voz

Este repositorio contiene una aplicación en Python que convierte texto a voz utilizando `pyttsx3`, gestiona el historial de conversiones en una base de datos PostgreSQL, y proporciona una interfaz gráfica de usuario construida con `DearPyGui`. La aplicación permite a los usuarios convertir texto a voz, gestionar las conversiones (guardar, actualizar y eliminar) y reproducir el audio generado.

## Características

- **Conversión de Texto a Voz**: Convierte cualquier texto a voz, ajustando la velocidad y el volumen.
- **Selección de Voz**: Elige entre una lista de voces disponibles para la síntesis de voz.
- **Gestión de Historial**: Visualiza, actualiza y elimina conversiones pasadas.
- **Reproducción de Audio**: Escucha los archivos de audio generados previamente.
- **Integración con Base de Datos**: Almacena los detalles de la conversión y los archivos de audio en una base de datos PostgreSQL.
- **Manejo de Archivos**: Carga texto desde archivos y guarda el audio en archivos MP3.

## Requisitos

- Python 3.x
- `pyttsx3`
- `psycopg2`
- `DearPyGui`
- Una base de datos PostgreSQL (asegúrate de que el esquema de tabla requerido esté configurado)

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/gabo4481/TextToAudioDB.git

2. Instala los paquetes de Python requeridos:
    ```bash
    pip install -r requirements.txt
    ```

3. Asegúrate de que tu base de datos PostgreSQL esté configurada. Puedes modificar la configuración de conexión de la base de datos en `BD_control.py`.

4. Ejecuta la aplicación:
    ```bash
    python main.py
    ```

## Flujo de la Aplicación

1. **Conversión de Texto a Voz**:
    - Carga un archivo de texto usando el botón `Cargar texto`.
    - Ajusta los parámetros de voz (velocidad, volumen y voz).
    - Haz clic en "Convertir Texto" para generar la voz y guardarla como un archivo MP3.
    - La aplicación también mostrará el tiempo que tomó la conversión.

2. **Visualización y Gestión del Historial de Conversiones**:
    - El historial de conversiones se muestra en una tabla con las siguientes columnas: ID, Nombre, Audio, Caracteres, Palabras, Fecha, Acciones.
    - Puedes reproducir el audio, actualizar o eliminar cualquier conversión desde la tabla del historial.

3. **Actualización de una Conversión**:
    - Puedes abrir un registro de conversión específico para editarlo haciendo clic en el botón "Actualizar".
    - Actualiza los campos según sea necesario,dale clic al boton generar archivo mp3 y esperar a que cambie el tiempo de conversion
    - Una vez hecho todo lo anterior puedesh hacer clic en "Confirmar Cambio" para guardar los cambios.

4. **Integración con la Base de Datos**:
    - Las conversiones se guardan en la base de datos PostgreSQL, incluyendo el archivo de audio, la cantidad de caracteres y palabras, y el tiempo de conversión.
    - Usa la función `actualizar_historial()` para actualizar la tabla de historial después de cualquier cambio.

## Estructura del Código

- **BD_control.py**: Contiene la clase `BD_controler` que maneja las interacciones con la base de datos PostgreSQL, incluyendo la creación, lectura, actualización y eliminación de registros. Los métodos clave son:
  - `conectar()`: Establece la conexión con la base de datos.
  - `buscar_audio(id)`: Recupera el audio de una conversión por su ID.
  - `crear_conversion(datos)`: Crea una nueva conversión y la guarda en la base de datos.
  - `leer_historial()`: Lee el historial completo de conversiones.
  - `eliminar_conversion(id)`: Elimina una conversión de la base de datos por su ID.
  - `buscar_registro_especifico(id)`: Busca un registro específico de conversión por su ID.
  - `actualizar_registro(id, datos)`: Actualiza un registro de conversión con nuevos datos.

- **app.py**: El script principal donde se define la lógica de la aplicación, incluyendo la interfaz DearPyGui, la lógica de conversión y las interacciones con la base de datos.
- **Configuración de la UI**: La interfaz de usuario está construida con `DearPyGui`, con temas y widgets para facilitar la experiencia del usuario.

