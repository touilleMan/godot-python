#ifndef PY_SCRIPT_H
#define PY_SCRIPT_H

#include <iostream>
#include "micropython.h"
// Godot imports
#include "script_language.h"
// Pythonscript imports
#include "py_language.h"


#define DEBUG_TRACE_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << ":" << __VA_ARGS__ << "\n")
#define DEBUG_TRACE_METHOD() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\t(" << (long)this << ")\n")
#define DEBUG_TRACE_METHOD_ARGS(...) (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << __VA_ARGS__ << "\t(" << (long)this << ")\n")
#define DEBUG_TRACE() (std::cout << __FILE__ << ":" << __LINE__ << ":" << __func__ << "\n")


class PyInstance;


/**
 * PyScript represents two things at the same time:
 * 1) A Python script (e.g. `foo.py`) loaded into godot
 * 2) A Python class defined into this script and flagged to
 *    be exported (if available).
 */
class PyScript : public Script {

    OBJ_TYPE(PyScript, Script);

friend class PyInstance;
friend class PyLanguage;

private:

    bool tool;
    bool valid;

    struct MemberInfo {
        int index;
        StringName setter;
        StringName getter;
        ScriptInstance::RPCMode rpc_mode;

    };

    mp_obj_t _mpo_exposed_class;
    mp_obj_t _mpo_module;

    // Ref<PyNativeClass> native;
    Ref<PyScript> base;
    PyScript *_base; //fast pointer access
    // PyScript *_owner; //for subclasses
    Map<StringName,PropertyInfo> member_info;

    Set<Object*> _instances;
    //exported members
    String source;
    String path;
    String name;

    PyInstance* _create_instance(const Variant** p_args, int p_argcount, Object *p_owner);

protected:

    static void _bind_methods();

#ifdef TOOLS_ENABLED
    Set<PlaceHolderScriptInstance*> placeholders;
    virtual void _placeholder_erased(PlaceHolderScriptInstance *p_placeholder);
#endif
public:

    bool can_instance() const;

    Ref<Script> get_base_script() const; //for script inheritance

    StringName get_instance_base_type() const; // this may not work in all scripts, will return empty if so
    ScriptInstance* instance_create(Object *p_this);
    bool instance_has(const Object *p_this) const;


    bool has_source_code() const;
    String get_source_code() const;
    void set_source_code(const String& p_code);
    Error reload(bool p_keep_state=false);
    Error load_source_code(const String& p_path);

    bool has_method(const StringName& p_method) const;
    MethodInfo get_method_info(const StringName& p_method) const;

    bool is_tool() const { return tool; }

    String get_node_type() const;

    ScriptLanguage *get_language() const;

    bool has_script_signal(const StringName& p_signal) const;
    void get_script_signal_list(List<MethodInfo> *r_signals) const;

    bool get_property_default_value(const StringName& p_property,Variant& r_value) const;

    virtual void update_exports() {} //editor tool
    void get_script_method_list(List<MethodInfo> *p_list) const;
    void get_script_property_list(List<PropertyInfo> *p_list) const;

    PyScript();
    ~PyScript();
};


#endif // PY_SCRIPT_H
