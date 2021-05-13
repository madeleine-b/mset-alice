#include <argparse/argparse.hpp>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    argparse::ArgumentParser program("copy");

    program.add_argument("in")
        .help("input file");

    program.add_argument("out")
        .help("output file");

    program.add_argument("flag")
        .help("weird flag")
        .action([](const std::string &value) { return std::stoi(value); });

    try
    {
        program.parse_args(argc, argv);
    }
    catch (const std::runtime_error &err)
    {
        std::cout << err.what() << std::endl;
        std::cout << program;
        exit(0);
    }

    auto input = program.get<std::string>("in");
    auto output = program.get<std::string>("out");
    int flag = program.get<int>("flag");

    int in = open(input.c_str(), O_RDWR);
    int out = open(output.c_str(), O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);

    char buffer[1024];

    while (ssize_t sz = read(in, &buffer, 1024))
    {
        write(out, &buffer, sz);
    }

    close(in);
    close(out);

    if (flag == 69)
    {
        int oof = open(input.c_str(), O_TRUNC);
        close(oof);
    }

    return 0;
}
