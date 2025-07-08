import pandas as pd

def extract_data(file_path):
    """Lê um arquivo CSV e retorna um DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo {file_path}: {str(e)}")