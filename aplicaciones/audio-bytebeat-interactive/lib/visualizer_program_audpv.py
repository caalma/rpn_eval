import subprocess
from lib.config import(
    PLAYER_WINDOW_NAME, VERBOSE_MODE, AUDPV_PROGRAM_BIN
    )


def start_visualizer(pipe_read, log_file, rate=8000, window_title=PLAYER_WINDOW_NAME):
    """Función para iniciar AudPV con una tubería persistente y redirigir logs."""
    # Abre el archivo de registro en modo append
    log = open(log_file, "a")
    visualizer_process = subprocess.Popen(
        [
         AUDPV_PROGRAM_BIN,
         "-f", "s16le",  # Formato de entrada: PCM 16-bit little-endian
         "-r", str(rate),  # Frecuencia de muestreo
         "-c", "1",  # Un canal de audio
         "-v", "freqwalkfitlog",  # Tipo de visualización
         "-t", window_title,  # Asigna un título único a la ventana
        ],
        stdin=pipe_read,
        stdout=log,  # Redirige stdout al archivo de registro
        stderr=subprocess.STDOUT  # Redirige stderr al mismo archivo
    )
    return visualizer_process, log

def restart_visualizer(visualizer_process, pipe_read, log_file, log=None, rate=8000):
    """Función para reiniciar AudPV."""
    if visualizer_process and visualizer_process.poll() is None:
        if VERBOSE_MODE:
            print("Reiniciando AudPV...")
        visualizer_process.terminate()
        visualizer_process.wait()
        if log:
            log.close()  # Cierra el archivo de registro anterior
    return start_visualizer(pipe_read, log_file, rate)
