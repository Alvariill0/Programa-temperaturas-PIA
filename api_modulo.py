# api_modulo.py - Modulo API Weathermap - ÁLVARO FERNANDEZ BECERRA
import requests
import json
import xml.etree.ElementTree as ET
import bd_modulo
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración API
API_KEY = os.getenv('API_KEY', '')
URL_BASE = os.getenv('API_URL', 'https://api.openweathermap.org/data/2.5/weather')

def obtener_temperaturas_todos_paises():
    """Obtiene las temperaturas de todas las capitales guardadas en la BD.

    - La primera mitad de paises se deben tratar en JSON y la otra en XML

    - Para JSON usamos `r.json()` que devuelve un diccionario.
    - Para XML usando la libreria `xml.etree.ElementTree.fromstring` parsea el texto y devuelve
    un arbol. Permite buscar en cada nodo con `find()` y leer atributos con `get()`.
    """
    conexion = bd_modulo.conectar_bd()
    paises = bd_modulo.obtener_todos_paises(conexion)
    if not paises:
        print("No hay países en la base de datos")
        conexion.close()
        return

    print(f"\nObteniendo temperaturas para {len(paises)} países...")
    
    mitad = len(paises) // 2  
    insertadas = 0
    errores = 0
    
    for i in range(len(paises)):
        pais = paises[i]
        
        try:
            capital = pais['capital']
            cca2 = pais['cca2'].lower()
            
            if not capital:
                # Saltar si no hay capital
                continue
            
            if i < mitad:
                # Primera mitad de paises en JSON
                url = f"{URL_BASE}?q={capital},{cca2}&appid={API_KEY}&units=metric"
                r = requests.get(url)
                datos = r.json()
                
                temperatura = datos['main']['temp']
                sensacion = datos['main']['feels_like']
                minima = datos['main']['temp_min']
                maxima = datos['main']['temp_max']
                humedad = datos['main']['humidity']

                # sys.sunrise y sys.sunset vienen como timestamps, hay que convertir a hora
                amanecer = datetime.fromtimestamp(datos['sys']['sunrise']).time().strftime('%H:%M:%S')
                atardecer = datetime.fromtimestamp(datos['sys']['sunset']).time().strftime('%H:%M:%S')
                
            else:
                # Segunda mitad de paises en XML
                url = f"{URL_BASE}?q={capital},{cca2}&appid={API_KEY}&units=metric&mode=xml"
                r = requests.get(url)
                raiz = ET.fromstring(r.text)
                
                temperatura = float(raiz.find('.//temperature').get('value'))
                sensacion = float(raiz.find('.//feels_like').get('value'))
                minima = float(raiz.find('.//temperature').get('min'))
                maxima = float(raiz.find('.//temperature').get('max'))
                humedad = float(raiz.find('.//humidity').get('value'))
                sun = raiz.find('.//city/sun') or raiz.find('.//sun')
                amanecer = sun.get('rise').split('T')[1][:8]
                atardecer = sun.get('set').split('T')[1][:8]
            
            # GUARDAR BD
            ahora = datetime.now()
            bd_modulo.insertar_temperatura(conexion, pais['idpais'], ahora, temperatura, sensacion, minima, maxima, humedad, amanecer, atardecer)
            insertadas += 1
            
        except Exception as e:
            errores += 1
            print(f"  Error en {pais['nombre']}: {str(e)}")
    
    conexion.close()
    
    print(f"\n✓ Inserción completada: {insertadas} temperaturas guardadas.")
    if errores > 0:
        print(f"  ({errores} errores durante la inserción)")

