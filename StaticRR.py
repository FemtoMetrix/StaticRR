# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 18:24:26 2019

@author: Rkim
"""
from multidir_dialog import multi_dir_dialog
from FemtoData import FemtoData
import pandas as pd
import os
import numpy as np
import csv


class StaticRR(FemtoData):
    #Splits the input .tsv file into 2 dataframes with one containing the header info, and the other containing the raw data
    def __init__(self, filepath):
        super().__init__(filepath)
        self.avg_humid = self.avg_data(self.humidity)
        self.avg_temp = self.avg_data(self.temperature)
        self.avg_power = self.avg_data(self.actual_laser_power)
        print(self.shg_data)
        # self.__data_title = self.getHeader(df1, r'Measurement_File_Name')
        # self.__job_recipe_name = self.getHeader(df1, r'ProcessJobRecipeName')
        # self.__source_port = self.getHeader(df1, r'Source_Port')
        # self.__slot_number = self.getHeader(df1, r'Slot_Number')
        #
        # self.__date = self.getData(df2, 'Date')
        # self.__time = self.getData(df2, 'Time')
        # self.__time_axis = self.__date + self.__time
        
        # self.__avg_temp = self.avgData(df2, 'Temperature')
        # self.__avg_humid = self.avgData(df2, 'Humidity')
        # self.__avg_power = self.avgData(df2, 'Actual_Laser_Power')
        #
        # if 'SHG Record Time [sec]' in df1:
        #     self.__SHG_record_time = self.getHeader(df1, r'SHG Record Time [sec]')
        #     self.__SHG_record_extension = self.getHeader(df1, r'SHG Record Extension [sec]')
        #     self.__sampling_rate = self.getHeader(df1, r'Sampling Rate [Hz]')
        #     self.__site_n = self.getCol(df2, 'Site')
        #     self.__spot_n = self.getCol(df2, 'Spot')
        #
        #     self.__signal_matrix = self.formParameters2(df2, '0.030', self.__SHG_record_time, self.__sampling_rate, self.__site_n, self.__spot_n)
        #     self.__SHG_signal_matrix = self.__signal_matrix[0]
        #     self.__REF_signal_matrix = self.__signal_matrix[1]
        # else:
        #     self.__signal_matrix = self.formParameters1(df2, '0.030')
        #     self.__SHG_signal_matrix = self.__signal_matrix[0]
        #     self.__REF_signal_matrix = self.__signal_matrix[1]

        self.scan_average_shg_signal = np.mean(self.shg_data, axis = 0)
        self.time_average_shg_signal = np.mean(self.shg_data, axis = 1)
        self.shg_max = np.max(self.shg_data)
        self.shg_min = np.min(self.shg_data)

        # self.__time_average_SHG_signal = self.__SHG_signal_matrix.mean(axis = 1)
        # self.__time_average_REF_signal = self.__REF_signal_matrix.mean(axis = 1)
        # self.__time_std_REF_signal = self.__REF_signal_matrix.std(axis = 1, ddof = 0)
        # self.__SHG_max = self.__SHG_signal_matrix.values.max()
        # self.__SHG_min = self.__SHG_signal_matrix.values.min()

        # self.__REF_grand_mean = self.__time_average_REF_signal.mean()
        # self.__REF_grand_std = self.__time_std_REF_signal.mean()
        # self.__REF_normalized_three_sigma = 3*self.__REF_grand_std/self.__REF_grand_mean
        #
        self.grand_Avg = np.mean(self.time_average_shg_signal) #Grand average
        self.grand_Std = np.std(self.time_average_shg_signal, ddof = 0) # degrees of freedom to 0
        self.grand_Sigma = self.grand_Std/self.grand_Avg
        self.grand_3Sigma = 3 * self.grand_Sigma
        # self.__gAvg = self.__time_average_SHG_signal.mean() #not a 2D dataframe ¯\_(ツ)_/¯
        # self.__gStd = self.__time_average_SHG_signal.std(ddof = 0)
        # self.__gSigma = self.__gStd/self.__gAvg
        # self.__g3Sigma = 3 * self.__gSigma
        #
        self.I0statdata = self.stats(self.shg_data, 0)
        self.I0Avg = self.I0statdata[0]
        self.I0Std = self.I0statdata[1]
        self.I0Sigma = self.I0statdata[2]
        self.I03Sigma = self.I0statdata[3]
        self.Ifstatdata = self.stats(self.shg_data, -1)
        self.IfAvg = self.Ifstatdata[0]
        self.IfStd = self.Ifstatdata[1]
        self.IfSigma = self.Ifstatdata[2]
        self.If3Sigma = self.Ifstatdata[3]
        # self.__Iostatdat = self.Stats(self.__SHG_signal_matrix, 0)
        # self.__I0Avg = self.__Iostatdat[0]
        # self.__I0Std = self.__Iostatdat[1]
        # self.__I0Sigma = self.__Iostatdat[2]
        # self.__I03Sigma = self.__Iostatdat[3]
        # self.__Ifstatdat = self.Stats(self.__SHG_signal_matrix, -1)
        # self.__IfAvg = self.__Ifstatdat[0]
        # self.__IfStd = self.__Ifstatdat[1]
        # self.__IfSigma = self.__Ifstatdat[2]
        # self.__If3Sigma = self.__Ifstatdat[3]

        rsquare = self.rsquare(self.shg_data, self.scan_average_shg_signal)

        self.squareRR = rsquare[0]
        self.sqrtRR = rsquare[1]
        self.curveRR = rsquare[2]
        print(rsquare)
    #     #Bit of formatting
    #     title4 = ['Date', 'Recipe']
    #     title_info4 = [self.__date, self.__job_recipe_name]
    #     Title4 = pd.DataFrame(title_info4, title4)
    #     d_record4 = {'Time/Slot':df2.loc[0, '0.030':].index, self.__slot_number: self.__scan_average_SHG_signal}
    #     data_record4 = pd.DataFrame(d_record4)
    #
    #     self.report_data = [[self.__slot_number,self.__date,self.__time,self.__avg_temp,self.__avg_humid,self.__avg_power,self.__I0Avg,self.__I0Std,self.__IfAvg,self.__IfStd,self.__gAvg,self.__gStd,
    #                      self.__SHG_max,self.__SHG_min,self.__REF_grand_mean,self.__REF_grand_std,self.__REF_normalized_three_sigma,self.__job_recipe_name],
    #                     [self.__date,self.__time,self.__slot_number,self.__I0Avg,self.__I0Std,self.__I0Sigma,self.__I03Sigma,self.__IfAvg,self.__IfStd,self.__IfSigma,self.__If3Sigma,
    #                      self.__job_recipe_name,self.__curveRR,self.__REF_grand_mean],[self.__date,self.__time,self.__slot_number,self.__gAvg,self.__gStd,self.__gSigma,self.__g3Sigma,
    #                     self.__job_recipe_name,self.__REF_grand_mean],Title4, data_record4]
    #
    # def fileSplit(self, file_name):
    #     #Splits our tsv file at the blank line
    #     df1 = []
    #     i = 0
    #     with open(file_name, 'r') as tsvin:
    #         df = csv.reader(tsvin, delimiter = '\t')
    #
    #         for row in df:
    #             if len(row) > 2:
    #                 break
    #             else:
    #                 df1.append(row)
    #                 i += 1
    #
    #     # print(pd.DataFrame(df1))
    #     # df2 = 0
    #     df1 = pd.DataFrame(df1, columns = ['Name', 'Info']) #our headers
    #     df2 = pd.read_csv(file_name, skiprows = i, delimiter = '\t') #our data
    #
    #     return [df1, df2]
    #
    # def getHeader(self, df1, info):
    #     #this method finds the desired information and returns it
    #     return df1[df1['Name'] == info]['Info'].iloc[0]
    #
    # def getData(self, df2, info):
    #     #this method finds the desired information and returns it
    #     return df2[info][1]
    #
    # def getCol(self, df2, info):
    #     #this method finds the desired column and returns it
    #     df2 = df2[info]
    #     return df2.drop([0])


#     def formParameters1(self, df2, info):
#         #this method splits the REF and SHG Signal
#
#         if df2.Measurement_Parameters.str.contains('SHG_REF').any() == True:
#             data_matrix = df2.loc[1:, info:].astype(str).astype(float)
#             for column in data_matrix:
#                 SHG_signal_matrix = data_matrix[data_matrix.index % 2 != 0]
#                 REF_signal_matrix = data_matrix[data_matrix.index % 2 == 0]
#         else:
#             SHG_signal_matrix = df2.loc[1:, info:].astype(str).astype(float)
#             REF_signal_matrix = pd.DataFrame().reindex_like(SHG_signal_matrix)
#
#         return [SHG_signal_matrix, REF_signal_matrix]
#
#     def formParameters2(self, df2, tg1, rec_time, samp_rate, site, spot): #all new
# #    def formParameters(self, df2, tg1):
#         #this method splits the REF and SHG Signal
#         #updated to handle Buffer Gate & Dot Average features
#         tg = float(tg1)
#         tg2 = ((rec_time * samp_rate)/ 100.0) + (tg - 0.01) #amount of gates we need to read
#         tg2 = str(tg2)
#         num_avg = spot.values.max() #number of points being averaged
#
#         if df2.Measurement_Parameters.str.contains('SHG_REF').any() == True:
#             data_matrix = df2.loc[1:, tg1:tg2].astype(str).astype(float)
#             for column in data_matrix:
#                 SHG_signal_matrix1 = data_matrix[data_matrix.index % 2 != 0]
#                 REF_signal_matrix = data_matrix[data_matrix.index % 2 == 0]
#         else:
#             SHG_signal_matrix = df2.loc[1:, tg1:tg2].astype(str).astype(float)
#             REF_signal_matrix = pd.DataFrame().reindex_like(SHG_signal_matrix)
#
#
#         SHG_signal_matrix = SHG_signal_matrix1.groupby(np.arange(len(SHG_signal_matrix1))//num_avg).mean()
#
#         return [SHG_signal_matrix, REF_signal_matrix]


    def stats(self, a, ind): #fly works when matrix is a 2D dataframe
        #calculates statistic data
        avg = np.mean(a[:, ind])
        std = np.std(a[:, ind], ddof = 0)
        sigma = std/avg
        three_sigma = 3 * sigma

        return [avg, std, sigma, three_sigma]

    def rsquare(self, SHG_signal_matrix, Scan_average_SHG_signal):
        #calculates rsquare
        residual_square = np.square((SHG_signal_matrix - Scan_average_SHG_signal)/Scan_average_SHG_signal)
        square_RR = residual_square.mean(axis = 1)
        sqrt_RR = np.sqrt(square_RR)
        curve_RR = sqrt_RR.mean()

        return [square_RR, sqrt_RR, curve_RR]



# def main():
#     filepath = r"C:\Users\FemtometrixRD10\PycharmProjects\DQRR\DQRR Test Data v2\DQ 5 SItes v1_LP_1_SL_01_12-29-19 -- 17-24-47\DQ 5 SItes v1_LP_1_SL_01_12-29-19 -- 17-24-47_SHG final.tsv"
#     raw_data = StaticRR(filepath)
#
#     print("processing finished")
#
# if __name__ == "__main__":
#     main()
#
    
    
