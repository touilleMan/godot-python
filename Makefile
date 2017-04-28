# Bootstrap this script:
# 1 - create a symlink to godot in this Makefile's dir
# 2 - create another symlink to pythonscript dir as godot/modules/pythonscript
#

BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot

BUILD_PYTHON_PATH = $(BASEDIR)/pythonscript/cpython/build
PYTHON = LD_LIBRARY_PATH=$(BUILD_PYTHON_PATH)/lib $(BUILD_PYTHON_PATH)/bin/python3

# Add `LIBGL_ALWAYS_SOFTWARE=1` if you computer sucks with opengl3...
ifndef DEBUG
GODOT_CMD = $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
else
DEBUG ?= lldb
GODOT_CMD = $(DEBUG) $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
endif

OPTS ?= platform=x11 -j6 use_llvm=yes                  \
CCFLAGS=-fcolor-diagnostics CFLAGS=-fcolor-diagnostics \
target=debug module_pythonscript_enabled=yes           \
PYTHONSCRIPT_SHARED=no

ifeq ($(TARGET), pythonscript)
OPTS += $(shell cd $(GODOT_DIR) && ls bin/libpythonscript*.so)
else
OPTS += $(TARGET)
endif

OPTS += $(EXTRA_OPTS)


setup:
ifndef GODOT_TARGET_DIR
	echo "GODOT_TARGET_DIR must be set to Godot source directory" && exit 1
else
	ln -s $(GODOT_TARGET_DIR) $(GODOT_DIR)/godot
	ln -s $(BASEDIR)/pythonscript $(GODOT_TARGET_DIR)/modules/pythonscript
endif


run:
	$(GODOT_CMD)


run_example:
	cd example && $(GODOT_CMD)


compile:
	cd $(GODOT_DIR) && scons $(OPTS)


clean:
	rm -f pythonscript/*.o  pythonscript/*.os
	rm -f pythonscript/cffi_bindings/*.o pythonscript/cffi_bindings/*.os
	rm -f $(GODOT_DIR)/bin/godot*
	rm -f $(GODOT_DIR)/bin/libpythonscript*


test:
	cd tests/bindings && $(GODOT_CMD)


generate_cffi_bindings:
	$(PYTHON) -m pip install cffi
	$(PYTHON) $(BASEDIR)/pythonscript/cffi_bindings/generate.py
