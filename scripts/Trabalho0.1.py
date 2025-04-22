# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:50:14 2025

@author: dudad
"""

#%%
import os
import pandas as pd
import numpy as np
import folium
#%% separando cada unidade 

dataDir = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\IQA_até_2021.csv"

df = pd.read_csv(dataDir, encoding='latin1')

coluna_uf = 'SGUF'
try:
    df = pd.read_csv(dataDir, encoding='latin1')
    print(f"Arquivo '{dataDir}' lido com sucesso. DataFrame tem {len(df)} linhas.")

    # Especifique o nome da coluna que contém as unidades federativas
      # Substitua pelo nome real da sua coluna de UF

    # Obtém os valores únicos das unidades federativas
    ufs_unicas = df[coluna_uf].unique()

    # Cria um dicionário para armazenar os DataFrames separados por UF
    dataframes_por_uf = {}

    # Itera pelas UFs únicas e cria um DataFrame para cada UF
    for uf in ufs_unicas:
        df_uf = df[df[coluna_uf] == uf].copy()
        dataframes_por_uf[uf] = df_uf

  
    print(f"\nO DataFrame foi separado por {len(ufs_unicas)} Unidades Federativas:")
    for uf, df_uf in dataframes_por_uf.items():
        print(f"UF: {uf} tem {len(df_uf)} linhas.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo '{dataDir}': {e}")
    


#%%
df = df.rename(columns={'latitude': 'longitude', 'longitude': 'latitude'})
print(df.columns)

#%%
coluna_latitude = 'latitude'
coluna_longitude = 'longitude'

outputDir = "C:/Users/dudad/Documents/GitHub/ENS5132/Trabalho/outputs/mapas_por_uf" # Diretório para salvar os mapas HTML

# Criar o diretório de saída se não existir
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

try:
    # Filtrar linhas com dados de latitude e longitude válidos
    df_com_coordenadas = df.dropna(subset=[coluna_latitude, coluna_longitude, coluna_uf])

    # Obter a lista única de Unidades Federativas
    ufs_unicas = df_com_coordenadas[coluna_uf].unique()

    # Iterar por cada UF única
    for uf in ufs_unicas:
        # Filtrar o DataFrame para a UF atual
        df_uf = df_com_coordenadas[df_com_coordenadas[coluna_uf] == uf]

        if not df_uf.empty:
            # Calcular o centro do mapa para a UF atual
            centro_lat = df_uf[coluna_latitude].mean()
            centro_lon = df_uf[coluna_longitude].mean()

            # Criar o mapa para a UF atual
            mapa_uf = folium.Map(location=[centro_lat, centro_lon], zoom_start=6) # Ajuste o zoom conforme necessário

            # Adicionar marcadores para cada ponto na UF
            for index, row in df_uf.iterrows():
                latitude = row[coluna_latitude]
                longitude = row[coluna_longitude]
                popup_text = f"UF: {uf}<br>Latitude: {latitude}<br>Longitude: {longitude}"
                folium.Marker([latitude, longitude], popup=popup_text).add_to(mapa_uf)

            # Salvar o mapa para a UF atual em um arquivo HTML
            nome_arquivo = os.path.join(outputDir, f'mapa_{uf}.html')
            mapa_uf.save(nome_arquivo)
            print(f"Mapa para a UF {uf} salvo em {nome_arquivo}")
        else:
            print(f"Não foram encontradas coordenadas para a UF {uf}.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao processar o arquivo: {e}")