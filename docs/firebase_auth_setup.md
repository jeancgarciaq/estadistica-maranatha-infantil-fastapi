# Firebase Auth + Roles (Kivy)

Este proyecto usa Firebase Auth para login por usuario, y Realtime Database para sincronizacion.

## Variables de entorno requeridas

- `FIREBASE_WEB_API_KEY`: API key del proyecto Firebase (web config).
- `FIREBASE_DATABASE_URL`: URL de Realtime Database.
- `FIREBASE_AUTH_EMAIL_DOMAIN` (opcional): si el login usa usuario sin `@`, se completa como `usuario@dominio`.

No se debe incluir `serviceAccount` ni secretos de administrador en la app cliente.

## Flujo implementado

1. Usuario inicia sesion en pantalla login.
2. `UsuariosController.autenticar` intenta Firebase Auth REST.
3. Si autentica, consulta `user_roles/{uid}` en Realtime Database.
4. Con ese rol se construye un usuario de ejecucion con permisos de la app.
5. En sincronizacion, se usa `idToken` del usuario actual.
6. Si el token expira, se refresca automaticamente con `refreshToken`.

## Estructura requerida en Realtime Database

Nodo `user_roles`:

```json
{
  "user_roles": {
    "UID_FIREBASE_1": {
      "role": "root",
      "active": true,
      "username": "root"
    },
    "UID_FIREBASE_2": {
      "role": "administrador",
      "active": true,
      "username": "secretaria"
    },
    "UID_FIREBASE_3": {
      "role": "maestro",
      "active": true,
      "username": "maestra_1"
    },
    "UID_FIREBASE_4": {
      "role": "distribuidor",
      "active": true,
      "username": "distribucion_1"
    }
  }
}
```

## Roles soportados

- `root`
- `administrador`
- `maestro`
- `distribuidor`

Los permisos se derivan de `models/security.py` (`DEFAULT_ROLE_PERMISSIONS`).

## Reglas Firebase

Publica estas reglas en Realtime Database:

- Archivo: `config/firebase_database.rules.json`

## Provisionamiento recomendado de usuarios

1. Crear usuario en Firebase Auth (correo + contrasena).
2. Copiar su UID.
3. Crear/actualizar `user_roles/{uid}` con `role`, `active`, `username`.
4. Probar login desde la app.

## Nota sobre fallback local

Si Firebase no esta configurado o falla, el controlador intenta autenticacion local SQLAlchemy como respaldo.

## Sincronizacion inicial de datos locales a Firebase

La app encola cambios nuevos en `sync_queue`, pero los registros que ya existian antes de activar Firebase no se suben solos.

Para migrar la data actual de SQLite hacia Realtime Database:

1. Asegura en tu `.env`:
  - `FIREBASE_DATABASE_URL`
  - `FIREBASE_WEB_API_KEY`
  - Una de estas opciones de autenticacion para bootstrap:
    - `FIREBASE_AUTH_TOKEN` (si usas token manual), o
    - `FIREBASE_BOOTSTRAP_EMAIL` + `FIREBASE_BOOTSTRAP_PASSWORD`, o
    - `FIREBASE_BOOTSTRAP_USERNAME` + `FIREBASE_BOOTSTRAP_PASSWORD` (usa `FIREBASE_AUTH_EMAIL_DOMAIN` si aplica)
2. Ejecuta:

```sh
python scratch/sync_local_to_firebase.py
```

Si quieres limitarlo temporalmente a unas colecciones, puedes pasar `--collections` manualmente.

Si aparece `Permission denied (401)`, normalmente significa:

- Usuario sin entrada en `user_roles/{uid}`
- Usuario con `active: false`
- Rol sin permisos para la coleccion solicitada (por ejemplo `usuarios` requiere `root` o `administrador`)

## Orden sugerido para subir la base completa

1. `areas`
2. `salones`
3. `aulas`
4. `donaciones`
5. `alimentos_preparados`
6. `alimento_preparado_componentes`
7. `ensenanza`
8. `logistica`
9. `otras_areas`
10. `recepciones`
11. `servidores`
12. `distribuciones`
13. `usuarios`
14. `roles`
15. `permisos`
