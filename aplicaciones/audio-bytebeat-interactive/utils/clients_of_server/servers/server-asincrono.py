#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio

# Función para emitir sonido (puedes reemplazar esto con tu lógica de emisión de sonido)
def emit_sound(expression_result):
    print(f"Emitiendo sonido para: {expression_result}")

async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f"Conexión establecida desde {client_address}")

    try:
        while True:
            # Recibir datos del cliente
            data = await reader.read(1024)
            if not data:
                break  # Si no hay más datos, salir del loop

            expression = data.decode('utf-8').strip()
            print(f"Expresión recibida: {expression}")

            # Evaluar la expresión
            try:
                result = eval(expression)  # Evalúa la expresión
                emit_sound(result)         # Emitir sonido basado en el resultado
                response = f"Resultado: {result}"
            except Exception as e:
                error_message = f"Error al evaluar la expresión: {str(e)}"
                print("Expresión no válida.")
                response = error_message

            # Enviar respuesta al cliente
            writer.write(response.encode('utf-8'))
            await writer.drain()

    except ConnectionResetError:
        print("Cliente desconectado abruptamente.")
    finally:
        print(f"Cerrando conexión con {client_address}")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 65432)
    async with server:
        print(f"Servidor escuchando en 127.0.0.1:65432...")
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
