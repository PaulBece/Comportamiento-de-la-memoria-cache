#include <iostream>
#include <chrono>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;
using namespace std::chrono;

int N, BS;

double* A;
double* B;
double* C;

// ================= INIT =================
void init() {
    A = new double[N * N];
    B = new double[N * N];
    C = new double[N * N];

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i*N + j] = 1.0;
            B[i*N + j] = 1.0;
            C[i*N + j] = 0.0;
        }
    }
}

void resetC() {
    for (int i = 0; i < N*N; i++) C[i] = 0.0;
}

// ================= TESTS =================

void test_ijk() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                C[i*N + j] += A[i*N + k] * B[k*N + j];
}

void test_ikj() {
    for (int i = 0; i < N; i++)
        for (int k = 0; k < N; k++) {
            double a = A[i*N + k];
            for (int j = 0; j < N; j++)
                C[i*N + j] += a * B[k*N + j];
        }
}

void test_blocks() {
    for (int ii = 0; ii < N; ii += BS)
        for (int jj = 0; jj < N; jj += BS)
            for (int kk = 0; kk < N; kk += BS) {

                int i_max = min(ii + BS, N);
                int j_max = min(jj + BS, N);
                int k_max = min(kk + BS, N);

                for (int i = ii; i < i_max; i++)
                    for (int k = kk; k < k_max; k++) {
                        double a = A[i*N + k];
                        for (int j = jj; j < j_max; j++)
                            C[i*N + j] += a * B[k*N + j];
                    }
            }
}

// matrix-vector
double* x;
double* y;

void test_ij() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            y[i] += A[i*N + j] * x[j];
}

void test_ji() {
    for (int j = 0; j < N; j++)
        for (int i = 0; i < N; i++)
            y[i] += A[i*N + j] * x[j];
}

void run_test(const string& t) {
    if (t == "ijk") test_ijk();
    else if (t == "ikj") test_ikj();
    else if (t == "blocks") test_blocks();
    else if (t == "ij") test_ij();
    else if (t == "ji") test_ji();
}

// ================= MAIN =================

int main(int argc, char* argv[]) {

    if (argc < 5) {
        cout << "Usage: worker <test> <runs> <N> <BS>\n";
        return 1;
    }

    string test = argv[1];
    int runs = stoi(argv[2]);
    N = stoi(argv[3]);
    BS = stoi(argv[4]);

    x = new double[N];
    y = new double[N];

    for (int i = 0; i < N; i++) {
        x[i] = 1.0;
        y[i] = 0.0;
    }

    init();

    ofstream file("results.csv", ios::app);

    for (int r = 0; r < runs; r++) {

        resetC();
        fill(y, y + N, 0.0);

        auto start = high_resolution_clock::now();

        run_test(test);

        auto end = high_resolution_clock::now();

        auto time = duration_cast<microseconds>(end - start).count();

        // evitar optimización
        cout << "Run " << r << ": " << C[0] << endl;

        file << test << "," << N << "," << BS << "," << r << "," << time << "\n";
    }

    file.close();

    return 0;
}