# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:50:14 2025

@author: duda matos
"""

#%%
import os
import pandas as pd
import numpy as np
import folium
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as geop
import re 
import matplotlib.ticker as ticker
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
    #for uf, df_uf in dataframes_por_uf.items():
        #print(f"UF: {uf} tem {len(df_uf)} linhas.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo '{dataDir}': {e}")
    


#%%

#%% criando mapas para cada UF

coluna_latitude = 'latitude'
coluna_longitude = 'longitude'
#%% direcionar diretório de saida
outputDir = "C:/Users/dudad/Documents/GitHub/ENS5132/Trabalho/outputs/mapas_por_uf" # Diretório para salvar os mapas HTML

# Criar o diretório de saída se não existir
#if not os.path.exists(outputDir):
#    os.makedirs(outputDir)
#%%
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
gdf.plot(ax=ax, marker='o', color='red', markersize=10)

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
gdf.plot(ax=ax, marker='o', color='red', markersize=10)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Mapa dos Pontos")
plt.show()

    # Para salvar o mapa como uma imagem:
    # plt.savefig('mapa_estatico.png')
#%%     ATÉ AQUI TA LINDO MAS DAQUI PRA BAIXO AINDA NÃO TENTEI

#%%  GRÁFICO DE DISPERSÃO TORCENDO PRA DAR BOM  
# ta teve q tratar mais os dados do que eu imaginei mas bora lá
uf_sele = 'SP'

# Substituir espaços vazios por nan em todas as colunas 

prefixos = ['MED_','MIN_','MAX_']

anos = range(1978, 2020)
colunas_anos = [prefixo + str(ano) for prefixo in prefixos for ano in anos]
 

#df[colunas_anos] = df[colunas_anos].apply(lambda col: col.str.strip()).replace('', np.nan)



#%%    Desconsidera esse e vai pro proximo la na linha 235
df_uf = df[df['SGUF'] == uf_sele]
#%%
df = df.rename(columns={'ReservatÃ³rio do Rio Grande': 'Reservatorio do Rio Grande'})
#%%

pasta_graficos =  r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\outputs\graficos_SP"
print(df_uf['CORPODAGUA'].apply(type).unique())

#%% ARRUMAR DADOS
#pasta_graficos =  r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\outputs\graficos_SC_"
df_uf = df_uf.dropna(subset=['CORPODAGUA'])
print(f"Linhas com NaN na coluna 'CORPODAGUA' foram excluídas. Novo tamanho do DataFrame: {len(df_uf)}")



def sanitize_filename(filename):
    """Remove caracteres especiais e espaços de um nome de arquivo."""
    sanitized_name = filename.replace(" ", "_")
    # Remove caracteres que não são alfanuméricos, underscores ou pontos
    sanitized_name = re.sub(r'[^a-zA-Z0-9_.]', '', sanitized_name)
    return sanitized_name


print(df_uf['CORPODAGUA'].apply(type).unique())
#%%

print(df_uf.iloc[20:66]['CORPODAGUA'])
#%%definir quais corpos dagua
lista_pontos =[
    'ReservatÃ³rio do Rio Grande',
    'Rio CubatÃ£o',
]



#%%

anos_analise = range(1979, 2022)

anos_rotulos = [ano for ano in anos_analise if ano % 10 == 0]  # Filtra de 10 em 10

print(f"anos_plot: {anos_plot}")
print(f"anos_rotulos: {anos_rotulos}")
#%%


for index, row in df_uf.iterrows():
    nome_ponto_original = str(row['CORPODAGUA'])  # Conversão para string AQUI
    nome_ponto_limpo = sanitize_filename(nome_ponto_original)
    anos_str = [str(ano) for ano in range(1978, 2022)]
    anos_plot = [int(ano) for ano in anos_str]
   
for corpo_dagua in lista_pontos:
    # Filtra o DataFrame df_uf para incluir apenas o CORPODAGUA atual
    df_uf_filtrado = df_uf[df_uf['CORPODAGUA'] == corpo_dagua]

    # Verifica se o corpo d'água foi encontrado no DataFrame
    if df_uf_filtrado.empty:
        print(f"O CORPODAGUA '{corpo_dagua}' não foi encontrado nos dados para a UF selecionada.")
    else:
        for index, row in df_uf_filtrado.iterrows():
            nome_ponto_original = str(row['CORPODAGUA'])
            nome_ponto_limpo = sanitize_filename(nome_ponto_original)
            anos_str = [str(ano) for ano in range(1979, 2022)]
            anos_plot = [int(ano) for ano in anos_str]
            
    plt.figure(figsize=(25, 5))

  # Gráfico de Médio
    plt.subplot(1,3 , 1)
    colunas_medio = ['MED_' + ano for ano in anos_str]
    valores_medio = row[colunas_medio].tolist()
    plt.scatter(anos_plot, valores_medio)
    plt.title(f'{nome_ponto_original} - Médio')
    plt.xlabel('Ano')
    plt.ylabel('Valor Médio')
    
    ax = plt.gca()

    # Grade vertical a cada 2 anos
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.grid(True, which='major', linestyle='-', alpha=0.5)

    # Grade horizontal a cada 5 no eixo y
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.grid(True, which='major', linestyle='-', alpha=0.5)

    plt.xticks(anos_rotulos)  # Ticks apenas para cada 10 anos
    nome_arquivo_medio = os.path.join(pasta_graficos, f'{nome_ponto_limpo}_medio.png')
    plt.savefig(nome_arquivo_medio)
    plt.close()

    
    

    plt.figure(figsize=(25, 5))

    # Gráfico de Máximo
    plt.subplot(1, 3, 1)
    colunas_maximo = ['MAX_' + ano for ano in anos_str]
    valores_maximo = row[colunas_maximo].tolist()
    plt.scatter(anos_plot, valores_maximo)
    plt.title(f'{nome_ponto_original} - Máximo')
    plt.xlabel('Ano')
    plt.ylabel('Valor Máximo')
    plt.grid(True)
    plt.xticks(anos_rotulos)

    # Salvar o gráfico de máximo com nome de arquivo limpo
    nome_arquivo_maximo = os.path.join(pasta_graficos, f'{nome_ponto_limpo}_maximo.png')
    plt.savefig(nome_arquivo_maximo)
    plt.close()

    plt.figure(figsize=(25, 5))

    # Gráfico de Mínimo
    plt.subplot(1, 3, 1)
    colunas_minimo = ['MIN_' + ano for ano in anos_str]
    valores_minimo = row[colunas_minimo].tolist()
    plt.scatter(anos_plot, valores_minimo)
    plt.title(f'{nome_ponto_original} - Mínimo')
    plt.xlabel('Ano')
    plt.ylabel('Valor Mínimo')
    plt.grid(True)
    plt.xticks(anos_rotulos)

    # Salvar o gráfico de mínimo com nome de arquivo limpo
    nome_arquivo_minimo = os.path.join(pasta_graficos, f'{nome_ponto_limpo}_minimo.png')
    plt.savefig(nome_arquivo_minimo)
    plt.close()

print(f"Gráficos salvos na pasta '{pasta_graficos}'")







