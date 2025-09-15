#!/bin/bash

HOST="127.0.0.1"
PORT=65432

show_help() {
    echo "Uso: $0"
    echo "Comandos especiales:"
    echo "  exit - Salir del cliente."
    echo "  help - Mostrar esta ayuda."
}

show_help

while true; do
    # Solicitar entrada al usuario
    read -p "Ingrese una expresión a evaluar: " EXPRESSION

    # Comprobar si el usuario quiere salir
    if [[ "$EXPRESSION" == "exit" ]]; then
        echo "Cerrando cliente..."
        break
    elif [[ "$EXPRESSION" == "help" ]]; then
        show_help
        continue
    fi

    # Enviar la expresión al servidor usando netcat
    RESPONSE=$(echo "$EXPRESSION" | nc -q 1 "$HOST" "$PORT" 2>/dev/null)

    # Verificar si el servidor respondió
    if [[ $? -ne 0 ]]; then
        echo "Error: No se pudo conectar al servidor."
    else
        echo "Respuesta del servidor:\n$RESPONSE"
    fi
done
