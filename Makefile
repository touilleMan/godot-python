.PHONY: all build clean test build_python


BASEDIR = $(shell pwd)
GODOT_DIR ?= $(BASEDIR)/godot
BACKEND ?= cpython
EXTRA_OPTS ?=

SCONS_BIN ?= scons
SCONS_CMD = $(SCONS_BIN) backend=$(BACKEND) backend_path=$(BACKEND_DIR) $(EXTRA_OPTS)

# Add `LIBGL_ALWAYS_SOFTWARE=1` if you computer sucks with opengl3...
GODOT_BIN ?= `ls $(GODOT_DIR)/bin/godot* | head -n 1`
ifndef DEBUG
GODOT_CMD = $(GODOT_BIN) $(EXTRA_OPTS)
else
DEBUG ?= lldb
GODOT_CMD = $(DEBUG) $(GODOT_BIN) $(EXTRA_OPTS)
endif


all: build


ifeq ($(BACKEND),cpython)

BUILD_OPTS ?=
ifdef DEBUG
BUILD_OPTS += --with-pydebug
endif

PYTHON = LD_LIBRARY_PATH=$(BACKEND_DIR)/lib $(BACKEND_DIR)/bin/python3
PIP = LD_LIBRARY_PATH=$(BACKEND_DIR)/lib $(BACKEND_DIR)/bin/pip3
PYTHON_SRC_DIR ?= $(BASEDIR)/$(BACKEND)
BACKEND_DIR ?= $(PYTHON_SRC_DIR)/build

build_python:
	@printf '\033[0;32mRemember to do `sudo apt-get build-dep python3.6` to get optional libraries support.\033[0m\n'
	cd $(PYTHON_SRC_DIR) && ./configure --enable-shared --prefix=$(BACKEND_DIR) $(BUILD_OPTS)
	cd $(PYTHON_SRC_DIR) && make -j4
	cd $(PYTHON_SRC_DIR) && make install
	# Install cffi is a pita...
	$(PIP) install cffi
else
ifeq ($(BACKEND),pypy)
BACKEND_DIR ?= $(BASEDIR)/$(BACKEND)

build_python:
	@printf '\033[0;31mOnly supported for CPython backend.\033[0m\n'
	exit 1
else
$(error PYTHONSCRIPT_BACKEND should be `cpython` (default) or `pypy`)
endif
endif


build:
	$(SCONS_CMD) build


clean:
	$(SCONS_CMD) -c


veryclean:
	rm -rf $(BASEDIR)/build*


test:
	$(SCONS_CMD) install-build-symlink
	cd tests/bindings && $(GODOT_CMD)


example:
	$(SCONS_CMD) install-build-symlink
	cd examples/pong && $(GODOT_CMD)
