#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "rpnf.h"
#include "utils.h"

int main(int argc, char *argv[]) {
  if (argc < 3) {
    fprintf(stderr, "Uso: %s \"expresion_rpn\"\n", argv[0]);
    return 1;
  }

  const char *last_t_file = "/dev/shm/evalrpn_last_t";
  const int multivalue_stack = 1;
  const int debug_mode = 0;
  const char *expression = argv[1];

  char *endptr;
  errno = 0;
  double t = strtod(argv[2], &endptr);
  if (errno != 0 || *endptr != '\0') {
    fprintf(stderr, "Error: '%s' no es un número válido.\n", argv[2]);
    return 1;
  }


  for (;;t++) {
    putchar(eval_rpn_f(expression, t, multivalue_stack, debug_mode));

    if ((int)t % 1000 == 0) {
      save_last_t((int)t, last_t_file);
    }
  }

  save_last_t((int)t, last_t_file);

  return 0;
}
