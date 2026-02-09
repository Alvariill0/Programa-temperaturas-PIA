# bd_modulo.py - Módulo Base de Datos - ÁLVARO FERNANDEZ BECERRA
import mysql.connector
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# CONFIG BD
CONFIG_DB = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'temperaturas')
}

# Códigos CCA3 paises de la Union europea
EU_CCA3 = {
    'AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE'
}

def conectar_bd():
    """
        Funcion basica de conexion a la base de datos.
    """
    try:
        return mysql.connector.connect(**CONFIG_DB)
    except Exception as e:
        print(f"Error conexion BD: {e}")
        return None

def insertar_pais(conexion, cca2, cca3, nombre, capital, region, subregion, miembro_ue, latitud=None, longitud=None):
    """
    Inserta un país en la base de datos.
    Params:
        conexion: Conexión a la base de datos.
        cca2: Código alfa-2 del país.
        cca3: Código alfa-3 del país.
        nombre: Nombre del país.
        capital: Capital del país.
        region: Región del país.
        subregion: Subregión del país.
        miembro_ue: Indica si el país pertenece a la Unión Europea.
        latitud: Latitud del país.
        longitud: Longitud del país.
    Devuelve:
        id del país insertado.
    """
    cursor = conexion.cursor()
    # Comprobar si ya existe
    cursor.execute("SELECT idpais FROM paises WHERE cca3=%s", (cca3,))
    existente = cursor.fetchone()
    if existente:
        id_existente = existente[0]
        cursor.close()
        return id_existente

    cursor.execute("""
        INSERT INTO paises (cca2, cca3, nombre, capital, region, subregion, miembroUE, latitud, longitud)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
        (cca2, cca3, nombre, capital, region, subregion, miembro_ue, latitud, longitud))
    conexion.commit()
    id_nuevo = cursor.lastrowid
    cursor.close()
    return id_nuevo

def insertar_frontera(conexion, id_pais, cca3_frontera):
    """
    Inserta una frontera para un país si no existe ya.
    Params:
        conexion: Conexión a la base de datos.
        id_pais: ID del país.
        cca3_frontera: Código alfa-3 de la frontera.
    """
    cursor = conexion.cursor()
    # Comrpbar si ya existe
    cursor.execute("SELECT 1 FROM fronteras WHERE idpais=%s AND cca3_frontera=%s", (id_pais, cca3_frontera))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO fronteras (idpais, cca3_frontera) VALUES (%s,%s)", (id_pais, cca3_frontera))
        conexion.commit()
    cursor.close()

def insertar_temperatura(conexion, id_pais, timestamp, temperatura, sensacion, minima, maxima, humedad, amanecer, atardecer):
    """
    Inserta un registro de temperatura para un país.
    Params:
        conexion: Conexión a la base de datos.
        id_pais: ID del país.
        timestamp: Marca temporal del registro.
        temperatura: Temperatura actual.
        sensacion: Sensación térmica.
        minima: Temperatura mínima.
        maxima: Temperatura máxima.
        humedad: Humedad relativa.
        amanecer: Hora del amanecer.
        atardecer: Hora del atardecer.
    """
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO temperaturas (idpais, timestamp, temperatura, sensacion, minima, maxima, humedad, amanecer, atardecer)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
        (id_pais, timestamp, temperatura, sensacion, minima, maxima, humedad, amanecer, atardecer))
    conexion.commit()
    cursor.close()

def insertar_desde_json(conexion, ruta_json):
    """
        Inserta los datos desde el archivo JSON
    """
    # Ajutar ruta absoluta / relativa
    ruta = ruta_json if os.path.isabs(ruta_json) else os.path.join(os.path.dirname(__file__), ruta_json)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encuentra el archivo JSON: {ruta}")

    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    for pais_data in datos:
        cca2 = pais_data['cca2']
        cca3 = pais_data['cca3']
        nombre = pais_data['name']['common']
        capital = pais_data.get('capital', [''])[0]
        region = pais_data['region']
        subregion = pais_data.get('subregion', '')
        latitud = pais_data['latlng'][0] if 'latlng' in pais_data and len(pais_data['latlng']) > 0 else None
        longitud = pais_data['latlng'][1] if 'latlng' in pais_data and len(pais_data['latlng']) > 1 else None

        # ----- Revisar lo de unMember **
        miembro_ue = 1 if cca3 in EU_CCA3 else 0
        
        id_pais = insertar_pais(conexion, cca2, cca3, nombre, capital, region, subregion, miembro_ue, latitud, longitud)
        
        # Insert fronteras
        fronteras = pais_data.get('borders', [])
        for frontera in fronteras:
            insertar_frontera(conexion, id_pais, frontera)

def obtener_todos_paises(conexion):
    """
    Obtiene todos los paises existentesen la base de datos.
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paises ORDER BY nombre")
    filas = cursor.fetchall()
    cursor.close()
    return filas

def obtener_temperaturas(conexion):
    """
        Obtiene temperatura y nombre de pais de la BD
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT t.*, p.nombre FROM temperaturas t JOIN paises p ON t.idpais=p.idpais ORDER BY t.timestamp DESC")
    filas = cursor.fetchall()
    cursor.close()
    return filas

def obtener_fronteras(conexion):
    """
        Obtiene fronteras y nombre de pais de la BD
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, p.nombre as pais, pf.nombre as frontera 
        FROM fronteras f 
        JOIN paises p ON f.idpais=p.idpais 
        LEFT JOIN paises pf ON f.cca3_frontera=pf.cca3""")
    filas = cursor.fetchall()
    cursor.close()
    return filas

def obtener_temperaturas_fronteras(conexion, nombre_pais):
    """
        Obtiene las temperaturas de un pais y sus fronteras.
        Búsqueda tolerante: intenta coincidencia exacta (case-insensitive), por códigos
        (cca2/cca3) y por coincidencia parcial (LIKE) si no encuentra nada.
    """
    cursor = conexion.cursor(dictionary=True)
    nombre_pais = nombre_pais.strip()

    # 1- Busqueda por nombre xacto
    cursor.execute("SELECT idpais, nombre FROM paises WHERE LOWER(nombre)=LOWER(%s)", (nombre_pais,))
    pais = cursor.fetchone()

    # 2- Busqueda por codigos cca2/cca3
    if not pais:
        code = nombre_pais.upper()
        if len(code) in (2, 3):
            cursor.execute("SELECT idpais, nombre FROM paises WHERE cca3=%s OR cca2=%s", (code, code))
            pais = cursor.fetchone()

    if not pais:
        cursor.close()
        return None

    id_pais = pais['idpais']
    nombre_p = pais.get('nombre', nombre_pais)

    # Temp pais: obtener el registro más reciente (si existe)
    cursor.execute("SELECT * FROM temperaturas WHERE idpais=%s ORDER BY timestamp DESC LIMIT 1", (id_pais,))
    temp_pais = cursor.fetchone()

    # Temps fronteras: registro más reciente por país frontera
    cursor.execute("""
        SELECT t.*, pf.nombre 
        FROM temperaturas t
        JOIN (
            SELECT idpais, MAX(timestamp) AS maxt FROM temperaturas GROUP BY idpais
        ) mt ON t.idpais = mt.idpais AND t.timestamp = mt.maxt
        JOIN paises pf ON t.idpais = pf.idpais
        JOIN fronteras f ON pf.cca3 = f.cca3_frontera
        WHERE f.idpais = %s
        ORDER BY pf.nombre
    """, (id_pais,))
    temps_fronteras = cursor.fetchall()
    cursor.close()

    return {'pais': nombre_p, 'temp_pais': temp_pais, 'fronteras': temps_fronteras}


# # Funciones test
#
# def prueba():
#     print("=== PRUEBA MÓDULO BD ===")
#     conexion = conectar_bd()
#     
#     # Insertar desde JSON (países y fronteras)
#     print("1 INERTAR PAISES (Ejemplo)")
#     insertar_desde_json(conexion, "PaisesEjemplo.json")
#     cursor_test = conexion.cursor()
#     cursor_test.execute("SELECT nombre, cca3, miembroUE FROM paises WHERE cca3='ITA'")
#     ita = cursor_test.fetchone()
#     print("Comprobación Italia:", ita)
#     cursor_test.close()
#     
#     # Recuperar datos
#     print("\n 2 MOSTRAR INSERCIONES:")
#     paises = obtener_todos_paises(conexion)
#     print(f"Total: {len(paises)} países")
#     
#     print("\n3 ") 
#     temps = obtener_temperaturas(conexion)
#     print(f"Total: {len(temps)} registros")
#     
#     print("\n4. Fronteras:")
#     frs = obtener_fronteras(conexion)
#     print(f"Total: {len(frs)} fronteras")
#     # Mostrar una frontera:
#     for fr in frs:
#         # 'obtener_fronteras' devuelve columnas 'pais' y 'frontera'
#         if fr['pais'] == 'Estonia':
#             print(fr)
#     
#     print("\n5. Temps. España y fronteras:")
#     res = obtener_temperaturas_fronteras(conexion, "Spain")
#     print(res)
#
#     print("--------------.")
#     conexion.close()
    

# def limpiar_bd():
#     """
#     Limpia las tablas de la base de datos.
#     """
#     conexion = conectar_bd()
#     cursor = conexion.cursor()
#     cursor.execute("DELETE FROM temperaturas")
#     cursor.execute("DELETE FROM fronteras")
#     cursor.execute("DELETE FROM paises")
#     conexion.commit()
#     cursor.close()
#     conexion.close()
#     print("BD limpiada.")
