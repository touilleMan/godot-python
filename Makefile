# Bootstrap this script:
# 1 - create a symlink to godot in this Makefile's dir
# 2 - create another symlink to pythonscript dir as godot/modules/pythonscript
#

BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot

ifndef DEBUG
GODOT_CMD = LD_LIBRARY_PATH="$(GODOT_DIR)/bin" $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
else
DEBUG ?= lldb
GODOT_CMD = LD_LIBRARY_PATH="$(GODOT_DIR)/bin" $(DEBUG) $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
endif

OPTS ?= platform=x11 -j6 use_llvm=yes                  \
CCFLAGS=-fcolor-diagnostics CFLAGS=-fcolor-diagnostics \
target=debug module_pythonscript_enabled=yes           \
PYTHONSCRIPT_SHARED=yes

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
	rm -f pythonscript/*.o  pythonscript/*.so
	rm -f pythonscript/bindings/*.o pythonscript/bindings/*.so
	rm -f pythonscript/bindings/builtins_binder/*.o pythonscript/bindings/builtins_binder/*.so
	rm -f $(GODOT_DIR)/bin/godot*
	rm -f $(GODOT_DIR)/bin/libpythonscript*


rebuild_micropython:
	cd pythonscript/micropython && make clean
	cd pythonscript/micropython && make -j6 DEBUG=y

test:
	cd tests/bindings && LIBGL_ALWAYS_SOFTWARE=1 $(GODOT_CMD)
