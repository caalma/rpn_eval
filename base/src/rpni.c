#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define INITIAL_STACK_SIZE 1024 // Mayor capacidad inicial

const char *rpni_operators[] = {
  "+", "-", "*", "/", "%", "swap", "dup", "put", "pick", "only", "drop", "~",
    "==", "!=", ">", "<", ">=", "<=", "&&", "||", "<<", ">>", "&", "|", "^"
  };

const int rpni_operators_length = sizeof(rpni_operators) / sizeof(rpni_operators[0]);

typedef struct {
  int *data;
  int size;
  int capacity;
} Stack;

// Funciones auxiliares para la pila
void stack_init(Stack *stack) {
  stack->data = malloc(INITIAL_STACK_SIZE * sizeof(int));
  stack->size = 0;
  stack->capacity = INITIAL_STACK_SIZE;
}

void stack_resize(Stack *stack, int new_capacity) {
  stack->data = realloc(stack->data, new_capacity * sizeof(int));
  stack->capacity = new_capacity;
}

static inline void stack_push(Stack *stack, int value) {
  if (stack->size == stack->capacity) {
    stack_resize(stack, stack->capacity + 256); // Incremento fijo
  }
  stack->data[stack->size++] = value;
}

static inline int stack_pop(Stack *stack) {
  if (stack->size == 0) {
    fprintf(stderr, "Pila vacía\n");
    exit(1);
  }
  return stack->data[--stack->size];
}

const int *stack_peek(const Stack *stack, int index) {
  if (index < 0 || index >= stack->size) {
    fprintf(stderr, "Índice fuera de rango en la pila\n");
    exit(1);
  }
  return &stack->data[index]; // Devuelve un puntero
}

void stack_free(Stack *stack) {
  free(stack->data);
  stack->data = NULL;
  stack->size = stack->capacity = 0;
}

void stack_print(const Stack *stack) {
    if (stack->size == 0) {
        printf("Stack vacío\n");
        return;
    }
    printf("-- DEBUG: contenido del stack (de tope a base):\n");
    printf("-- ");
    for (int i = stack->size - 1; i >= 0; i--) {
        printf("%d ", stack->data[i]);
    }
    printf("\n");
}

/**
 * @brief Evalúa una expresión en notación polaca inversa (RPN).
 *
 * @param expr Expresión RPN a evaluar.
 * @param t Valor de la variable 't' en la expresión.
 * @param multivalue_stack Indica si se permite un stack con múltiples valores al final.
 * @param debug_mode Indica si se permiten salidas de control para el desarrollo.
 * @return El resultado de la evaluación.
 */
