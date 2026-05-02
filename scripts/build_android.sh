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

LOG_DIR="tmp/build_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/buildozer_$(date +%Y%m%d_%H%M%S).log"

echo "Buildozer log: $LOG_FILE"

set +e
buildozer "$@" 2>&1 | tee "$LOG_FILE"
STATUS=${PIPESTATUS[0]}
set -e

if [[ $STATUS -ne 0 ]]; then
    echo "Buildozer fallo con codigo $STATUS. Revisa: $LOG_FILE" >&2
fi

exit "$STATUS"