#ifndef PYTHONSCRIPT_PY_INSTANCE_H
#define PYTHONSCRIPT_PY_INSTANCE_H

// Pythonscript imports
// #include "py_script.h"
class PyScript;


/**
 * PyInstance is from Godot point of view an instance of a PyScript. However
 * from Python it's a binding on an instance of the exported Python class.
 */
class PyInstance : public ScriptInstance {
friend class PyScript;

private:

    Ref<PyScript> _script;
    Object *_owner;
    py::object _py_obj;

public:

    _FORCE_INLINE_ Object* get_owner() { return this->_owner; }

    virtual bool set(const StringName& p_name, const Variant& p_value);
    virtual bool get(const StringName& p_name, Variant &r_ret) const;
    virtual void get_property_list(List<PropertyInfo> *p_properties) const;
    virtual Variant::Type get_property_type(const StringName& p_name,bool *r_is_valid=NULL) const;

    virtual void get_method_list(List<MethodInfo> *p_list) const;
    virtual bool has_method(const StringName& p_method) const;

    virtual Variant call(const StringName& p_method,const Variant** p_args,int p_argcount,Variant::CallError &r_error);
    #if 0
    // Rely on default implementations provided by ScriptInstance for the moment.
    // Note that multilevel call could be removed in 3.0 release, so stay tunned
    // (see https://godotengine.org/qa/9244/can-override-the-_ready-and-_process-functions-child-classes)
    virtual void call_multilevel(const StringName& p_method,const Variant** p_args,int p_argcount);
    virtual void call_multilevel_reversed(const StringName& p_method,const Variant** p_args,int p_argcount);
    #endif

    virtual void notification(int p_notification);

    virtual Ref<Script> get_script() const;

    virtual ScriptLanguage *get_language();

    void set_path(const String& p_path);

    virtual RPCMode get_rpc_mode(const StringName& p_method) const;
    virtual RPCMode get_rset_mode(const StringName& p_variable) const;

    PyInstance();
    bool init(PyScript *p_script, Object *p_owner);
    ~PyInstance();

};

#endif // PYTHONSCRIPT_PY_INSTANCE_H
