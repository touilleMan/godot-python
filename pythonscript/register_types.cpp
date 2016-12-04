#include "py_language.h"
#include "py_script.h"
#include "py_loader.h"


PyLanguage *script_language_py = NULL;
ResourceFormatLoaderPyScript *resource_loader_py = NULL;
ResourceFormatSaverPyScript *resource_saver_py = NULL;

#if 0
class PyNativeClass: public Reference {
    OBJ_TYPE(PyNativeClass, Reference);
private:
    mp_obj_t mp_cls;

protected:
    static void _bind_methods() {
        auto func = [] () { cout << "Hello world"; };
        ObjectTypeDB::bind_method("add",&Sumator::add);
        ObjectTypeDB::bind_method("reset",&Sumator::reset);
        ObjectTypeDB::bind_method("get_total",&Sumator::get_total);
    }

public:
    static void initialize_type() {
        static bool initialized=false;
        if (initialized)
            return;
        m_inherits::initialize_type();
        ObjectTypeDB::_add_type<m_type>();
        if (m_type::_get_bind_methods() != m_inherits::_get_bind_methods())
            _bind_methods();
        initialized=true;
    }

public:
    PyNativeClass(mp_obj_t mp_cls): mp_cls(mp_cls);
}

void register_mp_obj(mp_obj_t mp_obj) {

}
#endif


void register_pythonscript_types() {

    ObjectTypeDB::register_type<PyScript>();
    // ObjectTypeDB::register_virtual_type<PyFunctionState>();

    script_language_py = memnew(PyLanguage);
    ScriptServer::register_language(script_language_py);

    resource_loader_py = memnew(ResourceFormatLoaderPyScript);
    ResourceLoader::add_resource_format_loader(resource_loader_py);
    resource_saver_py = memnew(ResourceFormatSaverPyScript);
    ResourceSaver::add_resource_format_saver(resource_saver_py);

    // Update sys path
#if 0
    mp_obj_list_append(mp_sys_path, MP_OBJ_NEW_QSTR(qstr_from_str("/home/emmanuel/projects/godot-python/example")));
    mp_execute_expr("import godot");
    mp_execute_expr("import player");
    mp_obj_t mp_player_cls = mp_execute_expr("godot.get_exposed_class_per_module('player')");
    // mp_obj_print(mp_player_cls, PRINT_REPR);

    ERR_EXPLAIN("Module didn't defined an exported class.");
    ERR_FAIL_COND(mp_player_cls == mp_const_none);
    // register_type only works for static c++ class, we have to do it freestyle here !
    // ObjectTypeDB::register_type<PyScript>();

    ERR_FAIL_COND(!MP_OBJ_IS_OBJ(mp_player_cls));
    // TODO: make sure it inherit godot Variant base classe
    mp_obj_type_t *p_mp_player_cls = static_cast<mp_obj_type_t*>(MP_OBJ_TO_PTR(mp_player_cls));
// mp_obj_type_t *type = mp_obj_get_type(fun_in);


    const StringName type = StaticCString::create(qstr_str(MP_OBJ_QSTR_VALUE(p_mp_player_cls->name)));
    // TODO: segfault when retrieving qstr...
    // const StringName inherits = StaticCString::create(qstr_str(MP_OBJ_QSTR_VALUE(p_mp_player_cls->base.type->name)));
    const StringName inherits = StaticCString::create("Object");
    ObjectTypeDB::_add_type2(type, inherits);
#endif
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
