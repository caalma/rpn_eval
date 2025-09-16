import os

class AbbError(Exception):
    """Excepción personalizada para errores propios de la aplicación."""
    pass

class Object:
    """Clase vacia."""
    pass

# Nombre la utilidad
REPL_NAME = 'REPL para generación y reproducción de audio estilo bytebeat,\nmediante expresiones RPN.'
SERVER_NAME = 'SERVER para generación y reproducción de audio estilo bytebeat,\nmediante expresiones RPN.'
VERSION = '0.0.1'

# Características de audio
AUDIO_SAMPLERATE = 8000
AUDIO_INITIAL_EXPRESSION = '0'

# Seteos de reproductor-visualizador
PLAYER_WINDOW_NAME = ":)"
PLAYER_WINDOW_SLEEP_FOR_POSITION = 0.2
PLAYER_WINDOW_COMPOSITION_TYPE = 'HalfBottom'

FILENAME_LAST_T = "/dev/shm/evalrpn_last_t"
FILENAME_PLAYER_LOG = "/tmp/abb_player_log.txt"
AUDIO_PROGRAM_FOLDER = '../../base/'
AUDIO_PROGRAM_COMPILE = False
SESSION_FOLDER = './sesiones_grabadas/'
SESSION_SPEED = 1.0

FFPLAY_PROGRAM_BIN = 'ffplay'
AUDPV_PROGRAM_BIN = '../../../audpv/bin/audpv'
PLAYER_VISUALIZER_SOFTWARE = 'audpv'


# Sesión
SESSION_AUTOSAVE = True

# Constantes útiles para desarrollo
VERBOSE_MODE = True
TEST_MODE = 1

# Prompt receptivo de expresiones y comandos
PROMPT = ':: '
PREFIX_LEVEL_1 = '--'
PREFIX_LEVEL_2 = '··'

# Nombres personalizables de comandos especiales
CMDS = Object()
CMDS.comments = '--'
CMDS.help = '??'
CMDS.end_session_1 = '..'
CMDS.end_session_2 = ''
CMDS.clear_console = 'cc'
CMDS.set_rate = 'set_rate'
CMDS.set_t = 'set_t'
CMDS.get_t = 'get_t'
CMDS.reset_visual = 'reset_v'
CMDS.compose_visual = 'compose_v'
CMDS.save_session = 'save_session'
CMDS.load_session = 'load_session'
CMDS.play_session = 'play_session'
CMDS.set_speed = 'set_speed'
CMDS.show_session = 'show_session'
CMDS.list_sessions = 'list_sessions'
CMDS.empty_session = 'empty_session'
CMDS.delete_session_item = 'delete_si'
CMDS.preserve_session_item = 'preserve_si'
CMDS.dev_test = '__'

CMDS_WORDS_MAX_LENGTH = max([len(v) for v in vars(CMDS).values()])


def clean_env():
    """Función para eliminar archivos temporales y logs. Preferentemente de la sesión previa."""
    if os.path.exists(FILENAME_LAST_T): os.remove(FILENAME_LAST_T)
    if os.path.exists(FILENAME_PLAYER_LOG): os.remove(FILENAME_PLAYER_LOG)
