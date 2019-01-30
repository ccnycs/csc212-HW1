#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cstdio>
#include <gtest/gtest.h>

class TestIO : public testing::Test{
    public:
        std::string command = "./main";
};

TEST_F(TestIO, TestOutput){
    std::array<char, 128> buffer;
    std::string result;
    FILE* pipe = popen(command.c_str(), "r");
    ASSERT_TRUE(pipe);

    while (fgets(buffer.data(), 128, pipe) != NULL) {
        result += buffer.data();
    }
    auto returnCode = pclose(pipe);

    ASSERT_EQ(0, returnCode);
    ASSERT_EQ("Hello World!\n", result);
}



//-----------------------------------------------------------------------------
int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
