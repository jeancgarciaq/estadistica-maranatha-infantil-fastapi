import sys
import os

# Añadir la raíz del proyecto al path para resolver las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import configure_database, SessionLocal, shutdown_db
from controllers.servidor_controller import ServidorController
from controllers.usuarios_controller import UsuariosController
from models.security import ROLE_ADMIN, ROLE_MAESTRO, Usuario

def run_test():
    print("=== Iniciando Pruebas Locales del Modelo Servidores ===")
    
    # 1. Asegurar que la base de datos esté configurada y las tablas existan
    configure_database()
    db = SessionLocal()
    
    try:
        # 2. Verificar Lógica de Permisos
        print("\n[1] Verificando Lógica de Acceso...")
        # Obtenemos el usuario root (creado por el seed inicial)
        root = db.query(Usuario).filter(Usuario.username == 'root').first()
        
        # Simulamos objetos de usuario para verificar permisos sin necesidad de login real
        admin_user = type('User', (), {'rol': type('Rol', (), {'nombre': ROLE_ADMIN, 'permisos': [type('P', (), {'codigo': 'servidores.view'})]})})()
        maestro_user = type('User', (), {'rol': type('Rol', (), {'nombre': ROLE_MAESTRO, 'permisos': []})})()

        can_root = UsuariosController.usuario_tiene_permiso(root, 'servidores.view')
        can_admin = UsuariosController.usuario_tiene_permiso(admin_user, 'servidores.view')
        can_maestro = UsuariosController.usuario_tiene_permiso(maestro_user, 'servidores.view')

        print(f" - Root tiene acceso: {'✅' if can_root else '❌'}")
        print(f" - Administrador tiene acceso: {'✅' if can_admin else '❌'}")
        print(f" - Maestro tiene acceso (debe ser False): {'✅' if can_maestro else '❌'}")

        if not (can_root and can_admin) or can_maestro:
            print("\n⚠️ ALERTA: La lógica de permisos no cumple con los requerimientos.")
        else:
            print("\n✅ Configuración de seguridad validada correctamente.")

        # 3. Probar CRUD
        print("\n[2] Probando Operaciones CRUD...")
        # Instanciamos el controlador sin pasarle la sesión 'db' externa.
        # Esto permite que el controlador abra y cierre sus propias transacciones de forma aislada.
        controller = ServidorController()
        
        datos_nuevo = {
            "nombre": "Prueba Servidor",
            "edad": 25,
            "cedula": 99999999,
            "celular": "123456789",
            "correo": "test@iglesia.com",
            "numero_equipo": 1,
            "area_servicio": "Pruebas",
            "capitan": "Capitán Test"
        }

        # Operación: Crear
        exito, msg = controller.crear_servidor(datos_nuevo)
        print(f" - Creación: {msg}")
        if not exito: return

        # Operación: Leer (Listar)
        servidores = controller.listar_servidores()
        servidor = next((s for s in servidores if s.cedula == 99999999), None)
        if servidor:
            print(f" - Lectura: Encontrado '{servidor.nombre}'")
            
            # Operación: Actualizar
            exito, msg = controller.actualizar_servidor(servidor.id, {"nombre": "Servidor Modificado"})
            print(f" - Actualización: {msg}")
            
            # Operación: Eliminar (Soft delete)
            exito, msg = controller.eliminar_servidor(servidor.id)
            print(f" - Eliminación: {msg}")
        else:
            print("❌ ERROR: No se pudo recuperar el registro creado.")

        print("\n=== Pruebas de backend completadas exitosamente ===")

    finally:
        db.close()
        shutdown_db()

if __name__ == "__main__":
    run_test()