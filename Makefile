PYTHON=python3
COMPILER=gcc
LINKER=gcc

CFLAGS=-O9

help:
	@echo "OctoBot Components Cython Makefile.  Available tasks:"
	@echo "build  -> build the Cython extension module."
	@echo "clean -> clean the Cython extension module."

all: build

.PHONY: build
build: clean
	$(PYTHON) setup.py build_ext --inplace

.PHONY: clean
clean:
	rm -rf *~ **/*.so **/*.c **/*.o **/*.html build

# Suffix rules
.PRECIOUS: %.c
%: %.o
	$(LINKER) -o $@ -L$(LIBRARY_DIR) -l$(PYTHON_LIB) $(SYSLIBS) $<

%.o: %.c
	$(COMPILER) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

%.c: %.py
	cython -a --embed $<

%.c: %.pyx
	cython -a --embed $<
