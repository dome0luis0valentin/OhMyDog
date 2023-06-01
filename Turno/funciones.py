import csv
import os
from openpyxl import load_workbook
from pyexcel_ods3 import get_data




def leer_archivo(archivo):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../media/'+archivo))
    if archivo.endswith('.csv'):
        with open(csv_path) as file:
            reader = csv.reader(file)
            data = list(reader)
    elif archivo.endswith('.xlsx') or archivo.endswith('.lsx') :
        workbook = load_workbook(filename=archivo)
        sheet = workbook.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
    elif archivo.endswith('.ods'):
        arch = get_data(archivo)
        data = []
        
        for sheet_name in data:
            sheet_data = data[sheet_name]
            for row in sheet_data:
                for cell in row:
                    print(cell)
        
    else:
        data = []

    return data
