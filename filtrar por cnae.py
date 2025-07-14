import pandas as pd
from tqdm import tqdm

# Lista de CNAEs a serem filtrados
lista_cnae = [
    111301, 111302, 111399, 112101, 112102, 112199, 113000, 115600, 116402, 116499,
    119901, 119902, 119905, 119906, 119907, 119908, 119999, 121101, 121102, 122900,
    131800, 132600, 133401, 133402, 133403, 133404, 133405, 133406, 133407, 133408,
    133409, 133410, 133499, 134200, 135100, 139303, 139304, 139305, 139306, 139399,
    141501, 141502, 142300, 153902, 155505, 159801, 161099, 163600, 210101, 210102,
    210103, 210104, 210106, 220903, 220904, 220905, 220999, 230600, 312403, 1031700,
    1032501, 1032599, 1033301, 1033302, 1041400, 1042200, 1043100, 1051100, 1052000,
    1053800, 1061901, 1061902, 1062700, 1063500, 1064300, 1065101, 1065102, 1066000,
    1069400, 1071600, 1072401, 1081301, 1081302, 1082100, 1092900, 1093701, 1093702,
    1094500, 1095300, 1099601, 1099602, 1099603, 1099605, 1099606, 1099607, 1099699,
    1111901, 1111902, 1112700, 1113502, 1122401, 1122402, 1122403, 1122499, 1311100,
    1312000, 1322700, 1340501, 1340599, 1353700, 1359600, 1412603, 1414200, 1422300,
    1521100, 1539400, 1629302, 1931400, 1932200, 2012600, 2013401, 2013402, 2029100,
    2062200, 2063100, 2110600, 2121101, 2121102, 2121103, 2122000, 2123800, 2219600,
    2342702, 2349499, 2399101, 2399102, 159899, 210199, 1013902, 1340502, 1351100,
    1352900, 1354500, 1510600, 1529700, 1540800, 2330303, 3212400, 3250705, 3291400,
    3299006
]

def filtrar_linhas(input_csv, output_csv, cnae_lista, chunksize=100000):
    # Criar arquivo de saída com cabeçalho
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        primeiro_chunk = True  # Para escrever o cabeçalho apenas no primeiro chunk
        
        # Ler o arquivo CSV em chunks
        for chunk in tqdm(pd.read_csv(input_csv, encoding='utf-8', sep=';', header=None, 
                                      low_memory=False, chunksize=chunksize), desc="Processando chunks"):
            
            # Remover espaços extras da coluna 12 (índice 11) e garantir que seja um número
            chunk[11] = chunk[11].apply(lambda x: str(x).strip() if isinstance(x, str) else x)

            # Converter os valores da coluna 12 para inteiro, se possível
            chunk[11] = pd.to_numeric(chunk[11], errors='coerce')  # Converte para NaN caso não seja numérico

            # Aplicar a condição de filtragem para CNAEs
            mask = chunk[11].isin(cnae_lista)

            # Filtrar o chunk de acordo com a máscara
            chunk_filtrado = chunk[mask]

            # Se houver dados filtrados, escrever no arquivo
            if not chunk_filtrado.empty:
                chunk_filtrado.to_csv(f_out, index=False, header=primeiro_chunk, sep=';', encoding='utf-8', mode='a')
                primeiro_chunk = False  # Apenas o primeiro chunk escreve o cabeçalho

    print(f"Linhas filtradas salvas em {output_csv}")

# Parâmetros
input_csv = 'filtrado_estados.csv'
output_csv = 'filtrado_ativo.csv'

# Executar
filtrar_linhas(input_csv, output_csv, lista_cnae, chunksize=100000)  # 100 mil linhas por chunk







