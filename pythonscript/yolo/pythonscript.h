#ifndef PYTHONSCRIPT_H
#define PYTHONSCRIPT_H

extern "C" {

#include "modules/pluginscript/pluginscript.h"

extern godot_pluginscript_language_desc_t *godot_pluginscript_init(const godot_pluginscript_init_options *options);

}

#endif // PYTHONSCRIPT_H
