#!/bin/bash

EXPRESSION="$1"
HOST="127.0.0.1"
PORT=65432

show_help() {
    echo "Uso: $0 <expresion>"
}

if [[ "$EXPRESSION" == "" ]]; then
    show_help
    exit 1
fi

RESPONSE=$(echo "$EXPRESSION" | nc -q 1 "$HOST" "$PORT" 2>/dev/null)

echo -e "Respuesta del servidor:\n$RESPONSE"
