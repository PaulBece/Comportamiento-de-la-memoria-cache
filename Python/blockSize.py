import pandas as pd
import matplotlib.pyplot as plt

def plot_block_impact():
    # 1. Cargar los datos promediados
    try:
        cpp = pd.read_csv('results_cpp_avg.csv')
        go = pd.read_csv('results_go_avg.csv')
    except FileNotFoundError:
        print("Error: Asegúrate de tener los archivos .csv promediados.")
        return

    # 2. Filtrar solo el test de bloques
    cpp_blocks = cpp[cpp['test'] == 'blocks']
    go_blocks = go[go['test'] == 'blocks']

    # 3. Crear la figura con dos paneles (C++ y Go)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    # Gráfico para C++
    for n in sorted(cpp_blocks['N'].unique()):
        subset = cpp_blocks[cpp_blocks['N'] == n].sort_values('BS')
        ax1.plot(subset['BS'], subset['time'], marker='o', label=f'N={n}')
    
    ax1.set_title('C++: Tiempo vs Block Size')
    ax1.set_xlabel('Block Size (BS)')
    ax1.set_ylabel('Tiempo (ms)')
    ax1.set_xticks(sorted(cpp_blocks['BS'].unique()))
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Gráfico para Go
    for n in sorted(go_blocks['N'].unique()):
        subset = go_blocks[go_blocks['N'] == n].sort_values('BS')
        ax2.plot(subset['BS'], subset['time'], marker='s', linestyle='--', label=f'N={n}')
    
    ax2.set_title('Go: Tiempo vs Block Size')
    ax2.set_xlabel('Block Size (BS)')
    ax2.set_xticks(sorted(go_blocks['BS'].unique()))
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Usar escala logarítmica si los tiempos entre N=512 y N=2048 son muy distantes
    ax1.set_yscale('log')
    ax2.set_yscale('log')

    plt.suptitle('Análisis del Tamaño de Bloque (Algoritmo Blocking)', fontsize=16)
    plt.tight_layout()
    
    plt.savefig('grafica_3_impacto_BS.png')
    print("Gráfica 3 guardada como 'grafica_3_impacto_BS.png'")
    plt.show()

if __name__ == "__main__":
    plot_block_impact()