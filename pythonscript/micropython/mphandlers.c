#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

#include "micropython/py/lexer.h"
#include "micropython/py/runtime.h"
#include "micropython/py/compile.h"


/* Needed by micropython */

uint mp_import_stat(const char *path) {
    struct stat st;
    if (stat(path, &st) == 0) {
        if (S_ISDIR(st.st_mode)) {
            return MP_IMPORT_STAT_DIR;
        } else if (S_ISREG(st.st_mode)) {
            return MP_IMPORT_STAT_FILE;
        }
    }
    return MP_IMPORT_STAT_NO_EXIST;
}


void nlr_jump_fail(void *val) {
    printf("FATAL: uncaught NLR %p\n", val);
    exit(1);
}


mp_obj_t mp_execute_from_lexer(mp_lexer_t *lex, mp_parse_input_kind_t input_kind, bool is_repl) {
    nlr_buf_t nlr;
    if (nlr_push(&nlr) == 0) {
        mp_parse_tree_t pt = mp_parse(lex, input_kind);
        mp_obj_t module_fun = mp_compile(&pt, lex->source_name, MP_EMIT_OPT_NONE, is_repl);
        mp_call_function_0(module_fun);

        // Handle exceptions
        if (MP_STATE_VM(mp_pending_exception) != MP_OBJ_NULL) {
            mp_obj_t obj = MP_STATE_VM(mp_pending_exception);
            MP_STATE_VM(mp_pending_exception) = MP_OBJ_NULL;
            nlr_raise(obj);
        }

        nlr_pop();
        return mp_const_none;
    } else {
        mp_obj_print_exception(&mp_plat_print, (mp_obj_t)nlr.ret_val);
        // uncaught exception
        return (mp_obj_t)nlr.ret_val;
    }
}


mp_obj_t mp_execute_as_module(const char *str) {
    mp_lexer_t *lex = mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, str, strlen(str), false);
    return mp_execute_from_lexer(lex, MP_PARSE_FILE_INPUT, false);
}

mp_obj_t mp_execute_expr(const char *str) {
    mp_lexer_t *lex = mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, str, strlen(str), false);
    return mp_execute_from_lexer(lex, MP_PARSE_SINGLE_INPUT, true);
}
#if 0
#define MP_EXEC_AS_EXPR(code) MP_EXEC_GENERIC(code, MP_PARSE_SINGLE_INPUT, true)

#define MP_EXEC_GENERIC(code, input_kind, is_repl) \
    const mp_lexer_t *lex = mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, code, strlen(code), false);
    const mp_parse_tree_t pt = mp_parse(lex, input_kind);
    const mp_obj_t module_fun = mp_compile(&pt, lex->source_name, MP_EMIT_OPT_NONE, is_repl);
    mp_obj_t error = 0;
    const auto import_module = [&module_fun]() {
        return mp_call_function_0(module_fun);
    };
    const auto handle_ex = [&error](mp_obj_t ex) {
        mp_obj_print_exception(&mp_plat_print, ex);
        error = ex;
    };
    upywrap::WrapMicroPythonCall<decltype(import_module), decltype(handle_ex)>(import_module, handle_ex);
#endif