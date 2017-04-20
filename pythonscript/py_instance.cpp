// Pythonscript imports
#include "py_language.h"
#include "py_script.h"
#include "py_instance.h"
#include "cffi_bindings/api.h"

#include "core/variant.h"


bool PyInstance::set(const StringName& p_name, const Variant& p_value) {
    DEBUG_TRACE_METHOD();

    const wchar_t *propname = String(p_name).c_str();
    return pybind_set_prop(this->_py_obj2, propname, (const godot_variant*)&p_value);
}


bool PyInstance::get(const StringName& p_name, Variant &r_ret) const {
    DEBUG_TRACE_METHOD();

    const wchar_t *propname = String(p_name).c_str();
    return pybind_get_prop(this->_py_obj2, propname, (godot_variant*)&r_ret);
}


Ref<Script> PyInstance::get_script() const {
    DEBUG_TRACE_METHOD();

    return this->_script;
}


ScriptLanguage *PyInstance::get_language() {
    DEBUG_TRACE_METHOD();

    return PyLanguage::get_singleton();
}


Variant::Type PyInstance::get_property_type(const StringName& p_name,bool *r_is_valid) const {
    DEBUG_TRACE_METHOD();


#if 0
    const PyScript *sptr=script.ptr();
    while(sptr) {

        if (sptr->member_info.has(p_name)) {
            if (r_is_valid)
                *r_is_valid=true;
            return sptr->member_info[p_name].type;
        }
        sptr = sptr->_base;
    }

    if (r_is_valid)
        *r_is_valid=false;
#endif
    return Variant::NIL;
}

void PyInstance::get_property_list(List<PropertyInfo> *p_properties) const {
    DEBUG_TRACE_METHOD();
#if 0
    // exported members, not doen yet!

    const PyScript *sptr=script.ptr();
    List<PropertyInfo> props;

    while(sptr) {


        const Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(PyScriptLanguage::get_singleton()->strings._get_property_list);
        if (E) {


            Variant::CallError err;
            Variant ret = const_cast<GDFunction*>(E->get())->call(const_cast<PyInstance*>(this),NULL,0,err);
            if (err.error==Variant::CallError::CALL_OK) {

                if (ret.get_type()!=Variant::ARRAY) {

                    ERR_EXPLAIN("Wrong type for _get_property list, must be an array of dictionaries.");
                    ERR_FAIL();
                }
                Array arr = ret;
                for(int i=0;i<arr.size();i++) {

                    Dictionary d = arr[i];
                    ERR_CONTINUE(!d.has("name"));
                    ERR_CONTINUE(!d.has("type"));
                    PropertyInfo pinfo;
                    pinfo.type = Variant::Type( d["type"].operator int());
                    ERR_CONTINUE(pinfo.type<0 || pinfo.type>=Variant::VARIANT_MAX );
                    pinfo.name = d["name"];
                    ERR_CONTINUE(pinfo.name=="");
                    if (d.has("hint"))
                        pinfo.hint=PropertyHint(d["hint"].operator int());
                    if (d.has("hint_string"))
                        pinfo.hint_string=d["hint_string"];
                    if (d.has("usage"))
                        pinfo.usage=d["usage"];

                    props.push_back(pinfo);

                }

            }
        }

        //instance a fake script for editing the values

        Vector<_PyScriptMemberSort> msort;
        for(Map<StringName,PropertyInfo>::Element *E=sptr->member_info.front();E;E=E->next()) {

            _PyScriptMemberSort ms;
            ERR_CONTINUE(!sptr->member_indices.has(E->key()));
            ms.index=sptr->member_indices[E->key()].index;
            ms.name=E->key();
            msort.push_back(ms);

        }

        msort.sort();
        msort.invert();
        for(int i=0;i<msort.size();i++) {

            props.push_front(sptr->member_info[msort[i].name]);

        }
#if 0
        if (sptr->member_functions.has("_get_property_list")) {

            Variant::CallError err;
            GDFunction *f = const_cast<GDFunction*>(sptr->member_functions["_get_property_list"]);
            Variant plv = f->call(const_cast<PyInstance*>(this),NULL,0,err);

            if (plv.get_type()!=Variant::ARRAY) {

                ERR_PRINT("_get_property_list: expected array returned");
            } else {

                Array pl=plv;

                for(int i=0;i<pl.size();i++) {

                    Dictionary p = pl[i];
                    PropertyInfo pinfo;
                    if (!p.has("name")) {
                        ERR_PRINT("_get_property_list: expected 'name' key of type string.")
                                continue;
                    }
                    if (!p.has("type")) {
                        ERR_PRINT("_get_property_list: expected 'type' key of type integer.")
                                continue;
                    }
                    pinfo.name=p["name"];
                    pinfo.type=Variant::Type(int(p["type"]));
                    if (p.has("hint"))
                        pinfo.hint=PropertyHint(int(p["hint"]));
                    if (p.has("hint_string"))
                        pinfo.hint_string=p["hint_string"];
                    if (p.has("usage"))
                        pinfo.usage=p["usage"];


                    props.push_back(pinfo);
                }
            }
        }
#endif

        sptr = sptr->_base;
    }

    //props.invert();

    for (List<PropertyInfo>::Element *E=props.front();E;E=E->next()) {

        p_properties->push_back(E->get());
    }
#endif
}

void PyInstance::get_method_list(List<MethodInfo> *p_list) const {
    DEBUG_TRACE_METHOD();
#if 0

    const PyScript *sptr=script.ptr();
    while(sptr) {

        for (Map<StringName,GDFunction*>::Element *E = sptr->member_functions.front();E;E=E->next()) {

            MethodInfo mi;
            mi.name=E->key();
            mi.flags|=METHOD_FLAG_FROM_SCRIPT;
            for(int i=0;i<E->get()->get_argument_count();i++)
                mi.arguments.push_back(PropertyInfo(Variant::NIL,"arg"+itos(i)));
            p_list->push_back(mi);
        }
        sptr = sptr->_base;
    }

#endif
}

