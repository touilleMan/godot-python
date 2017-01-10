#include <stdlib.h>

#include "micropython.h"
// Pythonscript imports
#include "py_language.h"
#include "py_script.h"
#include "bindings/dynamic_binder.h"
// Godot imports
#include "core/globals.h"
#include "core/os/os.h"
#include "core/os/file_access.h"


/************* SCRIPT LANGUAGE **************/
/************* SCRIPT LANGUAGE **************/
/************* SCRIPT LANGUAGE **************/
/************* SCRIPT LANGUAGE **************/
/************* SCRIPT LANGUAGE **************/


// TODO: Allocate this dynamically ?
PyLanguage *PyLanguage::singleton = NULL;



String PyLanguage::get_name() const {

    return "Python";
}


/* LANGUAGE FUNCTIONS */

mp_obj_t PyLanguage::get_mp_exposed_class_from_module(const qstr qstr_module_name) {
    static mp_obj_t mpo_get_exposed_class_per_module = 0;
    mp_obj_t mpo_exposed_cls = mp_const_none;
    const auto import_module = [this, &qstr_module_name, &mpo_exposed_cls]() {
        if (!mpo_get_exposed_class_per_module) {
            mpo_get_exposed_class_per_module = mp_load_attr(
                this->_mpo_godot_module, qstr_from_str("get_exposed_class_per_module"));
        }
        mpo_exposed_cls = mp_call_function_1(mpo_get_exposed_class_per_module, MP_OBJ_NEW_QSTR(qstr_module_name));
    };
    MP_WRAP_CALL(import_module);
    return mpo_exposed_cls;
}


void _mp_init_sys_path_and_argv(String path) {
    String resource_path = Globals::get_singleton()->get_resource_path();
    String data_dir = OS::get_singleton()->get_data_dir();
    printf("MITROPYTHON_PATH %s\n", path.utf8().get_data());

    // Init sys.path list
    auto pathes = path.split(";");
    mp_uint_t path_num = pathes.size() + 1; // [0] is for current dir (or base dir of the script)
    mp_obj_t *path_items;
    mp_obj_list_init(static_cast<mp_obj_list_t*>(MP_OBJ_TO_PTR(mp_sys_path)), path_num);
    mp_obj_list_get(mp_sys_path, &path_num, &path_items);
    path_items[0] = MP_OBJ_NEW_QSTR(MP_QSTR_);
    for (int i=0; i < pathes.size(); ++i) {
        auto curr_path = pathes[i];
        if (curr_path.begins_with("res://")) {
            curr_path = curr_path.replace("res:/", resource_path);
        }
        else if (curr_path.begins_with("user://")) {
            if (data_dir != "") {
                curr_path = curr_path.replace("user:/", data_dir);
            };
            curr_path = curr_path.replace("user://", "");
        }
        printf("-> %s\n", curr_path.utf8().get_data());
        path_items[i+1] = mp_obj_new_str(curr_path.utf8().get_data(), curr_path.length(), false);
    }

    // Init sys.argv
    mp_obj_list_init(static_cast<mp_obj_list_t*>(MP_OBJ_TO_PTR(mp_sys_argv)), 0);
}


