from datetime import datetime

def getSelectedRowData(tableWidget):
    selected_rows = tableWidget.selectionModel().selectedRows()  

    if selected_rows:
        for index in selected_rows:
            row_data = []  
            for column in range(tableWidget.columnCount()):
                item = tableWidget.item(index.row(), column)  
                if item is not None:
                    row_data.append(item.text())  
            return row_data
    else:
        pass

def getCurrDate():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d/%m/%Y')
    return formatted_date

def getCurrTime():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time
