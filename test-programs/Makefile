COMPILER = clang++-9
CFLAGS = -std=c++17 -Iargparse/include

copy: copy.cpp
	mkdir -p bin
	$(COMPILER) $(CFLAGS) copy.cpp -o bin/copy

sort: sort.cpp
	mkdir -p bin
	$(COMPILER) $(CFLAGS) sort.cpp -o bin/sort

copyllvm: copy.cpp
	mkdir -p llvm
	$(COMPILER) $(CFLAGS) -emit-llvm -c copy.cpp -o llvm/copy.bc

all: copy copyllvm

clean:
	rm -rf bin
	rm out
