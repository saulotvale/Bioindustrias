import csv
import os
from glob import glob

# Configurações com caminho completo
pasta_origem = r'C:\Users\Saulo Vale\Documents\Pitao escriptes\empresas'
arquivo_saida = r'C:\Users\Saulo Vale\Documents\Pitao escriptes\empre_consolidado.csv'

contador = 0

# Processa os arquivos
with open(arquivo_saida, 'w', encoding='utf-8', newline='') as f_out:
    writer = csv.writer(f_out, delimiter=';')
    
    # Lista todos os arquivos CSV da pasta
    arquivos_csv = glob(os.path.join(pasta_origem, '*.csv'))
    total_arquivos = len(arquivos_csv)
    
    if total_arquivos == 0:
        print("Nenhum arquivo CSV encontrado na pasta especificada!")
        exit()
    
    print(f"Iniciando processamento de {total_arquivos} arquivos...")
    
    for i, arquivo in enumerate(arquivos_csv, 1):
        print(f"Processando arquivo {i}/{total_arquivos}: {os.path.basename(arquivo)}")
        
        # Abre em modo binário para remover caracteres nulos
        with open(arquivo, 'rb') as f_in_bin:
            # Filtra caracteres nulos (0x00) e decodifica
            for bin_line in f_in_bin:
                # Remove bytes nulos e decodifica de latin1 para string
                clean_line = bin_line.replace(b'\x00', b'').decode('latin1').strip()
                
                # Ignora linhas vazias após limpeza
                if not clean_line:
                    continue
                
                # Converte a linha limpa para lista de campos
                try:
                    row = next(csv.reader([clean_line], delimiter=';'))
                except csv.Error as e:
                    print(f"  Erro na linha: {clean_line[:100]}... | {e}")
                    continue
                
                # Escreve a linha processada
                writer.writerow(row)
                contador += 1
                
                # Exibe progresso a cada 500 mil registros
                if contador % 500000 == 0:
                    print(f"  Registros processados: {contador:,}")

print("\n" + "="*50)
print(f"Consolidação concluída com sucesso!")
print(f"Total de arquivos processados: {total_arquivos}")
print(f"Total de registros consolidados: {contador:,}")
print(f"Arquivo de saída: {arquivo_saida}")
print("="*50)