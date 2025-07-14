# Bioindustrias
Códigos necessários para a produção e/ou atualização da base de dados de bioindústrias da Amazônia Legal

Metodologia de atualização da base de bioindústrias
1)	Acessar base da Receita Federal e baixar os arquivos referentes a estabelecimentos, empresas e do simples nacional:
Fonte: https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj
2)	Fazer a junção dos arquivos, sendo um arquivo para estabelecimentos e um arquivo para empresas com os códigos de junção de nome "Juntatcsvs.py"
3)	Filtrar os arquivos pela lista de cnaes escolhidos tanto no arquivos de estabelecimentos, quanto no arquivo de empresas com o código de nome "filtrar por cnae.py"
4)	Realizar um merge  dos estabelecimentos e das empresas para ter as informações em um lugar só com o código "merge de cnpjs.py"
5)	Adicionar a  informação de se é MEI ou não pegando os arquivos do merge e juntando com a base do simples nacional com o código "filtrar_mei.py"
6)  Filtrar para o estado da amazônia legal com o código "filtrar ativas e amazonia legal.py"
7)	Realizar a adição dos códigos de natureza jurídica, CNAE e código de município do ibge no excel utilizando a fórmula PROCV e os arquivos presentes na base de CNPJs da receita federal, o excel foi utilizado dada o volume de dados, que aqui é mais ou menos 10k linhas.
8)	Realizar mediante busca ativa e por rêferencias a verificação de critérios de sustentabilidade produzidos pela equipe do projeto
O passo 6 pode ser realizado logo após  da junção, que ai deixa os arquivos mais leves.
