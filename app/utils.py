from time import strftime, localtime

import gspread


def add_to_sheet(count):
    gc = gspread.service_account(filename='key.json')

    sh = gc.open("HamsterApp")
    worksheet = sh.sheet1
    size = len(worksheet.col_values(1))
    today = strftime("%d.%m.%Y", localtime())
    if today != worksheet.col_values(1)[size - 1]:
        worksheet.update_cell(size + 1, 1, today)
        worksheet.update_cell(size + 1, 2, count)
    else:
        worksheet.update_cell(size, 2, count)
