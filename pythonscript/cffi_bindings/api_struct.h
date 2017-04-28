#ifndef PYTHONSCRIPT_API_STRUCT_H
#define PYTHONSCRIPT_API_STRUCT_H

#include "modules/gdnative/godot.h"

typedef struct {
	int type;
	godot_string name;
	int hint;
	godot_string hint_string;
	uint32_t usage;
} pybind_prop_info;

#endif // PYTHONSCRIPT_API_STRUCT_H