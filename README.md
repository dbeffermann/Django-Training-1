# 📚 Django Library - Basic Training 1

Proyecto de aprendizaje de Django enfocado en **Admin First** sin necesidad de crear vistas HTML personalizadas.

---

## 📋 Contenido del Proyecto

| Archivo | Descripción |
|---------|-------------|
| **RECREAR_PROYECTO.md** | Guía paso a paso para recrear el proyecto desde cero |
| **USAR_APLICACION.md** | Cómo usar la aplicación una vez recreada (con diagramas Mermaid) |
| **MODELO_ER.md** | Diagrama ER completo del modelo relacional |
| **README.md** | Este archivo |
| **manage.py** | Script principal de Django |
| **library_demo/** | Carpeta del proyecto Django |
| **library/** | Carpeta de la aplicación |

---

## 🎯 ¿Qué es este proyecto?

Un sistema de **gestión de biblioteca** basado en Django con:
- 📚 **Catálogo de libros** (Authors, Books)
- 👥 **Registro de miembros**
- 📅 **Sistema de préstamos** (Loans)
- 🎛️ **Panel administrativo** (Django Admin)

---

## 🚀 Requisitos

- **Python 3.8+**
- **Django 4.2.0**
- **VS Code** (recomendado para mejor experiencia)

---

## 📦 Extensión de VS Code Requerida

Para visualizar correctamente los **diagramas Mermaid** en los archivos `.md`, instala:

#### 🔧 Instalación Rápida

**Opción 1: Desde VS Code**
1. Abre VS Code
2. Ve a **Extensions** (Ctrl+Shift+X)
3. Busca: `markdown-mermaid`
4. Haz click en **Install** (publisher: bierner)

#### ✅ Verificar Instalación

- Abre cualquier archivo `.md`
- Si ves diagramas Mermaid con colores y formas, ¡está correctamente instalado! ✨
- Si ves solo código, necesitas instalar la extensión

---

## 📚 Uso de la Documentación

### 1️⃣ **RECREAR_PROYECTO.md**
Sigue esta guía si quieres **crear el proyecto desde cero**.

```bash
# Pasos rápidos:
mkdir django-library
cd django-library
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install Django==4.2.0
django-admin startproject library_demo .
python manage.py startapp library
# ... (ver archivo para más pasos)
```

### 2️⃣ **USAR_APLICACION.md**
Aprende a usar el panel administrativo una vez creado.

**Incluye diagramas para:**
- 🎯 Flujo general de la aplicación
- 📚 Cómo crear autores, libros, miembros
- 📅 Ciclo de vida de préstamos
- 🔍 Búsqueda y filtrado
- 📊 Casos de uso realistas

### 3️⃣ **MODELO_ER.md**
Diagrama entidad-relación del proyecto con explicación detallada.

**Incluye:**
- 📊 Diagrama ER formal en Mermaid
- 📋 Descripción de cada tabla y campos
- 🔗 Relaciones y cardinalidad (1:N)
- 🔐 Restricciones de integridad (PROTECT, CASCADE)
- 💾 Mapeo a SQL SQLite
- 📝 Datos de ejemplo

---

## 📖 Orden de Lectura Recomendado

```
1. Leer este README.md ← Estás aquí
     ↓
2. Leer MODELO_ER.md ← Entender la estructura
     ↓
3. Seguir RECREAR_PROYECTO.md ← Crear el proyecto
     ↓
4. Consultar USAR_APLICACION.md ← Aprender a usarlo
```

---

## 🎛️ Acceso al Panel Admin

Una vez el proyecto esté ejecutándose:

```bash
python manage.py runserver
```

**URL:** `http://localhost:8000/admin/`

**Credenciales por defecto:**
- **Username:** `admin`
- **Password:** `admin123`

---

## 📊 Estructura de Datos

### Tablas del Sistema

```
Author (Autor)
├── id (PK)
├── name
├── country (optional)
└── created_at

Book (Libro)
├── id (PK)
├── title
├── isbn (UNIQUE)
├── author_id (FK → Author)
├── status (AVAILABLE | LOANED | LOST)
└── created_at

Member (Miembro)
├── id (PK)
├── full_name
├── email (UNIQUE)
└── joined_at

Loan (Préstamo)
├── id (PK)
├── book_id (FK → Book)
├── member_id (FK → Member)
├── loan_date
├── due_date
└── return_date (nullable)
```

---

## 🔗 Relaciones

| De | A | Tipo | Comportamiento |
|----|---|------|-----------------|
| **Author** | Book | 1:N | PROTECT (no eliminar autor con libros) |
| **Book** | Loan | 1:N | PROTECT (no eliminar libro con préstamos) |
| **Member** | Loan | 1:N | CASCADE (eliminar miembro → elimina préstamos) |

---

## 💡 Flujo de Trabajo Típico

```
1. Crear Autores
    ↓
2. Crear Libros (asignar autores)
    ↓
3. Registrar Miembros
    ↓
4. Crear Préstamos (libro + miembro + fecha)
    ↓
5. Editar préstamo cuando se devuelve el libro
    ↓
6. Generar reportes buscando/filtrando datos
```

---

## 🎓 Conceptos Aprendidos

- ✅ Estructura de proyecto Django
- ✅ Creación de modelos relacionales
- ✅ Uso del Django Admin
- ✅ Foreign Keys y relaciones 1:N
- ✅ Búsqueda y filtrado en admin
- ✅ Migraciones de BD

---

## 🔗 Enlaces Útiles

| Recurso | Enlace |
|---------|--------|
| Documentación Django | https://docs.djangoproject.com/ |
| Django Admin | https://docs.djangoproject.com/en/4.2/ref/contrib/admin/ |
| Mermaid Diagrams | https://mermaid.js.org/ |
| VS Code Extensions | https://marketplace.visualstudio.com/ |

---

## 📞 Soporte

Si tienes problemas:

1. **Verifica la extensión Mermaid** esté instalada
2. **Lee RECREAR_PROYECTO.md** si hay errores de setup
3. **Revisa USAR_APLICACION.md** para usar la app
4. **Consulta Django docs** para preguntas avanzadas

---

## ✨ ¡Listo para Aprender!

Comienza con **RECREAR_PROYECTO.md** y luego explora **USAR_APLICACION.md**. 🚀
