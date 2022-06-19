#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mattias
"""


import pandas as pd

'''Laddar in data till pandas dataframe'''
def loadfile(filename):
    data = pd.read_csv(filename, encoding= 'latin1', sep=';')
    return data

'''Skapar efterfrågad tabell enligt uppgiftsbeskrivning'''
def platser(data):
    df2 = data.rename(columns = {'MätplatsID':'Antal Kameror', 'Vägnummer':'Vägnummer    Antal Kameror'})
    grupp = df2.groupby(['Kommun', 'Vägnummer    Antal Kameror'])[ 'Antal Kameror'].count()
    return grupp
    

'''Funktions anrop samt utskrivning av data'''
df_platsData = loadfile('platsData.csv')
grupp = platser(df_platsData)
print('   Hastighetsövervakning i Västra Götaland')
print(grupp)
