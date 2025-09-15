#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <termios.h>
#include <unistd.h>
#include "../rpni.h"
#include "autocomplete.h"
#include "history.h"
#include "comun.h"
#include "linenavigate.h"
#include "variablemanager.h"
#include "modulemanager.h"

#define APP_NAME "Calculadora RPN interactiva"
#define APP_VERSION "0.0.1"

struct termios orit, newt;

void restore_terminal() {
    tcsetattr(STDIN_FILENO, TCSANOW, &orit);
}

void show_welcome() {
  printf("%s. Escribe ':.' para salir.\n\n", APP_NAME);
}

void show_bye() {
  printf("\nHasta luego! :D\n");
  restore_terminal();
}

void handle_sigint(int sig) {
  show_bye();
  exit(0);
}

int main() {
  int debug_mode = 0;
  int multivalue_stack = 1;

  // Reserva de estado actual de la terminal
  tcgetattr(STDIN_FILENO, &orit);

  // Configurar el manejador para Ctrl+C
  signal(SIGINT, handle_sigint);

  autocomplete_append(rpni_operators, rpni_operators_length);
  load_history();
  show_welcome();

  while (1) {
    printf("%s ", PROMPT_SYMBOL);
    char *line = get_input_with_history();

    // Ignorar entradas vacías
    if (strcmp(line, "") == 0) {
      continue;
    }

    if (strcmp(line, ":.") == 0) {
      break;
    }

    save_history(line);

    // Verificar si es un comando para cargar una librería
    if (strstr(line, ":@")) {
      // Extraer la ruta del archivo
      char file_path[1024];
      if (sscanf(line, "%s :@", file_path) != 1) {
        fprintf(stderr, "Error: Sintaxis incorrecta para cargar una librería\n");
        continue;
      }
      // Cargar y evaluar el archivo
      if (!load_library(file_path)) {
        continue; // Error al cargar la librería
      }
    } else if (strstr(line, ":=")) {
      // Manejar asignaciones directas
      if (!handle_assignment(line)) {
        continue; // Error en la asignación
      }
    } else {
      // Reemplazar variables en la expresión
      char *processed_expr = replace_variables(line);
      if (!processed_expr) {
        continue; // Error en el reemplazo
      }

      // Evaluar la expresión RPN
      int result = eval_rpn_i(processed_expr, 0, multivalue_stack, debug_mode);
      printf("[[ %d ]]\n", result);
    }
  }

  show_bye();
  return 0;
}
