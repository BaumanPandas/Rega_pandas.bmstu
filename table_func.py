import json
import gspread
import config

spreadsheet_key = config.TABLE_KEY

account = gspread.service_account(filename = 'credentials.json')
main_table = account.open_by_key(spreadsheet_key)
output_sheet = main_table.worksheet(config.TABLE_TO_USE)


def get_all_persosns(log = False):
	all_persons = []
	list_of_list_of_persons = output_sheet.get(config.TABLE_RANGE)
	for list_persons in list_of_list_of_persons:
		all_persons.append(list_persons[0])
	if log:
		print("Getting persons from table")
		print(all_persons)
	return all_persons

