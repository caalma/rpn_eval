# Variables
CC = gcc
CFLAGS = -Wall -lm
RM = rm -f
SRC_DIR = src
BIN_DIR = bin

# Programas y fuentes
AUDIO_PROGRAM_F = $(BIN_DIR)/audio_rpn_f
AUDIO_PROGRAM_I = $(BIN_DIR)/audio_rpn_i
AUDIO_SOURCES_F = $(addprefix $(SRC_DIR)/, rpnf.c utils.c audio_rpn_f.c)
AUDIO_SOURCES_I = $(addprefix $(SRC_DIR)/, rpni.c utils.c audio_rpn_i.c)

CALC_PROGRAM_F = $(BIN_DIR)/calc_f
CALC_PROGRAM_I = $(BIN_DIR)/calc_i
CALC_SOURCES_F = $(addprefix $(SRC_DIR)/, rpnf.c calc_f.c)
CALC_SOURCES_I = $(addprefix $(SRC_DIR)/, rpni.c calc_i.c)

REPL_PROGRAM_I = $(BIN_DIR)/repl/repl_i
REPL_SOURCES_I = $(addprefix $(SRC_DIR)/, rpni.c repl/autocomplete.c repl/history.c repl/linenavigate.c repl/variablemanager.c repl/modulemanager.c repl/repl_i.c)


# Regla por defecto
all: clean $(AUDIO_PROGRAM_F) $(AUDIO_PROGRAM_I) $(CALC_PROGRAM_F) $(CALC_PROGRAM_I) $(REPL_PROGRAM_I)

# Crear la carpeta bin si no existe
$(BIN_DIR):
	mkdir -p $(BIN_DIR)
	mkdir -p $(BIN_DIR)/repl

# Compilación para el modo "f" (audio)
$(AUDIO_PROGRAM_F): $(AUDIO_SOURCES_F) | $(BIN_DIR)
	$(CC) -o $@ $^ $(CFLAGS)

# Compilación para el modo "i" (audio)
$(AUDIO_PROGRAM_I): $(AUDIO_SOURCES_I) | $(BIN_DIR)
	$(CC) -o $@ $^ $(CFLAGS)

# Compilación para el modo "f" (calc)
$(CALC_PROGRAM_F): $(CALC_SOURCES_F) | $(BIN_DIR)
	$(CC) -o $@ $^ $(CFLAGS)

# Compilación para el modo "i" (calc)
$(CALC_PROGRAM_I): $(CALC_SOURCES_I) | $(BIN_DIR)
	$(CC) -o $@ $^ $(CFLAGS)

# Compilación para el modo "i" (repl)
$(REPL_PROGRAM_I): $(REPL_SOURCES_I) | $(BIN_DIR)
	$(CC) -o $@ $^ -I$(SRC_DIR)/repl/ $(CFLAGS)

# Limpiar archivos generados
clean:
	rm -rf bin
	rm -f history.txt

# Regla para compilar según el modo (f o i)
mode:
ifeq ($(bb_modo),af)
    $(MAKE) $(AUDIO_PROGRAM_F)
else ifeq ($(bb_modo),ai)
	$(MAKE) $(AUDIO_PROGRAM_I)
else ifeq ($(bb_modo),cf)
	$(MAKE) $(CALC_PROGRAM_F)
else ifeq ($(bb_modo),ci)
	$(MAKE) $(CALC_PROGRAM_I)
else ifeq ($(bb_modo),ri)
	$(MAKE) $(REPL_PROGRAM_I)
else
	echo "Modo no válido. Usa 'af', 'ai', 'cf', 'ci', 'ri'."
endif

# Reglas de prueba
test_audio_f:
	$(AUDIO_PROGRAM_F) "t 1.01 * t 1.1 * *" "0" | ffplay -hide_banner -infbuf -f s16le -ar 8000 -ac 1 -vn -i -

test_audio_i:
	$(AUDIO_PROGRAM_I) "t 5 >> t 11 >> & t *" "0" | ffplay -hide_banner -infbuf -f s16le -ar 8000 -ac 1 -vn -i -

test_calc_f:
	$(CALC_PROGRAM_F) "4 0.5 *"

test_calc_i:
	$(CALC_PROGRAM_I) "3 4 *"

test_repl_i:
	$(REPL_PROGRAM_I)


.PHONY: all clean mode
