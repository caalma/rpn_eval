import time
import json
import os

class SessionManager:
    def __init__(self, folder='./'):
        self.folder = folder
        self.session = []
        self.init_time = 0
        self.previous_time = 0
        self.debug = False


    def activate(self):
        """Inicia el tiempo de la sesión."""
        self.init_time = time.time()
        self.previous_time = self.init_time
        if self.debug:
            print("Sesión activada. Tiempo inicial registrado.")


    def add(self, data):
        """
        Agrega un dato a la sesión junto con el tiempo transcurrido desde el último evento.

        :param data: str - El dato (string) a agregar a la sesión.
        """
        if self.init_time == 0:
            raise ValueError("La sesión no ha sido activada. Usa el método activate() primero.")

        current_time = time.time()
        elapsed_time = current_time - self.previous_time
        self.session.append({"data": data, "elapsed_time": elapsed_time})
        self.previous_time = current_time
        if self.debug:
            print(f"Dato '{data}' agregado con tiempo transcurrido: {elapsed_time:.2f} segundos.")


    def save(self, filename):
        """Guarda los datos de la sesión en un archivo JSON.
        :param filename: str - Nombre del archivo (sin extensión).
        """
        if not self.session:
            if self.debug:
                print("No hay datos en la sesión para guardar.")
            return

        full_filename = os.path.join(self.folder, f"{filename}.json")
        with open(full_filename, "w") as file:
            json.dump(self.session, file, indent=4)

        if self.debug:
            print(f"Sesión guardada en '{full_filename}'.")


    def load(self, filename):
        """Función que reemplaza los datos de la sesión actual por los cargados."""
        error, data = self.read(filename)
        if not error:
            self.session = data
        return not error


    def read(self, filename):
        """Función que carga los datos de sesión según el nombre indicado."""
        full_filename = os.path.join(self.folder, f"{filename}.json")
        # Verifica si el archivo de sesión existe
        if os.path.exists(full_filename):
            # Carga la sesión desde el archivo JSON
            with open(full_filename, "r") as file:
                return False, json.load(file)
        return True, []


    def data(self):
        return self.session


    def empty(self):
        self.session = []
        self.activate()


    def preserve_items(self, li):
        result = []
        for i, v in enumerate(self.session):
            if i in li:
                result.append(v)
        self.session = result


    def delete_items(self, li):
        result = []
        for i, v in enumerate(self.session):
            if not i in li:
                result.append(v)
        self.session = result
