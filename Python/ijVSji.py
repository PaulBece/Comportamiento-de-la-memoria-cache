import pandas as pd
import matplotlib.pyplot as plt

def plot_ij_ji():
    # 1. Cargar los datos promediados
    try:
        cpp = pd.read_csv('results_cpp_avg.csv')
        go = pd.read_csv('results_go_avg.csv')
    except FileNotFoundError:
        print("Error: No se encuentran los archivos .csv promediados.")
        return

    # 2. Filtrar solo los tests ij y ji
    tests = ['ij', 'ji']
    cpp_mv = cpp[cpp['test'].isin(tests)]
    go_mv = go[go['test'].isin(tests)]

    # 3. Crear la gráfica
    plt.figure(figsize=(10, 6))

    # Graficar C++
    for t in tests:
        subset = cpp_mv[cpp_mv['test'] == t].sort_values('N')
        plt.plot(subset['N'], subset['time'], marker='o', label=f'C++ {t}')

    # Graficar Go
    for t in tests:
        subset = go_mv[go_mv['test'] == t].sort_values('N')
        plt.plot(subset['N'], subset['time'], marker='x', linestyle='--', label=f'Go {t}')

    # Configuración de estética
    plt.title('Comparación de Recorrido: ij (Filas) vs ji (Columnas)')
    plt.xlabel('Tamaño de Matriz (N)')
    plt.ylabel('Tiempo (ms)')
    
    # En esta prueba la diferencia suele ser lineal o cuadrática, 
    # pero si N=2048 tarda mucho más, puedes activar log.
    plt.yscale('log')
    
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig('grafica_4_ij_vs_ji.png')
    print("Gráfica 4 guardada como 'grafica_4_ij_vs_ji.png'")
    plt.show()

if __name__ == "__main__":
    plot_ij_ji()