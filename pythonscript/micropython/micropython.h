#ifndef MICROPYTHON_H
#define MICROPYTHON_H


extern "C" {

#include "py/compile.h"
#include "py/runtime.h"
#include "py/gc.h"
#include "py/stackctrl.h"
#include "py/objmodule.h"

// Bonus functions !
mp_obj_t mp_execute_from_lexer(mp_lexer_t *lex);
mp_obj_t mp_execute_as_module(const char *str);
mp_obj_t mp_execute_expr(const char *str);

}


#endif // MICROPYTHON_H
