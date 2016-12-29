#ifndef MICROPYTHON_H
#define MICROPYTHON_H


extern "C" {

#include "py/compile.h"
#include "py/runtime.h"
#include "py/gc.h"
#include "py/stackctrl.h"
#include "py/objmodule.h"
#include "py/objtype.h"

// Bonus functions !
mp_obj_t mp_execute_from_lexer(mp_lexer_t *lex);
mp_obj_t mp_execute_as_module(const char *str);
mp_obj_t mp_execute_expr(const char *str);

}

// Shamelessly inspired from micropython-wrap

#define MP_WRAP_CALL(f) \
	MP_WRAP_CALL_EX(f, [](mp_obj_t ret_val) {})

#define MP_WRAP_CALL_EX(f, ex) \
    nlr_buf_t nlr; \
    if (nlr_push(&nlr) == 0) { \
      f(); \
      nlr_pop(); \
    } else { \
      ex(nlr.ret_val); \
    }


#endif // MICROPYTHON_H
