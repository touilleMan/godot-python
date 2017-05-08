#ifndef PYTHONSCRIPT_PY_LANGUAGE_H
#define PYTHONSCRIPT_PY_LANGUAGE_H

// Pythonscript imports
#include "pythonscript.h"
// Godot imports
#include "core/io/resource_loader.h"
#include "core/io/resource_saver.h"
#include "core/script_language.h"
#include "core/self_list.h"
#include "core/map.h"


class PyScript;
class PyInstance;

class PyLanguage : public ScriptLanguage {
	friend class PyScript;
	friend class PyInstance;

	Mutex *lock;
	static PyLanguage *singleton;
	SelfList<PyScript>::List script_list;
#ifdef DEBUG_ENABLED
	struct MethProfile {
		uint64_t call_count;
		uint64_t self_time;
		uint64_t total_time;
		uint64_t frame_call_count;
		uint64_t frame_self_time;
		uint64_t frame_total_time;
		uint64_t last_frame_call_count;
		uint64_t last_frame_self_time;
		uint64_t last_frame_total_time;
		MethProfile() : call_count(0), self_time(0), total_time(0),
			frame_call_count(0), frame_self_time(0), frame_total_time(0),
			last_frame_call_count(0), last_frame_self_time(0),
			last_frame_total_time(0) {}
	};
	Map<StringName, MethProfile> per_meth_profiling;
	bool profiling;
#endif

public:
	String get_name() const;
	_FORCE_INLINE_ static PyLanguage *get_singleton() { return singleton; }

	/* LANGUAGE FUNCTIONS */
	void init();
	String get_type() const;
	String get_extension() const;
	Error execute_file(const String &p_path);
	void finish();

	/* EDITOR FUNCTIONS */
	void get_reserved_words(List<String> *p_words) const;
	void get_comment_delimiters(List<String> *p_delimiters) const;
	void get_string_delimiters(List<String> *p_delimiters) const;
	Ref<Script> get_template(const String &p_class_name, const String &p_base_class_name) const;
	bool validate(const String &p_script, int &r_line_error, int &r_col_error, String &r_test_error, const String &p_path = "", List<String> *r_functions = NULL) const;
	Script *create_script() const;
	bool has_named_classes() const;
	int find_function(const String &p_function, const String &p_code) const;
	String make_function(const String &p_class, const String &p_name, const PoolStringArray &p_args) const;
	// Error complete_code(const String& p_code, const String& p_base_path, Object*p_owner,List<String>* r_options,String& r_call_hint) { return ERR_UNAVAILABLE; }
	void auto_indent_code(String &p_code, int p_from_line, int p_to_line) const;
	void add_global_constant(const StringName &p_variable, const Variant &p_value);

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
	void debug_get_stack_level_locals(int p_level, List<String> *p_locals, List<Variant> *p_values, int p_max_subitems = -1, int p_max_depth = -1);
	void debug_get_stack_level_members(int p_level, List<String> *p_members, List<Variant> *p_values, int p_max_subitems = -1, int p_max_depth = -1);
	void debug_get_globals(List<String> *p_locals, List<Variant> *p_values, int p_max_subitems = -1, int p_max_depth = -1);
	String debug_parse_stack_level_expression(int p_level, const String &p_expression, int p_max_subitems = -1, int p_max_depth = -1);

	// virtual Vector<StackInfo> debug_get_current_stack_info() { return Vector<StackInfo>(); }

	void reload_all_scripts();
	void reload_tool_script(const Ref<Script> &p_script, bool p_soft_reload);
	/* LOADER FUNCTIONS */

	void get_recognized_extensions(List<String> *p_extensions) const;
	void get_public_functions(List<MethodInfo> *p_functions) const;
	void get_public_constants(List<Pair<String, Variant> > *p_constants) const;

	void profiling_start();
	void profiling_stop();

	int profiling_get_accumulated_data(ProfilingInfo *p_info_arr, int p_info_max);
	int profiling_get_frame_data(ProfilingInfo *p_info_arr, int p_info_max);

	void frame();

	~PyLanguage();
	PyLanguage();
};

#endif // PYTHONSCRIPT_PY_LANGUAGE_H
