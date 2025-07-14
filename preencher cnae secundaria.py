import pandas as pd
import re

# Carrega o arquivo
arquivo = 'Base 2.3 junho 2025.xlsx'
df = pd.read_excel(arquivo, sheet_name='Base de dados')
legenda = pd.read_excel(arquivo, sheet_name='cnaes')

# Prepara o dicionário da legenda (remove zeros à esquerda)
legenda_codigos = legenda.iloc[:, 0].astype(str).str.replace(r'\D', '', regex=True).str.lstrip('0')
dicionario_cnae = dict(zip(legenda_codigos, legenda.iloc[:, 1]))

# Função para traduzir a lista de CNAEs
def traduzir_cnaes(codigos):
    if pd.isna(codigos):
        return ''
    
    # Separa os códigos corretamente por vírgula (mantendo vírgulas intactas)
    codigos_separados = str(codigos).split(',')

    nomes_traduzidos = []

    for codigo in codigos_separados:
        # Remove qualquer coisa que não seja número e zeros à esquerda
        codigo_limpo = re.sub(r'\D', '', codigo).lstrip('0')

        # Só processa códigos com pelo menos 6 dígitos
        if len(codigo_limpo) >= 6:
            nome = dicionario_cnae.get(codigo_limpo, f'Código {codigo_limpo} não encontrado')
            nomes_traduzidos.append(nome)

    return ', '.join(nomes_traduzidos)

# Aplica a função à coluna CNAE FISCAL SECUNDÁRIA
df['cnae_secund_extenso'] = df['cnae_secund'].apply(traduzir_cnaes)

# Salva o arquivo
arquivo_saida = 'Base 2.3 junho 2025 - CNAE secundária FINAL CORRIGIDO.xlsx'
df.to_excel(arquivo_saida, index=False)

print(f'Arquivo salvo com sucesso como: {arquivo_saida}')





