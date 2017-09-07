#ifndef PYTHONSCRIPT_H
#define PYTHONSCRIPT_H

#ifndef BACKEND_CPYTHON
#ifndef BACKEND_PYPY
#error "one of BACKEND_CPYTHON/BACKEND_PYPY must be defined"
#endif
#endif

#include "Python.h"
#include "cffi_bindings/api.h"

#ifdef DEBUG_ENABLED

// #define DEBUG_TRACE_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << ":" << __VA_ARGS__ << "\n")
// #define DEBUG_TRACE_METHOD() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\t(" << (long)this << ")\n")
// #define DEBUG_TRACE_METHOD_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << __VA_ARGS__ << "\t(" << (long)this << ")\n")
// #define DEBUG_TRACE() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\n")

// #else

#define DEBUG_TRACE_ARGS(...)
#define DEBUG_TRACE_METHOD()
#define DEBUG_TRACE_METHOD_ARGS(...)
#define DEBUG_TRACE()

#endif

#endif // PYTHONSCRIPT_H
