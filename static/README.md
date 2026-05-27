# 🛒 INVENTARIO AVA

Sistema web de gestión de inventario desarrollado con Flask, SQL Server y Python.

Permite administrar productos, controlar stock, gestionar imágenes, autenticación de usuarios y operaciones CRUD completas.

---

# 🚧 Estado del proyecto

Proyecto en desarrollo activo.
Actualmente enfocado en mejoras de seguridad, arquitectura backend y futuras funcionalidades inteligentes.

---
# 🚀 Tecnologías utilizadas

- Python
- Flask
- SQL Server
- HTML5
- CSS3
- Jinja2
- PyODBC

---

# 🔐 Funcionalidades

✅ Login seguro con sesiones  
✅ Protección de rutas  
✅ Logout de usuarios  
✅ Hash de contraseñas  
✅ CRUD de productos  
✅ Subida de imágenes  
✅ Papelera de productos  
✅ Reactivación de productos  
✅ Eliminación permanente  
✅ Filtros de búsqueda  
✅ Resumen de inventario  
✅ Arquitectura modular con Blueprints  

---


# 📸 Capturas del sistema

## 🔑 Login

![Login](static/screenshots/login.png)

---

## 📦 Inventario Principal

![Inventario](static/screenshots/inventario.png)

---

## 🗳 Papelera de Productos

![Papelera](static/screenshots/papelera.png)

---

## 📋 Registro y filtrado de producto

![Registro y búsqueda](static/screenshots/registro-busqueda.png)


“Inicialmente desarrollé el sistema como una aplicación CLI en Python y luego evolucioné la arquitectura hacia una aplicación web modular con Flask.”

# Evolución del proyecto
- Versión inicial CLI en Python
- Migración a Flask
- Implementación web
- Sistema de autenticación
- Arquitectura modular

# 📂 Estructura del proyecto

```bash
InventarioAVA/
│
├── app.py
├── cli/
├── database/
├── routes/
├── utils/
├── tests/
├── static/
├── templates/
└── README.md
```
---

# ⚙ Instalación

## 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

---

## 3. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Instalar dependencias

```bash
pip install flask pyodbc werkzeug
```

---

# ▶ Ejecución

```bash
python app.py
```

---

# 🔐 Seguridad implementada

- Protección de rutas mediante session
- Contraseñas cifradas con generate_password_hash()
- Validación de login con check_password_hash()

---

# 🚀 Próximas mejoras

- Dashboard administrativo
- Roles de usuario
- Exportación Excel/PDF
- API REST
- Machine Learning para predicción de stock
- Deploy en Render o Railway

---

## Conceptos aprendidos

- Arquitectura modular con Flask
- Manejo de sesiones
- CRUD completo
- SQL Server con PyODBC
- Blueprints
- Organización profesional backend
- Gestión de archivos e imágenes
- Validaciones backend
- Autenticación de usuarios
- Rutas protegidas

---

# 👨‍💻 Autor

Andrés Felipe Valencia Alvis

Tecnólogo en Análisis y Desarrollo de Software 