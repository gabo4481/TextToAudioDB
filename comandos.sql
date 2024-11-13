CREATE TABLE datos_conversion(
id SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
contenido VARCHAR(1000) NOT NULL,
audio_binario BYTEA NOT NULL,
cantidad_caracteres VARCHAR(500) NOT NULL,
cantidad_palabras VARCHAR(500) NOT NULL,
tiempo_conversion varchar(50) NOT NULL,
velocidad integer NOT NULL,
volumen float NOT NULL,
fecha_conversion DATE DEFAULT CURRENT_DATE
)
DELETE FROM datos_conversion;
ALTER SEQUENCE datos_conversion_id_seq RESTART WITH 1;

select * from datos_conversion
select audio_binario,velocidad,volumen from datos_conversion where id = 1
SELECT audio_binario,velocidad,volumen FROM datos_conversion where id = 8