#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "autocomplete.h"


#define MAX_TOKENS 512

typedef struct {
  char name[64];
  char expression[1024]; // Almacena la expresión como una cadena
} Variable;

Variable variables[64];
int variable_count = 0;

const char *get_variable_value(const char *name) {
  for (int i = 0; i < variable_count; i++) {
    if (strcmp(variables[i].name, name) == 0) {
      return variables[i].expression;
    }
  }
  return NULL; // Variable no encontrada
}


void set_variable(const char *name, const char *expression) {
  for (int i = 0; i < variable_count; i++) {
    if (strcmp(variables[i].name, name) == 0) {
      strncpy(variables[i].expression, expression, sizeof(variables[i].expression) - 1);
      return;
    }
  }
  strncpy(variables[variable_count].name, name, sizeof(variables[0].name) - 1);
  strncpy(variables[variable_count].expression, expression, sizeof(variables[0].expression) - 1);
  // Agregar el nombre de la variable al autocompletado
  autocomplete_add_word(name);
  variable_count++;
}

int handle_assignment(const char *input) {
  char tokens[MAX_TOKENS][64];
  int token_count = 0;

  // Dividir la entrada en tokens
  const char *delimiters = " ";
  char *token = strtok((char *)input, delimiters);
  while (token != NULL && token_count < MAX_TOKENS) {
    strncpy(tokens[token_count], token, sizeof(tokens[0]) - 1);
    token_count++;
    token = strtok(NULL, delimiters);
  }

  // Verificar si es una asignación válida
  if (token_count < 3 || strcmp(tokens[token_count - 1], ":=") != 0) {
    fprintf(stderr, "Error: Sintaxis incorrecta para asignación\n");
    return 0;
  }

  // Extraer el nombre de la variable
  char *var_name = tokens[token_count - 2];

  // Construir la expresión (todos los tokens antes del nombre)
  char expression[1024] = "";
  for (int i = 0; i < token_count - 2; i++) {
    strcat(expression, tokens[i]);
    if (i < token_count - 3) {
      strcat(expression, " ");
    }
  }

  // Asignar la variable
  set_variable(var_name, expression);
  return 1; // Éxito
}


char *replace_variables(const char *input) {
  static char output[1024];
  char tokens[MAX_TOKENS][64];
  int token_count = 0;

  // Dividir la entrada en tokens
  const char *delimiters = " ";
  char *token = strtok((char *)input, delimiters);
  while (token != NULL && token_count < MAX_TOKENS) {
    strncpy(tokens[token_count], token, sizeof(tokens[0]) - 1);
    token_count++;
    token = strtok(NULL, delimiters);
  }

  // Reconstruir la expresión reemplazando variables
  output[0] = '\0';
  for (int i = 0; i < token_count; i++) {
    if (isalpha(tokens[i][0])) {
      // Es un posible nombre de variable
      const char *value = get_variable_value(tokens[i]);
      if (value != NULL) {
        // Si es una variable definida, reemplazarla por su valor
        strcat(output, value);
      } else {
        // Si no es una variable definida, dejar el token sin cambios
        strcat(output, tokens[i]);
      }
    } else {
      // No es un nombre de variable, dejar el token sin cambios
      strcat(output, tokens[i]);
    }
    if (i < token_count - 1) {
      strcat(output, " ");
    }
  }

  return output;
}
