import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os

def parse_cache_file(filename, lang):
    """Extrae datos de archivos de Valgrind Cachegrind."""
    if not os.path.exists(filename):
        print(f"Error: No se encontró {filename}")
        return pd.DataFrame()
    
    data = []
    with open(filename, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_test, current_n, current_bs = None, None, 0
    d1_rate, lld_rate = 0.0, 0.0

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detectar cabecera: "ij 1024", "ijk 512" o "blocks(32) 1024"
        header = re.match(r'^([a-z]+)(\((\d+)\))?\s+(\d+)$', line)
        if header:
            current_test = header.group(1)
            current_bs = int(header.group(3)) if header.group(3) else 0
            current_n = int(header.group(4))
            continue
            
        # Extraer tasa de fallos D1 (L1 Data)
        if "D1  miss rate:" in line:
            m = re.search(r'(\d+\.\d+)%', line)
            if m: d1_rate = float(m.group(1))
                
        # Extraer tasa de fallos LLd (Last Level Data)
        if "LLd miss rate:" in line:
            m = re.search(r'(\d+\.\d+)%', line)
            if m:
                lld_rate = float(m.group(1))
                data.append({
                    'lang': lang, 'test': current_test, 'N': current_n,
                    'BS': current_bs, 'D1': d1_rate, 'LLd': lld_rate
                })
    return pd.DataFrame(data)

def main():
    # 1. Cargar y procesar archivos
    cpp_cache = parse_cache_file('cacheMissesC++.txt', 'C++')
    go_cache = parse_cache_file('cacheMissesGO.txt', 'Go')
    df = pd.concat([cpp_cache, go_cache], ignore_index=True)

    if df.empty: return

    # Filtramos para N=1024 como punto de referencia
    n_val = 1024
    sub = df[df['N'] == n_val]
    
    # Definir orden de etiquetas
    base_order = ['ij', 'ji', 'ijk', 'ikj']
    block_sizes = sorted(sub[sub['test'] == 'blocks']['BS'].unique())
    labels = base_order + [f"blocks-{bs}" for bs in block_sizes]

    # --- GRÁFICA 1: Tasa de Fallos D1 (L1) ---
    def get_rates(metric):
        c_vals, g_vals = [], []
        for L in labels:
            if 'blocks-' in L:
                bs = int(L.split('-')[1])
                c = sub[(sub['lang'] == 'C++') & (sub['test'] == 'blocks') & (sub['BS'] == bs)][metric]
                g = sub[(sub['lang'] == 'Go') & (sub['test'] == 'blocks') & (sub['BS'] == bs)][metric]
            else:
                c = sub[(sub['lang'] == 'C++') & (sub['test'] == L)][metric]
                g = sub[(sub['lang'] == 'Go') & (sub['test'] == L)][metric]
            c_vals.append(c.values[0] if not c.empty else 0)
            g_vals.append(g.values[0] if not g.empty else 0)
        return c_vals, g_vals

    d1_cpp, d1_go = get_rates('D1')
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, d1_cpp, width, label='C++', color='skyblue', edgecolor='black')
    plt.bar(x + width/2, d1_go, width, label='Go', color='salmon', edgecolor='black', hatch='//')
    plt.title(f'Tasa de Fallos de Caché L1 (D1) - N = {n_val}')
    plt.ylabel('Miss Rate (%)')
    plt.xticks(x, labels, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('cache_miss_d1_n1024.png')

    # --- GRÁFICA 2: Tasa de Fallos LLd (L3) ---
    lld_cpp, lld_go = get_rates('LLd')
    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, lld_cpp, width, label='C++', color='blue', alpha=0.6)
    plt.bar(x + width/2, lld_go, width, label='Go', color='red', alpha=0.6)
    plt.title(f'Tasa de Fallos de Último Nivel (LLd) - N = {n_val}')
    plt.ylabel('Miss Rate (%)')
    plt.xticks(x, labels, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('cache_miss_lld_n1024.png')

    # --- GRÁFICA 3: Impacto del BS en Fallos D1 ---
    plt.figure(figsize=(10, 6))
    for lang in ['C++', 'Go']:
        block_data = df[(df['test'] == 'blocks') & (df['lang'] == lang) & (df['N'] == 1024)].sort_values('BS')
        plt.plot(block_data['BS'], block_data['D1'], marker='o', label=f'{lang} N=1024')
    plt.title('Influencia del Block Size en la Tasa de Fallos L1')
    plt.xlabel('Block Size (BS)')
    plt.ylabel('D1 Miss Rate (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('cache_miss_bs_impact.png')

    print("Gráficas de caché generadas exitosamente.")

if __name__ == "__main__":
    main()