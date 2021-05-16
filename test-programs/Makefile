COMPILER = clang++-9
CFLAGS = -std=c++17 -g -Iargparse/include

MY_CXX_FLAGS=-nostdinc++ -stdlib=libc++ -lc++ -lc++abi \
	-I/usr/local/lib/llvm-90/libcxx/include \
	-I/usr/local/lib/llvm-90/libcxxabi/include \
	-Wl,-L/usr/local/lib/libc++-install-90/lib -Wl,-L/usr/local/lib/llvm-90/libcxxabi/lib \
	-Wl,-rpath=/usr/local/lib/libc++-install-90/lib -Wl,-rpath=/usr/local/lib/llvm-90/libcxxabi/lib

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
	$(COMPILER) $(CFLAGS) $(MY_CXX_FLAGS) -emit-llvm -c sort.cpp -o llvm/sort.bc

clean:
	rm -rf bin
	rm -rf llvm
	rm out
