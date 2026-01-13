# 🔄 Django Library - Admin First Setup

**Tutorial conciso para recrear el proyecto desde cero**

---

## 🚀 Quick Start (10 minutos)

| Paso | Comando |
|------|---------|
| 1 | `mkdir django-library && cd django-library` |
| 2 | `python -m venv venv` |
| 3 | `.\venv\Scripts\Activate.ps1` |
| 4 | `pip install Django==4.2.0` |
| 5 | `django-admin startproject library_demo .` |
| 6 | `python manage.py startapp library` |
| 7 | Editar `library_demo/settings.py` (agregar `'library'`) |
| 8 | Escribir `library/models.py` |
| 9 | Escribir `library/admin.py` |
| 10 | `python manage.py makemigrations` |
| 11 | `python manage.py migrate` |
| 12 | `python manage.py createsuperuser` (admin/admin123) |
| 13 | `python manage.py runserver` → `http://localhost:8000/admin/` ✅ |

---

## 📋 Requisitos

- Python 3.8+ (`python --version`)
- pip (`pip --version`)

---

## ⚙️ Paso 7: settings.py

En `library_demo/settings.py`, agrega `'library'` en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library',  # ← Agregar
]
```

---

## 📊 Paso 8: models.py

**Estructura de datos:**

| Tabla | Campos | Relación |
|-------|--------|----------|
| **Author** | name, country, created_at | → Book (1:N) |
| **Book** | title, isbn (unique), author_id, status, created_at | ← Author |
| **Member** | full_name, email (unique), joined_at | → Loan (1:N) |
| **Loan** | book_id, member_id, loan_date, due_date, return_date | ← Book, Member |

**Copiar en `library/models.py`:**

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name if not self.country else f"{self.name} ({self.country})"

class Book(models.Model):
    STATUS_CHOICES = [('AVAILABLE', 'Available'), ('LOANED', 'Loaned'), ('LOST', 'Lost')]
    title = models.CharField(max_length=300)
    isbn = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['title']
    def __str__(self):
        return f"{self.title} by {self.author.name}"

class Member(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['full_name']
    def __str__(self):
        return self.full_name

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['-loan_date']
    def __str__(self):
        return f"{self.book.title} → {self.member.full_name}"
```

---

## 🎛️ Paso 9: admin.py

**Copiar en `library/admin.py`:**

```python
from django.contrib import admin
from .models import Author, Book, Member, Loan

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'created_at']
    search_fields = ['name']
    list_filter = ['country']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'status']
    search_fields = ['title', 'isbn']
    list_filter = ['status', 'author']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'joined_at']
    search_fields = ['full_name', 'email']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'loan_date', 'due_date', 'return_date']
    search_fields = ['book__title', 'member__full_name']
    list_filter = ['loan_date']
```

---

## 🎯 Referencia Rápida

| Comando | Función |
|---------|---------|
| `python manage.py makemigrations` | Generar migraciones |
| `python manage.py migrate` | Aplicar a BD |
| `python manage.py createsuperuser` | Crear admin |
| `python manage.py runserver` | Iniciar servidor |
| `python manage.py shell` | Consola Django |

---

## 🔧 Errores Comunes

| Error | Solución |
|-------|----------|
| "No module named 'django'" | `pip install Django==4.2.0` |
| "'library' not in INSTALLED_APPS" | Editar `settings.py` |
| "OperationalError" | `python manage.py migrate` |
| "Puerto 8000 en uso" | `python manage.py runserver 8001` |

---

✅ **¡Proyecto creado!** Accede a `http://localhost:8000/admin/`
