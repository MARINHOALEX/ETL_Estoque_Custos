# ETL Stock and Cost Analytics

Este projeto implementa um pipeline ETL para processar dados de estoque e custos de de importação, gerando um relatório consolidado em Excel que serve como base para um dashboard para tomada de descisão.

**Afim de proteger os dados privados, os Dataframes de exemplo e as informações sensiveis nos códigos foram simuladas/anonimizadas utilizando AI.**

## Estrutura do Projeto
- **src/**: Contém os scripts Python (`main.py`, `extract.py`, `transform.py`, `load.py`).
- **data/**: Contém arquivos CSV fictícios com dados de estoque e custo.
- **.env.example**: Exemplo de arquivo de configuração.
- **requirements.txt**: Dependências do projeto.
- **LICENSE**: Licença MIT.
- **.gitignore**: Arquivos ignorados pelo Git.

## Pré-requisitos
- Python 3.12.6
- Dependências listadas em `requirements.txt`

## Estrutura dos Dados
- **sample_loja_a_estoque.csv** e **sample_loja_b_estoque.csv**: Dados de estoque (nacionalizado e aguardando).
- **sample_loja_a_custo.csv** e **sample_loja_b_custo.csv**: Dados de custo por item.
- **stock_report.xlsx**: Relatório final com abas `Estoque` (dados consolidados) e `Atualizacao` (data de execução).

## Transformações
- Limpeza de dados (remoção de nulos, ajuste de cabeçalhos).
- Anonimização de campos sensíveis (ARMAZEM, NAVIO, MATERIAL).
- Conversão de TON (divisão por 1000, arredondamento).
- Ajuste de ESPESSURA (ex.: 2.60 para 2.65 para HRC).
- Merge com dados de custo usando a chave específicas.

## Autor
Alex Marinho