// Backend imports
#if BACKEND_CPYTHON
#include "Python.h"
#else
// TODO: pypy
#endif
// PyBind11 imports
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
// Pythonscript imports
#include "py_language.h"
#include "py_script.h"
#include "py_loader.h"


namespace py = pybind11;


PyLanguage *script_language_py = NULL;
ResourceFormatLoaderPyScript *resource_loader_py = NULL;
ResourceFormatSaverPyScript *resource_saver_py = NULL;


void register_pythonscript_types() {
#ifdef BACKEND_CPYTHON
    Py_SetProgramName(L"godot");  /* optional but recommended */
    // Py_SetPythonHome(PYTHON_HOME);
    Py_Initialize();
#else
    // TODO: pypy
#endif

    ClassDB::register_class<PyScript>();

    script_language_py = memnew(PyLanguage);
    ScriptServer::register_language(script_language_py);

    resource_loader_py = memnew(ResourceFormatLoaderPyScript);
    ResourceLoader::add_resource_format_loader(resource_loader_py);
    resource_saver_py = memnew(ResourceFormatSaverPyScript);
    ResourceSaver::add_resource_format_saver(resource_saver_py);
}


void unregister_pythonscript_types() {
    ScriptServer::unregister_language(script_language_py);

    if (script_language_py)
        memdelete(script_language_py);
    if (resource_loader_py)
        memdelete(resource_loader_py);
    if (resource_saver_py)
        memdelete(resource_saver_py);

#ifdef BACKEND_CPYTHON
    Py_FinalizeEx()
#else
    // TODO: pypy
#endif
}



#if 0

void register_pythonscript_types() {
    py::object scope = py::module::import("__main__").attr("__dict__");
    py::eval<py::eval_statements>("import sys\n"
                                  "print(sys.path)\n", scope);
    // PyRun_SimpleString("import sys\n"
    //                    "print(sys.path)\n");
    PyRun_String("import sys\nprint(sys.path)\n", Py_file_input, PyEval_GetGlobals(), PyEval_GetGlobals());
    // PyRun_SimpleString("from time import time,ctime\n"
    //                    "print('Today is', ctime(time()))\n");
    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    // PyMem_RawFree(program);
}
#endif
