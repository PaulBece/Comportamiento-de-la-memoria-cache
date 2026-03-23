package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

var N, BS int
var A, B, C []float64
var x, y []float64

// ================= INIT =================
func initMatrices() {
	A = make([]float64, N*N)
	B = make([]float64, N*N)
	C = make([]float64, N*N)

	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			A[i*N+j] = 1.0
			B[i*N+j] = 1.0
			C[i*N+j] = 0.0
		}
	}
}

func resetC() {
	for i := range C {
		C[i] = 0.0
	}
}

// ================= TESTS =================

// matrix-matrix
func test_ijk() {
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			for k := 0; k < N; k++ {
				C[i*N+j] += A[i*N+k] * B[k*N+j]
			}
		}
	}
}

func test_ikj() {
	for i := 0; i < N; i++ {
		for k := 0; k < N; k++ {
			a := A[i*N+k]
			for j := 0; j < N; j++ {
				C[i*N+j] += a * B[k*N+j]
			}
		}
	}
}

func test_blocks() {
	for ii := 0; ii < N; ii += BS {
		for jj := 0; jj < N; jj += BS {
			for kk := 0; kk < N; kk += BS {

				iMax := min(ii+BS, N)
				jMax := min(jj+BS, N)
				kMax := min(kk+BS, N)

				for i := ii; i < iMax; i++ {
					for k := kk; k < kMax; k++ {
						a := A[i*N+k]
						for j := jj; j < jMax; j++ {
							C[i*N+j] += a * B[k*N+j]
						}
					}
				}
			}
		}
	}
}

// matrix-vector
func test_ij() {
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			y[i] += A[i*N+j] * x[j]
		}
	}
}

func test_ji() {
	for j := 0; j < N; j++ {
		for i := 0; i < N; i++ {
			y[i] += A[i*N+j] * x[j]
		}
	}
}

func runTest(t string) {
	switch t {
	case "ijk":
		test_ijk()
	case "ikj":
		test_ikj()
	case "blocks":
		test_blocks()
	case "ij":
		test_ij()
	case "ji":
		test_ji()
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// ================= MAIN =================

func main() {

	if len(os.Args) < 5 {
		fmt.Println("Usage: worker <test> <runs> <N> <BS>")
		return
	}

	test := os.Args[1]
	runs, _ := strconv.Atoi(os.Args[2])
	N, _ = strconv.Atoi(os.Args[3])
	BS, _ = strconv.Atoi(os.Args[4])

	// vectors
	x = make([]float64, N)
	y = make([]float64, N)

	for i := 0; i < N; i++ {
		x[i] = 1.0
		y[i] = 0.0
	}

	initMatrices()

	file, _ := os.OpenFile("results_go.csv", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer file.Close()

	for r := 0; r < runs; r++ {

		resetC()
		for i := range y {
			y[i] = 0.0
		}

		start := time.Now()

		runTest(test)

		elapsed := time.Since(start).Microseconds()

		// evitar optimización
		fmt.Println("Run", r, ":", C[0])

		line := fmt.Sprintf("%s,%d,%d,%d,%d\n", test, N, BS, r, elapsed)
		file.WriteString(line)
	}
}
