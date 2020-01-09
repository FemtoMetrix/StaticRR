import pandas as pd
import os
import numpy as np

class FemtoData(object):
    def __init__(self, fp = None): # The class that contains information on the data
        self.measure_params = pd.read_csv(fp, nrows = 28, delimiter = '\t', header = None, names = ["Title", "Info"], index_col = 0) #Measurement parameters in Pandas data frame
        self.shg = pd.read_csv(fp, skiprows = 29, delimiter = '\t', header = None) # SHG signal in pandas data frame
        self.shg_data = self.extract_shg_data  #The values are in list format
        print(self.avg_data(self.shg_data))
        new_shg_header = self.shg.iloc[0] # grab the first row for the header
        self.shg = self.shg[1:] # The entire shg column
        self.shg.columns = new_shg_header
        self.slot = self.measure_params.loc['Slot_Number','Info']
        self.carrier_id = self.measure_params.loc['Carrier_ID', 'Info']
        self.process_job_recipe_name = self.measure_params.loc['ProcessJobRecipeName', 'Info']
        self.report_type = self.measure_params.loc["Report_Type (Patterned vs Unpatterned)", 'Info']
        self.die_pitch_x = self.measure_params.loc['Die_pitch_X', 'Info']
        self.die_pitch_y = self.measure_params.loc['Die_pitch_Y', 'Info']
        self.product_id = self.measure_params.loc['Product_ID', 'Info']
        self.wafer_id = self.measure_params.loc['Wafer_ID', 'Info']
        self.tool_id = self.measure_params.loc['Tool_ID' , 'Info']
        self.sampling_rate = self.measure_params.loc['Sampling Rate [Hz]', 'Info']
        self.shg_record_time = self.measure_params.loc['SHG Record Time [sec]', 'Info']
        self.temperature = self.get_params("Temperature")
        self.humidity = self.get_params("Humidity")
        self.set_laser_power = self.get_params("Setpoint_Laser_Power")
        self.actual_laser_power = self.get_params("Actual_Laser_Power")
        self.set_input_pol = self.get_params("Setpoint_Input_Polarization")
        self.actual_input_pol = self.get_params("Actual_Input_Polarization")
        self.set_output_pol = self.get_params("Setpoint_Output_Polarization")
        self.actual_output_pol = self.get_params("Actual_Output_Polarization")
        self.set_azimuth_position = self.get_params("Setpoint_Azimuth_(Theta)_Position")
        self.act_azimuth_position = self.get_params("Actual_Azimuth_(Theta)_Position")
        self.date = self.get_params_str("Date")[0] # String
        self.time = self.get_params_str("Time")[0] # String
        self.die_x_col = self.get_params("Die_X_Column")
        self.die_y_col = self.get_params("Die_Y_Row")
        self.die_rel_x = self.get_params("Die_Relative_X")
        self.die_rel_y = self.get_params("Die_Relative_Y")
        self.ref_x = self.get_params("Reference_X")
        self.ref_y = self.get_params("Reference_Y")
        self.ref_rel_x = self.get_params("Reference_Relative_X")
        self.ref_rel_Y = self.get_params("Reference_Relative_Y")
        self.site = self.get_params("Site")
        self.spot = self.get_params("Spot")
        self.set_point_x = self.get_params("Setpoint_X")
        self.set_point_y = self.get_params("Setpoint_Y")
        self.actual_x = self.get_params("Actual_X")
        self.actual_y = self.get_params("Actual_Y")
        self.error_code = self.get_params("Error_Code")

    @property
    def extract_shg_data(self):
        self.shg_units = self.shg.loc[1].values.tolist()
        ind_signal = self.shg_units.index('[Signal]')
        shg_data = self.shg.iloc[2:, ind_signal + 2:] # The ind_signal + 2 makes it such that the signal starts from I0 (time = 0.03 seconds)
        shg_data = shg_data.to_numpy(dtype = float)
        print(shg_data)
        return shg_data

    def get_params(self, key):
        params = self.shg[key][1:]
        params = pd.to_numeric(params)
        params = params.to_numpy()
        return(params)

    def get_params_str(self, key):
        params = self.shg[key][1:]
        params = list(params)
        return(params)

    def avg_data(self, var): #Find the average of a list
        return np.mean(var)



#f = FemtoData(r"C:\Users\FemtometrixRD10\PycharmProjects\DQRR\DQRR Test Data v2\DQ 5 SItes v1_LP_1_SL_01_12-29-19 -- 17-24-47\DQ 5 SItes v1_LP_1_SL_01_12-29-19 -- 17-24-47_SHG final.tsv")