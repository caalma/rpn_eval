import os
import time
import readline
from datetime import datetime

from lib.config import(
    AUDIO_SAMPLERATE, AUDIO_INITIAL_EXPRESSION,
    REPL_NAME, VERSION, PLAYER_WINDOW_COMPOSITION_TYPE,
    PLAYER_WINDOW_SLEEP_FOR_POSITION, CMDS, PROMPT,
    FILENAME_PLAYER_LOG, VERBOSE_MODE, AUDIO_PROGRAM_COMPILE,
    SESSION_AUTOSAVE, SESSION_FOLDER, SESSION_SPEED,
    PLAYER_VISUALIZER_SOFTWARE, TEST_MODE,
    clean_env, AbbError
    )
from lib.audioprogram import(
    compile_audioprogram, get_binpath_audioprogram, run_audioprogram,  read_last_t
    )
from lib.windowcompose import(
    player_visualizer_compose, clear_screen,
    focus_window, get_activewindow_id
    )
from lib.sessionmanager import SessionManager
from lib.processmanager import(
    stop_processes, force_stop_process, flush_pipe
    )
from lib.visualizer_program_ffplay import start_visualizer as start_ffplay
from lib.visualizer_program_ffplay import restart_visualizer as restart_ffplay

from lib.visualizer_program_audpv import start_visualizer as start_audpv
from lib.visualizer_program_audpv import restart_visualizer as restart_audpv

#--- de uso seguro
from lib.texts import(
    welcome, bye, internal_help, select_mode, error, info
    )


