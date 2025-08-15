import pandas as pd
from tqdm import tqdm

# Lista de CNAEs a serem filtrados
lista_cnae = [
    "0111301", "0111302", "0111303", "0111399", "0112101", "0112102", "0112199", "0113000",
    "0114800", "0115600", "0116401", "0116403", "0119901", "0119903", "0119904", "0119905",
    "0119906", "0119907", "0119908", "0119999", "0121101", "0121102", "0122900", "0131800",
    "0132600", "0133401", "0133402", "0133403", "0133404", "0133405", "0133406", "0133407",
    "0133408", "0133409", "0133410", "0133411", "0133499", "0135100", "0139301", "0139302",
    "0139303", "0139304", "0139305", "0139306", "0139399", "0141502", "0142300", "0151202",
    "0151203", "0152102", "3091101", "3091102", "3092000", "3099700", "3101200", "3102100",
    "3103900", "3104700", "3211601", "3211602", "3211603", "3212400", "3230200", "3240001",
    "3240002", "3240099", "3250701", "3250702", "3250703", "3250704", "3250705", "3250706",
    "3250707", "3250708", "3250709", "3291400", "3292201", "3292202", "3299001", "3299002",
    "3299004", "3299005", "3299006", "3299099", "3311200", "3312101", "3312102", "3312103",
    "3312104", "3313901", "3313902", "3313999", "3314701", "3314702", "3314703", "3314704",
    "3314706", "3314707", "3314708", "3314709", "3314710", "3314711", "3314712", "3314713",
    "3314714", "3314715", "3314716", "3314717", "3314718", "3314719", "3314720", "3314721",
    "3314722", "3314799", "3316301", "3316302", "3317101", "3319800", "3321000", "3329501",
    "3329599"
]

def filtrar_linhas(input_csv, output_csv, cnae_lista, chunksize=100000):
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        primeiro_chunk = True
        
        for chunk in tqdm(pd.read_csv(
            input_csv,
            encoding='utf-8',
            sep=';',
            header=None,
            dtype={11: str},  # Forçar coluna 11 como string
            low_memory=False,
            chunksize=chunksize
        ), desc="Processando chunks"):
            
            # Limpar espaços e garantir formato
            chunk[11] = chunk[11].str.strip()

            # Aplicar filtro
            mask = chunk[11].isin(cnae_lista)
            chunk_filtrado = chunk[mask]

            if not chunk_filtrado.empty:
                chunk_filtrado.to_csv(f_out, index=False, header=primeiro_chunk,
                                      sep=';', encoding='utf-8', mode='a')
                primeiro_chunk = False

    print(f"Linhas filtradas salvas em {output_csv}")


# Parâmetros
input_csv = 'estab_merged.csv'
output_csv = 'estab_cnae.csv'

# Executar
filtrar_linhas(input_csv, output_csv, lista_cnae, chunksize=100000)






