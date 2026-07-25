# 🚀 GUÍA COMPLETA DE DESPLIEGUE - FastAPI en CloudingHosting (cPanel)

## 📋 RESUMEN DE LA ARQUITECTURA

```
Usuario → administromicondominio.com/semi/
         ↓
Laravel (public_html/public/) 
         ↓ .htaccess + PHP Proxy (semi-proxy.php)
         ↓
FastAPI (cPanel Python App - Puerto asignado, ej: 8555)
         ↓
PostgreSQL (localhost:5432 - CloudingHosting)
```

**La app FastAPI NO se modifica** - sigue sirviendo en `/`
El proxy PHP en Laravel maneja el prefijo `/semi/`

---

## 📦 ARCHIVOS CREADOS PARA EL DESPLIEGUE

| Archivo | Destino en Servidor | Descripción |
|---------|---------------------|-------------|
| `passenger_wsgi.py` | Raíz app FastAPI | Entry point Passenger ASGI |
| `passenger_wsgi.ini` | Raíz app FastAPI | Configuración Passenger |
| `.env.production` | → `.env` en servidor | Variables de entorno producción |
| `semi-proxy.php` | Laravel `public/` | Proxy PHP /semi → FastAPI |
| `htaccess-for-laravel-public.txt` | Laravel `public/.htaccess` | Reglas rewrite para proxy |

---

## 🗄️ PASO 1: CREAR BASE DE DATOS POSTGRESQL EN CPANEL

1. **cPanel → Databases → PostgreSQL Databases**
2. **Crear base de datos:** `emk_db` (se crea como `usuario_emk_db`)
   - Nombre sugerido: `emk_db` → Resulta: `administ_emk_db`
3. **Crear usuario:** `adminprosql` (se crea como `usuario_adminprosql`)
   - Contraseña fuerte: `jean_9010jcBD%` (tu contraseña)
4. **Agregar usuario a BD:** Todos los privilegios (ALL PRIVILEGES)
5. **Anotar:**
   - Host: `localhost`
   - Puerto: `5432`
   - BD: `administ_emk_db`
   - Usuario: `administ_adminprosql`

---

## 🐍 PASO 2: CREAR PYTHON APP EN CPANEL

1. **cPanel → Software → Setup Python App**
2. **Create Application:**
   ```
   Python version: 3.11 (o superior disponible)
   Application root: estadistica-maranatha-infantil-fastapi
   Application URL: (dejar vacío - NO poner /semi aquí)
   Application startup file: passenger_wsgi.py
   Passenger log file: passenger.log
   ```
3. **Create** → Esperar a que se cree el entorno virtual
4. **Anotar el puerto asignado** (ej: `8555`) - aparece en la interfaz
5. **Environment Variables** → Agregar TODAS desde `.env.production`:
   ```
   DATABASE_URL=postgresql+pg8000://administ_adminprosql:jean_9010jcBD%25@localhost:5432/administ_emk_db
   DB_USER=administ_adminprosql
   DB_PASS=jean_9010jcBD%
   DB_NAME=administ_emk_db
   DB_HOST=localhost
   DB_PORT=5432
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=465
   SMTP_EMAIL=jeansiervodedios@gmail.com
   SMTP_PASSWORD=lmnvdsuiulbewuvp
   ENV=production
   RESET_ALEMBIC=false
   ```
6. **Save** → **Restart** app

---

## 📁 PASO 3: SUBIR CÓDIGO AL SERVIDOR

### Opción A: Git (Recomendado)
```bash
# En servidor via SSH
cd ~/estadistica-maranatha-infantil-fastapi
git clone https://github.com/TU_USUARIO/TU_REPO.git .
```

### Opción B: File Manager / FTP
1. Comprimir local → Subir → Descomprimir
2. **Excluir:** `.git/`, `venv/`, `__pycache__/`, `models/app.db`, `.env` local

