# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 17:02:59 2025

@author: dudad
"""
#%% importando 
import os
import pandas as pd
#import numpy as np
#import folium
#from shapely.geometry import Point
import matplotlib.pyplot as plt
#import geopandas as geop
import re 
import matplotlib.ticker as ticker
#%%
dataDir = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\ODSerieHistorica.csv"

#%% ver em ia como em vez de usar um arquivo tirar as informações de turb e fosforo de dois diferentes e 
#utilizar eles juntos ou separados para retirar as informações dos pontos escolhidos 
dataTurb = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\TurbidezSerieHistotica.csv"
dataFos = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\FosforoTotalSerieHistorica.csv"
parametro = 'Oxigenio_Dissolvido'
#%%
df = pd.read_csv(dataDir, encoding='latin1')

coluna_uf = 'SGUF'

uf_sele = 'MT'

# Substituir espaços vazios por nan em todas as colunas 
prefixos=['MED_','MIN_', 'MAX_']
#prefixos = ['med_','min_','max_']

anos = range(2003, 2020)
colunas_anos = [prefixo + str(ano) for prefixo in prefixos for ano in anos]

#cdestacao

df_uf = df[df['SGUF'] == uf_sele]
#%%


df_uf = df_uf.dropna(subset=['CDESTACAO'])
print(f"Linhas com NaN na coluna 'CORPODAGUA' foram excluídas. Novo tamanho do DataFrame: {len(df_uf)}")



def sanitize_filename(filename):
    """Remove caracteres especiais e espaços de um nome de arquivo."""
    sanitized_name = filename.replace(" ", "_")
    # Remove caracteres que não são alfanuméricos, underscores ou pontos
    sanitized_name = re.sub(r'[^a-zA-Z0-9_.]', '', sanitized_name)
    return sanitized_name


print(df_uf['CDESTACAO'].apply(type).unique())
#%%
#print(df_uf.iloc[20:66]['corpodagua'])

print(df.columns)

#%%
pasta_graficos =  r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\outputs\analisedeParametros"

#definir quais corpos dagua
lista_pontos =[

    'CBA671', 'JAU389']

#%%
anos_analise = range(2003, 2021)
anos_str = [str(ano) for ano in anos_analise]
anos_plot = list(anos_analise)
valores_min = []
#anos_rotulos = list(range(min(anos_analise), max(anos_analise) + 1, 10))

#%%
for corpo_dagua in lista_pontos:
    # Filtra o DataFrame df_uf para incluir apenas o CORPODAGUA atual
    df_uf_filtrado = df_uf[df_uf['CDESTACAO'] == corpo_dagua]

    # Verifica se o corpo d'água foi encontrado no DataFrame
    if not df_uf_filtrado.empty:
        for index, row in df_uf_filtrado.iterrows():
            nome_ponto_original = str(row['CORPODAGUA'])
            nome_ponto_limpo = sanitize_filename(nome_ponto_original)

            plt.figure(figsize=(18, 6))  # Uma única figura para os três subplots
            plt.suptitle(f'Variação Anual - {parametro} - {nome_ponto_limpo}', fontsize=16, y=0.98)
            
            # Gráfico de Médio (subplot 1)
            plt.subplot(1, 3, 1)
            colunas_medio = ['MED_' + ano for ano in anos_str]
            valores_medio = row[colunas_medio].tolist()
            plt.plot(anos_plot, valores_medio)
            plt.title(' Médio')
            plt.xlabel('Ano')
            plt.ylabel('Valor Médio')
            ax = plt.gca()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
            ax.xaxis.grid(True)#, which='major', linestyle='-', alpha=0.5)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
            ax.yaxis.grid(True)#, which='major', linestyle='-', alpha=0.5)
            plt.xticks(anos_plot, rotation=45, ha='right')
            plt.xlim(min(anos_plot) - 1, max(anos_plot) + 1)
            

            # Gráfico de Máximo (subplot 2)
            plt.subplot(1, 3, 2)
            colunas_maximo = ['MAX_' + ano for ano in anos_str]
            valores_maximo = row[colunas_maximo].tolist()
            plt.plot(anos_plot, valores_maximo)
            plt.title( 'Máximo')#{nome_ponto_original}
            plt.xlabel('Ano')
            plt.ylabel('Valor Máximo')
            ax = plt.gca()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
            ax.xaxis.grid(True)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
            ax.yaxis.grid(True)
            plt.xticks(anos_plot, rotation=45, ha='right')
            plt.xlim(min(anos_plot) - 1, max(anos_plot) + 1)
            
            # Gráfico de Mínimo (subplot 3)
            plt.subplot(1, 3, 3)
            colunas_minimo = ['MIN_' + ano for ano in anos_str]
            valores_minimo = row[colunas_minimo].tolist()
            plt.plot(anos_plot, valores_minimo)
            plt.title(' Mínimo') 
            plt.xlabel('Ano')
            plt.ylabel('Valor Mínimo')
            ax = plt.gca()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
            ax.xaxis.grid(True)#, which='major', linestyle='-', alpha=0.5)
            ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
            ax.yaxis.grid(True)#, which='major', linestyle='-', alpha=0.5)
            plt.xticks(anos_plot, rotation=45, ha='right')
            plt.xlim(min(anos_plot) - 1, max(anos_plot) + 1)

            plt.tight_layout()  # Ajusta o espaçamento entre os subplots
            nome_arquivo = os.path.join(pasta_graficos, f'{parametro}_{nome_ponto_limpo}.png')
            plt.savefig(nome_arquivo)
            plt.close()

print(f"Gráficos dos três tipos (Médio, Máximo, Mínimo) salvos na pasta '{pasta_graficos}' para os corpos d'água especificados.")




