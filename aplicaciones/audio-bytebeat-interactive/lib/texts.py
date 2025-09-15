from lib.config import (
    REPL_NAME, SERVER_NAME, VERSION,
    PREFIX_LEVEL_1, PREFIX_LEVEL_2,
    CMDS, CMDS_WORDS_MAX_LENGTH
    )
from lib.converters import *


SEPARATOR = '·'*60


def welcome(dat={}):
    """Función que muestra información inicial."""
    if dat['context'] == 'repl':
        name = REPL_NAME
    elif dat['context'] == 'server':
        name = SERVER_NAME

    data = f"{name}".split('\n')
    data.extend([
        f"    El generador de audio es: {dat['audio_generator']}",
         "    Escribe '??' y presiona 'Enter' para ver la ayuda.",
         "    Presiona 'Enter' con una expresión vacía para salir.\n"
    ])
    return info(data)


def bye(dat={}):
    """Función que muestra información de la sesión actual."""
    # TODO - incluir duración de session, fecha, etc
    duracion = seconds_to_texttime(dat["duration_session"])
    data = [
        f'La sesión duró {duracion}.',
         'Hasta luego! :D'
    ]
    return info(data)


def internal_help(context):
    """Función para mostrar la ayuda interna del REPL."""
    pad = CMDS_WORDS_MAX_LENGTH + 6
    _ = ' '
    t = []
    name = '¿?'
    if context == 'repl':
        name = REPL_NAME
    elif context == 'server':
        name = SERVER_NAME
    t.extend(f"{name}".split('\n'))
    t.append(f'{VERSION}')
    t.append(SEPARATOR)
    t1 = [
        '    + - * / %',
        '    << >> & | ^ ~',
        '    && || == != <= >= < >',
        '    dup swap put drop pick only',
        '',
        'Operadores de expresion solo disponible en modo "f"',
        'para expresiones de punto flotante:',
        '    sin cos tan',
        '    exp sqrt log pow',
        '    abs floor ceil',
        '    pi e inf nan',
        '',
        'Comandos especiales del repl:',
        f'{CMDS.comments:<{pad}} Las líneas que comienzan con "--" se consideran ',
        f'{_:<{pad}} como comentarios.',
        f'{CMDS.help:<{pad}} Muestra esta ayuda.',
        f'{CMDS.end_session_1:<{pad}} Finaliza la sesión. Funciona igual a introducir',
        f'{_:<{pad}} una expresión vacia y también a presionar Ctrl+C.',
    ]
    t.extend(t1)
    if context == 'repl':
        t.append(f'{CMDS.clear_console:<{pad}} Limpia el contenido de la consola.')
    t2 = [
        '',
        f'<n> {CMDS.set_rate:<{pad-4}} Actualiza el sample-rate. <n> es un entero positivo.',
        f'<n> {CMDS.set_t:<{pad-4}} Actualiza al valor de "t". <n> es un entero positivo',
        f'{_:<{pad}} que representa al instante en microsegundos.',
        f'{CMDS.get_t:<{pad}} Devuelve el valor actual de t.',
        f'{CMDS.reset_visual:<{pad}} Reinicia el reproductor-visualizador.',
    ]

    t.extend(t2)
    if context == 'repl':
        t3 = [
            f'<m> {CMDS.compose_visual:<{pad-4}} Establece el modo de composición de la ventana',
            f'{_:<{pad}} del reproductor-visualizador. <m> puede ser:',
            f'{_:<{pad}}    HalfRight',
            f'{_:<{pad}}    HalfLeft',
            f'{_:<{pad}}    HalfTop',
            f'{_:<{pad}}    HalfBottom',
            f'{_:<{pad}}    QuarterTopRight',
            f'{_:<{pad}}    QuarterTopLeft',
            f'{_:<{pad}}    QuarterBottomRight',
            f'{_:<{pad}}    QuarterBottomLeft',
            ]
        t.extend(t3)
    t4 = [
        '',
        f'<f> {CMDS.save_session:<{pad-4}} <f> es un texto que será el nombre de la sesión que',
        f'{_:<{pad}} se grabarán las expresiones de la sesión actual.',
        f'<f> {CMDS.load_session:<{pad-4}} <f> es el nombre de una sesión previamente grabada',
        f'{_:<{pad}} que se cargará reemplazando a la actual.',
        f'{CMDS.play_session:<{pad}} Reproduce la sesión actual.',
        f'{CMDS.show_session:<{pad}} Muestra las expresiones de la sesión actual.',
        f'<f> {CMDS.show_session:<{pad-4}} Muestra las expresiones de la sesión con nombre <f>.',
        f'{CMDS.list_sessions:<{pad}} Lista los nombres de sesión almacenados.',
        f'{CMDS.empty_session:<{pad}} Vacia todas las expresiones cargadas en la sesión',
        f'{_:<{pad}} y reinicia el tiempo a 0.',
        f'[<n>] {CMDS.delete_session_item:<{pad-6}} Borra los items indicados de la sesión actual.',
        f'[<n>] {CMDS.preserve_session_item:<{pad-6}} Preserva los items indicados de la sesión actual.',
        f'<n> {CMDS.set_speed:<{pad-4}} Establece la velocidad de reproducción de las sesiones.',
        '',
        f'{CMDS.dev_test:<{pad}} Llama a una acción para testeos de desarrollo.',
        SEPARATOR
    ]

    t.extend(t4)
    return info(t)


def select_mode(name):
    data = []
    if name == 'repl':
        data.extend(f"{REPL_NAME}".split('\n'))
    elif name == 'server':
        data.extend(f"{SERVER_NAME}".split('\n'))
    data.extend([
        f'{VERSION}',
        SEPARATOR,
        "Modos numéricos del generador de audio:",
        "   i <-- números enteros.",
        "   f <-- números decimales."
    ])
    return info(data)


def error(text):
    """Función que muestra los errores."""
    text = str(text).rstrip('.')
    return f'  \_(·_·)_/  {text}.'


def info(data, level=1):
    prefix = { 1: PREFIX_LEVEL_1, 2: PREFIX_LEVEL_2 }
    if type(data) == str:
        result = f'{prefix[level]} {data}'
    elif type(data) == list:
        r_list = []
        for text in data:
            r_list.append(f'{prefix[level]} {text}')
        result = '\n'.join(r_list)
    return result
