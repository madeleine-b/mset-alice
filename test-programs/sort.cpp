#include <algorithm>
#include <fstream>
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

    for (std::string& line : lines) {
        out << line;
        out << "\n";
    }
    out.close();

    return 0;
}
