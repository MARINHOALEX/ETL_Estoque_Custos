import pandas as pd

def save_to_excel(df_estoque, df_update, output_path):
    """Salva os DataFrames em um arquivo Excel."""
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_estoque.to_excel(writer, sheet_name='Estoque', index=False)
            df_update.to_excel(writer, sheet_name='Atualizacao', index=False)
    except Exception as e:
        raise Exception(f"Erro ao salvar o arquivo Excel: {str(e)}")