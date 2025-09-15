#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
import traceback
import sys

# Función para emitir sonido (puedes reemplazar esto con tu lógica de emisión de sonido)
def emit_sound(expression_result):
    print(f"Emitiendo sonido para: {expression_result}")

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección IP del servidor (localhost)
PORT = 65432        # Puerto para la comunicación

def main():
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reutilizar el puerto
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Servidor escuchando en {HOST}:{PORT}...")

            while True:
                try:
                    # Esperar una conexión
                    client_socket, client_address = server_socket.accept()
                    with client_socket:
                        print(f"Conexión establecida desde {client_address}")
                        while True:
                            try:
                                # Recibir datos del cliente
                                data = client_socket.recv(1024).decode('utf-8')
                                if not data:
                                    break  # Si no hay más datos, salir del loop

                                print(f"Expresión recibida: {data}")

                                # Evaluar la expresión
                                try:
                                    result = eval(data)  # Evalúa la expresión
                                    emit_sound(result)   # Emitir sonido basado en el resultado
                                    response = f"Resultado: {result}"
                                except Exception as e:
                                    error_message = f"Error al evaluar la expresión: {str(e)}"
                                    print("Expresión no válida.")
                                    traceback.print_exc()  # Muestra el error en la consola del servidor
                                    response = error_message

                                # Enviar respuesta al cliente
                                client_socket.sendall(response.encode('utf-8'))

                            except ConnectionResetError:
                                print("Cliente desconectado abruptamente.")
                                break
                            except Exception as e:
                                # Manejo de errores inesperados
                                error_message = f"Sucedió algo inesperado: {str(e)}"
                                print(error_message)
                                traceback.print_exc()
                                client_socket.sendall(error_message.encode('utf-8'))

                except KeyboardInterrupt:
                    # Manejar Ctrl+C durante la espera de conexiones
                    print("\nInterrupción detectada. Cerrando el servidor...")
                    break

    except KeyboardInterrupt:
        # Manejar Ctrl+C al inicio del programa
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        # Manejo de errores inesperados
        print(f"Error inesperado: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
