#include <stdlib.h>
#include <stdio.h>

#include "micropython/py/lexer.h"

/* Needed by mycropython */

mp_import_stat_t mp_import_stat(const char *path) {
    return MP_IMPORT_STAT_NO_EXIST;
}


void nlr_jump_fail(void *val) {
    printf("FATAL: uncaught NLR %p\n", val);
    exit(1);
}
