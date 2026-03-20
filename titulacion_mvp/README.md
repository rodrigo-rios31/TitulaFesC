# TitulaYA — Validador de Carpeta de Titulación

MVP completo con FastAPI + SQLite + Frontend SPA incluido.

---

## 🗂 Estructura del proyecto

```
titulacion_mvp/
├── main.py                          # Punto de entrada
├── requirements.txt
├── backend/
│   ├── app.py                       # FastAPI app + startup
│   ├── database.py                  # Modelos SQLAlchemy + SQLite
│   ├── controllers/                 # (disponible para lógica futura de controladores)
│   ├── services/
│   │   ├── auth_service.py          # Registro, login, JWT
│   │   └── carpeta_service.py       # Lógica del checklist
│   ├── repository/
│   │   ├── user_repository.py       # CRUD usuarios
│   │   ├── catalog_repository.py    # Carreras, opciones, requisitos
│   │   └── carpeta_repository.py    # Carpeta, documentos, historial
│   ├── routers/
│   │   ├── auth_router.py           # POST /api/auth/login|register
│   │   ├── catalog_router.py        # GET /api/catalogo/...
│   │   └── carpeta_router.py        # GET/POST/PATCH /api/carpeta/...
│   ├── utils/
│   │   ├── config.py                # Settings (JWT secret, etc.)
│   │   ├── security.py              # Hash, JWT, dependencia auth
│   │   └── seed.py                  # Datos iniciales de carreras
│   └── static/
│       └── index.html               # Frontend SPA completo
└── uploads/                         # Archivos subidos por alumnos (auto-creado)
```

---

## 🚀 Instalación y ejecución

### 1. Instalar dependencias

```bash
cd titulacion_mvp
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
python main.py
```

O directamente con uvicorn:

```bash
uvicorn backend.app:app --reload
```

### 3. Abrir en el navegador

```
http://localhost:8000        → Frontend SPA
http://localhost:8000/docs   → Swagger UI (API interactiva)
```

Al iniciar por primera vez, la DB se crea automáticamente y se pobla con:
- 3 carreras: Ingeniería Industrial, Ingeniería en Computación, Administración
- 5 opciones de titulación con sus requisitos detallados

---

## 📡 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/register` | Registro de alumno |
| POST | `/api/auth/login` | Login → JWT |
| GET | `/api/catalogo/carreras` | Listar carreras |
| GET | `/api/catalogo/carreras/{id}/opciones` | Opciones de una carrera |
| POST | `/api/carpeta/iniciar` | Crear carpeta con checklist |
| GET | `/api/carpeta/resumen` | Resumen del progreso |
| PATCH | `/api/carpeta/documento/marcar` | Marcar doc como completo/pendiente |
| POST | `/api/carpeta/documento/subir` | Subir archivo (PDF, JPG, PNG, DOCX, ZIP) |
| GET | `/api/carpeta/historial` | Historial de cambios |

---

## ✨ Mejoras incluidas vs el documento original

| Feature | Documento original | Este MVP |
|---|---|---|
| Instrucciones por requisito | ❌ | ✅ Guía detallada por documento |
| Historial de actividad | ❌ | ✅ Log completo de cambios |
| Validación de tipo de archivo | ❌ | ✅ Whitelist de extensiones |
| Requisitos opcionales | ❌ | ✅ Badge "Opcional" + no bloquea entrega |
| Carpeta persistente por sesión | Básico | ✅ Guarada con usuario, reanudable |
| Quick-toggle en checklist | ❌ | ✅ Click en círculo = marcar/desmarcar |
| Progreso en % visual | Básico | ✅ Barra animada + contador |
| Documentos con notas | ❌ | ✅ Campo de notas por documento |

---

## 🔧 Personalización

### Agregar más carreras o requisitos
Edita `backend/utils/seed.py` → estructura `SEED_DATA`. Borra `titulacion.db` y reinicia para re-sembrar.

### Cambiar el secreto JWT
En `backend/utils/config.py` o crea un archivo `.env`:
```
SECRET_KEY=mi-clave-super-segura
```

### Cambiar tiempo de sesión
`ACCESS_TOKEN_EXPIRE_MINUTES` en `config.py` (default: 8 horas).