bool PyInstance::has_method(const StringName& p_method) const {
    DEBUG_TRACE_METHOD();
#if 0

    const PyScript *sptr=script.ptr();
    while(sptr) {
        const Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(p_method);
        if (E)
            return true;
        sptr = sptr->_base;
    }

#endif
    return false;
}


Variant PyInstance::call(const StringName& p_method, const Variant **p_args, int p_argcount, Variant::CallError &r_error) {
    DEBUG_TRACE_METHOD_ARGS(" : " << String(p_method).utf8());
    // TODO: precompute p_method lookup for faster access
    Variant ret;
    pybind_call_meth(this->_py_obj2, String(p_method).c_str(), (void **)p_args, p_argcount, &ret, (int*)&r_error.error);
    // TODO handle argument/type attributes
    if (r_error.error) {
        r_error.argument = 0;
        r_error.expected = Variant::NIL;
    }
    return ret;
#if 0

    //printf("calling %ls:%i method %ls\n", script->get_path().c_str(), -1, String(p_method).c_str());

    PyScript *sptr=script.ptr();
    while(sptr) {
        Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(p_method);
        if (E) {
            return E->get()->call(this,p_args,p_argcount,r_error);
        }
        sptr = sptr->_base;
    }
    r_error.error=Variant::CallError::CALL_ERROR_INVALID_METHOD;
    return Variant();
#endif
}

#if 0  // TODO: Don't rely on default implementations provided by ScriptInstance ?
void PyInstance::call_multilevel(const StringName& p_method,const Variant** p_args,int p_argcount) {
    DEBUG_TRACE_METHOD_ARGS(" : " << String(p_method).utf8());

#if 0
    PyScript *sptr=script.ptr();
    Variant::CallError ce;

    while(sptr) {
        Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(p_method);
        if (E) {
            E->get()->call(this,p_args,p_argcount,ce);
        }
        sptr = sptr->_base;
    }
#endif

}


#if 0
void PyInstance::_ml_call_reversed(PyScript *sptr,const StringName& p_method,const Variant** p_args,int p_argcount) {

    if (sptr->_base)
        _ml_call_reversed(sptr->_base,p_method,p_args,p_argcount);

    Variant::CallError ce;

    Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(p_method);
    if (E) {
        E->get()->call(this,p_args,p_argcount,ce);
    }

}
#endif


void PyInstance::call_multilevel_reversed(const StringName& p_method,const Variant** p_args,int p_argcount) {
    DEBUG_TRACE_METHOD_ARGS(" : " << String(p_method).utf8());

#if 0
    if (script.ptr()) {
        _ml_call_reversed(script.ptr(),p_method,p_args,p_argcount);
    }
#endif
}
#endif  // Multilevel stuff


void PyInstance::notification(int p_notification) {
    DEBUG_TRACE_METHOD();
    // TODO

    // //notification is not virutal, it gets called at ALL levels just like in C.
    // Variant value=p_notification;
    // const Variant *args[1]={&value };

    // PyScript *sptr = this->_script.ptr();
    // while(sptr) {
    //     Map<StringName,GDFunction*>::Element *E = sptr->member_functions.find(PyScriptLanguage::get_singleton()->strings._notification);
    //     if (E) {
    //         Variant::CallError err;
    //         E->get()->call(this,args,1,err);
    //         if (err.error!=Variant::CallError::CALL_OK) {
    //             //print error about notification call

    //         }
    //     }
    //     sptr = sptr->_base;
    // }

}


PyInstance::RPCMode PyInstance::get_rpc_mode(const StringName& p_method) const {
    DEBUG_TRACE_METHOD();
    // TODO

    // const PyScript *cscript = script.ptr();

    // while(cscript) {
    //     const Map<StringName,GDFunction*>::Element *E=cscript->member_functions.find(p_method);
    //     if (E) {

    //         if (E->get()->get_rpc_mode()!=RPC_MODE_DISABLED) {
    //             return E->get()->get_rpc_mode();
    //         }

    //     }
    //     cscript=cscript->_base;
    // }

    return RPC_MODE_DISABLED;
}


PyInstance::RPCMode PyInstance::get_rset_mode(const StringName& p_variable) const {
    DEBUG_TRACE_METHOD();
    // TODO

    // const PyScript *cscript = script.ptr();

    // while(cscript) {
    //     const Map<StringName,PyScript::MemberInfo>::Element *E=cscript->member_indices.find(p_variable);
    //     if (E) {

    //         if (E->get().rpc_mode) {
    //             return E->get().rpc_mode;
    //         }

    //     }
    //     cscript=cscript->_base;
    // }

    return RPC_MODE_DISABLED;
}


PyInstance::PyInstance() {
    DEBUG_TRACE_METHOD();
}


bool PyInstance::init(PyScript *p_script, Object *p_owner) {
    DEBUG_TRACE_METHOD();

    this->_owner = p_owner;
    this->_owner_variant = Variant(p_owner);
    this->_script = Ref<PyScript>(p_script);
    this->_py_obj2 = pybind_wrap_gdobj_with_class(p_script->get_py_exposed_class(), p_owner);
    if (this->_py_obj2 == nullptr) {
        ERR_FAIL_V(false);
    }
    p_owner->set_script_instance(this);
    return true;
}


PyInstance::~PyInstance() {
    DEBUG_TRACE_METHOD();
    pybind_release_instance(this->_py_obj2);
}
