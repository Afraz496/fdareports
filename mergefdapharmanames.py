import xlwt
import pandas as pd
from xlwt import Workbook
import xlwt
from xlwt import Workbook

def add_excel_sheetvalue(df, excel_data_pointer,wb):
    for i in range(0, len(df)):
        sheet.write(excel_data_pointer,0,df[i])
        excel_data_pointer += 1
    wb.save('PharmanamesNew.csv')
    return excel_data_pointer
#-----Create excel workbook and sheet----
wb = Workbook()

sheet = wb.add_sheet('Pharmacy Names')
#Create column names
sheet.write(0,0,'Pharmacy Name')
excel_data_pointer = 1
for i in range(1,95):
    data = pd.read_csv("FDA Approved Drug Reports/DrugsFDA FDA-Approved Drugs(" + str(i) +").csv")
    df = data['Company'].values.tolist()
    excel_data_pointer = add_excel_sheetvalue(df, excel_data_pointer,wb)
