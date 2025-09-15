# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
FLASK_APP = app.py

# Opción 'init': Crear el entorno virtual e instalar dependencias
init:
	@echo "Creando entorno virtual..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		echo "Entorno virtual creado en '$(VENV_DIR)'."; \
	else \
		echo "El entorno virtual ya existe."; \
	fi
	@echo "Entrando al entorno virtual e instalando dependencias..."
	@$(PIP) install --upgrade pip > /dev/null
	@$(PIP) install flask > /dev/null
	@echo "Dependencias instaladas."

# Opción 'start': Iniciar el servidor Flask
start:
	@echo "Iniciando el servidor Flask..."
	@$(PYTHON) $(FLASK_APP)

# Opción 'clean': Limpiar el entorno virtual y archivos temporales
clean:
	@echo "Limpiando entorno virtual y archivos temporales..."
	@rm -rf $(VENV_DIR)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Limpieza completada."

# Opción 'help': Mostrar ayuda
help:
	@echo "Uso: make [comando]"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  init    - Crea el entorno virtual e instala dependencias"
	@echo "  start   - Inicia el servidor Flask"
	@echo "  clean   - Limpia el entorno virtual y archivos temporales"
	@echo "  help    - Muestra esta ayuda"

.PHONY: init start clean help
