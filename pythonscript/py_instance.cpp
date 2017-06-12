// Pythonscript imports
#include "py_instance.h"
#include "cffi_bindings/api.h"
#include "py_language.h"
#include "py_script.h"
// Godot imports
#include "core/os/os.h"
#include "core/variant.h"


bool PyInstance::set(const StringName &p_name, const Variant &p_value) {
	DEBUG_TRACE_METHOD();

	const wchar_t *propname = String(p_name).c_str();
	return pybind_set_prop(this->_py_obj, propname, (const godot_variant *)&p_value);
}

bool PyInstance::get(const StringName &p_name, Variant &r_ret) const {
	DEBUG_TRACE_METHOD();

	const wchar_t *propname = String(p_name).c_str();
	return pybind_get_prop(this->_py_obj, propname, (godot_variant *)&r_ret);
}

Ref<Script> PyInstance::get_script() const {
	DEBUG_TRACE_METHOD();

	return this->_script;
}

ScriptLanguage *PyInstance::get_language() {
	DEBUG_TRACE_METHOD();

	return PyLanguage::get_singleton();
}

Variant::Type PyInstance::get_property_type(const StringName &p_name, bool *r_is_valid) const {
	DEBUG_TRACE_METHOD();

	const wchar_t *propname = String(p_name).c_str();
	Variant::Type prop_type;
	const bool is_valid = pybind_get_prop_type(this->_py_obj, propname, (int *)&prop_type);
	if (r_is_valid) {
		*r_is_valid = is_valid;
	}
	return prop_type;
}

void PyInstance::get_property_list(List<PropertyInfo> *p_properties) const {
	DEBUG_TRACE_METHOD();
	this->_script.ptr()->get_script_property_list(p_properties);
}

void PyInstance::get_method_list(List<MethodInfo> *p_list) const {
	DEBUG_TRACE_METHOD();
	this->_script.ptr()->get_script_method_list(p_list);
}

bool PyInstance::has_method(const StringName &p_method) const {
	DEBUG_TRACE_METHOD();
	return this->_script.ptr()->has_method(p_method);
}

// #ifdef DEBUG_ENABLED
// void godot_method_bind_ptrcall_profiled(godot_method_bind *p_method_bind, godot_object *p_instance, const void **p_args, void *p_ret) {
//     uint64_t call_time;
//     uint64_t function_call_time;

//     if (GDScriptLanguage::get_singleton()->profiling) {
//         call_time = OS::get_singleton()->get_ticks_usec();
//     }

// 	MethodBind *mb = (MethodBind *)p_method_bind;
// 	Object *o = (Object *)p_instance;
//     godot_method_bind_ptrcall(p_method_bind, p_instance, p_args, p_ret);

//     if (GDScriptLanguage::get_singleton()->profiling) {
//         function_call_time += OS::get_singleton()->get_ticks_usec() - call_time;
//     }
// }
// #else
// #define godot_method_bind_ptrcall_profiled godot_method_bind_ptrcall
// #endif

Variant PyInstance::call(const StringName &p_method, const Variant **p_args, int p_argcount, Variant::CallError &r_error) {
	DEBUG_TRACE_METHOD_ARGS(" : " << String(p_method).utf8());
	// TODO: optimize when calling a Godot method from Godot to avoid param conversion
	// TODO: precompute p_method lookup for faster access
	Variant ret;
#ifdef DEBUG_ENABLED

	uint64_t function_start_time;
	// uint64_t function_call_time;

	PyLanguage::MethProfile *profile = nullptr;
	if (PyLanguage::get_singleton()->profiling) {
		StringName signature = ((PyScript *)this->get_script().ptr())->get_meth_signature(p_method);
		auto e = PyLanguage::get_singleton()->per_meth_profiling.find(signature);
		if (e == NULL) {
			PyLanguage::get_singleton()->per_meth_profiling[signature] = PyLanguage::MethProfile();
			e = PyLanguage::get_singleton()->per_meth_profiling.find(signature);
		}
		profile = &e->value();
		function_start_time = OS::get_singleton()->get_ticks_usec();
		profile->frame_call_count++;
	}
#endif

	// Instead of passing C++ Variant::CallError object through cffi, we compress
	// it arguments into a single int, yeah this is a hack ;-)
	int error = 0;
	pybind_call_meth(this->_py_obj, String(p_method).c_str(), (void **)p_args, p_argcount, &ret, &error);
	// TODO handle argument/type attributes
	r_error.error = (Variant::CallError::Error)(error & 0xFF);
	if (error) {
		r_error.argument = (error >> 2) & 0xFF;
		r_error.expected = (Variant::Type)(error >> 4);
	}

#ifdef DEBUG_ENABLED
	if (PyLanguage::get_singleton()->profiling) {
		uint64_t time_taken = OS::get_singleton()->get_ticks_usec() - function_start_time;
		profile->frame_total_time += time_taken;
		profile->frame_self_time += time_taken;
		// profile->frame_self_time += time_taken - function_call_time;
	}

#endif
	return ret;
}

#if 0 // TODO: Don't rely on default implementations provided by ScriptInstance ?
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
#endif // Multilevel stuff

void PyInstance::notification(int p_notification) {
	DEBUG_TRACE_METHOD();
	pybind_notification(this->_py_obj, p_notification);
}

PyInstance::RPCMode PyInstance::get_rpc_mode(const StringName &p_method) const {
	DEBUG_TRACE_METHOD();
	const wchar_t *methname = String(p_method).c_str();
	return (PyInstance::RPCMode)pybind_get_rpc_mode(this->_py_obj, methname);
}

PyInstance::RPCMode PyInstance::get_rset_mode(const StringName &p_variable) const {
	DEBUG_TRACE_METHOD();
	const wchar_t *varname = String(p_variable).c_str();
	return (PyInstance::RPCMode)pybind_get_rset_mode(this->_py_obj, varname);
}

PyInstance::PyInstance() {
	DEBUG_TRACE_METHOD();
}

bool PyInstance::init(PyScript *p_script, Object *p_owner) {
	DEBUG_TRACE_METHOD();

	this->_owner = p_owner;
	this->_owner_variant = Variant(p_owner);
	this->_script = Ref<PyScript>(p_script);
	this->_py_obj = pybind_wrap_gdobj_with_class(p_script->get_py_exposed_class(), p_owner);
	if (this->_py_obj == nullptr) {
		ERR_FAIL_V(false);
	}
	p_owner->set_script_instance(this);
	return true;
}

PyInstance::~PyInstance() {
	DEBUG_TRACE_METHOD();
	pybind_release_instance(this->_py_obj);
}
