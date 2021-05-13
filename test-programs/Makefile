COMPILER = g++
CFLAGS = -std=c++17 -Iargparse/include

copy: copy.cpp
	mkdir -p bin
	$(COMPILER) $(CFLAGS) copy.cpp -o bin/copy

all: copy

clean:
	rm -rf bin
	rm out
