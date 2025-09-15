#include <stdio.h>
#include <string.h>
#include "history.h"

#define HISTORY_FILE "history.txt"

char history[MAX_HISTORY][MAX_INPUT];
int history_count = 0;
int history_index = 0;

void load_history() {
  FILE *file = fopen(HISTORY_FILE, "r");
  if (!file) return;

  while (fgets(history[history_count], sizeof(history[0]), file)) {
    history[history_count][strcspn(history[history_count], "\n")] = '\0';
    if (history_count < MAX_HISTORY - 1) {
      history_count++;
    }
  }
  fclose(file);
}

void save_history(const char *command) {
  if (history_count > 0 && strcmp(history[history_count - 1], command) == 0) {
    return; // Evitar duplicados consecutivos
  }

  strncpy(history[history_count % MAX_HISTORY], command, sizeof(history[0]) - 1);
  history_count++;

  FILE *file = fopen(HISTORY_FILE, "a");
  if (file) {
    fprintf(file, "%s\n", command);
    fclose(file);
  }
}
