#!/usr/bin/env bash
set -euo pipefail

JAVA_17_HOME="/usr/lib/jvm/java-17-openjdk-amd64"

if [[ ! -x "$JAVA_17_HOME/bin/java" ]]; then
    echo "No se encontro Java 17 en $JAVA_17_HOME" >&2
    exit 1
fi

export JAVA_HOME="$JAVA_17_HOME"
export PATH="$JAVA_HOME/bin:$PATH"

if [[ $# -eq 0 ]]; then
    set -- -v android debug
fi

exec buildozer "$@"