import asyncio
from lib.texts import info
from lib.abb_logic import AbbLogicManager


# Configuración inicial
audio_queue = None # Cola para comunicar el manejador de clientes con el hilo de audio
response_queue = None # Cola para comunicar el manejador de clientes con el hilo de respuestas
shutdown_event = None # Evento asíncrono de finalización


def interface_server_abb():
    try:
        asyncio.run(server_abb())
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")


async def server_abb():
    """Función que controla la lógica principal del ciclo para el SERVER."""

    # Crear la cola en el mismo bucle de eventos
    global audio_queue
    global shutdown_event
    global response_queue

    audio_queue = asyncio.Queue()
    response_queue = asyncio.Queue()
    shutdown_event = asyncio.Event()

    # Actualización de configuración
    config = {
        'interface': 'server',
        'txtout': print,
        'txtoutAsync': response_queue.put,
        'audioqueueAsync': audio_queue.get,
        'shutdownServer': shutdown_event.set
    }

    loop = AbbLogicManager()
    await loop.config(config)
    await loop.initialize()

    # Obtener el bucle de eventos actual
    loop_server = asyncio.get_event_loop()

    # Iniciar el hilo de audio en el mismo bucle
    audio_task = loop_server.create_task(loop.run())

    # Iniciar el servidor en el mismo bucle
    server = await asyncio.start_server(handle_client, '127.0.0.1', 65432)
    async with server:
        print(info(f"Servidor escuchando en 127.0.0.1:65432..."))
        # Esperar hasta que se active el evento de apagado
        await shutdown_event.wait()

    # Detener el hilo de audio cuando el servidor se apague
    await audio_queue.put(None)
    await audio_task



async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(info(f"Conexión establecida desde {client_address}"))

    try:
        while True:
            # Recibir datos del cliente
            data = await reader.read(1024)
            if not data:
                break  # Si no hay más datos, salir del loop

            expression = data.decode('utf-8').strip()
            print(info(f"Expresión recibida: {expression}"))

            # Colocar la expresión en la cola del hilo de audio
            await audio_queue.put(expression)

            # Enviar confirmación al cliente
            response = await response_queue.get()

            writer.write(response.encode('utf-8'))
            await writer.drain()

    except ConnectionResetError:
        print(info("Cliente desconectado abruptamente."))
    finally:
        print(info(f"Cerrando conexión con {client_address}"))
        writer.close()
        await writer.wait_closed()
