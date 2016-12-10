# Bootstrap this script:
# 1 - create a symlink to godot in this Makefile's dir
# 2 - create another symlink to pythonscript dir as godot/modules/pythonscript
#

BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot

ifndef DEBUG
GODOT_CMD = LD_LIBRARY_PATH="$(GODOT_DIR)/bin" $(GODOT_DIR)/bin/godot*
else
DEBUG ?= lldb
GODOT_CMD = LD_LIBRARY_PATH="$(GODOT_DIR)/bin" $(DEBUG) $(GODOT_DIR)/bin/godot*
endif

OPTS ?= platform=x11 -j6 use_llvm=yes                  \
CCFLAGS=-fcolor-diagnostics CFLAGS=-fcolor-diagnostics \
target=debug module_pythonscript_enabled=yes           \
PYTHONSCRIPT_SHARED=yes $(EXTRA_OPTS)

ifeq ($(TARGET), pythonscript)
OPTS += $(shell cd $(GODOT_DIR) && ls bin/libpythonscript*.so)
else
OPTS += $(TARGET)
endif

run:
	cd example && $(GODOT_CMD)

compile:
	cd $(GODOT_DIR) && scons $(OPTS)
