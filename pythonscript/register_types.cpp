// Pythonscript imports
// #include "Python.h"
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>

namespace py = pybind11;



void register_pythonscript_types() {
    Py_SetProgramName(L"godot");  /* optional but recommended */
    Py_SetPythonHome(PYTHON_HOME);
    Py_Initialize();
    py::eval<py::eval_statements>("import sys\n"
                                  "print(sys.path)\n");
    // PyRun_SimpleString("import sys\n"
    //                    "print(sys.path)\n");
    // PyRun_SimpleString("from time import time,ctime\n"
    //                    "print('Today is', ctime(time()))\n");
    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    // PyMem_RawFree(program);
}


void unregister_pythonscript_types() {
}
