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
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as geop
#%% Lendo o arquivo

dataDir = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\IQA_até_2021.csv"

df = pd.read_csv(dataDir, encoding='latin1')

#tem q mudar o nome pq o X veio estranho do arquivo
df = df.rename(columns={'ï»¿X': 'longitude', 'Y': 'latitude'})
print(df.columns)

#%%separando cada unidade 
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

#%% criando mapas para cada UF

coluna_latitude = 'latitude'
coluna_longitude = 'longitude'
#%%
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
    #%% adicionando u shapifile do brasil
   # Caminho para o arquivo shapefile dos estados
path_estados = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\uf brasil\BR_UF_2023.shp"  # Substitua pelo caminho real

# Ler o shapefile
estados = geop.read_file(path_estados)

# Exibir as primeiras linhas do GeoDataFrame para entender sua estrutura
print(estados.head())
print(estados.crs) # Verificar o sistema de coordenadas 
    
    #%%
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plotar os estados
estados.plot(ax=ax, color='lightgray', edgecolor='black')

# Plotar seus dados de pontos no mesmo eixo
gdf.plot(ax=ax, marker='o', color='red', markersize=15)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Mapa dos Pontos com Delimitação dos Estados")

plt.show()
# plt.savefig('mapa_com_estados.png')
gdf = gdf.to_crs(estados.crs)
    
    #%%Fazendo um mapa com todos os pontos
    
    

geometry = [Point(xy) for xy in zip(df_com_coordenadas[coluna_longitude], df_com_coordenadas[coluna_latitude])]

df_com_coordenadas = df.dropna(subset=[coluna_latitude, coluna_longitude])
    # Criar um GeoDataFrame
gdf = geop.GeoDataFrame(df_com_coordenadas, geometry=geometry, crs="EPSG:4326") # CRS é o sistema de coordenadas (WGS 84)

    # Criar o mapa
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.plot(ax=ax, marker='o', color='red', markersize=15)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Mapa dos Pontos")
plt.show()

    # Para salvar o mapa como uma imagem:
    # plt.savefig('mapa_estatico.png')
#%% Grafico de datas     ATÉ AQUI TA LINDO MAS DAQUI PRA BAIXO AINDA NÃO TENTEI

ponto_de_interesse = 'NomeDoPontoEspecifico'  # Substitua pelo valor real da coluna de identificação do ponto

# Nome da coluna que identifica o ponto (ex: 'ENTIDADE')
coluna_ponto = 'ENTIDADE'  # Substitua pelo nome real da coluna de identificação

# Nome da coluna com a data da análise (pode precisar de formatação ou extração do ano)
coluna_data = 'DataDaAnalise'  # Substitua pelo nome real da coluna de data

# Nome da coluna com o resultado da análise (ex: 'IQA_Valor')
coluna_resultado = 'ValorDaAnalise'  # Substitua pelo nome real da coluna de resultado

try:
    df = pd.read_csv(dataDir, encoding='latin1')
    print(f"Arquivo '{dataDir}' lido com sucesso. DataFrame tem {len(df)} linhas.")

    # Filtrar os dados para o ponto de interesse
    df_ponto = df[df[coluna_ponto] == ponto_de_interesse].copy()

    # Verificar se a coluna de data já é o ano ou precisa de extração
    if df_ponto[coluna_data].dtype == 'object':
        # Tentar converter para datetime e extrair o ano
        try:
            df_ponto['Ano'] = pd.to_datetime(df_ponto[coluna_data]).dt.year
        except:
            print(f"A coluna '{coluna_data}' não pôde ser convertida para datetime. Verifique o formato.")
            exit()
    elif df_ponto[coluna_data].dtype in ['int64', 'float64']:
        # Assumir que já é o ano (ou precisa de ajuste dependendo dos seus dados)
        df_ponto['Ano'] = df_ponto[coluna_data].astype(int)
    else:
        print(f"Formato da coluna '{coluna_data}' não reconhecido.")
        exit()

    # Agrupar por ano e calcular a média do resultado (você pode usar outra função como max(), min(), etc.)
    resultados_por_ano = df_ponto.groupby('Ano')[coluna_resultado].mean()

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(resultados_por_ano.index, resultados_por_ano.values, marker='o', linestyle='-')
    plt.title(f'Variação da Análise para {ponto_de_interesse} ao Longo dos Anos')
    plt.xlabel('Ano')
    plt.ylabel('Valor da Análise (Média)')
    plt.grid(True)
    plt.xticks(resultados_por_ano.index.astype(int)) # Mostrar todos os anos no eixo x
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao processar o arquivo: {e}")


