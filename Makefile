.PHONY: all clean test build_godot build_python


BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot

PYTHONSCRIPT_BACKEND ?= cpython

ifeq ($(PYTHONSCRIPT_BACKEND),cpython)
PYTHON_DIR = $(BASEDIR)/pythonscript/cpython
PYTHON_LIB = $(PYTHON_DIR)/libpython*.so.1.0
BUILD_PYTHON_PATH = $(PYTHON_DIR)/build
BUILD_PYTHON_OPTS =
PYTHON = LD_LIBRARY_PATH=$(BUILD_PYTHON_PATH)/lib $(BUILD_PYTHON_PATH)/bin/python3
PIP = LD_LIBRARY_PATH=$(BUILD_PYTHON_PATH)/lib $(BUILD_PYTHON_PATH)/bin/pip3
else
ifeq ($(PYTHONSCRIPT_BACKEND),pypy)
PYTHON_DIR = $(BASEDIR)/pythonscript/pypy
PYTHON_LIB = $(PYTHON_DIR)/bin/libpypy3-c.so
PYTHON = $(PYTHON_DIR)/bin/pypy3
PIP =
else
$(error PYTHONSCRIPT_BACKEND should be `cpython` (default) or `pypy`)
endif
endif

GDNATIVE_CFFIDEFS = $(BASEDIR)/pythonscript/cffi_bindings/cdef.gen.h
GDNATIVE_CFFI_BINDINGS = $(BASEDIR)/pythonscript/cffi_bindings/pythonscriptcffi.gen.cpp

# Add `LIBGL_ALWAYS_SOFTWARE=1` if you computer sucks with opengl3...
GODOT_BIN ?= `ls $(GODOT_DIR)/bin/godot* | head -n 1`
ifndef DEBUG
GODOT_CMD = $(GODOT_BIN) $(EXTRA_OPTS)
else
DEBUG ?= lldb
GODOT_CMD = $(DEBUG) $(GODOT_BIN) $(EXTRA_OPTS)
BUILD_PYTHON_OPTS += --with-pydebug
endif


all:
	scons backend_path=$(BUILD_PYTHON_PATH)


build:
	scons backend_path=$(BUILD_PYTHON_PATH) build


clean:
	scons backend_path=$(BUILD_PYTHON_PATH) -c


test:
	cd tests/bindings && $(GODOT_CMD)


build_python:
	@printf '\033[0;32mRemember to do `sudo apt-get build-dep python3.6` to get optional libraries support.\033[0m\n'
	cd $(PYTHON_DIR) && ./configure --enable-shared --prefix=$(BUILD_PYTHON_PATH) $(BUILD_PYTHON_OPTS)
	cd $(PYTHON_DIR) && make -j4
	cd $(PYTHON_DIR) && make install
	# Install cffi is a pita...
	$(PIP) install cffi
