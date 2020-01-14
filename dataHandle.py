# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:45:47 2020

@author: Rkim
"""

from FemtoData import FemtoData
import pandas as pd
import numpy as np

class DataHandle(FemtoData):
#contains functions for assorting shg data table
    #df2 - dataframe, so self.shg should be the input
    #tg1 - string value representing time gate 1, should be "0.030"
    def formParameters(self, df2, tg1): 
        #this method splits the REF and SHG Signal
        if df2.Measurement_Parameters.str.contains('SHG_REF').any() == True:
            data_matrix = df2.loc[1:, tg1:].astype(str).astype(float)
            for column in data_matrix:
                SHG_signal_matrix = data_matrix[data_matrix.index % 2 != 0]
                REF_signal_matrix = data_matrix[data_matrix.index % 2 == 0]   
        else:
            SHG_signal_matrix = df2.loc[1:, tg1:].astype(str).astype(float)
            REF_signal_matrix = pd.DataFrame().reindex_like(SHG_signal_matrix)

        return [SHG_signal_matrix, REF_signal_matrix]

    def dotAvg(self, df2, tg1, rec_time, samp_rate, site, spot): #all new   
        #this method splits the REF and SHG Signal
        #updated to handle Buffer Gate & Dot Average features
        tg = float(tg1)
        tg2 = ((rec_time * samp_rate)/ 100.0) + (tg - 0.01) #amount of gates we need to read 
        tg2 = str(tg2)
        num_avg = spot.values.max() #number of points being averaged
        
        if df2.Measurement_Parameters.str.contains('SHG_REF').any() == True:
            data_matrix = df2.loc[1:, tg1:tg2].astype(str).astype(float)
            for column in data_matrix:
                SHG_signal_matrix1 = data_matrix[data_matrix.index % 2 != 0]
                REF_signal_matrix = data_matrix[data_matrix.index % 2 == 0]
        else:
            SHG_signal_matrix = df2.loc[1:, tg1:tg2].astype(str).astype(float)
            REF_signal_matrix = pd.DataFrame().reindex_like(SHG_signal_matrix)
        
        
        SHG_signal_matrix = SHG_signal_matrix1.groupby(np.arange(len(SHG_signal_matrix1))//num_avg).mean()
        
        return [SHG_signal_matrix, REF_signal_matrix]
                    
    












