#ifndef PY_SCRIPT_LANGUAGE_H
#define PY_SCRIPT_LANGUAGE_H

// Microphython
#include "micropython/micropython.h"
// Godot imports
#include "core/script_language.h"
#include "core/self_list.h"
#include "core/io/resource_loader.h"
#include "core/io/resource_saver.h"


class PyScript;
class PyInstance;


class PyLanguage : public ScriptLanguage {
    friend class PyScript;
    friend class PyInstance;

    Mutex *lock;
    static PyLanguage *singleton;
    SelfList<PyScript>::List script_list;
    mp_obj_t _mpo_godot_module;
    char *_mp_heap;

public:
    /* CUSTOM PYTHONSCRIPT FUNCTIONS */
    mp_obj_t get_mp_exposed_class_from_module(const qstr qstr_module_name);
    _FORCE_INLINE_ mp_obj_t get_mp_exposed_class_from_module(const char *module_name) {return get_mp_exposed_class_from_module(qstr_from_str(module_name));}

    String get_name() const;
    _FORCE_INLINE_ static PyLanguage *get_singleton() { return singleton; }

    /* LANGUAGE FUNCTIONS */
    void init();
    String get_type() const;
    String get_extension() const;
    Error execute_file(const String& p_path) ;
    void finish();

    /* EDITOR FUNCTIONS */
    void get_reserved_words(List<String> *p_words) const;
    void get_comment_delimiters(List<String> *p_delimiters) const;
    void get_string_delimiters(List<String> *p_delimiters) const;
    Ref<Script> get_template(const String& p_class_name, const String& p_base_class_name) const;
    bool validate(const String& p_script, int &r_line_error,int &r_col_error,String& r_test_error, const String& p_path="",List<String> *r_functions=NULL) const;
    Script *create_script() const;
    bool has_named_classes() const;
    int find_function(const String& p_function,const String& p_code) const;
    String make_function(const String& p_class,const String& p_name,const PoolStringArray& p_args) const;
    // Error complete_code(const String& p_code, const String& p_base_path, Object*p_owner,List<String>* r_options,String& r_call_hint) { return ERR_UNAVAILABLE; }
    void auto_indent_code(String& p_code,int p_from_line,int p_to_line) const;
    void add_global_constant(const StringName& p_variable,const Variant& p_value);

    /* MULTITHREAD FUNCTIONS */

    //some VMs need to be notified of thread creation/exiting to allocate a stack
    // void thread_enter() {}
    // void thread_exit() {}

    /* DEBUGGER FUNCTIONS */

