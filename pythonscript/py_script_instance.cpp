#include "py_script_language.h"
#include "py_script.h"
#include "py_script_instance.h"

#if 0
class ScriptInstance {
public:


    virtual bool set(const StringName& p_name, const Variant& p_value)=0;
    virtual bool get(const StringName& p_name, Variant &r_ret) const=0;
    virtual void get_property_list(List<PropertyInfo> *p_properties) const=0;
    virtual Variant::Type get_property_type(const StringName& p_name,bool *r_is_valid=NULL) const=0;

    virtual void get_property_state(List<Pair<StringName,Variant> > &state);

    virtual void get_method_list(List<MethodInfo> *p_list) const=0;
    virtual bool has_method(const StringName& p_method) const=0;
    virtual Variant call(const StringName& p_method,VARIANT_ARG_LIST);
    virtual Variant call(const StringName& p_method,const Variant** p_args,int p_argcount,Variant::CallError &r_error)=0;
    virtual void call_multilevel(const StringName& p_method,VARIANT_ARG_LIST);
    virtual void call_multilevel(const StringName& p_method,const Variant** p_args,int p_argcount);
    virtual void call_multilevel_reversed(const StringName& p_method,const Variant** p_args,int p_argcount);
    virtual void notification(int p_notification)=0;

    //this is used by script languages that keep a reference counter of their own
    //you can make make Ref<> not die when it reaches zero, so deleting the reference
    //depends entirely from the script

    virtual void refcount_incremented() {}
    virtual bool refcount_decremented() { return true; } //return true if it can die

    virtual Ref<Script> get_script() const=0;

    virtual bool is_placeholder() const { return false; }

    enum RPCMode {
        RPC_MODE_DISABLED,
        RPC_MODE_REMOTE,
        RPC_MODE_SYNC,
        RPC_MODE_MASTER,
        RPC_MODE_SLAVE,
    };

    virtual RPCMode get_rpc_mode(const StringName& p_method) const=0;
    virtual RPCMode get_rset_mode(const StringName& p_variable) const=0;

    virtual ScriptLanguage *get_language()=0;
    virtual ~ScriptInstance();
};

#endif


bool PyInstance::set(const StringName& p_name, const Variant& p_value) {

#if 0
    //member
    {
        const Map<StringName,PyScript::MemberInfo>::Element *E = script->member_indices.find(p_name);
        if (E) {
            if (E->get().setter) {
                const Variant *val=&p_value;
                Variant::CallError err;
                call(E->get().setter,&val,1,err);
                if (err.error==Variant::CallError::CALL_OK) {
                    return true; //function exists, call was successful
                }
            }
            else
                members[E->get().index] = p_value;
            return true;
        }
    }

    PyScript *sptr=script.ptr();
    while(sptr) {


        Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(PyScriptLanguage::get_singleton()->strings._set);
        if (E) {

            Variant name=p_name;
            const Variant *args[2]={&name,&p_value};

            Variant::CallError err;
            Variant ret = E->get()->call(this,(const Variant**)args,2,err);
            if (err.error==Variant::CallError::CALL_OK && ret.get_type()==Variant::BOOL && ret.operator bool())
                return true;
        }
        sptr = sptr->_base;
    }
#endif
    return false;
}


bool PyInstance::get(const StringName& p_name, Variant &r_ret) const {

#if 0
    const PyScript *sptr=script.ptr();
    while(sptr) {

        {
            const Map<StringName,PyScript::MemberInfo>::Element *E = script->member_indices.find(p_name);
            if (E) {
                if (E->get().getter) {
                    Variant::CallError err;
                    r_ret=const_cast<PyInstance*>(this)->call(E->get().getter,NULL,0,err);
                    if (err.error==Variant::CallError::CALL_OK) {
                        return true;
                    }
                }
                r_ret=members[E->get().index];
                return true; //index found

            }
        }

        {

            const PyScript *sl = sptr;
            while(sl) {
                const Map<StringName,Variant>::Element *E = sl->constants.find(p_name);
                if (E) {
                    r_ret=E->get();
                    return true; //index found

                }
                sl=sl->_base;
            }
        }

        {
            const Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(PyScriptLanguage::get_singleton()->strings._get);
            if (E) {

                Variant name=p_name;
                const Variant *args[1]={&name};

                Variant::CallError err;
                Variant ret = const_cast<GDFunction*>(E->get())->call(const_cast<PyInstance*>(this),(const Variant**)args,1,err);
                if (err.error==Variant::CallError::CALL_OK && ret.get_type()!=Variant::NIL) {
                    r_ret=ret;
                    return true;
                }
            }
        }
        sptr = sptr->_base;
    }
#endif
    return false;

}


Ref<Script> PyInstance::get_script() const {

    return script;
}


ScriptLanguage *PyInstance::get_language() {

    return PyScriptLanguage::get_singleton();
}
