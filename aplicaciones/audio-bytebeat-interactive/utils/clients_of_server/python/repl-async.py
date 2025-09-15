#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
import readline

HOST = '127.0.0.1'
PORT = 65432
PROMPT = ':: '

def help():
    print(f"Uso: {__file__}")
    print("Comandos especiales:")
    print("  exit        Salir del cliente.")
    print("  help        Mostrar esta ayuda.")


async def send_expression(expression):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    print(f"Enviando expresión: {expression}")
    writer.write(expression.encode('utf-8'))
    await writer.drain()

    # Recibir respuesta del servidor
    data = await reader.read(1024)
    response = data.decode('utf-8').strip()
    print(f"SERVER :: --->\n{response}")

    writer.close()
    await writer.wait_closed()

async def repl():
    help()
    while True:
        try:
            expression = input(PROMPT)
            if expression.lower() == 'exit':
                print("Saliendo...")
                break
            elif expression.lower() == 'help':
                help()
                continue

            await send_expression(expression)

            if expression.lower() == '..':
                print("Saliendo...")
                break
        except KeyboardInterrupt:
            print("Saliendo...")
            exit()

if __name__ == "__main__":
    try:
        asyncio.run(repl())
    except KeyboardInterrupt:
        print("\nCliente detenido por el usuario.")
