#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mattias
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

''''''
def loadfile(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data
'''Skapar diagrammet genom att sortera och filtrera för vald kommun och hastigheter per tid. '''   
def createDiagram(kommun, platsdata, kameradata):
    merged_plats_kamera = platsdata.merge(kameradata, on= 'MätplatsID')
    mdf_update = merged_plats_kamera.drop(['Namn', 'Datum', 'MätplatsID'], axis=1)
    kommun_spec = mdf_update.loc[mdf_update['Kommun'] == kommun]
    kommun_spec['Tid'] = kommun_spec['Tid'].str.slice(stop = 2)
    
    medelhast_pertimme = np.zeros(18)
    roads = kommun_spec.drop_duplicates(subset = ['Vägnummer'])
    roads_k = roads['Vägnummer'].tolist()
    
    '''Data placeras i listor samt arrayer för enklare hantering och plottning.'''
    hs_vagar = []
    mhs_vagar = []
    for j in range(len(roads_k)):
        medelhast_pertimme = np.zeros(18)
        pervag = kommun_spec.loc[kommun_spec['Vägnummer'] == roads_k[j]]
        hs = pervag.drop_duplicates(subset = ['Gällande Hastighet'])
        hs_vagar.append(hs['Gällande Hastighet'].tolist())
        for i in range(11):
            pervag['Tid'] = pervag['Tid'].astype('int')
            pertimme = pervag.loc[pervag['Tid'] == i+7]
            medelhast_pertimme[7+i] = pertimme['Hastighet'].sum()/pertimme.shape[0]
        mhs_vagar.append(medelhast_pertimme)
    
    return mhs_vagar, hs_vagar, roads_k
    

valdKommun = input('Välj en kommun:')

df_platsData = loadfile('platsData.csv')
df_kameraData = loadfile('kameraData.csv')
mhs_data, vag_hastighet, vagar = createDiagram(valdKommun, df_platsData, df_kameraData)

'''Alla vägar per kommun plottas genom for loopen'''
plt.figure()
x = np.arange(7, 18, 1)
i = 0
for road in mhs_data:
    plt.plot(x, road[7:], label = 'Väg: {}, Hastighet: {}'.format(vagar[i], vag_hastighet[i][:]))
    i +=1

plt.legend(loc='lower right',fancybox=True, shadow=True, fontsize=5)
klock_x= ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
plt.xticks(x, klock_x)
titel = 'Medelhastigheter uppmätta per vägnummer i {}s kommun i mätområdet 2021-09-11'.format(valdKommun)
plt.title(titel)
plt.xlabel('Klockslag')
plt.ylabel('Medelhastighet km/h')
plt.grid(True)
plt.show()

