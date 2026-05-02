#!/usr/bin/env bash
# Wrapper para clang del NDK que remueve opciones no soportadas
# Específicamente: -print-multi-os-directory (no soportada por clang-14)

# Detectar cuál clang se pasó como argv[0]
CLANG_BASENAME="$(basename "$0")"

# Mapear clang-X -> clang-X real
case "$CLANG_BASENAME" in
    clang-14)
        CLANG_REAL="/home/codespace/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/clang-14"
        ;;
    clang)
        CLANG_REAL="/home/codespace/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/clang"
        ;;
    *)
        CLANG_REAL="/home/codespace/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/${CLANG_BASENAME}"
        ;;
esac

# Filtrar argumentos problemáticos
declare -a ARGS
skip_next=0
for arg in "$@"; do
    if [[ $skip_next -eq 1 ]]; then
        skip_next=0
        continue
    fi
    
    # Remover -print-multi-os-directory completamente
    if [[ "$arg" == "-print-multi-os-directory" ]]; then
        continue
    fi
    
    # Remover -print-file-name=libc.so si va sin valor
    if [[ "$arg" == "-print-file-name=libc.so" ]]; then
        continue
    fi
    
    ARGS+=("$arg")
done

# Ejecutar clang real con los argumentos filtrados
exec "$CLANG_REAL" "${ARGS[@]}"
