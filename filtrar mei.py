import csv

def selecionar_linhas(arquivo_base, arquivo_alvo, arquivo_saida):
    # Ler os valores da primeira coluna do arquivo base e armazenar em um conjunto
    valores_base = set()
    with open(arquivo_base, 'r', newline='', encoding='utf-8') as f_base:
        reader = csv.reader(f_base, delimiter=';')
        for row in reader:
            valores_base.add(row[0].replace('"', ''))

    # Ler o arquivo alvo e gravar as linhas desejadas no arquivo de saída
    with open(arquivo_alvo, 'r', newline='', encoding='utf-8') as f_alvo, \
            open(arquivo_saida, 'w', newline='', encoding='utf-8') as f_saida:
        reader = csv.reader(f_alvo, delimiter=';', quoting=csv.QUOTE_NONE)
        writer = csv.writer(f_saida, delimiter=";")
        for row in reader:
            # Remover aspas da primeira coluna
            row[0] = row[0].replace('"', '')
            if row[0] in valores_base:
                writer.writerow(row)
                
# Exemplo de uso
arquivo_base = 'filtrado_ativo.csv'
arquivo_alvo = 'simples.csv'
arquivo_saida = 'bio_simples.csv'

selecionar_linhas(arquivo_base, arquivo_alvo, arquivo_saida)