### Estructura final en servidor:
```
/home/usuario/estadistica-maranatha-infantil-fastapi/
├── main_web.py
├── passenger_wsgi.py
├── passenger_wsgi.ini
├── .env                    ← Copia de .env.production
├── requirements.txt
├── alembic.ini
├── models/
├── controllers/
├── web/
├── utils/
├── config/
├── alembic/
└── scripts/
```

---

## ⚙️ PASO 4: INSTALAR DEPENDENCIAS Y MIGRAR BD

### Via SSH (Recomendado):
```bash
cd ~/estadistica-maranatha-infantil-fastapi

# Activar entorno virtual de cPanel
source ~/virtualenv/estadistica-maranatha-infantil-fastapi/3.11/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar conexión BD
python -c "
from models.database import engine
with engine.connect() as conn:
    print('✅ Conexión BD OK:', conn.execute('SELECT version()').scalar())
"

# Ejecutar migraciones Alembic
alembic upgrade head

# Verificar tablas creadas
python -c "
from models.database import SessionLocal
from models.security import Usuario, Rol
db = SessionLocal()
print('Usuarios:', db.query(Usuario).count())
print('Roles:', db.query(Rol).count())
db.close()
"
```

### Si NO tienes SSH - Via cPanel Terminal:
Mismos comandos en **cPanel → Advanced → Terminal**

---

## 🌐 PASO 5: CONFIGURAR LARAVEL (PROXY /semi)

### 5.1 Copiar archivos a Laravel public/
```bash
# En tu proyecto Laravel LOCAL
cp semi-proxy.php /ruta/a/tu/laravel/public/
# Editar semi-proxy.php línea 8: FASTAPI_PORT = puerto real de cPanel (ej: 8555)
```

### 5.2 Actualizar .htaccess en Laravel public/
```bash
# Reemplazar /ruta/a/tu/laravel/public/.htaccess con contenido de htaccess-for-laravel-public.txt
```

**Contenido final .htaccess Laravel:**
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    # Proxy /semi/* → FastAPI
    RewriteRule ^semi(.*)$ /semi-proxy.php$1 [L,QSA]
    # Rutas normales Laravel
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^ index.php [L]
</IfModule>
```

### 5.3 Subir cambios a producción
```bash
# En servidor
cd ~/public_html  # o donde esté tu Laravel
# Subir semi-proxy.php y .htaccess actualizado
```

---

## ✅ PASO 6: VERIFICACIÓN Y PRUEBAS

### 6.1 Verificar FastAPI directa (puerto interno)
```bash
# En servidor SSH
curl -H "Host: localhost" http://127.0.0.1:8555/dashboard
# Debe responder HTML (redirect a login si no hay sesión)
```

### 6.2 Verificar via dominio público
```
https://administromicondominio.com/semi/
→ Debe mostrar página de login FastAPI

https://administromicondominio.com/semi/dashboard
→ Debe redirigir a /semi/login
```

### 6.3 Probar login completo
1. Acceder a `https://administromicondominio.com/semi/login`
2. Ingresar credenciales
3. Debe redirigir a `/semi/dashboard`
4. Navegar por módulos (Áreas, Salones, Donaciones, etc.)

### 6.4 Verificar logs si hay errores
```bash
# Logs Passenger
tail -f ~/estadistica-maranatha-infantil-fastapi/passenger.log

# Logs Laravel
tail -f ~/public_html/storage/logs/laravel.log

# Logs PHP proxy (error_log de Apache)
tail -f /home/usuario/logs/error_log
```

---

## 🔧 PASO 7: CONFIGURACIONES ADICIONALES

### 7.1 Primera migración (BD vacía)
Si la BD está vacía, **una sola vez**:
```bash
# En cPanel Python App → Environment Variables
RESET_ALEMBIC=true
# Save → Restart
# Verificar en logs: "stamp head" completado
# Luego volver a RESET_ALEMBIC=false
```

### 7.2 Certificado SSL (HTTPS)
- cPanel → SSL/TLS → Let's Encrypt → Install
- Fuerza HTTPS en Laravel `.htaccess`

