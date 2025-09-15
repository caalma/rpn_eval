#ifndef VARIABLEMANAGER_H
#define VARIABLEMANAGER_H

const char *get_variable_value(const char *name);
void set_variable(const char *name, const char *expression);
int handle_assignment(const char *input);
char *replace_variables(const char *input);

#endif
