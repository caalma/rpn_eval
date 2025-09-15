#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "rpni.h"

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Calculadora para enteros en RPN\n");
    fprintf(stderr, "Uso: %s <rpn_expresion> [t ...]\n", argv[0]);
    return 1;
  }

  const int  multivalue_stack = 0;
  const int  debug_mode = 0;
  const char *expression = argv[1];
  int t = 0;

  if (argc == 3){
    char *endptr; // Puntero para verificar si la conversión fue exitosa
    errno = 0;    // Reiniciar errno antes de la conversión
    t = (int)strtod(argv[2], &endptr);
    // Verificar si hubo un error en la conversión
    if (errno != 0 || *endptr != '\0') {
      fprintf(stderr, "Error: '%s' no es un número válido.\n", argv[2]);
      return 1;
    }
  }

  const int result = eval_rpn_i(expression, t, multivalue_stack, debug_mode);
  fprintf(stdout, "%d", result);
}
