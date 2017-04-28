#pragma once

#if PYTHONSCRIPT_BACKEND == cpython
#define BACKEND_CPYTHON
#else
#error "Pypy is not supported yet :'-("
#define BACKEND_PYPY
#endif

#ifdef BACKEND_CPYTHON
#include "Python.h"
#else
// TODO: pypy
#endif

#include "cffi_bindings/api.h"

#define DEBUG_TRACE_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << ":" << __VA_ARGS__ << "\n")
#define DEBUG_TRACE_METHOD() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\t(" << (long)this << ")\n")
#define DEBUG_TRACE_METHOD_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << __VA_ARGS__ << "\t(" << (long)this << ")\n")
#define DEBUG_TRACE() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\n")

typedef void* cffi_handle;
