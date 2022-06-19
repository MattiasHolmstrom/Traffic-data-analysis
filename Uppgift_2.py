#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mattias
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''Laddar in data till pandas dataframe'''
def loadfile(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data
    
'''Funktionen nedan plockar ur trafikflöde per timme.'''
def antalPerTimma(kamera):
    antal = np.zeros(18)
    tider = kamera['Tid']
    sliced_tider = tider.str.slice(stop = 2)
    timme = np.asarray(sliced_tider).astype(int)    
    for value in timme:
            antal[value] = antal[value]+1  
    return antal
        

'''Data plottas'''
df_kameraData = loadfile('kameraData.csv')
x = np.arange(7, 18, 1)
y = antalPerTimma(df_kameraData)

plt.plot(x, y[7:],  color='red', marker='o')
klock_x= ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
plt.xticks(x, klock_x)
plt.title('Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11')
plt.xlabel('Klockslag')
plt.ylabel('Antal Fordon')
plt.grid(True)
plt.show()
