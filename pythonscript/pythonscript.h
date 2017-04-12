#pragma once

#if PYTHONSCRIPT_BACKEND == cpython
# define BACKEND_CPYTHON
#else
# error "Pypy is not supported yet :'-("
# define BACKEND_PYPY
#endif

#ifdef BACKEND_CPYTHON
# include "Python.h"
#else
// TODO: pypy
#endif

// PyBind11 imports
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>

#include "cffi_bindings/api.h"

namespace py = pybind11;
