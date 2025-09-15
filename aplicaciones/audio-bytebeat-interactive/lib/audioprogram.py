import os
import sys
import time
import subprocess
import threading
from lib.config import(
    AUDIO_PROGRAM_FOLDER, FILENAME_LAST_T,
    AbbError
    )


programas_disponibles = {
    'i': 'audio_rpn_i',
    'f': 'audio_rpn_f',
}

modos_disponibles = {
    'i': 'ai',
    'f': 'af',
}

def compile_audioprogram(modo):
    """Función para compilar el programa."""
    # make -C $(dirname $bin_folder) -s mode bb_modo=$program_mode
    program = programas_disponibles[modo]
    clave = modos_disponibles[modo]
    try:
        subprocess.run(
            ['make', '-C', AUDIO_PROGRAM_FOLDER, '-s', 'mode', f'bb_modo={clave}' ]
            , check=True)
    except subprocess.CalledProcessError as e:
        raise AbbError(f"ERROR: Compilación fallida del generador de audio: {e}")

def get_binpath_audioprogram(modo):
    """Devuelve la ruta al binario."""
    program = programas_disponibles[modo]
    path_bin = os.path.join(AUDIO_PROGRAM_FOLDER, f"bin/{program}")
    return path_bin


def read_last_t(filename=FILENAME_LAST_T):
    """Función para leer el último valor de t desde un archivo."""
    t = 0
    try:
        with open(filename, "r") as file:
            t = int(file.read().strip())
    except FileNotFoundError:
        raise AbbError("ERROR: El archivo de intercambio no existe")
    except ValueError:
        raise AbbError("ERROR: El archivo contiene un valor inválido para t")
    finally:
        return t

def run_audioprogram(program, expression, pipe_write, init_t=0):
    """Función para ejecutar el programa compilado y escribir en la tubería."""
    error_message = None

    def check_errors():
        """Verifica si hay errores inmediatamente."""
        nonlocal error_message
        error_output = process.stderr.readline().strip()
        if error_output:
            error_message = f"ERROR en la expresión: {error_output}"
            process.terminate()
            process.wait()

    process = subprocess.Popen(
        ['stdbuf', '-oL', program, expression, str(init_t)],
        stdout=pipe_write,
        stderr=subprocess.PIPE,
        text=True
    )

    # Inicia un hilo para verificar errores sin bloquear el REPL
    error_thread = threading.Thread(target=check_errors)
    error_thread.start()
    error_thread.join(timeout=0.1)

    if error_message:
        raise AbbError(error_message)
    return process
