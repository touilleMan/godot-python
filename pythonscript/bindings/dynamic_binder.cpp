#include <cstring>

// Lazy Fucker implementation
#include "dynamic_binder.h"
#include "converter.h"

#include "micropython.h"


GodotBindingsModule::GodotBindingsModule() {
    // Module is created now to be able to reference it elsewhere,
    // however it is really populated within `init()`
    this->_mp_module = mp_obj_new_module(qstr_from_str("godot.bindings"));
}


void GodotBindingsModule::init() {
    if (this->_initialized) {
        return;
    }
    this->_initialized = true;
    // Retrieve and create all the modules for freeeeeeeee !
    List<StringName> types;
    ObjectTypeDB::get_type_list(&types);
    for(auto E=types.front(); E; E=E->next()) {
        // WARN_PRINTS("Start building " + String(E->get()));
        auto binder = memnew(DynamicBinder(E->get()));
        const mp_obj_type_t *type = binder->get_mp_type();
        mp_store_attr(this->_mp_module, type->name, MP_OBJ_FROM_PTR(type));
        this->_binders.push_back(binder);
    }
}


GodotBindingsModule::~GodotBindingsModule() {
    if (!this->_initialized) {
        return;
    }
    for(auto E=this->_binders.front(); E; E=E->next()) {
        memdelete(E->get());
    }
}


// Generate a python function calling `callback` with data as first
// parameter, usefull for dynamically create the binding functions
static mp_obj_t _generate_custom_trampoline(mp_obj_t callback, mp_obj_t data) {
    // Hold my beer...

    auto compile = [](const char *src) -> mp_obj_t {
        mp_lexer_t *lex = mp_lexer_new_from_str_len(MP_QSTR__lt_stdin_gt_, src, strlen(src), false);
        mp_parse_tree_t pt = mp_parse(lex, MP_PARSE_SINGLE_INPUT);
        mp_obj_t fun = mp_compile(&pt, lex->source_name, MP_EMIT_OPT_NONE, true);
        return fun;
    };

    nlr_buf_t nlr;
    if (nlr_push(&nlr) == 0) {
        // First thing to do: compile this code...
        const char src[] = "" \
            "def builder():\n" \
            "    cb = __global_cb\n" \
            "    data = __global_data\n" \
            "    def trampoline(*args):\n" \
            "        return cb(data, *args)\n" \
            "    return trampoline\n";
        mp_obj_t gen_fun = compile(src);

        const qstr cb_name = qstr_from_str("__global_cb");
        const qstr data_name = qstr_from_str("__global_data");
        const qstr builder_name = qstr_from_str("builder");

        // Now execute the code to create a builder function in our scope
        // Note that given we are extra-confident, we don't even bother to
        // set up a nlr context to catch exceptions...
        mp_call_function_n_kw(gen_fun, 0, 0, NULL);

        // Now set the configuration through global variables,
        // then call the builder to retrieve our custom trampoline !
        mp_store_name(cb_name, callback);
        mp_store_name(data_name, data);
        auto builder = mp_load_name(builder_name);
        auto trampoline = mp_call_function_n_kw(builder, 0, 0, NULL);

        // Don't forget to clean the scope before leaving
        mp_delete_name(cb_name);
        mp_delete_name(data_name);
        mp_delete_name(builder_name);

        return trampoline;
    } else {
        mp_obj_print_exception(&mp_plat_print, (mp_obj_t)nlr.ret_val);
        // uncaught exception
        return mp_const_none;
    }
}