### 7.3 Optimizaciones opcionales
```bash
# En passenger_wsgi.ini para plan Starter
min_instances = 1
max_instances = 1  # Ahorra memoria
```

---

## 🛑 SOBRE "AUTO-STOP" AL CERRAR VENTANA

**NO ES POSIBLE en hosting compartido cPanel.**

| Lo que sí puedes hacer | Lo que NO es posible |
|------------------------|----------------------|
| Detener/Iniciar manual en cPanel Python App | Que se detenga solo al cerrar pestaña |
| Programar cron para parar en horario nocturno | Detectar "usuario cerró ventana" |
| Usar pocos recursos en idle (~50-100MB RAM) | Proceso por sesión de usuario |

**Realidad:** La app corre como servicio persistente. En idle consume ~80-150MB RAM. En plan Starter (1-2GB RAM) no es problema.

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Error 502 Bad Gateway
```
Causa: FastAPI no responde en el puerto
Solución:
1. Verificar que Python App está "Running" en cPanel
2. Verificar puerto en semi-proxy.php coincide
3. Revisar passenger.log para errores de startup
4. Comprobar BD accesible: python -c "from models.database import engine; engine.connect()"
```

### Error 500 Internal Server Error
```
Causa: Excepción en código Python
Solución:
1. tail -f passenger.log
2. Verificar migraciones: alembic current
3. Verificar .env cargado correctamente
```

### Login no funciona / Cookies
```
Causa: Dominio/Path cookies con proxy
Solución: Verificar en main_web.py middleware
- Cookie path="/semi" si es necesario
- SameSite=Lax, Secure=True (HTTPS)
```

### Assets (CSS/JS) rotos en /semi
```
Causa: Rutas absolutas en templates
Solución: Los templates usan CDN (Tailwind, LineAwesome) → OK
Las imágenes en /images/ → Necesitan proxy o montar StaticFiles
```

---

## 📞 COMANDOS ÚTILES POST-DESPLIEGUE

```bash
# Reiniciar app FastAPI
# Opción 1: cPanel Python App → Restart
# Opción 2: SSH
touch ~/estadistica-maranatha-infantil-fastapi/tmp/restart.txt

# Ver logs en tiempo real
tail -f ~/estadistica-maranatha-infantil-fastapi/passenger.log

# Backup BD
pg_dump -h localhost -U administ_adminprosql administ_emk_db > backup_$(date +%Y%m%d).sql

# Restaurar BD
psql -h localhost -U administ_adminprosql administ_emk_db < backup_20240115.sql

# Actualizar código
cd ~/estadistica-maranatha-infantil-fastapi
git pull
source ~/virtualenv/.../bin/activate
pip install -r requirements.txt
alembic upgrade head
touch tmp/restart.txt
```

---

## ✅ CHECKLIST FINAL

- [ ] BD PostgreSQL creada en cPanel con usuario y permisos
- [ ] Python App creada en cPanel (3.11+, passenger_wsgi.py)
- [ ] Variables de entorno configuradas en cPanel Python App
- [ ] Código subido (Git o File Manager)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Migraciones ejecutadas (`alembic upgrade head`)
- [ ] `semi-proxy.php` en Laravel `public/` con puerto correcto
- [ ] `.htaccess` actualizado en Laravel `public/`
- [ ] SSL/HTTPS funcionando
- [ ] Login probado en `https://administromicondominio.com/semi/login`
- [ ] Navegación por módulos principal funciona
- [ ] Logs limpios sin errores críticos

---

## 📞 SOPORTE

Si algo falla:
1. **Revisar logs:** `passenger.log` + `laravel.log` + Apache `error_log`
2. **Verificar puertos:** `netstat -tlnp | grep 8555` (o tu puerto)
3. **Probar BD:** `psql -h localhost -U administ_adminprosql -d administ_emk_db -c "SELECT 1"`
4. **Reiniciar todo:** Python App Restart + Laravel cache clear

¡Tu app FastAPI estará corriendo en `https://administromicondominio.com/semi/`! 🎉