void PyLanguage::init() {
    DEBUG_TRACE_METHOD();
    // Register configuration
    auto globals = Globals::get_singleton();
    GLOBAL_DEF("python_script/stack_size", 40 * 1024);
    GLOBAL_DEF("python_script/heap_size", 128 * 1024 * 1024);
    GLOBAL_DEF("python_script/path", "res://;res://lib");

    // MicroPython init
    // Initialized stack limit
    mp_stack_set_limit(globals->get("python_script/stack_size") * (BYTES_PER_WORD / 4));
    // Initialize heap
    int heap_size = globals->get("python_script/heap_size");
    this->_mp_heap = static_cast<char*>(malloc(heap_size));
    gc_init(this->_mp_heap, this->_mp_heap + heap_size);
    // Disable automatic garbage collection
    MP_STATE_MEM(gc_auto_collect_enabled) = 0;
    // Initialize interpreter
    mp_init();
    _mp_init_sys_path_and_argv(globals->get("python_script/path"));
    // Build the bindings module and store into as part of the main godot module
    init_bindings();
    // Load godot python module and connect it to PyLanguage
    mp_obj_t error = 0;
    auto import_module = [this]() {
        // Load the module into micropython
        qstr qstr_module_path = qstr_from_str("godot");
        this->_mpo_godot_module = mp_import_name(qstr_module_path, mp_const_none, MP_OBJ_NEW_SMALL_INT(0));
        mp_store_global(qstr_module_path, this->_mpo_godot_module);
        // // Retrieve module's exposed class
        // this->_mpo_exposed_classes_per_module = mp_load_method(
        //     mpo_godot_module, qstr_from_str("__exposed_classes_per_module"));
        // TODO: make the bindings creation lazy ?
        mp_obj_dict_t *mod_globals = static_cast<mp_obj_module_t *>(MP_OBJ_TO_PTR(this->_mpo_godot_module))->globals;
        auto bindings = GodotBindingsModule::get_singleton();
        mp_obj_dict_store(MP_OBJ_FROM_PTR(mod_globals), MP_OBJ_NEW_QSTR(qstr_from_str("bindings")), bindings->get_mp_module());
    };
    auto handle_ex = [&error](mp_obj_t ex) {
        mp_obj_print_exception(&mp_plat_print, ex);
        error = ex;
    };
    MP_WRAP_CALL_EX(import_module, handle_ex);
    ERR_FAIL_COND(error);
#if 0
    //populate global constants
    int gcc=GlobalConstants::get_global_constant_count();
    for(int i=0;i<gcc;i++) {

        _add_global(StaticCString::create(GlobalConstants::get_global_constant_name(i)),GlobalConstants::get_global_constant_value(i));
    }

    _add_global(StaticCString::create("PI"),Math_PI);

    //populate native classes

    List<StringName> class_list;
    ObjectTypeDB::get_type_list(&class_list);
    for(List<StringName>::Element *E=class_list.front();E;E=E->next()) {

        StringName n = E->get();
        String s = String(n);
        if (s.begins_with("_"))
            n=s.substr(1,s.length());

        if (globals.has(n))
            continue;
        Ref<PyNativeClass> nc = memnew( PyNativeClass(E->get()) );
        _add_global(n,nc);
    }

    //populate singletons

    List<Globals::Singleton> singletons;
    Globals::get_singleton()->get_singletons(&singletons);
    for(List<Globals::Singleton>::Element *E=singletons.front();E;E=E->next()) {

        _add_global(E->get().name,E->get().ptr);
    }
#endif
}


String PyLanguage::get_type() const {
    DEBUG_TRACE_METHOD();
    return "Python";
}


String PyLanguage::get_extension() const {

    return "py";
}


Error PyLanguage::execute_file(const String& p_path)  {
    DEBUG_TRACE_METHOD();
    // ??
    return OK;
}


void PyLanguage::finish()  {
    DEBUG_TRACE_METHOD();
    mp_deinit();
    free(this->_mp_heap);
    GodotBindingsModule::finish();
}


/* MULTITHREAD FUNCTIONS */


/* DEBUGGER FUNCTIONS */


PyLanguage::~PyLanguage() {
    DEBUG_TRACE_METHOD();
    singleton = NULL;
    if (lock) {
        memdelete(lock);
        lock=NULL;
    }
}


#if 0
struct PyScriptDepSort {

    //must support sorting so inheritance works properly (parent must be reloaded first)
    bool operator()(const Ref<PyScript> &A, const Ref<PyScript>& B) const {

        if (A==B)
            return false; //shouldn't happen but..
        const PyScript *I=B->get_base().ptr();
        while(I) {
            if (I==A.ptr()) {
                // A is a base of B
                return true;
            }

            I=I->get_base().ptr();
        }

        return false; //not a base
    }
};

void PyLanguage::reload_all_scripts() {



#ifdef DEBUG_ENABLED
    print_line("RELOAD ALL SCRIPTS");
    if (lock) {
        lock->lock();
    }

    List<Ref<PyScript> > scripts;

    SelfList<PyScript> *elem=script_list.first();
    while(elem) {
        if (elem->self()->get_path().is_resource_file()) {
            print_line("FOUND: "+elem->self()->get_path());
            scripts.push_back(Ref<PyScript>(elem->self())); //cast to gdscript to avoid being erased by accident
        }
        elem=elem->next();
    }

    if (lock) {
        lock->unlock();
    }

    //as scripts are going to be reloaded, must proceed without locking here

    scripts.sort_custom<PyScriptDepSort>(); //update in inheritance dependency order

    for(List<Ref<PyScript> >::Element *E=scripts.front();E;E=E->next()) {

        print_line("RELOADING: "+E->get()->get_path());
        E->get()->load_source_code(E->get()->get_path());
        E->get()->reload(true);
    }
#endif
}


