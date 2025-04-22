# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:50:14 2025

@author: dudad
"""

#%%
import os
import pandas as pd
import numpy as np
#%%

dataDir = r"C:\Users\dudad\Documents\GitHub\ENS5132\Trabalho\inputs\IQA_até_2021.csv"

df = pd.read_csv(dataDir, encoding='latin1')
 
 
try:
    df = pd.read_csv(dataDir, encoding='latin1')
    print(f"Arquivo '{dataDir}' lido com sucesso. DataFrame tem {len(df)} linhas.")

    # Especifique o nome da coluna que contém as unidades federativas
    coluna_uf = 'SGUF'  # Substitua pelo nome real da sua coluna de UF

    # Obtém os valores únicos das unidades federativas
    ufs_unicas = df[coluna_uf].unique()

    # Cria um dicionário para armazenar os DataFrames separados por UF
    dataframes_por_uf = {}

    # Itera pelas UFs únicas e cria um DataFrame para cada UF
    for uf in ufs_unicas:
        df_uf = df[df[coluna_uf] == uf].copy()
        dataframes_por_uf[uf] = df_uf

    # 'dataframes_por_uf' agora é um dicionário onde as chaves são as UFs
    # e os valores são os DataFrames correspondentes a cada UF.

    # Se você quiser uma lista de DataFrames em vez de um dicionário:  NÃO FICOU BOM LISTA
    #lista_de_dataframes_uf = list(dataframes_por_uf.values())

    # Agora 'lista_de_dataframes_uf' contém os DataFrames separados por UF.
    # Você pode acessar cada DataFrame pela sua posição na lista.
    # Por exemplo: lista_de_dataframes_uf[0], lista_de_dataframes_uf[1], etc.
    # Ou pelo nome da UF no dicionário: dataframes_por_uf['SP'], dataframes_por_uf['RJ'], etc.

    # Opcional: Imprimir o número de UFs encontradas e o número de linhas por UF
    print(f"\nO DataFrame foi separado por {len(ufs_unicas)} Unidades Federativas:")
    for uf, df_uf in dataframes_por_uf.items():
        print(f"UF: {uf} tem {len(df_uf)} linhas.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{dataDir}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo '{dataDir}': {e}")
