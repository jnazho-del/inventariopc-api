# TechParts Limitada - Sistema de Inventario y API RESTful

Sistema web y API RESTful desarrollado con **Django** y **Django REST Framework (DRF)**, integrado con base de datos **MySQL / MariaDB**. Permite la administración completa (CRUD) de repuestos y componentes de computadoras, gestión de imágenes, validaciones de datos y autenticación por Token y JWT.

---

## 🚀 Requisitos Previos

* **Python 3.10+**
* **MySQL / MariaDB** (ej. XAMPP en puerto 3306)
* **Postman o Bruno** (para pruebas de la API)

---

## 🛠️ Instalación y Puesta en Marcha

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Base de Datos en MySQL:**
   * Iniciar MySQL en XAMPP.
   * Crear la base de datos `inventariopc` en phpMyAdmin o consola MySQL:
     ```sql
     CREATE DATABASE inventariopc;
     ```
   * *(Opcional)* Importar el archivo `inventariopc.sql` desde phpMyAdmin para cargar los datos iniciales y el usuario de prueba.

3. **Ejecutar migraciones (si no importaste el archivo .sql):**
   ```bash
   python manage.py migrate
   ```

4. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   El servidor estará disponible en `http://127.0.0.1:8000/`.

---

## 📌 Endpoints de la API RESTful

La API se encuentra disponible bajo la ruta `/api/repuestos/`:

| Método | Endpoint | Descripción | Autenticación | Código HTTP |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/repuestos/` | Listar catálogo de repuestos | Pública | `200 OK` |
| **GET** | `/api/repuestos/{id}/` | Detalle de un repuesto | Pública | `200 OK` / `404` |
| **POST** | `/api/repuestos/` | Crear repuesto (JSON o Imagen) | Token / JWT | `201 Created` / `400` / `401` |
| **PUT** | `/api/repuestos/{id}/` | Actualizar repuesto completo | Token / JWT | `200 OK` / `400` / `401` |
| **PATCH**| `/api/repuestos/{id}/` | Actualización parcial (precio/stock)| Token / JWT | `200 OK` / `400` / `401` |
| **DELETE**| `/api/repuestos/{id}/` | Eliminar repuesto y borrar imagen| Token / JWT | `204 No Content` / `401` |
| **POST** | `/api/auth/token/` | Obtener Token DRF | Pública | `200 OK` |
| **POST** | `/api/auth/jwt/` | Obtener tokens JWT (Access/Refresh) | Pública | `200 OK` |

---

## 🧪 Pruebas con Postman o Bruno

El proyecto incluye el archivo **`TechParts_API.postman_collection.json`** listo para importar en Postman o Bruno:
* **01 - Autenticación y Usuarios:** Obtención de Tokens (usuario: `juan`, clave: `admin123`).
* **02 - CRUD Operaciones Exitosas:** Pruebas de listado, creación con JSON o imagen, actualización y eliminación.
* **03 - Casos de Error y Validaciones:** Pruebas de error `401 Unauthorized` (sin token) y `400 Bad Request` (precio o stock negativo).
