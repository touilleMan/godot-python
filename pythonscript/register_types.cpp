// Pythonscript imports
#include "py_language.h"
#include "py_loader.h"
#include "py_script.h"

PyLanguage *script_language_py = NULL;
ResourceFormatLoaderPyScript *resource_loader_py = NULL;
ResourceFormatSaverPyScript *resource_saver_py = NULL;

void register_pythonscript_types() {
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
}
