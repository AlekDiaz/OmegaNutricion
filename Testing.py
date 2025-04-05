import Sheets

table = Sheets.get_table()

names = Sheets.get_titles(table)

print(names)