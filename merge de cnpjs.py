import pandas as pd

# Caminhos dos arquivos
arquivo_estab = 'estab_cnae.csv'
arquivo_empresas = 'estab_merged.csv'
arquivo_saida = 'estab_empre.csv'

# 1. Carrega a base de empresas inteira (assumindo que ela é menor)
df_empresas = pd.read_csv(arquivo_empresas, encoding="utf-8", sep=";", header=None, dtype={0: str})
df_empresas[0] = df_empresas[0].str.strip('"')

# 2. Define o tamanho do chunk
chunk_size = 100_000  # ajuste conforme sua RAM

# 3. Cria o arquivo de saída vazio ou sobrescreve se já existir
with open(arquivo_saida, 'w', encoding='utf-8') as f:
    pass  # apenas limpa o conteúdo

# 4. Processa a base de estabelecimentos em chunks
for i, chunk in enumerate(pd.read_csv(arquivo_estab, encoding="utf-8", sep=";", header=None,
                                      dtype={0: str}, chunksize=chunk_size)):
    chunk[0] = chunk[0].str.strip('"')

    # Merge com base na coluna 0 (CNPJ)
    df_merged = pd.merge(chunk, df_empresas, on=0, how='left')

    # Salva o resultado, sem header e sem index
    df_merged.to_csv(arquivo_saida, mode='a', index=False, header=False, sep=';', encoding='utf-8')

    print(f'Chunk {i+1} processado e salvo.')

print("Merge completo! Arquivo salvo em 'merge_estab_empresas.csv'.")
