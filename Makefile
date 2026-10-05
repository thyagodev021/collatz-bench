UNAME := $(shell uname -s)
EXT := $(if $(filter Darwin,$(UNAME)),dylib,so)
LIB := collatz_bench/_native/libcollatz.$(EXT)

.PHONY: all test bench clean

all: $(LIB)

$(LIB): csrc/collatz.c csrc/collatz.h
	mkdir -p collatz_bench/_native
	$(CC) -O2 -Wall -Wextra -shared -fPIC -o $@ csrc/collatz.c

test: all
	python -m pytest -q

bench: all
	python -m collatz_bench bench 200000

clean:
	rm -rf collatz_bench/_native build *.egg-info .pytest_cache
