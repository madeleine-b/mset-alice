#include <sys/stat.h>

#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

const static int N = 8;
const static unsigned char MAGIC = 0xFF;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        return -1;
    }

    char* input = argv[1];
    char* output = argv[2];

    std::ifstream in(input);
    if (!in) {
        return -2;
    }

    struct stat st;
    stat(input, &st);
    std::cout << st.st_size;

    std::string s;
    std::vector<std::string> lines;
    while (std::getline(in, s)) {
        lines.push_back(s);
    }
    in.close();

    std::sort(lines.begin(), lines.end());

    std::ofstream out(output);
    if (!out) {
        return -3;
    }

    size_t n = lines.size();
    for (size_t i = 0; i < n - 1; i++) {
        out << lines[i];
        out << "\n";
    }
    out << lines[n - 1];
    out.close();

    return 0;
}