void PyLanguage::reload_tool_script(const Ref<Script>& p_script,bool p_soft_reload) {


#ifdef DEBUG_ENABLED

    if (lock) {
        lock->lock();
    }

    List<Ref<PyScript> > scripts;

    SelfList<PyScript> *elem=script_list.first();
    while(elem) {
        if (elem->self()->get_path().is_resource_file()) {

            scripts.push_back(Ref<PyScript>(elem->self())); //cast to gdscript to avoid being erased by accident
        }
        elem=elem->next();
    }

    if (lock) {
        lock->unlock();
    }

    //when someone asks you why dynamically typed languages are easier to write....

    Map< Ref<PyScript>, Map<ObjectID,List<Pair<StringName,Variant> > > > to_reload;

    //as scripts are going to be reloaded, must proceed without locking here

    scripts.sort_custom<PyScriptDepSort>(); //update in inheritance dependency order

    for(List<Ref<PyScript> >::Element *E=scripts.front();E;E=E->next()) {

        bool reload = E->get()==p_script || to_reload.has(E->get()->get_base());

        if (!reload)
            continue;

        to_reload.insert(E->get(),Map<ObjectID,List<Pair<StringName,Variant> > >());

        if (!p_soft_reload) {

            //save state and remove script from instances
            Map<ObjectID,List<Pair<StringName,Variant> > >& map = to_reload[E->get()];

            while(E->get()->instances.front()) {
                Object *obj = E->get()->instances.front()->get();
                //save instance info
                List<Pair<StringName,Variant> > state;
                if (obj->get_script_instance()) {

                    obj->get_script_instance()->get_property_state(state);
                    map[obj->get_instance_ID()]=state;
                    obj->set_script(RefPtr());
                }
            }

            //same thing for placeholders
#ifdef TOOLS_ENABLED

            while(E->get()->placeholders.size()) {

                Object *obj = E->get()->placeholders.front()->get()->get_owner();
                //save instance info
                List<Pair<StringName,Variant> > state;
                if (obj->get_script_instance()) {

                    obj->get_script_instance()->get_property_state(state);
                    map[obj->get_instance_ID()]=state;
                    obj->set_script(RefPtr());
                }
            }
#endif

            for(Map<ObjectID,List<Pair<StringName,Variant> > >::Element *F=E->get()->pending_reload_state.front();F;F=F->next()) {
                map[F->key()]=F->get(); //pending to reload, use this one instead
            }
        }
    }

    for(Map< Ref<PyScript>, Map<ObjectID,List<Pair<StringName,Variant> > > >::Element *E=to_reload.front();E;E=E->next()) {

        Ref<PyScript> scr = E->key();
        scr->reload(p_soft_reload);

        //restore state if saved
        for (Map<ObjectID,List<Pair<StringName,Variant> > >::Element *F=E->get().front();F;F=F->next()) {

            Object *obj = ObjectDB::get_instance(F->key());
            if (!obj)
                continue;

            if (!p_soft_reload) {
                //clear it just in case (may be a pending reload state)
                obj->set_script(RefPtr());
            }
            obj->set_script(scr.get_ref_ptr());
            if (!obj->get_script_instance()) {
                //failed, save reload state for next time if not saved
                if (!scr->pending_reload_state.has(obj->get_instance_ID())) {
                    scr->pending_reload_state[obj->get_instance_ID()]=F->get();
                }
                continue;
            }

            for (List<Pair<StringName,Variant> >::Element *G=F->get().front();G;G=G->next()) {
                obj->get_script_instance()->set(G->get().first,G->get().second);
            }

            scr->pending_reload_state.erase(obj->get_instance_ID()); //as it reloaded, remove pending state
        }

        //if instance states were saved, set them!
    }


#endif
}


/* EDITOR FUNCTIONS */
void PyLanguage::get_reserved_words(List<String> *p_words) const  {

    static const char *_reserved_words[]={
        0};


    const char **w=_reserved_words;


    while (*w) {

        p_words->push_back(*w);
        w++;
    }

    for(int i=0;i<PyFunctions::FUNC_MAX;i++) {
        p_words->push_back(PyFunctions::get_func_name(PyFunctions::Function(i)));
    }

}

#endif // if 0
PyLanguage::PyLanguage() : _mpo_godot_module(mp_const_none) {
    DEBUG_TRACE_METHOD();
    ERR_FAIL_COND(this->singleton);
    this->singleton=this;

#ifdef NO_THREADS
    this->lock=NULL;
#else
    this->lock = Mutex::create();
#endif

#if 0
    calls=0;
    strings._init = StaticCString::create("_init");
    strings._notification = StaticCString::create("_notification");
    strings._set = StaticCString::create("_set");
    strings._get = StaticCString::create("_get");
    strings._get_property_list = StaticCString::create("_get_property_list");
    strings._script_source = StaticCString::create("script/source");
    _debug_parse_err_line = -1;
    _debug_parse_err_file = "";

#ifdef NO_THREADS
    lock = NULL;
#else
    lock = Mutex::create();
#endif
    profiling = false;
    script_frame_time = 0;

    _debug_call_stack_pos = 0;
    int dmcs = GLOBAL_DEF("debug/script_max_call_stack",1024);
    if (ScriptDebugger::get_singleton()) {
        //debugging enabled!

        _debug_max_call_stack = dmcs;
        if (_debug_max_call_stack < 1024)
            _debug_max_call_stack = 1024;
        _call_stack = memnew_arr( CallLevel, _debug_max_call_stack+1 );

    } else {
        _debug_max_call_stack = 0;
        _call_stack = NULL;
    }

#endif // if 0
}

