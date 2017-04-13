#include <stdlib.h>
// Godot imports
#include "core/global_config.h"
#include "core/os/os.h"
#include "core/os/file_access.h"
// Pythonscript imports
#include "pythonscript.h"
#include "py_language.h"
#include "py_script.h"
#include "static_bindings.h"
// #include "bindings/dynamic_binder.h"


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


void _init_sys_path_and_argv(String path) {
    String resource_path = GlobalConfig::get_singleton()->get_resource_path();
    String data_dir = OS::get_singleton()->get_data_dir();

    // Init sys.path list
    auto sys = py::module::import("sys");
    auto pathes = path.split(";");
    for (int i=0; i < pathes.size(); ++i) {
        auto curr_path = pathes[i];
        if (curr_path.begins_with("res://")) {
            // Keep on slash to make the path
            curr_path = curr_path.replace("res:/", resource_path);
        }
        else if (curr_path.begins_with("user://")) {
            if (data_dir != "") {
                // Keep on slash to make the path
                curr_path = curr_path.replace("user:/", data_dir);
            }
        }
        // TODO: should we shadow default modules ?
        // sys.attr("path").attr("append")(curr_path.utf8().get_data());
        sys.attr("path").attr("insert")(0, curr_path.utf8().get_data());
    }
    py::object scope = py::module::import("__main__").attr("__dict__");
    py::eval<py::eval_statements>("import sys\n"
                                  "print('PYTHON_PATH:', sys.path)\n", scope);

    // Init sys.argv
    sys.attr("argv") = py::list();
    sys.attr("argv").attr("append")(L"");
}


void PyLanguage::init() {
    DEBUG_TRACE_METHOD();
    // Register configuration
    auto globals = GlobalConfig::get_singleton();
    GLOBAL_DEF("python_script/path", "res://;res://lib");

    // Setup Python interpreter
    wchar_t name[6] = L"godot";
    Py_SetProgramName(name);  /* optional but recommended */
    Py_Initialize();
    if (pybind_init()) {
        ERR_PRINT("Couldn't initialize Python interpreter or CFFI bindings.");
        ERR_FAIL();
    }
    bindings::init();

    // TODO: think where to keep python standard lib ?
    // Py_SetPythonHome(globals->get("python_script/home"));
    try {
        _init_sys_path_and_argv(globals->get("python_script/path"));
    } catch(const py::error_already_set &e) {
        ERR_PRINT(e.what());
        ERR_FAIL();
    }

#if 0
    //populate global constants
    int gcc=GlobalConstants::get_global_constant_count();
    for(int i=0;i<gcc;i++) {

        _add_global(StaticCString::create(GlobalConstants::get_global_constant_name(i)),GlobalConstants::get_global_constant_value(i));
    }

    _add_global(StaticCString::create("PI"),Math_PI);

    //populate native classes

    List<StringName> class_list;
    ClassDB::get_type_list(&class_list);
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

    List<GlobalConfig::Singleton> singletons;
    GlobalConfig::get_singleton()->get_singletons(&singletons);
    for(List<GlobalConfig::Singleton>::Element *E=singletons.front();E;E=E->next()) {

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
    // TODO: Do we need to deinit the interpreter ?
    Py_FinalizeEx();
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

            Object *obj = ClassDB::get_instance(F->key());
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

#endif // if 0
PyLanguage::PyLanguage() {
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
