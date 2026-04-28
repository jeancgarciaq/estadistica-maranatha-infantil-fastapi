# Sistema Administrativo para el Área de Atención a Niños en la Iglesia

Este proyecto es una aplicación desarrollada en Python utilizando Kivy y SQLAlchemy para gestionar la asistencia y distribución de meriendas en el área de atención a niños dentro de una iglesia.

## Autor
**Jean Carlo Garcia**  
GitHub: [jeancgarciaq](https://github.com/jeancgarciaq)

## Tecnologías Utilizadas
- **Python** 3.13
- **Kivy** 2.3.1
- **SQLAlchemy** 2.0.38
- **SQLite** (Base de datos local)

## Características
- Control de asistencia de maestros y auxiliares por salón.
- Registro de la cantidad de niños atendidos por salón.
- Gestión de donaciones de meriendas.
- Registro de meriendas repartidas (a niños, maestros y auxiliares).
- Navegación intuitiva mediante Kivy con `ScreenManager`.
- Autenticación de usuarios con roles y permisos.
- Gestión de usuarios exclusiva para el rol `root`.

## Usuarios Iniciales
- Usuario root: `root`
- Contraseña root: `root123`
- Usuario administrador: `admin`
- Contraseña administrador: `admin123`

El usuario `root` es el único que puede acceder a la pantalla de gestión de usuarios para crear cuentas, cambiar contraseñas y asignar roles.

## Instalación
1. Clona este repositorio:
   ```sh
   git clone https://github.com/jeancgarciaq/New-Estadistica-Maranatha-Infantil-Kivy.git
   cd tu-repositorio
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate     # En Windows
   ```
3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
   *(Si el archivo `requirements.txt` no existe, instala manualmente Kivy y SQLAlchemy con `pip install kivy sqlalchemy`)*

## Ejecución del Proyecto
Para ejecutar la aplicación, usa el siguiente comando:
```sh
python app.py
```

## Contribuciones
Si deseas contribuir al desarrollo del proyecto, realiza un fork del repositorio, crea una nueva rama con tus cambios y envía un pull request.

---
© 2025 Jean Carlo Garcia. Todos los derechos reservados.

