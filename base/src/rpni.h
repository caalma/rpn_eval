#ifndef RPNI_H
#define RPNI_H

extern const char *rpni_operators[];
extern const int rpni_operators_length;

int eval_rpn_i(const char *expr, int t, int multivalue_stack, int debug_mode);

#endif
