# 🏛 EventPro — Sistema de Gestión para Eventos y Convenciones

**CEFIT · Profundización de la Programación Orientada a Objetos II**
**Estudiante:** Santiago Arcila Gutiérrez

---

## 🗂 Estructura del Proyecto (MVC)

```
eventpro/
├── main.py                  # Entry point — ventana principal (View)
├── models/
│   ├── __init__.py
│   └── database.py          # Conexión MySQL + Stored Procedures (Model)
├── utils/
│   ├── __init__.py
│   ├── validators.py        # Validaciones de campos (Controller)
│   ├── exportar.py          # Exportación Excel y PDF
│   ├── temas.py             # Temas claro / oscuro
│   └── favicon.py           # Generación de favicon con Pillow
├── assets/                  # Imágenes y favicon generados
├── exports/                 # Archivos Excel y PDF exportados
├── init.sql                 # Tablas + SP + datos de ejemplo
├── Dockerfile               # Imagen Docker de la app
├── docker-compose.yml       # Orquestación app + MySQL
└── requirements.txt         # Dependencias Python
```

---

## 📋 Requisitos

| Herramienta | Versión mínima |
|---|---|
| Python | 3.11+ |
| Docker Desktop | 4.x |
| Docker Compose | v2 |

---

## ⚙️ Instalación — Opción A: Docker (recomendado)

### 1. Clona el repositorio

```bash
git clone <url-del-repositorio>
cd eventpro
```

### 2. En Windows — permitir display para Tkinter

```bash
# Instala VcXsrv o use WSL2 con X11
# Exporta la variable de display
set DISPLAY=host.docker.internal:0
```

### 3. Levanta los contenedores

```bash
docker-compose up --build
```

Esto:
- Levanta MySQL 8.4 en el puerto 3306
- Ejecuta `init.sql` automáticamente (tablas + SP + datos)
- Construye y corre la app Python

### 4. Detener

```bash
docker-compose down
```

Para borrar también los datos de la BD:
```bash
docker-compose down -v
```

---

## ⚙️ Instalación — Opción B: Local (sin Docker)

### 1. Instala dependencias

```bash
pip install -r requirements.txt
```

### 2. Configura la BD

Abre `models/database.py` y cambia `"host": "db"` por `"host": "localhost"` y ajusta la contraseña.

Ejecuta `init.sql` en HeidiSQL o MySQL Workbench.

### 3. Corre la app

```bash
python main.py
```

---

## 🚀 Funcionalidades

### 4 Módulos
| Módulo | Tabla BD | Campos |
|---|---|---|
| 🏛 Recintos | `Recintos` | Código, nombre, tipo, ubicación, capacidad, tarifa, disponibilidad + **imagen** |
| 👥 Clientes | `Clientes` | Código, tipo, razón social, documento, teléfono, correo, contacto, clasificación + **foto** |
| 🎪 Eventos | `Eventos` | N° evento, título, tipo, cliente, **fechas con calendario**, asistentes, estado |
| 👷 Personal | `Personal` | Código, nombres, apellidos, especialidad, tarifa, evento, horario, disponibilidad |

### CRUD completo via Stored Procedures
- **Guardar** — INSERT con validaciones previas y confirmación
- **Actualizar** — UPDATE con confirmación
- **Eliminar** — DELETE con doble confirmación
- **Buscar** — SELECT por código o nombre
- **Limpiar** — limpia todos los campos

### Exportación
- **📊 Excel** — genera `.xlsx` con openpyxl (encabezados coloreados, filas alternadas)
- **📄 PDF** — genera `.pdf` con reportlab (tabla con logo de colores, landscape)
- Los archivos se guardan en la carpeta `exports/`

### Validaciones
- Formato de **email** con expresión regular
- **Teléfono** solo dígitos y caracteres válidos
- **Códigos** con prefijo correcto (RC-, CL-, EV-, EP-)
- **Longitud** mínima y máxima de campos de texto
- Campos **numéricos** rechazan texto
- Confirmación antes de **eliminar** y **actualizar**

### Imágenes (Pillow)
- Módulo **Recintos**: foto del recinto (JPG, PNG, GIF, máx 5MB)
- Módulo **Clientes**: foto del contacto (JPG, PNG, GIF, máx 5MB)
- Redimensionamiento automático con `Image.LANCZOS`

### Interfaz
- **2 temas**: claro (fondo blanco) y oscuro (fondo navy)
- **Favicon** generado automáticamente con Pillow
- **Fechas** con calendario flotante (tkcalendar `DateEntry`)
- Placeholders informativos en todos los campos

---

## 🗄 Base de Datos

**Motor:** MySQL 8.4  
**Base de datos:** `eventpro`  
**Puerto:** 3306  
**Usuario:** root / Contraseña: `eventpro123`

### 20 Stored Procedures (5 × 4 módulos)

| SP | Operación |
|---|---|
| `sp_insertar_*` | INSERT |
| `sp_actualizar_*` | UPDATE |
| `sp_eliminar_*` | DELETE |
| `sp_buscar_*` | SELECT con LIKE |
| `sp_listar_*` | SELECT todos |

---

## 🐳 Docker — Detalles

| Servicio | Imagen | Puerto |
|---|---|---|
| `db` | mysql:8.4 | 3306 |
| `app` | python:3.11-slim | — |

El servicio `app` espera a que `db` esté **healthy** antes de iniciar (healthcheck cada 10s).

Los datos de MySQL se persisten en el volumen `eventpro_data`.

---

*EventPro — Python · Tkinter · MySQL · Docker · 2026*