    String debug_get_error() const;
    int debug_get_stack_level_count() const;
    int debug_get_stack_level_line(int p_level) const;
    String debug_get_stack_level_function(int p_level) const;
    String debug_get_stack_level_source(int p_level) const;
    void debug_get_stack_level_locals(int p_level,List<String> *p_locals, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    void debug_get_stack_level_members(int p_level,List<String> *p_members, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    void debug_get_globals(List<String> *p_locals, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    String debug_parse_stack_level_expression(int p_level,const String& p_expression,int p_max_subitems=-1,int p_max_depth=-1);

    // virtual Vector<StackInfo> debug_get_current_stack_info() { return Vector<StackInfo>(); }

    void reload_all_scripts();
    void reload_tool_script(const Ref<Script>& p_script,bool p_soft_reload);
    /* LOADER FUNCTIONS */

    void get_recognized_extensions(List<String> *p_extensions) const;
    void get_public_functions(List<MethodInfo> *p_functions) const;
    void get_public_constants(List<Pair<String,Variant> > *p_constants) const;

    void profiling_start();
    void profiling_stop();

    int profiling_get_accumulated_data(ProfilingInfo *p_info_arr,int p_info_max);
    int profiling_get_frame_data(ProfilingInfo *p_info_arr,int p_info_max);

    void frame();

    ~PyLanguage();
    PyLanguage();
};




#if 0
class PyLanguage : public ScriptLanguage {

    static PyLanguage *singleton;

    Variant* _global_array;
    Vector<Variant> global_array;
    Map<StringName,int> globals;


    struct CallLevel {

        Variant *stack;
        PyFunction *function;
        PyInstance *instance;
        int *ip;
        int *line;

    };


    int _debug_parse_err_line;
    String _debug_parse_err_file;
    String _debug_error;
    int _debug_call_stack_pos;
    int _debug_max_call_stack;
    CallLevel *_call_stack;

    void _add_global(const StringName& p_name,const Variant& p_value);


    Mutex *lock;



friend class PyScript;

    SelfList<PyScript>::List script_list;
friend class PyFunction;

    SelfList<PyFunction>::List function_list;
    bool profiling;
    uint64_t script_frame_time;
public:


    int calls;

    bool debug_break(const String& p_error,bool p_allow_continue=true);
    bool debug_break_parse(const String& p_file, int p_line,const String& p_error);

    _FORCE_INLINE_ void enter_function(PyInstance *p_instance,PyFunction *p_function, Variant *p_stack, int *p_ip, int *p_line) {

        if (Thread::get_main_ID()!=Thread::get_caller_ID())
            return; //no support for other threads than main for now

        if (ScriptDebugger::get_singleton()->get_lines_left()>0 && ScriptDebugger::get_singleton()->get_depth()>=0)
            ScriptDebugger::get_singleton()->set_depth( ScriptDebugger::get_singleton()->get_depth() +1 );

        if (_debug_call_stack_pos >= _debug_max_call_stack) {
            //stack overflow
            _debug_error="Stack Overflow (Stack Size: "+itos(_debug_max_call_stack)+")";
            ScriptDebugger::get_singleton()->debug(this);
            return;
        }

        _call_stack[_debug_call_stack_pos].stack=p_stack;
        _call_stack[_debug_call_stack_pos].instance=p_instance;
        _call_stack[_debug_call_stack_pos].function=p_function;
        _call_stack[_debug_call_stack_pos].ip=p_ip;
        _call_stack[_debug_call_stack_pos].line=p_line;
        _debug_call_stack_pos++;
    }

    _FORCE_INLINE_ void exit_function() {

        if (Thread::get_main_ID()!=Thread::get_caller_ID())
            return; //no support for other threads than main for now

        if (ScriptDebugger::get_singleton()->get_lines_left()>0 && ScriptDebugger::get_singleton()->get_depth()>=0)
            ScriptDebugger::get_singleton()->set_depth( ScriptDebugger::get_singleton()->get_depth() -1 );

        if (_debug_call_stack_pos==0) {

            _debug_error="Stack Underflow (Engine Bug)";
            ScriptDebugger::get_singleton()->debug(this);
            return;
        }

        _debug_call_stack_pos--;
    }


    virtual Vector<StackInfo> debug_get_current_stack_info() {
        if (Thread::get_main_ID()!=Thread::get_caller_ID())
            return Vector<StackInfo>();

        Vector<StackInfo> csi;
        csi.resize(_debug_call_stack_pos);
        for(int i=0;i<_debug_call_stack_pos;i++) {
            csi[_debug_call_stack_pos-i-1].line=_call_stack[i].line?*_call_stack[i].line:0;
            csi[_debug_call_stack_pos-i-1].script=Ref<PyScript>(_call_stack[i].function->get_script());
        }
        return csi;
    }

    struct {

        StringName _init;
        StringName _notification;
        StringName _set;
        StringName _get;
        StringName _get_property_list;
        StringName _script_source;

    } strings;


    _FORCE_INLINE_ int get_global_array_size() const { return global_array.size(); }
    _FORCE_INLINE_ Variant* get_global_array() { return _global_array; }
    _FORCE_INLINE_ const Map<StringName,int>& get_global_map() { return globals; }

    _FORCE_INLINE_ static PyLanguage *get_singleton() { return singleton; }

    virtual String get_name() const;

    /* LANGUAGE FUNCTIONS */
    virtual void init();
    virtual String get_type() const;
    virtual String get_extension() const;
    virtual Error execute_file(const String& p_path) ;
    virtual void finish();

    /* EDITOR FUNCTIONS */
    virtual void get_reserved_words(List<String> *p_words) const;
    virtual void get_comment_delimiters(List<String> *p_delimiters) const;
    virtual void get_string_delimiters(List<String> *p_delimiters) const;
    virtual Ref<Script> get_template(const String& p_class_name, const String& p_base_class_name) const;
    virtual bool validate(const String& p_script,int &r_line_error,int &r_col_error,String& r_test_error, const String& p_path="",List<String> *r_functions=NULL) const;
    virtual Script *create_script() const;
    virtual bool has_named_classes() const;
    virtual int find_function(const String& p_function,const String& p_code) const;
    virtual String make_function(const String& p_class,const String& p_name,const PoolStringArray& p_args) const;
    virtual Error complete_code(const String& p_code, const String& p_base_path, Object*p_owner,List<String>* r_options,String& r_call_hint);
    virtual void auto_indent_code(String& p_code,int p_from_line,int p_to_line) const;
    virtual void add_global_constant(const StringName& p_variable,const Variant& p_value);


    /* DEBUGGER FUNCTIONS */

    virtual String debug_get_error() const;
    virtual int debug_get_stack_level_count() const;
    virtual int debug_get_stack_level_line(int p_level) const;
    virtual String debug_get_stack_level_function(int p_level) const;
    virtual String debug_get_stack_level_source(int p_level) const;
    virtual void debug_get_stack_level_locals(int p_level,List<String> *p_locals, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    virtual void debug_get_stack_level_members(int p_level,List<String> *p_members, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    virtual void debug_get_globals(List<String> *p_locals, List<Variant> *p_values, int p_max_subitems=-1,int p_max_depth=-1);
    virtual String debug_parse_stack_level_expression(int p_level,const String& p_expression,int p_max_subitems=-1,int p_max_depth=-1);

    virtual void reload_all_scripts();
    virtual void reload_tool_script(const Ref<Script>& p_script,bool p_soft_reload);

    virtual void frame();

    virtual void get_public_functions(List<MethodInfo> *p_functions) const;
    virtual void get_public_constants(List<Pair<String,Variant> > *p_constants) const;

    virtual void profiling_start();
    virtual void profiling_stop();

    virtual int profiling_get_accumulated_data(ProfilingInfo *p_info_arr,int p_info_max);
    virtual int profiling_get_frame_data(ProfilingInfo *p_info_arr,int p_info_max);

    /* LOADER FUNCTIONS */

    virtual void get_recognized_extensions(List<String> *p_extensions) const;

    PyLanguage();
    ~PyLanguage();
};
#endif


#endif // PY_SCRIPT_LANGUAGE_H
