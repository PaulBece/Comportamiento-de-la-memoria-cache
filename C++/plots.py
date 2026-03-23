import pandas as pd
import matplotlib.pyplot as plt

# ====== CONFIG ======
CSV_FILE = "results.csv"  # cambia si usas results_go.csv

# ====== LOAD DATA ======
df = pd.read_csv(CSV_FILE, names=["test","N","BS","run","time"])

# Crear nombre completo del test
df["test_full"] = df["test"]


# Para blocks: agregar tamaño de bloque
df.loc[df["test"] == "blocks", "test_full"] = (
    df["test"] + df["BS"].astype(str)
)

# Si tu CSV no tiene headers, usa:
df = pd.read_csv(CSV_FILE, names=["test","N","BS","run","time"])

# Promedio por test y tamaño
df_avg = df.groupby(["test_full", "N"], as_index=False)["time"].mean()

# ====== 1. Tiempo vs N ======
tests = ["ijk", "ikj", "blocks16", "blocks32", "blocks64", "blocks128"]

plt.figure()
for test in tests:
    subset = df_avg[df_avg["test_full"] == test]
    plt.plot(subset["N"], subset["time"], marker='o', label=test)

plt.xlabel("Matrix Size (N)")
plt.ylabel("Time (microseconds)")
plt.title("Time vs Matrix Size")
plt.legend()
plt.grid()
plt.savefig("time_vs_n.png")

# ====== 2. Comparación algoritmos (N fijo) ======
N_fixed = df_avg["N"].max()

subset = df_avg[df_avg["N"] == N_fixed]

tests = ["ijk", "ikj", "blocks16", "blocks32", "blocks64", "blocks128"]
subset = subset[subset["test_full"].isin(tests)]

plt.figure()
plt.bar(subset["test_full"], subset["time"])

plt.xlabel("Algorithm")
plt.ylabel("Time (microseconds)")
plt.title(f"Algorithm Comparison (N={N_fixed})")
plt.savefig("algorithms_comparison.png")

# ====== 3. Blocks: tamaño de bloque ======
subset = df_avg[df_avg["test_full"].isin(["ij", "ji"])]

plt.figure()
for N in subset["N"].unique():
    sub = subset[subset["N"] == N]
    plt.plot(sub["BS"], sub["time"], marker='o', label=f"N={N}")

plt.xlabel("Block Size (BS)")
plt.ylabel("Time (microseconds)")
plt.title("Block Size vs Performance")
plt.legend()
plt.grid()
plt.savefig("block_size.png")

# ====== 4. ij vs ji ======
subset = df_avg[df_avg["test"].isin(["ij", "ji"])]

plt.figure()
for test in ["ij", "ji"]:
    sub = subset[subset["test"] == test]
    plt.plot(sub["N"], sub["time"], marker='o', label=test)

plt.xlabel("N")
plt.ylabel("Time (microseconds)")
plt.title("ij vs ji")
plt.legend()
plt.grid()
plt.savefig("ij_vs_ji.png")

plt.show()