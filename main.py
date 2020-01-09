from StaticRR import StaticRR
from multidir_dialog import multi_dir_dialog
from tkinter import filedialog as fd
import xlsxwriter as xw
import numpy as np

def main():
    file_lists = multi_dir_dialog()
    file_paths = file_lists[0]
    slot_lists = file_lists[1]
    print(file_paths, file_lists)
    flist = [[] for i in range(max(slot_lists) + 1)]  # variable for writing all the number of slots inputted onto the file
    for i in range(len(file_paths)):  # iterate through the files that are imported onto the program
        flist[slot_lists[i]].append(file_paths[i])  # Create a dictionary for each slot number. The key is the slot number, the value is the respective raw data files
    save_filename = fd.asksaveasfilename(title="Save DQRR", defaultextension='.xlsx',filetypes=[("excel", ".xlsx")])
    workbook = xw.Workbook(save_filename)
    sheet_0 = workbook.add_worksheet("Static RR Summary")
    sheet_1 = workbook.add_worksheet("Time Dep")
    sheet_2 = workbook.add_worksheet("Time Indep")
    sheet_3 = workbook.add_worksheet("Site Average Raw Data")
    static_rr_summary(sheet_0)
    time_dep(sheet_1)
    time_indep(sheet_2)
    site_avg_raw_data(sheet_3)
    static_data = []
    n = 0
    for fp in flist:
        if not fp:
            continue
        for file_path in fp:
            n += 1
            femtodata = StaticRR(file_path)
            sheet_0.write(n, 0, femtodata.slot)
            sheet_0.write(n, 1, femtodata.date)
            sheet_0.write(n, 2, femtodata.time)
            sheet_0.write(n, 3, femtodata.avg_temp)
            sheet_0.write(n, 4, femtodata.avg_humid)
            sheet_0.write(n, 5, femtodata.avg_power)
            sheet_0.write(n, 6, femtodata.I0Avg)
            sheet_0.write(n, 7, femtodata.I0Std)
            sheet_0.write(n, 8, femtodata.IfAvg)
            sheet_0.write(n, 9, femtodata.IfStd)
            sheet_0.write(n, 10, femtodata.grand_Avg)
            sheet_0.write(n, 11, femtodata.grand_Std)
            sheet_0.write(n, 12, femtodata.process_job_recipe_name)

            sheet_1.write(n, 0, femtodata.date)
            sheet_1.write(n, 1, femtodata.time)
            sheet_1.write(n, 2, femtodata.slot)
            sheet_1.write(n, 3, femtodata.I0Avg)
            sheet_1.write(n, 4, femtodata.I0Std)
            sheet_1.write(n, 5, femtodata.I0Sigma)
            sheet_1.write(n, 6, femtodata.I03Sigma)
            sheet_1.write(n, 7, femtodata.IfAvg)
            sheet_1.write(n, 8, femtodata.IfStd)
            sheet_1.write(n, 9, femtodata.IfSigma)
            sheet_1.write(n, 10, femtodata.If3Sigma)
            sheet_1.write(n, 11, femtodata.process_job_recipe_name)
            sheet_1.write(n, 12, femtodata.curveRR)

            sheet_2.write(n, 0, femtodata.date)
            sheet_2.write(n, 1, femtodata.time)
            sheet_2.write(n, 2, femtodata.slot)
            sheet_2.write(n, 3, femtodata.grand_Avg)
            sheet_2.write(n, 4, femtodata.grand_Std)
            sheet_2.write(n, 5, femtodata.grand_Sigma)
            sheet_2.write(n, 6, femtodata.grand_3Sigma)
            sheet_2.write(n, 7, femtodata.process_job_recipe_name)

            sheet_3.write(0, n, femtodata.date)
            sheet_3.write(1, n ,femtodata.time)
            sheet_3.write(2, n, femtodata.slot)
            for i in range(len(femtodata.scan_average_shg_signal)):
                sheet_3.write(i+3, n, femtodata.scan_average_shg_signal[i])


    workbook.close()
    print("Processing Complete")






def static_rr_summary(sheet):
    Title = ["Slot Number", "Date", "Time", "Avg Temp", "Avg Humid",
             'Avg Power on Target', 'SHG Initial Avg', 'SHG Initial Error Bar',
             'SHG Final Avg', 'SHG Final Error Bar', 'SHG Grand Avg',
             'SHG Grand Error Bar', 'Job Recipe Name']

    for i in range(len(Title)):
        sheet.write(0, i, Title[i])

    return

def time_dep(sheet):
    Title = ["Date", "Time", "Slot", "Initial Avg", "Initial Std", "Initial Std/Avg",
             "I0 3Sigma/Avg", "Final Avg", "Final Std", "Final Std/Avg", "If 3Sigma/Avg", 'Job Recipe Name', ' Curve RR']

    for i in range(len(Title)):
        sheet.write(0,i, Title[i])

    return

def time_indep(sheet):
    Title = ["Date", "Time", "Slot", "Grand Avg", "Grand Std", "Grand Std/Avg", "Grand 3 Sigma/Avg", "Job Recipe Name"]

    for i in range(len(Title)):
        sheet.write(0,i, Title[i])

def site_avg_raw_data(sheet):
    Title = ["Date", "Recipe", "Time/Slot"]
    time_range = list(np.arange(0.030,5.000, 0.01))

    for i in range(len(Title)):
        sheet.write(i, 0, Title[i])

    for i in range(0, len(time_range)):
        sheet.write(i+3, 0, time_range[i])

    return




if __name__ == "__main__":
    main()
