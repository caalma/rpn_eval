#ifndef HISTORY_H
#define HISTORY_H

#define MAX_HISTORY 100
#define MAX_INPUT 1024

extern char history[MAX_HISTORY][MAX_INPUT];
extern int history_count;
extern int history_index;

void load_history();
void save_history(const char *command);

#endif
