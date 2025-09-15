#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include "comun.h"
#include "history.h"
#include "autocomplete.h"

char *get_input_with_history() {
  static char input[1024];
  memset(input, 0, sizeof(input)); // Limpiar el buffer
  int pos = 0;
  int ch;

  struct termios oldt, newt;
  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);

  while (1) {
    ch = getchar();

    if (ch == 10 || ch == 13) { // Enter
      printf("\n");
      break;
    } else if (ch == 27) { // Flechas
      getchar(); // Ignorar '['
      ch = getchar();
      if (ch == 'A') { // Flecha arriba
        if (history_index < history_count) {
          history_index++;
          if (history_index == history_count) {
            input[0] = '\0';
            pos = 0;
          } else {
            strncpy(input, history[(history_count - 1 - history_index + MAX_HISTORY) % MAX_HISTORY], sizeof(input));
            pos = strlen(input);
          }
          printf("\r%s %s\033[K", PROMPT_SYMBOL, input); // Actualizar la línea
        }
      } else if (ch == 'B') { // Flecha abajo
                if (history_index > 0) {
          history_index--;
          strncpy(input, history[(history_count - 1 - history_index + MAX_HISTORY) % MAX_HISTORY], sizeof(input));
          pos = strlen(input);
          printf("\r%s %s\033[K", PROMPT_SYMBOL, input); // Actualizar la línea
        }
      } else if (ch == 'C') { // Flecha derecha
        if (pos < strlen(input)) {
          pos++;
          printf("\033[C"); // Mover el cursor a la derecha
        }
      } else if (ch == 'D') { // Flecha izquierda
        if (pos > 0) {
          pos--;
          printf("\033[D"); // Mover el cursor a la izquierda
        }
      }
    } else if (ch == 127) { // Retroceso
      if (pos > 0) {
        input[--pos] = '\0';
        printf("\r%s %s \b", PROMPT_SYMBOL, input); // Limpiar la línea actual
      }
    } else if (ch == 9) { // Tab (autocompletado)
      autocomplete(input);
      pos = strlen(input);
      printf("\r%s %s", PROMPT_SYMBOL, input); // Actualizar la línea
    } else {
      if (pos < sizeof(input) - 1) {
        input[pos++] = ch;
        input[pos] = '\0';
        printf("\r%s %s", PROMPT_SYMBOL, input); // Actualizar la línea
      }
    }
  }

  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);

  // Eliminar espacios en blanco al inicio y final de la entrada
  char *trimmed = input;
  while (*trimmed == ' ') trimmed++; // Saltar espacios iniciales
  int len = strlen(trimmed);
  while (len > 0 && trimmed[len - 1] == ' ') trimmed[--len] = '\0'; // Eliminar espacios finales

  // Si la entrada está vacía, retornar una cadena vacía
  if (len == 0) {
    return "";
  }

  return trimmed;
}
