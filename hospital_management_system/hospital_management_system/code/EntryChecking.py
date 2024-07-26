from math import floor
from utils import getSelectedRowData

def checkEmptyFields(*args):
    if '' in args[0]:
        return False
    else:
        return True

def checkAgeOrExpOrFee(*data):
    try:
        for age_exp_fee in data[0]:
            check = floor(float(age_exp_fee))
            if check<=0:
                return False
        return True
    except Exception as e:
        return False

def checkPhone(data):
    if(len(data)==10):
        try:
            phone = int(data)
            return True
        except Exception as e:
            return False
    else:
        return False

def checkLicenseNumber(data,table):
    try:
        license_no = int(data)
        if int(license_no)>0:
            row_count = table.rowCount()
            column_values = []
            for row in range(row_count):
                item = table.item(row, 0)
                if item is not None:
                    column_values.append(item.text())
            if str(license_no) not in column_values:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False

def checkNumericalData(data):
    try:
        number = int(data)
        if number<=0:
            return False
        else:
            return True
    except Exception as e:
        return False
    
def checkPatientCommonEntry(data,table):
    if checkEmptyFields(data):
        if checkNumericalData(data[0]) and checkNumericalData(data[2]) and checkPhone(data[5]):
            if checkLicenseNumber(data[0],table):
                return True
    else:
        return False
    
def checkUpdatePatientCommonEntry(data,table):
    if checkEmptyFields(data):
        if checkNumericalData(data[0]) and checkNumericalData(data[2]) and checkPhone(data[5]):
            row = getSelectedRowData(table)
            if str(data[0]) != str(row[0]):
                if checkLicenseNumber(data[0],table):
                    return True
            else:
                return True
    else:
        return False

def checkHealthInsuranceNumber(data,table):
    try:
        hi_num = int(data)
        if int(hi_num)>0:
            row_count = table.rowCount()
            column_values = []
            for row in range(row_count):
                item = table.item(row, 7)
                if item is not None:
                    column_values.append(item.text())
            if str(hi_num) not in column_values:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False
    
def updtCheckHINo(data,table):
    row = getSelectedRowData(table)
    if data == row[-1]:
        return True
    else:
        checkHealthInsuranceNumber(data,table)

def checkNumericWith0(data):
    try:
        number = int(data)
        if number<0:
            return False
        else:
            return True
    except Exception as e:
        return False
    
def checkInvoiceNumber(data,table):
    try:
        license_no = int(data)
        if int(license_no)>0:
            row_count = table.rowCount()
            column_values = []
            for row in range(row_count):
                item = table.item(row, 1)
                if item is not None:
                    column_values.append(item.text())
            if str(license_no) not in column_values:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False