# 📖 Guía de Uso - Django Library Admin

Cómo usar la aplicación una vez recreada en el panel administrativo

---

## 🎯 Flujo General de Uso

```mermaid
graph TD
    A["🔐 Acceder a Admin<br/>localhost:8000/admin"] --> B["👤 Autenticar<br/>Usuario: admin<br/>Contraseña: admin123"]
    B --> C["📊 Panel Admin<br/>Authors | Books<br/>Members | Loans"]
    C --> D["➕ Crear Datos<br/>o<br/>📝 Editar Datos"]
    D --> E["✅ Guardar Cambios"]
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#c8e6c9
```

---

## 📚 Paso 1: Crear un Autor

```mermaid
graph LR
    A["1️⃣ Admin<br/>→ Authors"] --> B["➕ Add Author"]
    B --> C["Llenar Formulario<br/>name: string<br/>country: opcional"]
    C --> D["✅ Save"]
    D --> E["✔️ Autor Creado"]
    
    style E fill:#c8e6c9
```

**Datos a ingresar:**
- **Name:** Nombre del autor (ej: "J.K. Rowling")
- **Country:** País opcional (ej: "United Kingdom")

---

## 📖 Paso 2: Crear un Libro

```mermaid
graph LR
    A["1️⃣ Admin<br/>→ Books"] --> B["➕ Add Book"]
    B --> C["Llenar Formulario"]
    C --> D["Seleccionar Autor<br/>Dropdown"]
    D --> E["Seleccionar Status<br/>AVAILABLE"]
    E --> F["✅ Save"]
    F --> G["✔️ Libro Creado"]
    
    style G fill:#c8e6c9
```

**Datos a ingresar:**
- **Title:** Título del libro (ej: "Harry Potter")
- **ISBN:** Código único (ej: "9780747532699")
- **Author:** Seleccionar autor del dropdown
- **Status:** Seleccionar uno de:
  - `AVAILABLE` = Disponible para préstamo
  - `LOANED` = Actualmente prestado
  - `LOST` = Perdido

---

## 👥 Paso 3: Registrar un Miembro

```mermaid
graph LR
    A["1️⃣ Admin<br/>→ Members"] --> B["➕ Add Member"]
    B --> C["Llenar Formulario"]
    C --> D["Email Único<br/>No duplicados"]
    D --> E["✅ Save"]
    E --> F["✔️ Miembro Creado"]
    
    style F fill:#c8e6c9
```

**Datos a ingresar:**
- **Full Name:** Nombre completo (ej: "Juan Pérez")
- **Email:** Email único (ej: "juan@example.com")

---

## 📅 Paso 4: Crear un Préstamo

```mermaid
graph LR
    A["1️⃣ Admin<br/>→ Loans"] --> B["➕ Add Loan"]
    B --> C["Seleccionar Libro<br/>Dropdown"]
    C --> D["Seleccionar Miembro<br/>Dropdown"]
    D --> E["Ingresar Fecha Devolución<br/>14 días adelante"]
    E --> F["✅ Save"]
    F --> G["✔️ Préstamo Creado"]
    
    style G fill:#c8e6c9
```

**Datos a ingresar:**
- **Book:** Seleccionar libro disponible
- **Member:** Seleccionar miembro
- **Due Date:** Fecha de devolución esperada
- **Return Date:** Se rellena automáticamente cuando se devuelve

---

## 🔄 Ciclo de Vida de un Préstamo

```mermaid
graph TD
    A["📅 Préstamo Creado<br/>loan_date = HOY<br/>return_date = NULL"] -->|"Libro prestado"| B["🔄 Préstamo Activo<br/>Miembro tiene el libro"]
    B -->|"14 días después"| C["⚠️ Vencido?<br/>Hoy > due_date"]
    C -->|"Sí"| D["❌ Atrasado"]
    C -->|"No"| B
    B -->|"Devuelve libro"| E["✅ Marcado como Devuelto<br/>return_date = HOY"]
    E --> F["✔️ Préstamo Completado"]
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style D fill:#ffcdd2
    style E fill:#c8e6c9
    style F fill:#a5d6a7
```

---

## 📊 Estados de un Libro

```mermaid
graph TD
    A["📖 AVAILABLE<br/>(Disponible)<br/>Puede prestarse"] -->|"Se crea préstamo"| B["📖 LOANED<br/>(Prestado)<br/>En poder de miembro"]
    B -->|"Se devuelve"| A
    B -->|"Se pierde"| C["📖 LOST<br/>(Perdido)<br/>No se puede prestar"]
    A -->|"Se pierde"| C
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffcdd2
```

---

## 🔍 Búsqueda y Filtrado

```mermaid
graph LR
    A["📋 Tabla de Datos<br/>Authors | Books | Members | Loans"]
    A --> B["🔍 Search Bar<br/>Buscar por nombre<br/>título, email, etc"]
    A --> C["🏷️ Filtros<br/>Por status<br/>Por autor<br/>Por fecha"]
    B --> D["✅ Resultados Filtrados"]
    C --> D
    
    style D fill:#c8e6c9
```

**Ejemplos de búsqueda:**
- **Authors:** Buscar por nombre
- **Books:** Buscar por título o ISBN
- **Members:** Buscar por nombre o email
- **Loans:** Filtrar por fecha de préstamo

---

## ✏️ Editar Datos