static mp_obj_t _wrap_godot_method(StringName type_name, StringName method_name) {
    // TODO: micropython doesn't allow to store a name for native functions
    // TODO: don't use `m_new_obj` but good old' `malloc` to avoid useless
    // python gc work on those stay-forever functions
    auto p_method_bind = ObjectTypeDB::get_method(type_name, method_name);
    // It seems methods starting with "_" are considered private so ignore them
    if (!p_method_bind) {
        WARN_PRINTS("--- Bad Binding " + String(type_name) + ":" + String(method_name));
        return mp_const_none;
    // } else {
    //     WARN_PRINTS("+++ Good Binding " + String(type_name) + ":" + String(method_name));
    }

    // Define the wrapper function that is responsible to:
    // - Convert arguments to python obj
    // - Call the godot method from p_method_bind pointer passed as first argument
    // - Convert back result to Variant
    // - Handle call errors as python exceptions
    auto caller_fun = m_new_obj(mp_obj_fun_builtin_var_t);
    caller_fun->base.type = &mp_type_fun_builtin_var;
    caller_fun->is_kw = false;
    // Godot doesn't count self as an argument but python does
    // we will also be passed `p_method_bind` by the trampoline caller
    caller_fun->n_args_min = p_method_bind->get_argument_count() + 2;
    caller_fun->n_args_max = p_method_bind->get_argument_count() + 2;
    caller_fun->fun.var = [](size_t n, const mp_obj_t *args) -> mp_obj_t {
        // First arg is the p_method_bind
        auto p_method_bind = static_cast<MethodBind *>(args[0]);
        auto self = static_cast<mp_godot_bind_t *>(args[1]);
        // Remove self and also don't pass p_method_bind as argument
        const int godot_n = n - 2;
        // TODO: convert argument
        const Variant def_arg;
        const Variant *godot_args[godot_n];
        for (int i = 0; i < godot_n; ++i) {
            // godot_args[i] = pyobj_to_variant(args[i]);
            godot_args[i] = &def_arg;
        }
        Variant::CallError err;
        Variant ret = p_method_bind->call(self->godot_obj, godot_args, godot_n, err);
        if (err.error != Variant::CallError::CALL_OK) {
            // Throw exception
            // TODO: improve error message...
            nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Tough shit dude..."));
        }
        // TODO: convert return
        return variant_to_pyobj(ret);
        // return mp_const_none;
    };

    // Yes, p_method_bind is not an mp_obj_t... but it's only to pass to caller_fun
    auto trampoline = _generate_custom_trampoline(caller_fun, static_cast<mp_obj_t>(p_method_bind));

    return trampoline;
}


static mp_obj_t _mp_type_make_new(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) {
    auto p_type_binder = static_cast<const DynamicBinder *>(type->protocol);
    // TODO: optimize this by using TypeInfo::creation_func ?
    Object *godot_obj = ObjectTypeDB::instance(p_type_binder->get_type_name());
    mp_godot_bind_t *obj = m_new_obj_with_finaliser(mp_godot_bind_t);
    obj->base.type = type;
    obj->godot_obj = godot_obj;
    return MP_OBJ_FROM_PTR(obj);
}


static void _mp_type_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
    auto obj = static_cast<mp_godot_bind_t *>(MP_OBJ_TO_PTR(self_in));
    auto p_type_binder = static_cast<const DynamicBinder *>(obj->base.type->protocol);
    p_type_binder->get_attr(self_in, attr, dest);
}


void DynamicBinder::get_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) const {
    // Try to retrieve the attr as a method
    auto E = this->method_lookup.find(attr);
    if (E != NULL) {
        // attr is a method
        if (dest[0] == MP_OBJ_NULL) {
            // do a load
            dest[0] = E->get();
            dest[1] = self_in;
        }
#if 0
    } else {
        // TODO
        // We consider attr is a property
        if (dest[0] == MP_OBJ_NULL) {
            // do a load
            Variant r_value;
            if (ObjectTypeDB::get_property(o->godot_obj->ptr(), attr_name, r_value)) {
                // attr was actually a property
                // TODO:convert r_value to py object
                dest[0] = mp_const_none;
            }
        } else if (dest[1] != MP_OBJ_NULL) {
            // do a store
            bool r_valid = false;
            // TODO: convert dest[1] to variant
            Variant value = Variant(true);
            if (ObjectTypeDB::set_property(o->godot_obj->ptr(), attr_name, value, r_valid) && r_valid) {
                // attr was actually a property
                dest[0] = MP_OBJ_NULL;
            }
        }
#endif
    }
    // All other cases fail (i.e. don't modify `dest`)   
}


DynamicBinder::DynamicBinder(StringName type_name) : _type_name(type_name) {
    // Retrieve method&property from ObjectTypeDB and cook what can
    // be for faster runtime lookup
    // TODO: get inherited properties/methods as well ?
    List<PropertyInfo> properties;
    ObjectTypeDB::get_property_list(type_name, &properties, true);
    for(List<PropertyInfo>::Element *E=properties.front();E;E=E->next()) {
        const PropertyInfo info = E->get();
        this->property_lookup.insert(qstr_from_str(info.name.utf8().get_data()), info);
    }
    List<MethodInfo> methods;
    ObjectTypeDB::get_method_list(type_name, &methods, true);
    for(List<MethodInfo>::Element *E=methods.front();E;E=E->next()) {
        const MethodInfo info = E->get();
        const auto qstr_name = qstr_from_str(info.name.utf8().get_data());
        const auto mpo_method = _wrap_godot_method(type_name, info.name);
        if (mpo_method != mp_const_none) {
            this->method_lookup.insert(qstr_name, mpo_method);
        }
    }

    const String s_name = String(this->_type_name);
    this->_mp_type = {
        { &mp_type_type },
        .name = qstr_from_str(s_name.utf8().get_data()),
        .make_new = _mp_type_make_new,
        .attr = _mp_type_attr,
        .protocol = static_cast<void *>(this)
    };   
}
