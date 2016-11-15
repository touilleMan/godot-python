#include "register_types.h"

#ifndef PYTHONSCRIPT_USE_SHARED

#include "register_types_shared.cpp"

#else

#ifndef PYTHONSCRIPT_SHARED_LIB
#define PYTHONSCRIPT_SHARED_LIB "pythonscript.so"
#define STR(tok) tok
#else
#define STR_EXPAND(tok) #tok
#define STR(tok) STR_EXPAND(tok)
#endif

#include <dlfcn.h>
#include <sstream>
#include "script_language.h"


typedef void (*cb_t)();
static void *handle = 0;


void register_pythonscript_types() {
    ERR_EXPLAIN("pythonscript.so already loaded");
    ERR_FAIL_COND(handle);

    handle = dlopen(STR(PYTHONSCRIPT_SHARED_LIB), RTLD_LAZY);
    if (!handle) {
        std::stringstream ss;
        ss << "Cannot open library: " << dlerror();
        ERR_EXPLAIN(ss.str().c_str())
        ERR_FAIL();
    }

    cb_t cb = reinterpret_cast<cb_t>(dlsym(handle, "register_pythonscript_types"));
    const char *dlsym_error = dlerror();
    if (dlsym_error) {
        std::stringstream ss;
        ss << "Cannot load symbol 'register_pythonscript_types': " << dlsym_error;
        ERR_EXPLAIN(ss.str().c_str())
        ERR_FAIL();
    }
    cb();
}


void unregister_pythonscript_types() {
    cb_t cb = reinterpret_cast<cb_t>(dlsym(handle, "unregister_pythonscript_types"));
    const char *dlsym_error = dlerror();
    if (dlsym_error) {
        std::stringstream ss;
        ss << "Cannot load symbol 'unregister_pythonscript_types': " << dlsym_error;
        ERR_EXPLAIN(ss.str().c_str())
        ERR_FAIL();
    }
    cb();

    dlclose(handle);
    handle = NULL;
}

#endif
