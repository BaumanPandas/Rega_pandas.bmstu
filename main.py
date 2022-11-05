import config
import request_func
import table_func

if __name__ == '__main__':
	session = request_func.connect()
	secret_ls_key = request_func.get_sec_ls_key(session)
	all_persons = table_func.get_all_persosns()
	for person in all_persons:
		request_func.add_person(session, config.EVENT_NUMBER, request_func.get_person_id(session, secret_ls_key, person))
#сколько боли в этих 10 строчках...
