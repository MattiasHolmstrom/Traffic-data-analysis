#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mattias
"""
import pandas as pd
import numpy as np

'''Läser in fil för att skapa en Dataframe vi kan hantera.'''
def loadfile(filename):
    data = pd.read_csv(filename, encoding='latin', sep=';')
    return data 

'''Skapar sorterad tabell för kommuner, sorterad på procentuellt antal överträdelser.'''
def speeding(kamera_df, plats_df):
    kamera_df_copy = kamera_df.copy()
    plats_df_copy = plats_df.copy()
    
    
    plats_kamera_mrg = pd.merge(kamera_df_copy, plats_df_copy, left_on='MätplatsID', right_on='MätplatsID')
    bilar_perv = plats_kamera_mrg.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Antal fordon')
    bilar_perv.sort_values(['Kommun', 'Vägnummer'], inplace=True)

    kor_f_fort = plats_kamera_mrg.where(plats_kamera_mrg['Gällande Hastighet'] < plats_kamera_mrg['Hastighet']).dropna()
    kor_f_fort = kor_f_fort.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Överträdelser (%)')
    kor_f_fort.sort_values(['Kommun', 'Vägnummer'], inplace=True)


    '''Hastighetsöverträdelser räknas ut efter att data hanterats och sorterats.'''
    overtradelser_sum = np.array(kor_f_fort['Överträdelser (%)'])
    fordon_sum = np.array(bilar_perv['Antal fordon'])
    procentuellt = overtradelser_sum / fordon_sum * 100
    kor_f_fort['Överträdelser (%)'] = procentuellt
    kor_f_fort.sort_values(by='Överträdelser (%)', inplace=True, ascending=False)
    kor_f_fort.reset_index(inplace=True, drop=True)
    
    return kor_f_fort
    
    
kamera_df = loadfile('kameraData.csv')
plats_df = loadfile('platsData.csv')

out = speeding(kamera_df, plats_df)
print(out.to_string())
