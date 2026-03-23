import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_fixed_n_plot_ordered(n_value, cpp_df, go_df, filename):
    # 1. Filtrar por el N deseado
    c_sub = cpp_df[cpp_df['N'] == n_value].copy()
    g_sub = go_df[go_df['N'] == n_value].copy()

    # 2. Definir el ORDEN ESPECÍFICO
    # Primero los base
    base_order = ['ij', 'ji', 'ijk', 'ikj']
    
    # Luego los bloques ordenados por BS (16, 32, 64, 128...)
    block_sizes = sorted(c_sub[c_sub['test'] == 'blocks']['BS'].unique())
    block_labels = [f"blocks-{int(bs)}" for bs in block_sizes]
    
    # Lista final de etiquetas en el orden deseado
    final_labels = base_order + block_labels
    
    cpp_times = []
    go_times = []
    
    # Extraer los tiempos siguiendo estrictamente el orden de final_labels
    for label in final_labels:
        if 'blocks-' in label:
            bs_val = int(label.split('-')[1])
            c_val = c_sub[(c_sub['test'] == 'blocks') & (c_sub['BS'] == bs_val)]['time']
            g_val = g_sub[(g_sub['test'] == 'blocks') & (g_sub['BS'] == bs_val)]['time']
        else:
            c_val = c_sub[c_sub['test'] == label]['time']
            g_val = g_sub[g_sub['test'] == label]['time']
            
        cpp_times.append(c_val.values[0] if not c_val.empty else 0)
        go_times.append(g_val.values[0] if not g_val.empty else 0)

    # 3. Crear el gráfico de barras
    x = np.arange(len(final_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - width/2, cpp_times, width, label='C++', color='skyblue', edgecolor='black')
    ax.bar(x + width/2, go_times, width, label='Go', color='salmon', edgecolor='black', hatch='//')

    # 4. Estética y Escala
    ax.set_title(f'Comparación de Rendimiento (N = {n_value})')
    ax.set_xticks(x)
    ax.set_xticklabels(final_labels, rotation=45)
    ax.legend()
    
    # Escala logarítmica si hay mucha diferencia (típico entre ij e ijk)
    if max(cpp_times + go_times) / (min([t for t in (cpp_times + go_times) if t > 0]) or 1) > 10:
        ax.set_yscale('log')
        ax.set_ylabel('Tiempo (ms) - Escala Logarítmica')
    else:
        ax.set_ylabel('Tiempo (ms)')

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    plt.savefig(filename)
    print(f"Gráfica guardada: {filename}")
    plt.close()

def main():
    # Cargamos los promediados
    cpp_avg = pd.read_csv('results_cpp_avg.csv')
    go_avg = pd.read_csv('results_go_avg.csv')

    generate_fixed_n_plot_ordered(512, cpp_avg, go_avg, 'grafica_2_ordenada_N512.png')
    generate_fixed_n_plot_ordered(2048, cpp_avg, go_avg, 'grafica_2_ordenada_N2048.png')

if __name__ == "__main__":
    main()