import pandas as pd
from tqdm import tqdm

# Lista de UFs da Amazônia Legal
estados_amazonia_legal = ['AC', 'AM', 'AP', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

def filtrar_amazonia_e_ativas(input_csv, output_csv, lista_ufs, chunksize=100_000):
    # Criar/limpar o arquivo de saída
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        primeiro_chunk = True
        
        # Processa em chunks
        for chunk in tqdm(pd.read_csv(input_csv, encoding='utf-8', sep=';', header=None,
                                      low_memory=False, chunksize=chunksize), desc="Processando chunks"):

            # Normaliza a coluna UF (coluna 18 → índice 18)
            chunk[18] = chunk[18].astype(str).strip().str.upper()

            # Normaliza a coluna de situação cadastral (coluna 6 → índice 5)
            chunk[5] = chunk[5].astype(str).str.strip()

            # Filtra por UF da Amazônia Legal e empresas ativas (coluna 5 == '02')
            mask = (chunk[18].isin(lista_ufs)) & (chunk[5] == '02')
            chunk_filtrado = chunk[mask]

            # Salva se não estiver vazio
            if not chunk_filtrado.empty:
                chunk_filtrado.to_csv(f_out, index=False, header=primeiro_chunk, sep=';', encoding='utf-8', mode='a')
                primeiro_chunk = False

    print(f"Linhas filtradas salvas em: {output_csv}")

# Parâmetros
input_csv = 'filtrado_estados.csv'
output_csv = 'filtrado_amazonia_ativas.csv'

# Executar
filtrar_amazonia_e_ativas(input_csv, output_csv, estados_amazonia_legal)
