#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mattias
"""

import matplotlib.pyplot as plt
import pandas as pd


'''Läser in fil för att skapa en Dataframe vi kan hantera.'''
def loadfile(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data


kamera_data = loadfile('kameraData.csv')
plats_data = loadfile('platsData.csv')

''''''

def trafik_intensitet(kamera_data, plats_data):
    kamera_copy = kamera_data.copy()
    plats_data_copy = plats_data.copy()
    merge_kamera = pd.merge(kamera_copy, plats_data_copy, left_on='MätplatsID', right_on='MätplatsID')
    fordon = merge_kamera['MätplatsID'].value_counts()

    mtrafikerat = fordon.index[0]
    mest_trafik_saml = merge_kamera.loc[merge_kamera['MätplatsID'] == mtrafikerat].copy()

    mest_trafik_saml['Tid'] = pd.to_datetime(mest_trafik_saml['Tid'])
    
    klockslag=['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    bs =[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    mest_trafik_saml = pd.cut(mest_trafik_saml['Tid'].dt.hour, bs, labels=klockslag)

    output_data = mest_trafik_saml.value_counts(sort=False)

    return output_data, klockslag

    
''''''   

trafik_data, labels = trafik_intensitet(kamera_data, plats_data)
plt.bar(labels, trafik_data)
plt.title('Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11')
plt.xlabel('Klockslag')
plt.ylabel('Antal Fordon')




