#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include "rpni.h"
#include "utils.h"

int main(int argc, char *argv[]) {
  if (argc < 3) {
    fprintf(stderr, "Uso: %s \"expresion_rpn\" \"init_t\"\n", argv[0]);
    return 1;
  }

  const char *last_t_file = "/dev/shm/evalrpn_last_t";
  const int multivalue_stack = 1;
  const int debug_mode = 0;
  const char *expression = argv[1];

  char *endptr;
  errno = 0;
  long t_long = strtol(argv[2], &endptr, 10);
  if (errno != 0 || *endptr != '\0' || t_long < INT_MIN || t_long > INT_MAX) {
    fprintf(stderr, "Error: '%s' no es un número válido o está fuera del rango de un int.\n", argv[1]);
    return 1;
  }
  int t = (int)t_long;


  for (;;t++) {
    putchar(eval_rpn_i(expression, t, multivalue_stack, debug_mode));

    if (t % 1000 == 0) {
      save_last_t(t, last_t_file);
    }
  }

  save_last_t(t, last_t_file);

  return 0;
}
