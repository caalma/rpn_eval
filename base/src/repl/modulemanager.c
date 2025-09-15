#include <stdio.h>
#include <string.h>
#include "variablemanager.h"

int load_library(const char *file_path) {
  FILE *file = fopen(file_path, "r");
  if (!file) {
    fprintf(stderr, "Error: No se pudo abrir el archivo '%s'\n", file_path);
    return 0;
  }

  char line[1024];
  int line_number = 0;

  while (fgets(line, sizeof(line), file)) {
    line_number++;
    // Eliminar el salto de línea
    line[strcspn(line, "\n")] = '\0';

    // Ignorar líneas vacías o comentarios (líneas que comienzan con '#')
    if (line[0] == '\0' || line[0] == '#') {
      continue;
    }

    // Procesar la línea como una asignación
    if (!handle_assignment(line)) {
      fprintf(stderr, "Error en la línea %d del archivo '%s': '%s'\n", line_number, file_path, line);
      fclose(file);
      return 0;
    }
  }

  fclose(file);
  printf("Librería cargada correctamente desde '%s'\n", file_path);
  return 1;
}