int eval_rpn_i(const char *expr, int t, int multivalue_stack, int debug_mode) {
  Stack stack;
  stack_init(&stack);

  const char *ptr = expr;
  while (*ptr != '\0') {
    // Ignorar espacios
    if (isspace(*ptr)) {
      ptr++;
      continue;
    }

    // Procesar números
    if (isdigit(*ptr) || (*ptr == '-' && isdigit(*(ptr + 1)))) {
      int value = atoi(ptr);
      stack_push(&stack, value);
      // Avanzar al siguiente token
      while (*ptr != '\0' && !isspace(*ptr)) ptr++;

    } else {
      // Procesar operadores
      char token[64];
      int i = 0;
      while (*ptr != '\0' && !isspace(*ptr)) {
        token[i++] = *ptr++;
      }
      token[i] = '\0';

      if (strcmp(token, "t") == 0) {
        // Variable 't'
        stack_push(&stack, t);

      } else if (strcmp(token, "swap") == 0) {
        // Operador swap
        if (stack.size < 2) {
          fprintf(stderr, "Falta de operandos para 'swap'\n");
          stack_free(&stack);
          return 0;
        }
        int a = stack_pop(&stack);
        int b = stack_pop(&stack);
        stack_push(&stack, a);
        stack_push(&stack, b);

      } else if (strcmp(token, "dup") == 0) {
        // Operador dup
        if (stack.size < 1) {
          fprintf(stderr, "Falta de operandos para 'dup'\n");
          stack_free(&stack);
          return 0;
        }
        int a = *stack_peek(&stack, stack.size - 1);
        stack_push(&stack, a);

      } else if (strcmp(token, "put") == 0) {
        // Operador put
        if (stack.size < 2) {
          fprintf(stderr, "Falta de operandos para 'put'\n");
          stack_free(&stack);
          return 0;
        }
        int index = stack_pop(&stack);
        int value = stack_pop(&stack);
        if (index < 0 || index >= stack.size) {
          fprintf(stderr, "Índice inválido para 'put'\n");
          stack_free(&stack);
          return 0;
        }
        int index_lifo = stack.size - 1 - index;
        stack.data[index_lifo] = value;

      } else if (strcmp(token, "drop") == 0) {
        // Operador drop
        if (stack.size < 1) {
          fprintf(stderr, "Falta de operandos para 'drop'\n");
          stack_free(&stack);
          return 0;
        }
        stack_pop(&stack);

      } else if (strcmp(token, "pick") == 0) {
        // Operador pick
        if (stack.size < 1) {
          fprintf(stderr, "Falta de operandos para 'pick'\n");
          stack_free(&stack);
          return 0;
        }
        int index = stack_pop(&stack);
        if (index < 0 || index >= stack.size) {
          fprintf(stderr, "Índice inválido para 'pick'\n");
          stack_free(&stack);
          return 0;
        }
        int index_lifo = stack.size - 1 - index;
        int value = *stack_peek(&stack, index_lifo);
        stack_push(&stack, value);

      } else if (strcmp(token, "only") == 0) {
        // Operador only
        if (stack.size < 1) {
          fprintf(stderr, "Falta de operandos para 'only'\n");
          stack_free(&stack);
          return 0;
        }
        int index = stack_pop(&stack);
        if (index < 0 || index >= stack.size) {
          fprintf(stderr, "Índice inválido para 'only'\n");
          stack_free(&stack);
          return 0;
        }
        int index_lifo = stack.size - 1 - index;
        int value_to_keep = *stack_peek(&stack, index_lifo);

        // Vaciar el stack
        stack_free(&stack);
        stack_init(&stack);

        // Empujar el valor correspondiente al índice ajustado
        stack_push(&stack, value_to_keep);

      } else if (strcmp(token, "~") == 0) {
        // Operador unario: Negación binaria (~)
        if (stack.size < 1) {
          fprintf(stderr, "Falta de operandos para '%s'\n", token);
          stack_free(&stack);
          return 0;
        }
        int a = stack_pop(&stack);
        stack_push(&stack, ~a);

      } else {
        // Operadores binarios
        if (stack.size < 2) {
          fprintf(stderr, "Falta de operandos para '%s'\n", token);
          stack_free(&stack);
          return 0;
        }
        int b = stack_pop(&stack);
        int a = stack_pop(&stack);
        int result = 0;

        if (strcmp(token, "+") == 0) {
          result = a + b;

        } else if (strcmp(token, "-") == 0) {
          result = a - b;

        } else if (strcmp(token, "*") == 0) {
          result = a * b;

        } else if (strcmp(token, "/") == 0) {
          if (b == 0) {
            fprintf(stderr, "División por cero\n");
            stack_free(&stack);
            return 0;
          }
          result = a / b;

        } else if (strcmp(token, "%") == 0) {
          if (b == 0) {
            fprintf(stderr, "División por cero en módulo\n");
            stack_free(&stack);
            return 0;
          }
          result = a % b;

        } else if (strcmp(token, "==") == 0) {
          result = (a == b) ? 1 : 0;

        } else if (strcmp(token, "!=") == 0) {
          result = (a != b) ? 1 : 0;

        } else if (strcmp(token, ">") == 0) {
          result = (a > b) ? 1 : 0;

        } else if (strcmp(token, "<") == 0) {
          result = (a < b) ? 1 : 0;

        } else if (strcmp(token, ">=") == 0) {
          result = (a >= b) ? 1 : 0;

        } else if (strcmp(token, "<=") == 0) {
          result = (a <= b) ? 1 : 0;

        } else if (strcmp(token, "&&") == 0) {
          result = (a != 0 && b != 0) ? 1 : 0;

        } else if (strcmp(token, "||") == 0) {
          result = (a != 0 || b != 0) ? 1 : 0;

        } else if (strcmp(token, "<<") == 0) {
          result = (int)a << (int)b; // Desplazamiento a la izquierda

        } else if (strcmp(token, ">>") == 0) {
          result = (int)a >> (int)b; // Desplazamiento a la derecha

        } else if (strcmp(token, "&") == 0) {
          result = (int)a & (int)b; // AND bit a bit

        } else if (strcmp(token, "|") == 0) {
          result = (int)a | (int)b; // OR bit a bit

        } else if (strcmp(token, "^") == 0) {
          result = (int)a ^ (int)b; // XOR bit a bit

        } else {
          fprintf(stderr, "Operador desconocido '%s'\n", token);
          stack_free(&stack);
          return 0;
        }
        stack_push(&stack, result);
      }
    }
  }

  if (multivalue_stack == 0) {
    if (stack.size != 1) {
      fprintf(stderr, "Expresión incompleta o incorrecta\n");
      stack_free(&stack);
      return 0;
    }
  }

  if (debug_mode != 0){
    stack_print(&stack);
  }

  int result = stack_pop(&stack);
  stack_free(&stack);
  return result;
}
