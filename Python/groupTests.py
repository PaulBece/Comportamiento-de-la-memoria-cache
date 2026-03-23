import pandas as pd
import os

def procesar_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: No se encontró el archivo {input_file}")
        return

    # 1. Leer el CSV
    # Formato: test, N, BS, run, time
    df = pd.read_csv(input_file, header=None, names=['test', 'N', 'BS', 'run', 'time'])

    # 2. Agrupar y promediar
    # Agrupamos por test, N y BS. Ignoramos la columna 'run' al promediar.
    df_promediado = df.groupby(['test', 'N', 'BS'])['time'].mean().reset_index()

    # 3. Guardar el nuevo CSV
    df_promediado.to_csv(output_file, index=False)
    print(f"Archivo procesado: {output_file}")

if __name__ == "__main__":
    # Procesamos los datos de C++
    procesar_csv('results.csv', 'results_cpp_avg.csv')
    
    # Procesamos los datos de GO
    procesar_csv('results_go.csv', 'results_go_avg.csv')