class AbbLogicManager:

    def __init__(self):
        self.interface = None
        self.txtoutAsync = None
        self.txtout = None

    async def config(self, config={}):
        available_vars = ['interface', 'txtoutAsync', 'txtout', 'audioqueueAsync', 'shutdownServer']
        for k, v in config.items():
            if k in available_vars:
                setattr(self, k, v)


    async def initialize(self):
        self.current_player_window_composition_type = PLAYER_WINDOW_COMPOSITION_TYPE

        # Elección del visualizador/reproductor
        self.current_player_visualizer = PLAYER_VISUALIZER_SOFTWARE

        # Selección y compilación del generador de audio
        self._select_and_compile()

        # Crea una tubería para la comunicación entre el programa y el player-visualizer
        self.pipe_read, self.pipe_write = os.pipe()

        # Define el archivo de registro
        self.log_file = FILENAME_PLAYER_LOG

        # Inicia el player-visualizer con la tubería y el archivo de registro
        self.pv_process, self.log = self._start_pv()(self.pipe_read, self.log_file)

        # Inicializa varaibles necesarias
        self.current_process = None
        self.expression = None
        self.expression_normal = None
        self.previous_expression = AUDIO_INITIAL_EXPRESSION
        self.current_rate = AUDIO_SAMPLERATE
        self.current_speed = SESSION_SPEED
        self.current_t = 0
        self.pv_adjust_apply = True

        if self.interface == 'repl':
            self.window_console_id = None
            try:
                self.window_console_id = get_activewindow_id()
            except AbbError as e:
                self.txtout(error(e))

        # Inicia la sesión
        self.session = SessionManager(SESSION_FOLDER)
        self.session.activate()

        # Saludo de bienvenida
        clear_screen()
        self.txtout(welcome({
            'context': self.interface,
            'audio_generator': self.program
        }))

        # Instante de inicio de sessión.
        self.init_time = time.time()
        self.previus_time = self.init_time

        # Ejecuta el programa generador de audio en silencio y ajusta la ventana
        try:
            self.current_process = run_audioprogram(self.program, AUDIO_INITIAL_EXPRESSION, self.pipe_write, self.current_t)
        except AbbError as e:
            self.txtout(error(e))

        # Composición de ventanas
        if self.interface == 'repl':
            self._control_window()



    async def run(self):
        # Ciclo principal

        while True:
            try:
                # Solicita una expresión RPN al usuario
                if not (await self._get_expression()):
                    break


                # Comando especial para hacer pruebas de desarrollo
                if self.expression_normal == CMDS.dev_test:
                    await self._test(textout=self.txtoutAsync)
                    continue

                # Salir del loop
                if (self.expression_normal == CMDS.end_session_1
                    or self.expression_normal == CMDS.end_session_2):
                    self._finalize_loop()
                    break

                # Comando especial para incluir comentarios
                if self.expression.startswith(CMDS.comments):
                    self._add_comment()
                    continue

                # Comando especial para incluir comentarios
                if self.expression_normal == CMDS.clear_console:
                    clear_screen()
                    continue

                # Comando especial para mostrar la lista de comandos y ayuda del repl
                if self.expression_normal == CMDS.help:
                    await self.txtoutAsync(internal_help(self.interface))
                    continue

                # Comando especial para cambiar el valor del rate
                if self.expression_normal.endswith(f' {CMDS.set_rate}'):
                    await self._set_rate()
                    continue

                # Comando especial para grabar la sesión actual
                if self.expression_normal.endswith(f' {CMDS.save_session}'):
                    await self._save_session()
                    continue

                # Comando especial para cargar una sesión
                if self.expression_normal.endswith(f' {CMDS.load_session}'):
                    await self._load_session()
                    continue

                # Comando especial para reproducir automaticamente una sesión
                if self.expression_normal == CMDS.play_session:
                    await self._play_session()
                    continue

                # Comando especial para vaciar la sesión actual
                if self.expression_normal == CMDS.empty_session:
                    await self._empty_session()
                    continue

                # Comando especial para manejar los items de sesión - preservandolos
                if self.expression_normal.endswith(f' {CMDS.preserve_session_item}'):
                    await self._preserve_session_item()
                    continue

                # Comando especial para manejar los items de sesión - borrandolos
                if self.expression_normal.endswith(f' {CMDS.delete_session_item}'):
                    await self._delete_session_item()
                    continue

                # Comando especial para cargar una sesión
                if self.expression_normal.endswith(CMDS.show_session):
                    await self._show_session()
                    continue

                # Comando especial para listar las sessiones disponibles
                if self.expression_normal == CMDS.list_sessions:
                    await self._list_sessions()
                    continue

                # Comando especial para setear la velocidad de reproducción de las sesiones
                if self.expression_normal.endswith(f' {CMDS.set_speed}'):
                    await self._set_speed()
                    continue

                # Comando especial para reiniciar player-visualizer
                if self.expression_normal == CMDS.reset_visual:
                    self._restarting_pv()
                    continue

                # Comando especial para establecer el modo de composición del visualizador
                if self.expression_normal.endswith(f' {CMDS.compose_visual}'):
                    await self._visual_compose()
                    continue

                # Comando especial para obtener el valor actual de t
                if self.expression_normal == CMDS.get_t:
                    await self._get_t()
                    continue

                # Comando especial para cambiar el valor de t
                if self.expression_normal.endswith(f' {CMDS.set_t}'):
                    await self._set_t()
                else:
                    # Si no hay seteo explícito, tomará el valor almacenado al finalizar la última expresión
                    self.current_t = read_last_t()


                # Detiene el proceso anterior si está en ejecución
                force_stop_process(self.current_process)

                # Vaciar el pipe antes de enviar nuevos datos
                flush_pipe(self.pipe_read)

                # Ejecuta el programa con la nueva expresión
                try:
                    self.current_process = run_audioprogram(self.program, self.expression, self.pipe_write, self.current_t)
                except AbbError as e:
                    self.txtout(error(e))
                    continue

                # Composición de ventanas
                self._control_window()

                # Guarda la expresión actual para la próxima iteración
                self.previous_expression = self.expression

                # Guarda la expresión en la sesión
                self.session.add(self.expression)

                if self.interface == 'server':
                    await self.txtoutAsync(info(f'EXPRESÓN: {self.expression}'))

            except KeyboardInterrupt:
                if VERBOSE_MODE:
                    self.txtout(info('\nDeteniendo procesos...'))
                force_stop_process(self.current_process)
                break

            except Exception as e:
                await self.txtoutAsync(error(f'ERROR inesperado: {e}'))
                force_stop_process(self.current_process)
                break

        await self._end_loop()


    def _select_and_compile(self):
        """Selecciona el modo numérico del generdor de audio y lo compila."""

        # Selección de modo
        while True:
            clear_screen()
            self.txtout(select_mode(self.interface))
            self.modo = input(f"\n{PROMPT}ELIGE EL MODO {PROMPT}").lower().strip()
            if self.modo in ['i', 'f']:
                break

        # Limpia el entorno de temporales previos
        clean_env()

        self.program = get_binpath_audioprogram(self.modo)

        if AUDIO_PROGRAM_COMPILE:
            # Compila el programa
            try:
                compile_audioprogram(self.modo)
            except AbbError as e:
                self.txtout(error(e))


    def _start_pv(self):
        """Establece la función start para el player-visualzer,
        según la opción defina.
        """
        options = {
            'ffplay': start_ffplay,
            'audpv': start_audpv,
            }
        return options[self.current_player_visualizer]


    def _restart_pv(self):
        """Establece la función restart para el player-visualzer,
        según la opción defina.
        """
        options = {
            'ffplay': restart_ffplay,
            'audpv': restart_audpv,
            }
        return options[self.current_player_visualizer]


    def _control_window(self):
        """
        Compone la ventana de previsualización.
        Si la interface es REPL, también pone el foco en la consola.
        """

        # Espera preventiva
        time.sleep(PLAYER_WINDOW_SLEEP_FOR_POSITION)

        # Posicionamiento de ventana
        try:
            player_visualizer_compose(self.current_player_window_composition_type)
        except AbbError as e:
            self.txtout(error(e))

        if self.interface == 'repl':
            # Enfoque en la ventana de código
            focus_window(self.window_console_id)


    async def _get_expression(self):
        if self.interface == 'repl':
            readline.set_startup_hook(lambda: readline.insert_text(self.previous_expression))
            self.expression = input(PROMPT)
            readline.set_startup_hook(None)
        elif self.interface == 'server':
            self.expression = await self.audioqueueAsync()
        else:
            self.txtoutAsync(error(f'Obtención de expresión no implementada para la interfaz "{self.interface}".'))
            return False

        self.expression = self.expression.strip()
        self.expression_normal = self.expression.lower()
        return True


    def _finalize_loop(self):
        self.expression = ''


    def _add_comment(self):
        self.session.add(self.expression.strip())


    def _restarting_pv(self):
        self.pv_process, self.log = self._restart_pv()(
            self.pv_process, self.pipe_read, self.log_file, self.log, self.current_rate)


    async def _set_rate(self):
        resp = []
        try:
            new_rate = int(self.expression.split()[0])
            if new_rate > 0:
                if VERBOSE_MODE:
                    resp.append(info(f'Cambiando rate a {new_rate} Hz'))
                self.current_rate = new_rate
                self._restarting_pv()

                # Composición de ventanas
                self._control_window()

                # Agregado de expresión a la sesión
                self.session.add(self.expression)
            else:
                resp.append(error('ERROR: El rate debe ser un número positivo'))
        except ValueError:
            resp.append(error('ERROR: Formato incorrecto para el comando "set_rate"'))
        finally:
            await self.txtoutAsync('\n'.join(resp))


    async def _save_session(self):
        try:
            s_name = self.expression.split()[0]
            self.session.save(s_name)
            await self.txtoutAsync(info(f'Sesión "{s_name}" grabada correctamente'))
        except Exception as e:
            await self.txtoutAsync(error(f'ERROR: Al intentar grabar la sesión: {e}'))


    async def _load_session(self):
        resp = []
        try:
            s_name = self.expression.split()[0]
            if not self.session.load(s_name):
                resp.append(error(f'ERROR: El archivo de sesión "{s_name}" no existe'))
            else:
                resp.append(info(f'Sesión "{s_name}" cargada correctamente'))
        except Exception as e:
            resp.append(error(f'ERROR al cargar la sesión: {e}'))
        finally:
            await self.txtoutAsync('\n'.join(resp))


    async def _play_session(self):
        resp = []
        try:
            resp.append(info('Iniciando reproducción de la sesión...'))
            resp.append(info('Presiona Ctrl+C para detenerla'))
            await self.txtoutAsync('\n'.join(resp))
            try:
                for i, entry in enumerate(self.session.data()):
                    expr = entry.get('data', '').strip()
                    if not expr: continue  # Ignora entradas vacías
                    if expr.startswith(CMDS.comments):
                        await self.txtoutAsync(info(f'    {expr}', level=2))
                        continue  # Ignora comentarios
                    elapsed_time = entry.get('elapsed_time', 0) * self.current_speed
                    await self.txtoutAsync(info(f'    {expr} (durante {elapsed_time:.2f} segundos)', level=2))
                    force_stop_process(self.current_process)
                    flush_pipe(self.pipe_read)
                    try:
                        self.current_process = run_audioprogram(self.program, expr, self.pipe_write, self.current_t)
                    except AbbError as e:
                        await self.txtoutAsync(error(e))
                        continue
                    if i == 0:
                        self._control_window() # Composición de ventanas
                    time.sleep(elapsed_time)
            except KeyboardInterrupt:
                await self.txtoutAsync(info('\nReproducción de la sesión detenida por el usuario.'))
                force_stop_process(self.current_process)
                flush_pipe(self.pipe_read)
                self._restarting_pv()
                self._control_window() # Composición de ventanas

            force_stop_process(self.current_process)
            flush_pipe(self.pipe_read)

            self._restarting_pv()
            time.sleep(0.1)
            self._control_window() # Composición de ventanas

            await self.txtoutAsync(info('Sesión reproducida correctamente.'))
        except Exception as e:
            await self.txtoutAsync(error(f'ERROR al reproducir la sesión: {e}'))


    async def _empty_session(self):
        try:
            self.session.empty()
        except Exception as e:
            await self.txtoutAsync(error(f'ERROR al vaciar la sesión: {e}'))


    async def _preserve_session_item(self):
        resp = []
        try:
            l_items = [int(i) for i in self.expression.split()[0:-1]]
            self.session.preserve_items(l_items)
            resp.append(info(f'Preservados los items: {l_items}'))
        except Exception as e:
            resp.append(error(f'ERROR al manipular los items de la sesión: {e}'))
        finally:
            await self.txtoutAsync('\n'.join(resp))


    async def _delete_session_item(self):
        resp = []
        try:
            l_items = [int(i) for i in self.expression.split()[0:-1]]
            self.session.delete_items(l_items)
            resp.append(info(f'Borrados los items: {l_items}'))
        except Exception as e:
            resp.append(error(f'ERROR al manipular los items de la sesión: {e}'))
        finally:
            await self.txtoutAsync('\n'.join(resp))

    async def _show_session(self):
        resp = []
        try:
            d_expr = self.expression.split()
            if len(d_expr) == 2:
                # Carga datos de una sesión solicitada por nombre
                s_name = d_expr[0]
                _, d_session = self.session.read(s_name)
            else:
                # Usa los datos de la sesión actual
                d_session = self.session.data()
            if len(d_session) > 0:
                for i, dat in enumerate(d_session):
                    resp.append(info(f'[{i}]\t{round(dat["elapsed_time"], 2)}\t{dat["data"]}'))
            else:
                resp.append(info('La sessión actual está vacía.'))
        except Exception as e:
            resp.append(error(f'ERROR al cargar la sesión: {e}'))
        finally:
            await self.txtoutAsync('\n'.join(resp))

    async def _list_sessions(self):
        resp = []
        try:
            files = [f for f in os.listdir(SESSION_FOLDER) if f.endswith('.json')]
            if len(files) == 0:
                resp.append(info('No hay sessiones almacenadas en "{SESSION_FOLDER}":'))
            else:
                resp.append(info('Lista de sesiones almacenadas en "{SESSION_FOLDER}":'))
                for file in sorted(files):
                    fname = os.path.splitext(file)[0]
                    resp.append(info(f'    {fname}', level=2))
        except Exception as e:
            resp.append(error(f'ERROR al listar las sesiones almacenadas: {e}'))
        finally:
            await self.txtoutAsync('\n'.join(resp))

    async def _set_speed(self):
        resp = []
        try:
            new_speed = float(self.expression.split()[0])
            if new_speed > 0:
                if VERBOSE_MODE:
                    resp.append(info(f'Cambiando velocidad de reproducción a {new_speed} X ...'))
                self.current_speed = new_speed
            else:
                resp.append(error('ERROR: La velocidad de reproducción debe ser un número positivo'))
        except ValueError:
            resp.append(error('ERROR: Formato incorrecto para el comando "set_speed"'))
        finally:
            await self.txtoutAsync('\n'.join(resp))


    async def _visual_compose(self):
        try:
            self.current_player_window_composition_type = self.expression.split()[0]
            self._control_window() # Composición de ventanas
        except Exception as e:
            await self.txtoutAsync(error(f'ERROR al establecer el modo de composicón del visualizador: {e}'))


    async def _set_t(self):
        resp = []
        try:
            new_t = int(self.expression.split()[0])
            if VERBOSE_MODE:
                resp.append(info(f'Cambiando inicio de t {new_t} ...'))
            self.current_t = new_t
            self.session.add(self.expression)
        except ValueError:
            resp.append(error('ERROR: Formato incorrecto para el comando "set_t"'))
        finally:
            self.expression = self.previous_expression
            await self.txtoutAsync('\n'.join(resp))


    async def _get_t(self):
        resp = []
        try:
            self.current_t = read_last_t()
            resp.append(info(f't = {self.current_t}'))
        except ValueError:
            resp.append(error('ERROR: No se pudo obtener el valor de "t"'))
        finally:
            await self.txtoutAsync('\n'.join(resp))


    async def _test(self, textout, interface='repl'):
        if interface == 'repl':
            await self.txtoutAsync(info('Texto solo para REPL'))
        await self.txtoutAsync(info('TEEEESSSSTT !!!'))


    async def _end_loop(self):
        resp = ['']

        # Limpieza final
        stop_processes(self.current_process, self.pv_process,
                       self.pipe_read, self.pipe_write,
                       self.log_file, self.log)

        # Grabado automático de session
        if SESSION_AUTOSAVE:
            instante = datetime.now().strftime("%Y-%m-%d-%H-%M")
            self.session.save(f'{instante}')
            resp.append(info(f'Sesión almacenada en "{SESSION_FOLDER}{instante}".'))
        # Despedida
        resp.append(bye({
            'duration_session': time.time() - self.init_time,
        }))
        await self.txtoutAsync('\n'.join(resp))

        if self.interface == 'server':
            self.shutdownServer()
