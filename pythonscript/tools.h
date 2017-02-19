#if PYTHONSCRIPT_BACKEND == 'cpython'
#define BACKEND_CPYTHON
#else
#error "Pypy is not supported yet :'-("
#define BACKEND_PYPY
#endif
