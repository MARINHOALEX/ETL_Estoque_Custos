import pandas as pd
import re

def transform_estoque(df, loja):
    """Transforma o DataFrame de estoque, separando nacionalizado e aguardando."""
    try:
        # Identifica o índice onde começa os dados
        indice = df.loc[df[df.columns[0]] == 'DATA NF ENTRADA'].index[0]
        df = df.loc[indice:].copy()
        
        # Define colunas com base na primeira linha
        df.columns = df.loc[indice].values
        df = df[df['DATA NF ENTRADA'] != 'DATA NF ENTRADA']
        df.dropna(subset=['ARMAZEM'], inplace=True)
        
        # Divide em nacionalizado e aguardando
        df_nac = df[df['SITUACAO'] == 'NACIONALIZADO'].copy()
        df_aguardando = df[df['SITUACAO'] == 'AGUARDANDO NACIONALIZAR'].copy()
        
        # Transformações comuns
        for df_temp in [df_nac, df_aguardando]:
            # Converte TON
            objeto = df_temp['TON'].apply(type) == str
            df_temp.loc[objeto, 'TON'] = (
                df_temp.loc[objeto, 'TON']
                .astype(str)
                .str[:6]
                .str.replace('.', '')
                .astype(float) / 1000
            )
            df_temp['TON'] = df_temp['TON'].astype(float).round(3)
            
            # Extrai ESPESSURA
            df_temp['ESPESSURA'] = (
                df_temp['BITOLA']
                .str.extract(r'(\d+,\d+|\d+)', expand=False)
                .str.replace(',', '.')
                .astype(float)
            )
            
            # Ajustes de espessura para HRC
            df_temp.loc[(df_temp['BOBINA'] == 'HRC') & (df_temp['ESPESSURA'] == 2.60), 'ESPESSURA'] = 2.65
            df_temp.loc[(df_temp['BOBINA'] == 'HRC') & (df_temp['ESPESSURA'] == 2.20), 'ESPESSURA'] = 2.25
            
            # Extrai ESPECIFICAÇÃO
            df_temp['ESPECIFICAÇÃO'] = (
                df_temp['BITOLA'].str.split('X').str[-1].str.split(' ').str[2:].str.join(' ')
            )
            
            # Converte ESPESSURA para string
            df_temp['ESPESSURA'] = df_temp['ESPESSURA'].apply(lambda x: f"{x:.2f}")
            
            # Anonimiza campos sensíveis
            df_temp['ARMAZEM'] = df_temp['ARMAZEM'].replace({
                'ARMAZEM_1': 'ARMAZEM_X',
                'ARMAZEM_2': 'ARMAZEM_Y',
            })
            df_temp['NAVIO'] = df_temp['NAVIO'].replace({
                'NAVIO_1': 'NAVIO_X',
                'NAVIO_2': 'NAVIO_Y',
            })
            df_temp['MATERIAL'] = df_temp['MATERIAL'].replace({
                'AÇO CARBONO': 'MATERIAL_A',
                'AÇO INOX': 'MATERIAL_B',
            })
            
            # Define colunas finais
            df_temp = df_temp[['PROPRIO', 'TXL - UP', 'TON', 'MATERIAL', 'DESCRICAO',
                              'CODIGO', 'ARMAZEM', 'NAVIO', 'ESPESSURA', 'ESPECIFICAÇÃO',
                              'SITUACAO']]
            df_temp['LOJA'] = loja
        
        return df_nac, df_aguardando
    except Exception as e:
        raise Exception(f"Erro na transformação de estoque: {str(e)}")

def transform_custo(df):
    """Transforma o DataFrame de custo."""
    try:
        df = df[['TXL - UP', 'BITOLA', 'CUSTO']].copy()
        df['Cod'] = df['TXL - UP'] + '-' + df['BITOLA']
        df['Cod'] = df['Cod'].str.replace('\xa0', ' ').str.strip()
        df['CUSTO'] = df['CUSTO'].astype(float)
        return df[['Cod', 'CUSTO']]
    except Exception as e:
        raise Exception(f"Erro na transformação de custo: {str(e)}")

def merge_custo(df_estoque, df_custo):
    """Realiza o merge entre estoque e custo."""
    try:
        df_estoque['Cod'] = df_estoque['TXL - UP'] + '-' + df_estoque['DESCRICAO']
        df_estoque['Cod'] = df_estoque['Cod'].str.replace('\xa0', ' ').str.strip()
        df_estoque = pd.merge(df_estoque, df_custo, on='Cod', how='left')
        df_estoque.fillna({'CUSTO': 0}, inplace=True)
        df_estoque.drop(columns=['Cod'], inplace=True)
        return df_estoque
    except Exception as e:
        raise Exception(f"Erro no merge com custo: {str(e)}")