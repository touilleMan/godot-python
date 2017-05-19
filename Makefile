# Bootstrap this script:
# 1 - create a symlink to godot in this Makefile's dir
# 2 - create another symlink to pythonscript dir as godot/modules/pythonscript
#

.PHONY: all setup run run_example compile clean veryclean generate_gdnative_cffidefs \
	    generate_cffi_bindings generate_dev_dyn_cffi_bindings build_python

BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot

PYTHON_DIR = $(BASEDIR)/pythonscript/cpython
PYTHON_LIB = $(PYTHON_DIR)/libpython*.so.1.0
BUILD_PYTHON_PATH = $(PYTHON_DIR)/build
BUILD_PYTHON_OPTS =
PYTHON = LD_LIBRARY_PATH=$(BUILD_PYTHON_PATH)/lib $(BUILD_PYTHON_PATH)/bin/python3
PIP = LD_LIBRARY_PATH=$(BUILD_PYTHON_PATH)/lib $(BUILD_PYTHON_PATH)/bin/pip3

GDNATIVE_CFFIDEFS = $(BASEDIR)/pythonscript/cffi_bindings/cdef.gen.h
GDNATIVE_CFFI_BINDINGS = $(BASEDIR)/pythonscript/cffi_bindings/pythonscriptcffi.gen.cpp

# Add `LIBGL_ALWAYS_SOFTWARE=1` if you computer sucks with opengl3...
ifndef DEBUG
GODOT_CMD = $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
else
DEBUG ?= lldb
GODOT_CMD = $(DEBUG) $(GODOT_DIR)/bin/godot* $(EXTRA_OPTS)
BUILD_PYTHON_OPTS += --with-pydebug
endif

# Remove use_llvm and CCFLAGS/CFLAGS if you'r still using gcc
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


all:
	@echo 'Quickstart checklist:'
	@printf '\033[0;32msetup\033[0m:                      Install pythonscript inside the godot main repo\n'
	@printf '\033[0;32mbuild_python\033[0m:               Build Python interpreter\n'
	@printf '\033[0;32mgenerate_gdnative_cffidefs\033[0m: Generate GDnative cdef for CFFI\n'
	@printf '\033[0;32mgenerate_cffi_bindings\033[0m:     Generate the CFFI bindings source\n'
	@printf '\033[0;32mcompile\033[0m:                    Compile the Godot project with pythonscript module\n'
	@printf '\033[0;32mtest\033[0m:                       Run test and go have a beer ;-)\n'


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


compile: $(PYTHON_LIB) $(GDNATIVE_CFFI_BINDINGS)
	cd $(GODOT_DIR) && scons $(OPTS)


clean:
	rm -f pythonscript/*.o  pythonscript/*.os
	rm -f pythonscript/cffi_bindings/*.o pythonscript/cffi_bindings/*.os
	rm -f $(GODOT_DIR)/bin/godot*
	rm -f $(GODOT_DIR)/bin/libpythonscript*


veryclean: clean
	rm -f $(GDNATIVE_CFFIDEFS)
	rm -f $(GDNATIVE_CFFI_BINDINGS)

test:
	cd tests/bindings && $(GODOT_CMD)


$(GDNATIVE_CFFI_BINDINGS):
	make generate_cffi_bindings


generate_cffi_bindings: $(PYTHON_LIB) $(GDNATIVE_CFFIDEFS)
	$(PYTHON) $(BASEDIR)/pythonscript/cffi_bindings/generate.py


generate_dev_dyn_cffi_bindings: $(PYTHON_LIB) $(GDNATIVE_CFFIDEFS)
	$(PYTHON) $(BASEDIR)/pythonscript/cffi_bindings/generate.py --dev-dyn
	@printf "\033[0;32mPython .inc.py files are now dynamically loaded, don't share the binary !\033[0m\n"


$(GDNATIVE_CFFIDEFS):
	make generate_gdnative_cffidefs


generate_gdnative_cffidefs:
	$(BASEDIR)/tools/generate_gdnative_cffidefs.py --output $(GDNATIVE_CFFIDEFS) $(GODOT_DIR)


$(PYTHON_LIB):
	1>/dev/null make build_python


build_python:
	cd $(PYTHON_DIR) && ./configure --enable-shared --prefix=$(BUILD_PYTHON_PATH) $(BUILD_PYTHON_OPTS)
	cd $(PYTHON_DIR) && make -j4
	cd $(PYTHON_DIR) && make install
	# Install cffi is a pita...
	LD_LIBRARY_PATH=$(PYTHON_DIR) $(PIP) install cffi
	if ( [ ! -d $(GODOT_DIR)/bin ] ); then mkdir $(GODOT_DIR)/bin; fi
	cp $(PYTHON_LIB) $(GODOT_DIR)/bin/
	ln -s `basename $(PYTHON_LIB)` $(GODOT_DIR)/bin/libpython.so
