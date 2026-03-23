#include <iostream>
#include <vector>
#include <cstdlib>
#include <string>

using namespace std;

int main() {

    vector<string> tests = {"ij", "ji", "ijk", "ikj", "blocks"};
    vector<int> sizes = {512, 1024, 2048};
    vector<int> blockSizes = {16, 32, 64, 128};

    int runs = 3;

    for (auto& t : tests) {
        for (auto N : sizes) {

            if (t == "blocks") {
                for (auto BS : blockSizes) {
                    cout << "Running: " << t << " N=" << N << " BS=" << BS << endl;

                    string cmd = "./worker " + t + " " +
                                 to_string(runs) + " " +
                                 to_string(N) + " " +
                                 to_string(BS);

                    system(cmd.c_str());
                }
            } else {
                cout << "Running: " << t << " N=" << N << endl;

                string cmd = "./worker " + t + " " +
                             to_string(runs) + " " +
                             to_string(N) + " 0";

                system(cmd.c_str());
            }
        }
    }

    return 0;
}