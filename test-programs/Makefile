COMPILER = clang++-9
CFLAGS = -std=c++17 -Iargparse/include

all: copy copyllvm sort sortllvm

copy: copy.cpp
	mkdir -p bin
	$(COMPILER) $(CFLAGS) copy.cpp -o bin/copy

sort: sort.cpp
	mkdir -p bin
	$(COMPILER) $(CFLAGS) sort.cpp -o bin/sort

copyllvm: copy.cpp
	mkdir -p llvm
	$(COMPILER) $(CFLAGS) -emit-llvm -c copy.cpp -o llvm/copy.bc

sortllvm: sort.cpp
	mkdir -p llvm
	$(COMPILER) $(CFLAGS) -emit-llvm -c sort.cpp -o llvm/sort.bc

clean:
	rm -rf bin
	rm -rf llvm
	rm out
