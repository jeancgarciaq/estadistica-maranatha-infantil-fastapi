# Sistema de Gestión de Estadísticas Maranatha Kids - Web v0.1

Este proyecto es una aplicación web robusta diseñada para gestionar la asistencia, logística y distribución de donaciones del área infantil de la iglesia. Evolucionado de una versión de escritorio a una arquitectura web escalable.

## Autor
**Jean Carlo Garcia**  
GitHub: [jeancgarciaq](https://github.com/jeancgarciaq)

## Tecnologías Utilizadas
- **Backend:** Python 3.11 + FastAPI
- **Base de Datos:** SQLAlchemy 2.0 (Compatible con SQLite y PostgreSQL)
- **Frontend:** Jinja2 Templates + Tailwind CSS (Diseño Mobile-First)
- **Contenerización:** Docker
- **Seguridad:** Passlib (Bcrypt) + Sistema de Roles Dinámicos
- **Reportes:** ReportLab (Generación de PDF con gráficos vectoriales)

## Características
- **Dashboard Informativo:** Resumen visual de la asistencia y estados.
- **Control de Asistencia:** Registro detallado por aula (niños, niñas y servidores).
- **Gestión de Inventario:** Control de donaciones, alimentos preparados y su distribución.
- **Reporte Estadístico:** Generación de informes en PDF con detección automática de salones cerrados y gráficos de asistencia.
- **Seguridad Avanzada:** 
    - Registro con validación anti-bot (Honeypot + Desafío matemático).
    - Recuperación de contraseña mediante tokens temporales.
    - Gestión de usuarios exclusiva para el superusuario (`root`).

## Usuarios Iniciales
- Usuario root: `root`
- Contraseña root: `root123`

*Nota: El usuario root es el único con permisos para acceder al Panel de Gestión de Usuarios (`/usuarios`).*

## Instalación y Despliegue con Docker

La forma recomendada de ejecutar la aplicación es mediante Docker para asegurar la compatibilidad de todas las dependencias.

### 1. Construir la imagen
Desde la raíz del proyecto:
```bash
docker build -t emi-web-app .
```

### 2. Ejecutar localmente
```bash
docker run -p 8000:8080 emi-web-app
```
La aplicación estará disponible en `http://localhost:8000`.

## Despliegue en la Nube (Google Cloud Run)

1. **Habilitar la conexión a Cloud SQL:**
   Al configurar el servicio en Cloud Run, asegúrate de añadir la instancia de Cloud SQL (`emk-db`) en la pestaña de "Conexiones".

2. **Configurar la variable DATABASE_URL:**
   Utiliza el formato de socket de Unix para mayor seguridad:
   `DATABASE_URL=postgresql+psycopg2://[USER]:[PASSWORD]@/[DB_NAME]?host=/cloudsql/[PROJECT_ID]:[REGION]:emk-db`

   *Nota: La aplicación creará automáticamente las tablas y el usuario root al iniciar por primera vez.*

3. **Etiquetar la imagen:**
   ```bash
   docker tag emi-web-app gcr.io/[PROJECT_ID]/emi-web-app:v0.1
   ```
4. **Subir al registro:**
   ```bash
   docker push gcr.io/[PROJECT_ID]/emi-web-app:v0.1
   ```
5. **Desplegar:**
   ```bash
   gcloud run deploy emi-web-app --image gcr.io/[PROJECT_ID]/emi-web-app:v0.1 --platform managed --port 8080
   ```

---
© 2025 Jean Carlo Garcia. Versión Web 0.1.

---
© 2025 Jean Carlo Garcia. Todos los derechos reservados.
