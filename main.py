# main.py - Menú (Punto 5)
import bd_modulo
import api_modulo

RUTA_JSON = "PaisesEuropa.json"

while True:
    print("\n=== TEMPERATURAS EUROPA ===")
    print("1. Insertar países JSON")
    print("2. Temps todos los paises (de la API) y guardar en la BD") 
    print("3. Temps de un pais + fronteras")
    # print("33. Limpiar BD )
    print("0. Salir")
    
    opcion = input("Elige una opcion: ").strip()
    
    if opcion == "1":
        conn = bd_modulo.conectar_bd()
        if not conn:
            print("Error: no se pudo conectar a la base de datos")
        else:
            #Si se inserta correctamente, no habrá mensaje de error
            if bd_modulo.insertar_desde_json(conn, RUTA_JSON):
                print(" Inserción completada")
            conn.close()
            
    
    elif opcion == "2":
        if api_modulo.API_KEY:
            api_modulo.obtener_temperaturas_todos_paises()
        else:
            print(" Error / API_KEY vacía en api_modulo.py")
    
    elif opcion == "3":
        conn = bd_modulo.conectar_bd()
        if not conn:
            print("Error: no se pudo conectar a la base de datos")
        else:
            # Mostrar listado de países disponibles con sus códigos
            print("\n=== PAÍSES DISPONIBLES ===")
            paises_disp = bd_modulo.obtener_todos_paises(conn)
            if paises_disp:
                for p in paises_disp:
                    print(f"  {p['nombre']:<30} (CCA2: {p['cca2']}, CCA3: {p['cca3']})")
            else:
                print("No hay países en la base de datos. Primero debes insertar datos (opción 1)")
                conn.close()
            
            pais = input("\nNombre país: ").title()
            res = bd_modulo.obtener_temperaturas_fronteras(conn, pais)
            if not res:
                print("País no encontrado en la base de datos")
            else:
                temp_pais = res.get('temp_pais')
                fronteras = res.get('fronteras', [])

                def fmt_ts(ts):
                    if ts is None:
                        return "—"
                    try:
                        return ts.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        return str(ts)

                # Mostrar temperatura del país 
                if temp_pais:
                    ts = fmt_ts(temp_pais.get('timestamp'))
                    print(f"\n{res['pais']}: {temp_pais['temperatura']}°C @ {ts}")
                else:
                    print(f"\n{res['pais']}: Sin registro de temperatura")

                # Mostrar temperaturas de fronteras
                if fronteras:
                    for f in fronteras[:5]:
                        nombre_fr = f.get('nombre') or f.get('frontera') or 'Desconocido'
                        temp_fr = f.get('temperatura')
                        timestamp_fr = fmt_ts(f.get('timestamp'))
                        if temp_fr is not None:
                            print(f"{nombre_fr}: {temp_fr}°C @ {timestamp_fr}")
                        else:
                            print(f"{nombre_fr}: Sin datos")
                else:
                    print("Fronteras: Sin datos de temperatura")
            conn.close()
    
    elif opcion == "0":
        print("Chao pescao")
        break
    
    # # limpiar la base de datos test
    # elif opcion == "33":
    #     conn = bd_modulo.conectar_bd()
    #     if not conn:
    #         print("Error: no se pudo conectar a la base de datos")
    #     else:
    #         bd_modulo.limpiar_bd()
    #         conn.close()
    
    # Opción no válida
    else:
        print("-- Opción no válida --")

