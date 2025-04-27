# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 17:18:55 2025

@author: dudad
"""

import os
import pandas as pd
import numpy as np
import folium
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as geop
import re 
import matplotlib.ticker as ticker

#%%

dataDir = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\IQA_até_2021.csv"

df = pd.read_csv(dataDir, encoding='latin1')

#tem q mudar o nome pq o X veio estranho do arquivo
df = df.rename(columns={'ï»¿X': 'longitude', 'Y': 'latitude'})

coluna_uf = 'SGUF'
#%%
print(df.columns)
#%%


try:
    df = pd.read_csv(dataDir, encoding='latin1')
    print(f"Arquivo '{dataDir}' lido com sucesso. DataFrame tem {len(df)} linhas.")

    # Obtém os valores únicos das unidades federativas
    ufs_unicas = df[coluna_uf].unique()

    # Cria um dicionário para armazenar os DataFrames separados por UF
    dataframes_por_uf = {}

    # Itera pelas UFs únicas e cria um DataFrame para cada UF
    for uf in ufs_unicas:
        df_uf = df[df[coluna_uf] == uf].copy()
        dataframes_por_uf[uf] = df_uf

  
    print(f"\nO DataFrame foi separado por {len(ufs_unicas)} Unidades Federativas:")
    #for uf, df_uf in dataframes_por_uf.items():
        #print(f"UF: {uf} tem {len(df_uf)} linhas.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo '{dataDir}': {e}")
    
#%% criando mapas para cada UF

coluna_latitude = 'latitude'
coluna_longitude = 'longitude'
#%% direcionar diretório de saida
outputDir = "C:/Users/dudad/Documents/GitHub/ENS5132/Trabalho/outputs/mapas_por_uf_" # Diretório para salvar os mapas HTML

# Criar o diretório de saída se não existir
#if not os.path.exists(outputDir):
#    os.makedirs(outputDir)

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
    
#%%
df_com_coordenadas = df.dropna(subset=[coluna_latitude, coluna_longitude]).copy()
geometry = [Point(xy) for xy in zip(df_com_coordenadas[coluna_longitude], df_com_coordenadas[coluna_latitude])]
gdf = geop.GeoDataFrame(df_com_coordenadas, geometry=geometry, crs="EPSG:4326")

 # Converter o CRS do gdf para o mesmo dos estados (se necessário)
gdf = gdf.to_crs(estados.crs)

    # 2. Plotar o mapa com os estados e seus pontos
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
estados.plot(ax=ax, color='lightgreen', edgecolor='black')
gdf.plot(ax=ax, marker='o', color='blue', markersize=2)ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Pontos de Análise de IQA do Brasil")
plt.show()
# plt.savefig('mapa_com_estados.png')    