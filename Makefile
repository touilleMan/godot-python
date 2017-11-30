.PHONY: all build clean test example


BASEDIR = $(shell pwd)
BACKEND ?= cpython
PLATFORM ?= x11-64

EXTRA_OPTS ?=

SCONS_BIN ?= scons
SCONS_CMD = $(SCONS_BIN) backend=$(BACKEND) platform=$(PLATFORM) $(EXTRA_OPTS)

# Add `LIBGL_ALWAYS_SOFTWARE=1` if you computer sucks with opengl3...

all: build


build:
	$(SCONS_CMD)


clean:
	$(SCONS_CMD) -c


test:
	$(SCONS_CMD) test


example:
	$(SCONS_CMD) example
