import pandas as pd
from tqdm import tqdm

# Lista de UFs da Amazônia Legal
estados_amazonia_legal = ['AC', 'AM', 'AP', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

def filtrar_amazonia_e_ativas(input_csv, output_csv, lista_ufs, chunksize=100_000):
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        primeiro_chunk = True
        
        for chunk in tqdm(pd.read_csv(
            input_csv,
            encoding='utf-8',
            sep=';',
            header=None,
            low_memory=False,
            chunksize=chunksize,
            skiprows=1  # Ignorar cabeçalho que veio do primeiro script
        ), desc="Processando chunks"):

            # Garantir que UF (coluna 19) é string sem espaços
            chunk[19] = chunk[19].astype(str).str.strip()

            # Garantir que situação cadastral (coluna 5) é string com dois dígitos
            chunk[5] = chunk[5].astype(str).str.zfill(2)

            # Filtro
            mask = (chunk[19].isin(lista_ufs)) & (chunk[5] == '02')
            chunk_filtrado = chunk[mask]

            if not chunk_filtrado.empty:
                chunk_filtrado.to_csv(
                    f_out,
                    index=False,
                    header=primeiro_chunk,
                    sep=';',
                    encoding='utf-8',
                    mode='a'
                )
                primeiro_chunk = False

    print(f"Linhas filtradas salvas em: {output_csv}")


# Parâmetros
input_csv = 'estab_cnae.csv'
output_csv = 'filtrado_amazonia_ativas.csv'

# Executar
filtrar_amazonia_e_ativas(input_csv, output_csv, estados_amazonia_legal)


