// Godot imports
#include "os/file_access.h"
// Pythonscript imports
#include "py_loader.h"
#include "py_script.h"


RES ResourceFormatLoaderPyScript::load(const String &p_path, const String& p_original_path, Error *r_error)
{
	if (r_error)
		*r_error=ERR_FILE_CANT_OPEN;

	PyScript *script = memnew( PyScript );

	Ref<PyScript> scriptres(script);

	Error err = script->load_source_code(p_path);
	ERR_FAIL_COND_V(err != OK, RES());

	script->set_path(p_original_path);

	script->reload();

	if (r_error)
		*r_error=OK;

	return scriptres;
}

void ResourceFormatLoaderPyScript::get_recognized_extensions(List<String> *p_extensions) const
{
	p_extensions->push_back("py");
}

bool ResourceFormatLoaderPyScript::handles_type(const String& p_type) const
{
	return p_type == "Script" || p_type == "PyScript";
}

String ResourceFormatLoaderPyScript::get_resource_type(const String &p_path) const
{
	String el = p_path.get_extension().to_lower();
	if (el == "py")
		return "PyScript";
	return "";
}

Error ResourceFormatSaverPyScript::save(const String &p_path,const RES& p_resource,uint32_t p_flags)
{
	Ref<PyScript> sqscr = p_resource;
	ERR_FAIL_COND_V(sqscr.is_null(), ERR_INVALID_PARAMETER);

	String source = sqscr->get_source_code();

	Error err;
	FileAccess *file = FileAccess::open(p_path, FileAccess::WRITE, &err);
	ERR_FAIL_COND_V(err, err);

	file->store_string(source);
	if (file->get_error() != OK && file->get_error() != ERR_FILE_EOF) {
		memdelete(file);
		return ERR_CANT_CREATE;
	}
	file->close();
	memdelete(file);
	return OK;
}

void ResourceFormatSaverPyScript::get_recognized_extensions(const RES& p_resource,List<String> *p_extensions) const
{
	if (p_resource->cast_to<PyScript>()) {
		p_extensions->push_back("py");
	}
}

bool ResourceFormatSaverPyScript::recognize(const RES& p_resource) const
{
	return p_resource->cast_to<PyScript>() != NULL;
}
