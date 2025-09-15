import os
import fcntl

def stop_processes(process, ffplay_process, pipe_read, pipe_write, log_file=None, log=None):
    """Función para detener procesos."""
    if process and process.poll() is None:  # Si el proceso aún está en ejecución
        process.terminate()
        process.wait()
    if ffplay_process and ffplay_process.poll() is None:  # Si ffplay aún está en ejecución
        ffplay_process.terminate()
        ffplay_process.wait()
    os.close(pipe_read)
    os.close(pipe_write)
    if log:
        log.close()

def force_stop_process(process):
    """Función para detener el proceso especificado."""
    if process:
        process.terminate()
        process.wait()


def flush_pipe(pipe_read):
    """Función para vaciar el pipe"""
    try:
        # Guarda los flags actuales del pipe
        flags = fcntl.fcntl(pipe_read, fcntl.F_GETFL)
        # Cambia el modo del pipe a no bloqueante
        fcntl.fcntl(pipe_read, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        # Lee todos los datos pendientes del pipe
        while True:
            try:
                data = os.read(pipe_read, 4096 * 10)
                if not data:
                    break
            except BlockingIOError:
                # Si no hay más datos disponibles, salir del bucle
                break
    finally:
        # Restaura los flags originales del pipe (modo bloqueante)
        fcntl.fcntl(pipe_read, fcntl.F_SETFL, flags)
