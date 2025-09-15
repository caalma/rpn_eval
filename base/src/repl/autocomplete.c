#include <stdio.h>
#include <string.h>

// --- AUTOCOMPLETADO
#define MAX_AUTOCOMPLETE_WORDS 256

char *autocomplete_words[MAX_AUTOCOMPLETE_WORDS];
int autocomplete_count = 0;

void autocomplete_add_word(const char *word) {
  if (autocomplete_count >= MAX_AUTOCOMPLETE_WORDS) {
    fprintf(stderr, "Error: Límite de palabras de autocompletado alcanzado\n");
    return;
  }
  // Verificar si la palabra ya existe en la lista
  for (int i = 0; i < autocomplete_count; i++) {
    if (strcmp(autocomplete_words[i], word) == 0) {
      return; // La palabra ya está en la lista
    }
  }
  // Agregar la nueva palabra
  autocomplete_words[autocomplete_count] = strdup(word); // Duplicar la cadena para almacenarla
  autocomplete_count++;
}

void autocomplete_append(const char **words, int words_length) {
  for (int i = 0; i < words_length; i++) {
    autocomplete_add_word(words[i]);
  }
}

void autocomplete(char *input) {
  for (int i = 0; i < autocomplete_count; i++) {
    if (strncmp(input, autocomplete_words[i], strlen(input)) == 0) {
      strcpy(input, autocomplete_words[i]);
      return; // Completar con la primera coincidencia encontrada
    }
  }
}