```mermaid
graph LR
    A["📋 Lista de Datos"] --> B["Click en un Registro<br/>ej: 'Harry Potter'"]
    B --> C["📝 Formulario de Edición<br/>Cambiar campos"]
    C --> D["❌ Algunos campos<br/>son Read-Only<br/>created_at, joined_at, loan_date"]
    C --> E["✅ Save"]
    E --> F["✔️ Datos Actualizados"]
    
    style D fill:#fff3e0
    style F fill:#c8e6c9
```

**Campos Read-Only (No se pueden editar):**
- `created_at` (Autor, Libro)
- `joined_at` (Miembro)
- `loan_date` (Préstamo)

---

## 🗑️ Eliminar Datos

```mermaid
graph LR
    A["📋 Lista de Datos"] --> B["✅ Checkbox<br/>Seleccionar registros"]
    B --> C["⚠️ Delete Selected<br/>en dropdown"]
    C --> D["🚨 Confirmar Eliminación<br/>⚠️ IRREVERSIBLE"]
    D --> E["✔️ Registros Eliminados"]
    
    style D fill:#ffcdd2
    style E fill:#a5d6a7
```

**⚠️ Restricciones:**
- **No puedes eliminar un Author** si tiene libros (`on_delete=PROTECT`)
- **Si eliminas un Member**, se eliminan automáticamente sus préstamos (`on_delete=CASCADE`)
- **No puedes eliminar un Book** si tiene préstamos activos

---

## 🎯 Caso de Uso: Préstamo de Libro

```mermaid
graph TD
    A["👥 Cliente: Juan Pérez<br/>Quiere: Harry Potter"]
    A --> B["1️⃣ Admin → Authors<br/>Crear: J.K. Rowling"]
    B --> C["2️⃣ Admin → Books<br/>Crear: Harry Potter<br/>ISBN: 9780747532699<br/>Status: AVAILABLE"]
    C --> D["3️⃣ Admin → Members<br/>Crear: Juan Pérez<br/>Email: juan@example.com"]
    D --> E["4️⃣ Admin → Loans<br/>Crear Préstamo<br/>Book: Harry Potter<br/>Member: Juan Pérez<br/>Due Date: +14 días"]
    E --> F["✅ Préstamo Registrado"]
    F --> G["📚 Juan tiene el libro<br/>14 días para leer"]
    
    style F fill:#c8e6c9
    style G fill:#e1f5ff
```

---

## 📖 Caso de Uso: Devolución de Libro

```mermaid
graph TD
    A["📚 Juan devuelve Harry Potter<br/>después de 10 días"]
    A --> B["1️⃣ Admin → Loans<br/>Click en el préstamo"]
    B --> C["2️⃣ Formulario Edición<br/>Return Date: HOY"]
    C --> D["3️⃣ Guardar Cambios"]
    D --> E["✅ Préstamo Marcado<br/>como Devuelto"]
    E --> F["4️⃣ Admin → Books<br/>Verificar Status<br/>Harry Potter: AVAILABLE"]
    
    style E fill:#c8e6c9
    style F fill:#a5d6a7
```

---

## 🔎 Caso de Uso: Encontrar Libros Disponibles

```mermaid
graph LR
    A["Admin → Books"] --> B["🏷️ Filtro: Status<br/>Seleccionar: AVAILABLE"]
    B --> C["📋 Mostrar solo<br/>libros disponibles"]
    C --> D["👁️ Ver cuáles están<br/>listos para prestar"]
    
    style D fill:#c8e6c9
```

---

## 📊 Vista Rápida de Datos

| Sección | Qué ver | Acciones |
|---------|---------|----------|
| **Authors** | Lista de autores | ➕ Agregar, ✏️ Editar, 🗑️ Eliminar |
| **Books** | Todos los libros + estado | ➕ Agregar, ✏️ Editar, 🏷️ Filtrar por status |
| **Members** | Miembros registrados | ➕ Agregar, ✏️ Editar, 🗑️ Eliminar |
| **Loans** | Préstamos activos + completados | ➕ Agregar, ✏️ Editar (return_date), 🗑️ Eliminar |

---

## ⚡ Atajos Útiles

| Acción | Dónde |
|--------|-------|
| Ver todos los libros prestados | Books → Filtro: Status=LOANED |
| Ver libros perdidos | Books → Filtro: Status=LOST |
| Ver préstamos sin devolución | Loans → Filtro: Return Date = vacío |
| Buscar libros de un autor | Books → Search: nombre del autor |
| Ver todos los préstamos de un miembro | Loans → Search: nombre del miembro |

---

## 🎓 Ejercicio Práctico

**Objetivo:** Crear un sistema de préstamo funcional

1. ✅ Crear 3 autores diferentes
2. ✅ Crear 5 libros (variado de autores)
3. ✅ Registrar 3 miembros
4. ✅ Crear 4 préstamos (dejar 1 libro sin préstamo)
5. ✅ Marcar 1 préstamo como devuelto
6. ✅ Filtrar libros disponibles
7. ✅ Buscar préstamos de un miembro específico

---

## ✅ ¡Listo!

Ya sabes cómo usar el panel administrativo de Django Library. La aplicación es funcional para:
- 📚 Gestionar catálogo de libros
- 👥 Administrar miembros
- 📅 Registrar préstamos
- 🔍 Buscar y filtrar datos
