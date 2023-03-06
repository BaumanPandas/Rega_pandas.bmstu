import requests
import config
import datetime


#True to trace logs
def connect(log = False):

	#headers to avoid problems with site firewall
	my_headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,application/json, image/avif,image/webp,*/*;q=0.8",
	"Content-Type":"application/x-www-form-urlencoded"
	}

	#urls to enter
	login_url = "https://sso.bmstu.com/auth/ajax-login"
	get_tmp_key_url = "https://sso.bmstu.com/auth/?return_path=https%253A%252F%252Fsso.bmstu.com%252Foauth%252Fauthorization_code%252F&auth_request_key=oAuthRequest"
	get_au_code_url = "https://sso.bmstu.com/oauth/authorization_code/"
	naeb_url = "https://sso.bmstu.com/oauth/authorization_code?type=web_server&client_id=14&redirect_uri=https%3A%2F%2Fbmstu.net%2Fauth%2Fautoopenid%2Foauth%2Fbmstu%2F&response_type=code&scope="
	
	#making variable to operate with session
	session = requests.Session()
	
	#update this variable by adding our headers
	session.headers.update(my_headers)
	
	#getting tmp key for the first login request
	response_key = session.get(get_tmp_key_url)
	
	#searching key in the html code
	site_html_text = response_key.text
	key_index = site_html_text.index("LIVESTREET_SECURITY_KEY")+len("LIVESTREET_SECURITY_KEY")+4
	tmp_sec_ls_key = site_html_text[key_index:key_index+32]
	
	#data which we post, when we are enter the site
	#in this case my data to get access to site
	my_data = {
		'return-path': "https://sso.bmstu.com/oauth/authorization_code/",
	    	'login': config.EMAIL,
	    	'password': config.PASSWORD,
	    	'remember':'1',
	    	'security_ls_key': tmp_sec_ls_key	#tmp key which we parsed
	}

	#send first POST request with data
	response_login = session.post(login_url, data = my_data)
	#after previous request normal broweser automatically redirect us through some pages with filling codes and keys
	#so in this case we have to ebatsa v zhopu chtoby blyat zapolnit vse redirecty
	response_au_code = session.get(get_au_code_url)
	#after previous request we shold get keys and codes...but we get "poshel otsuda" from site
	#one million hours of pain after, after a lot of struggling, searching and experiments..
	#i dont now how it works(i think it's the bug on the site, which allows skip some defend walls)
	naeb = session.get(naeb_url)
	#simple logging, if 200 -> OK < zdes eta hren ne rabotaet...nichego zdes ne rabotaet(
	if log:
		print("Login to site")
		print("tmp_sec_ls_key --", tmp_sec_ls_key)
		print(response_login.status_code)
		print(response_login.text)

	#return variable session with access to our site
	return session


#function to get secret key from site page, to send it in requests
#session - var from connect, True to trace logs(very small piece of information)
def get_sec_ls_key(session, log = False):
	main_site_url = "https://pandas.bmstu.net/"
	
	response = session.get(main_site_url)
	
	site_html_text = response.text
	key_index = site_html_text.index("LIVESTREET_SECURITY_KEY")+len("LIVESTREET_SECURITY_KEY")+4
	sec_ls_key = site_html_text[key_index:key_index+32]
	if log:
		print("Getting sec_ls_key")
		print(response.status_code)
		#print(response.text)		#<uncomment this if status code == 200 but still not working
		print("sec_ls_key --", sec_ls_key)
	return sec_ls_key


#session - var from connect, sec_ls_key - key from get_sec_ls_key function, person_name - name in str, True to trace logs
def get_person_id(session, sec_ls_key, person_name, log = False):
	f = open('Wrong_person_id.txt', 'a')
	f.write(str(datetime.datetime.now())+'\n') 
	
	#url to send search requests
	search_url = "https://pandas.bmstu.net/admin/ajax/user/search"
	
	search_data = {
		"value": person_name,
		"security_ls_key": sec_ls_key
		}

	response = session.post(search_url, data = search_data)
	persons = response.json()['items']
	len_persons = len(persons)
	
	if len_persons == 1:
		person_id = persons[0]['id']
		print("ok", person_name)
		f.write(person_name+'ok'+'\n')
	elif len_persons > 1:
		print("---More than one---", person_name)
		f.write(person_name+'\n')
		person_id = None
	else:
		print("!!!Not found!!!", person_name)
		f.write(person_name+'\n')
		person_id = None

	if log:
		print("Searching")
		print(response)
		print(response.status_code)
		#print(response.text)
		print(response.json())
	
	f.close()
	#return the id of the person on site
	return person_id
	
def add_person(session, event_id, person_id, log = False):
	
	add_person_url = "https://pandas.bmstu.net/branch/ajax/event/add-user"
	
	add_data = {
		'user_id':person_id,
		'id':event_id,
		'security_ls_key':get_sec_ls_key(session)
	}
	
	response = session.post(add_person_url, data=add_data)
	if log:
		print("Add person")
		print(response)
		print(response.status_code)
		#print(response.text)
	#return the id of the person on site
	return response

