# Prácticas de Ingeniería de Datos con AWS S3 y Python

Este repositorio contiene una serie de prácticas y scripts diseñados para el procesamiento de datos, ingesta en la nube con **Amazon Web Services (AWS S3)**, perfilamiento, limpieza, modelado dimensional y pipelines **ETL hacia PostgreSQL**.

---

## 📂 Estructura del Repositorio

A continuación se describen los archivos incluidos en el proyecto:

* **`datos_sinteticos.py`**: Generación de datasets sintéticos de prueba.
* **`subir_a_raw.py`**: Ingesta y carga de archivos locales hacia la capa *Raw* del bucket en AWS S3.
* **`list_bucket.py`**: Verificación y listado de buckets/objetos dentro de AWS S3.
* **`perfilamiento_s3.py`**: Análisis exploratorio, estadístico y de calidad sobre los datos alojados en S3.
* **`limpieza.py`**: Transformación, tratamiento de nulos, duplicados y normalización de datos.
* **`esquema_estrella.py`**: Construcción de tablas de hechos y dimensiones (modelo multidimensional).
* **`etl_s3_postgres.py`**: Pipeline ETL completo para extraer datos procesados desde S3 y cargarlos en PostgreSQL.
* **`main.py`**: Script principal que coordina y ejecuta la secuencia del flujo de trabajo.
* **`requirements.txt`**: Archivo de dependencias del proyecto.

---

## ⚙️ Requisitos Previos e Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/javiersanchezbenitez03-eng/Practicas.git
cd Practicas
```

### 2. Creación del Entorno Virtual (Opcional pero Recomendado)

**En Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalación de Librerías y Dependencias

Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

> **Nota:** Las librerías principales utilizadas son `boto3`, `pandas`, `psycopg2-binary`, `sqlalchemy`, `python-dotenv` y `faker`.

---

## 🐘 Configuración de PostgreSQL

Para conectar el pipeline ETL a **PostgreSQL**, debes tener el servidor en ejecución y la base de datos configurada.

### 1. Instalación de PostgreSQL

* **Ubuntu / Debian:**
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```

* **macOS (con Homebrew):**
  ```bash
  brew install postgresql
  brew services start postgresql
  ```

* **Windows:** Descarga e instala la versión correspondiente desde el sitio oficial de [PostgreSQL Downloads](https://www.postgresql.org/download/windows/).

### 2. Configurar Usuario y Base de Datos

Accede a la consola interactiva de PostgreSQL (`psql`):

```bash
sudo -u postgres psql
```

Ejecuta las siguientes sentencias SQL para crear la base de datos y un usuario dedicado:

```sql
-- Crear la base de datos
CREATE DATABASE db_practicas;

-- Crear usuario con contraseña
CREATE USER usuario_etl WITH ENCRYPTED PASSWORD 'tu_contraseña_segura';

-- Conceder todos los privilegios sobre la base de datos al usuario
GRANT ALL PRIVILEGES ON DATABASE db_practicas TO usuario_etl;
```

---

## 🔑 Configuración de Credenciales y Tokens (Variables de Entorno)

Crea un archivo llamado `.env` en la raíz del proyecto para definir las credenciales de **AWS S3** y **PostgreSQL**:

```env
# ==========================================
# CREDENCIALES DE AWS (S3)
# ==========================================
AWS_ACCESS_KEY_ID=TU_ACCESS_KEY_AQUI
AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY_AQUI
AWS_SESSION_TOKEN=TU_SESSION_TOKEN_SI_USAS_AWS_ACADEMY
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=tu-nombre-de-bucket-s3

# ==========================================
# CONFIGURACIÓN Y CREDENCIALES DE POSTGRESQL
# ==========================================
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=db_practicas
POSTGRES_USER=usuario_etl
POSTGRES_PASSWORD=tu_contraseña_segura
```

---

## 🚀 Flujo de Ejecución

Puedes ejecutar cada etapa de manera independiente según el flujo del proyecto:

1. **Generar los datos sintéticos iniciales:**
   ```bash
   python datos_sinteticos.py
   ```

2. **Subir archivos a la capa Raw de AWS S3:**
   ```bash
   python subir_a_raw.py
   ```

3. **Verificar los archivos en el bucket de S3:**
   ```bash
   python list_bucket.py
   ```

4. **Perfilamiento y limpieza de datos:**
   ```bash
   python perfilamiento_s3.py
   python limpieza.py
   ```

5. **Construcción del modelo dimensional y carga a PostgreSQL:**
   ```bash
   python esquema_estrella.py
   python etl_s3_postgres.py
   ```

6. **Ejecución del Pipeline Completo (Automatizado):**
   ```bash
   python main.py
   ```