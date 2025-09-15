import subprocess
from lib.config import(
    PLAYER_WINDOW_NAME, VERBOSE_MODE, FFPLAY_PROGRAM_BIN
    )


def start_visualizer(pipe_read, log_file, rate=8000, window_title=PLAYER_WINDOW_NAME):
    """Función para iniciar ffplay con una tubería persistente y redirigir logs."""
    # Abre el archivo de registro en modo append
    log = open(log_file, "a")
    visualizer_process = subprocess.Popen(
        [
         FFPLAY_PROGRAM_BIN,
         "-hide_banner", # oculta el banner informativo
         "-vn", # no muestra video, en este caso es innecesario el video
         "-f", "s16le",  # Formato de entrada: PCM 16-bit little-endian
         "-ar", str(rate),  # Frecuencia de muestreo
         "-ac", "1",  # Un canal de audio
         "-i", "-",  # Entrada desde stdin
         "-fflags", "nobuffer",  # Desactiva el búfer de precarga
         "-analyzeduration", "0",  # Minimiza el tiempo de análisis inicial
         "-autoexit",  # Termina automáticamente al finalizar la entrada
         "-af", "aresample=async=1:min_hard_comp=0.1",  # Ajusta el búfer de audio
         "-vf", "showwaves=s=1280x720:mode=line",  # Visualización del espectro
         #"-noborder", # borderless window
         #"-alwaysontop", # window always on top
         "-probesize", "32",  # Reduce el tamaño de los datos iniciales analizados
         "-sync", "audio",  # Usa el reloj externo para sincronización
         "-max_delay", "1",  # Reduce el retraso máximo permitido
         "-window_title", window_title,  # Asigna un título único a la ventana
        ],
        stdin=pipe_read,
        stdout=log,  # Redirige stdout al archivo de registro
        stderr=subprocess.STDOUT  # Redirige stderr al mismo archivo
    )
    return visualizer_process, log

def restart_visualizer(visualizer_process, pipe_read, log_file, log=None, rate=8000):
    """Función para reiniciar ffplay."""
    if visualizer_process and visualizer_process.poll() is None:
        if VERBOSE_MODE:
            print("Reiniciando FFPLAY...")
        visualizer_process.terminate()
        visualizer_process.wait()
        if log:
            log.close()  # Cierra el archivo de registro anterior
    return start_visualizer(pipe_read, log_file, rate)
