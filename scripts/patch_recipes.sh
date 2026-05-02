#!/usr/bin/env bash
# Script post-download para parchear libffi y otros packages problemáticos
# Ejecutado por python-for-android si es posible

# Este script se puede activar agregando un hook en buildozer.spec
# o copiando la lógica en una receta custom de python-for-android

# Parche para libffi: remover -print-multi-os-directory
patch_libffi() {
    local libffi_dir="$1"
    local configure_file="$libffi_dir/configure"
    
    if [[ -f "$configure_file" ]]; then
        # Remover la opción -print-multi-os-directory de la detección de directorios
        sed -i 's/-print-multi-os-directory//g' "$configure_file" 2>/dev/null || true
        echo "[OK] Patcheado libffi configure"
    fi
}

# Usar: patch_libffi "/path/to/libffi"
