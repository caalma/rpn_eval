#ifndef AUTOCOMPLETE_H
#define AUTOCOMPLETE_H

void autocomplete_add_word(const char *word);
void autocomplete_append(const char **words, int words_length);
void autocomplete(char *input);

#endif
