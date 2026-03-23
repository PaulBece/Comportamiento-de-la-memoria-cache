package main

import (
	"fmt"
	"os/exec"
	"strconv"
)

func main() {

	tests := []string{"ij", "ji", "ijk", "ikj", "blocks"}
	sizes := []int{512, 1024, 2048}
	blockSizes := []int{16, 32, 64, 128}

	runs := 3

	for _, t := range tests {
		for _, N := range sizes {

			if t == "blocks" {
				for _, BS := range blockSizes {

					fmt.Println("Running:", t, "N=", N, "BS=", BS)

					cmd := exec.Command(
						"./worker",
						t,
						strconv.Itoa(runs),
						strconv.Itoa(N),
						strconv.Itoa(BS),
					)

					cmd.Stdout = nil
					cmd.Stderr = nil

					cmd.Run()
				}
			} else {

				fmt.Println("Running:", t, "N=", N)

				cmd := exec.Command(
					"./worker",
					t,
					strconv.Itoa(runs),
					strconv.Itoa(N),
					"0",
				)

				cmd.Stdout = nil
				cmd.Stderr = nil

				cmd.Run()
			}
		}
	}
}
