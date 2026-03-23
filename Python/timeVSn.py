import pandas as pd
import matplotlib.pyplot as plt

def plot_language_data(df, title, filename):
    plt.figure(figsize=(10, 7))
    
    # 1. Graficar ijk e ikj
    for algo in ['ijk', 'ikj']:
        subset = df[df['test'] == algo]
        if not subset.empty:
            plt.plot(subset['N'], subset['time'], marker='o', label=f'Algoritmo {algo}')

    # 2. Graficar cada tamaño de bloque (BS)
    for bs in df[df['test'] == 'blocks']['BS'].unique():
        subset_bs = df[(df['test'] == 'blocks') & (df['BS'] == bs)]
        plt.plot(subset_bs['N'], subset_bs['time'], marker='s', linestyle='--', label=f'Blocks (BS={bs})')

    # Configuración de la gráfica
    plt.title(title)
    plt.xlabel('Tamaño de Matriz (N)')
    plt.ylabel('Tiempo (ms)')
    plt.yscale('log')  # Escala logarítmica para ver mejor los rangos
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    
    plt.savefig(filename)
    print(f"Gráfica guardada como: {filename}")
    plt.close()

def main():
    # Cargar los datos promediados generados en el paso anterior
    try:
        cpp_avg = pd.read_csv('results_cpp_avg.csv')
        go_avg = pd.read_csv('results_go_avg.csv')
    except FileNotFoundError:
        print("Error: No se encuentran los archivos promediados. Ejecuta primero process_data.py")
        return

    # Generar gráfica para C++
    plot_language_data(cpp_avg, 'Rendimiento en C++: Tiempo vs N', 'grafica_1_cpp.png')
    
    # Generar gráfica para Go
    plot_language_data(go_avg, 'Rendimiento en Go: Tiempo vs N', 'grafica_1_go.png')

if __name__ == "__main__":
    main()