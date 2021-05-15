#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>

const static int N = 8;
const static unsigned char MAGIC = 0xFF;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        return -1;
    }

    char* input = argv[1];
    char* output = argv[2];

    int in = open(input, O_RDWR);
    if (in == -1) {
        return -2;
    }
    int out = open(output, O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);
    if (out == -1) {
        close(in);
        return -3;
    }

    unsigned char buffer[N];
    size_t num_written = 0;
    while (true) {
        ssize_t sz = read(in, &buffer, N);
        if (sz <= 0) {
            break;
        }
        write(out, &buffer, sz);
        if (buffer[0] != MAGIC) {
            fsync(out);
        }
        num_written += sz;
        printf("%lu\n", num_written);
    }

    close(in);
    close(out);
    return 0;
}
