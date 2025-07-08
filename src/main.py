import os
import datetime
from dotenv import load_dotenv
import pandas as pd
from extract import extract_data
from transform import transform_estoque, transform_custo, merge_custo
from load import save_to_excel

def main():
    """Executa o pipeline ETL para processar dados de estoque e custos."""
    print("Iniciando pipeline ETL...")
    
    try:
        # Carrega variáveis de ambiente
        load_dotenv()
        base_path = os.getenv("BASE_PATH", "data/")
        output_file = os.getenv("OUTPUT_FILE", "stock_report.xlsx")

        # Lista de lojas e arquivos
        lojas = {
            "Loja_A": {
                "estoque": "sample_loja_a_estoque.csv",
                "custo": "sample_loja_a_custo.csv",
            },
            "Loja_B": {
                "estoque": "sample_loja_b_estoque.csv",
                "custo": "sample_loja_b_custo.csv",
            },
        }

        # Processa dados para cada loja
        dfs_estoque = []
        for loja, files in lojas.items():
            print(f"Processando dados da {loja}...")
            
            # Extração
            df_estoque = extract_data(os.path.join(base_path, files["estoque"]))
            df_custo = extract_data(os.path.join(base_path, files["custo"]))
            
            # Transformação
            df_estoque_nac, df_estoque_aguardando = transform_estoque(df_estoque, loja)
            df_custo = transform_custo(df_custo)
            
            # Merge com custo
            df_estoque_nac = merge_custo(df_estoque_nac, df_custo)
            df_estoque_aguardando = merge_custo(df_estoque_aguardando, df_custo)
            
            # Concatena dados
            dfs_estoque.append(pd.concat([df_estoque_nac, df_estoque_aguardando]))
        
        # Concatena todos os dados
        df_final = pd.concat(dfs_estoque, ignore_index=True)
        
        # Data de atualização
        update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_update = pd.DataFrame({'Atualizacao': [update]})
        
        # Salva no Excel
        print(f"Salvando arquivo {output_file}...")
        save_to_excel(df_final, df_update, os.path.join(base_path, output_file))
        print("Arquivo atualizado com sucesso!")
    
    except Exception as e:
        print(f"Erro no pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()