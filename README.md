# Temperaturas Europa - UT3 Ejercicio 3 - Álvaro Fernández Becerra

Aplicación para obtener y consultar temperaturas de capitales europeas utilizando la API de OpenWeatherMap.

## Funcionalidades

1. **Insertar países desde JSON**: Carga datos de países europeos en la base de datos MySQL
2. **Obtener temperaturas**: Descarga temperaturas de la API de OpenWeatherMap para todos los países
3. **Consultar temperaturas**: Busca la temperatura actual de un país y sus fronteras

## Requisitos previos

- Python 3.8+
- MySQL Server ejecutándose
- API Key de OpenWeatherMap (obtén una en https://openweathermap.org/api)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
```

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install mysql-connector-python==8.2.0 python-dotenv==1.0.0 requests==2.31.0
```

### 3. Crear la base de datos MySQL

#### Requisitos previos:

- Tener MySQL Server (o MariaDB) ejecutándose en tu máquina
- Conocer el usuario y contraseña de MySQL (por defecto usuario `root`)

**Recomendación**: Utiliza [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) para administrar fácilmente tu base de datos de forma visual.

#### Opción 1: Desde PowerShell (Recomendado en Windows)

Dentro del directorio del proyecto:

```powershell
Get-Content esquema.sql | mysql -u root -pTU_CONTRASEÑA
```

Reemplaza `TU_CONTRASEÑA` con tu contraseña de MySQL. Si no hay contraseña configurada:

```powershell
Get-Content esquema.sql | mysql -u root
```

#### Opción 2: Desde CMD

```cmd
mysql -u root -pTU_CONTRASEÑA < esquema.sql
```

#### Opción 3: Desde MySQL CLI 

Abre el cliente de MySQL:

```bash
mysql -u root -p
```

Ingresa tu contraseña cuando te lo pida, luego ejecuta:

```sql
source esquema.sql;
```

#### Opción 4: Usando MySQL Workbench

1. Abre MySQL Workbench
2. Conecta a la instancia local de MySQL
3. Ve a **File** → **Open SQL Script**
4. Selecciona el archivo `esquema.sql`
5. Haz clic en el botón **Execute**

---

El script crea automáticamente:

- Base de datos `temperaturas`
- Tabla `paises`
- Tabla `fronteras`
- Tabla `temperaturas`

### 4. Configurar variables de entorno (.env)

Copiar el contenido de  `.env.example` a `.env` en el mismo directorio.

Se puede copiar manualmente o ejecutar el comando:

```bash
cp .env.example .env
```

Editar `.env` y reemplazar los valores:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=temperaturas

API_KEY=tu_api_key_de_openweathermap
API_URL=https://api.openweathermap.org/data/2.5/weather
```

## Uso

```bash
python main.py
```

### Menú interactivo

```
=== TEMPERATURAS EUROPA ===
1. Insertar países JSON
2. Temps todos los paises (de la API) y guardar en la BD
3. Temps de un pais + fronteras
0. Salir
```

- **Opción 1**: Ejecutar solo la primera vez para cargar los datos de países desde `PaisesEuropa.json`
- **Opción 2**: Descargar temperaturas de la API de OpenWeatherMap y guardarlas en BD (se puede ejecutar múltiples veces)
- **Opción 3**: Consultar temperatura de un país específico y fronteras.

## Estructura del proyecto

```
.
├── main.py                  # Menú principal y flujo de la aplicación
├── bd_modulo.py             # Funciones de acceso a base de datos
├── api_modulo.py            # Funciones para consultar la API OpenWeatherMap
├── esquema.sql              # Script SQL para crear la base de datos
├── PaisesEuropa.json        # Datos de países europeos
├── PaisesEjemplo.json       # Versión de prueba con menos países
├── requirements.txt         # Dependencias Python (pip install -r requirements.txt)
├── .env.example             # Plantilla de variables de entorno (copia a .env)
├── .gitignore               # Archivos a ignorar en Git
└── README.md                # Este archivo
```

## Archivos principales

### `esquema.sql`

Script SQL que crea la estructura completa de la base de datos. Ejecutarlo una sola vez.

### `requirements.txt`

Dependencias del proyecto:

- `mysql-connector-python`: Conector para MySQL
- `python-dotenv`: Lee variables de entorno desde `.env`
- `requests`: Cliente HTTP para llamadas a la API

### `PaisesEuropa.json`

Contiene datos de países europeos (nombre, capital, códigos ISO, etc.)

### `.env.example`

Plantilla de configuración. Copiar a `.env` y rellenar con tus valores.

## Datos guardados en BD

Para cada país se almacenan:

- `temperatura`: Temperatura actual en °C
- `sensacion`: Sensación térmica
- `minima`/`maxima`: Temperaturas extremas
- `humedad`: Humedad relativa (%)
- `amanecer`/`atardecer`: Horas del amanecer y atardecer
- `timestamp`: Fecha y hora de la consulta

## Obtener una API Key

1. Visitar https://openweathermap.org/api
2. Registrarse o iniciar sesión
3. Crear una nueva API Key en "API Keys"
4. Copiarla en la variable `API_KEY`

## Tratamiento de datos

- La aplicación obtiene temperaturas en **dos formatos**:

  - Primera mitad de países: **JSON**
  - Segunda mitad de países: **XML**

## Autor

Álvaro Fernández Becerra
