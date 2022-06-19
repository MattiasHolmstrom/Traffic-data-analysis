#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mattias
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''Läser in fil för att skapa en Dataframe vi kan hantera.'''
def loadfile(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data
    
def kommunval():
    kommun = input("Välj Kommun: ")
    return kommun

'''Påbyggnad från 3a för att ta fram böter och indragna körkort per vägnummer.'''
def overtradelse_analys(kommun, kamera_df, plats_df, pafoljd_df):
    
    '''Kopierar för ökad variabeltrygghet och enklare kodprocess.'''
    
    kamera_df_copy = kamera_df.copy()
    plats_df_copy = plats_df.copy()
    kommun_df = plats_df_copy.loc[plats_df_copy['Kommun'].str.contains(kommun)]
    
    plats_kamera_mrg = pd.merge(kamera_df_copy, plats_df_copy, left_on='MätplatsID', right_on='MätplatsID')

    df_over_analys = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Uppmätt Hastighet', 'Tidpunkt', 'Påföljd'])
    
    mat_id_lst = kommun_df['MätplatsID'].tolist()
    kamera_df_kommun = plats_kamera_mrg[plats_kamera_mrg['MätplatsID'].isin(mat_id_lst)]
    
    per_kommun = kamera_df_kommun.where(kamera_df_kommun['Gällande Hastighet'] < kamera_df_kommun['Hastighet']).dropna()
    
    '''analys df fylls med data från vald kommun'''
    df_over_analys['Max hastighet (km/h)'] = per_kommun['Gällande Hastighet'].tolist()
    df_over_analys['Vägnummer'] = per_kommun['Vägnummer'].tolist()
    df_over_analys['Uppmätt Hastighet'] = per_kommun['Hastighet'].tolist()
    
    date_time = per_kommun['Datum']+' '+per_kommun['Tid']
    df_over_analys['Tidpunkt'] = date_time.tolist()
    
    over_verdict = pafoljd_df['Påföljd'].tolist()
    over_limit = pafoljd_df['Hastighetsöverträdelse (km/h)'].tolist()

    hast_diff = 0.0

    straff_lst = []
    for a,b in zip(df_over_analys['Max hastighet (km/h)'], df_over_analys['Uppmätt Hastighet']):
        hast_diff = b-a
        hast_diff = round(hast_diff)

        # 0-30
        if (hast_diff > 0 and hast_diff <= over_limit[0]):
            # Varning och böter
            straff_lst.append(over_verdict[0])
        # 31-40
        elif (over_limit[0] < hast_diff <= over_limit[1]):
            # 2 mån
            straff_lst.append(over_verdict[1])
        # 41-50
        elif (over_limit[1] < hast_diff <= over_limit[2]):
            # 3 mån
            straff_lst.append(over_verdict[2])
        # 51-60
        elif (over_limit[2] < hast_diff <= over_limit[3]):
            # 4 mån
            straff_lst.append(over_verdict[3])
        # 61-70
        elif (over_limit[3] < hast_diff <= over_limit[4]):
            # 5 mån
            straff_lst.append(over_verdict[4])
        # 71-80
        elif (over_limit[4] < hast_diff <= over_limit[5]):
            # 6 mån
            straff_lst.append(over_verdict[5])
        # 81 +
        elif (over_limit[5] < hast_diff):
            # 8 mån
            straff_lst.append(over_verdict[6])

    df_over_analys['Påföljd'] = straff_lst
    print(df_over_analys['Uppmätt Hastighet'].nlargest(5))
    print(df_over_analys.loc[df_over_analys['Uppmätt Hastighet'] == 144.0].to_string())
    print(df_over_analys)
    return 0

kamera_df = loadfile('kameraData.csv')
plats_df = loadfile('platsData.csv')
pafoljd_df = loadfile('pafoljd.csv')

kommun = kommunval()
overtradelse_analys(kommun, kamera_df, plats_df, pafoljd_df)



