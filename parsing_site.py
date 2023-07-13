import telebot
import requests
import json
import time
from data import information

global group_of_vacancies
def auth():
    global OauthToken
    auth = {
        'client_id': 'JFAAQPKDP1OKT641UFAQO27JO81UOPPBR6O3LEIUH6AIN8NM9K1P46SAHM5CQP3F',
        'client_secret': 'S75HT47F1H25R01MVJRCB16VLUQOGTDKCFH95IIISA4PHH395R82DK01K4BMJ1P4',
        'grant_type': 'client_credentials'
    }
    url = 'https://hh.ru/oauth/token'
    response = requests.post(url, auth)
    OauthToken = response.json()
    print(OauthToken)
    OauthToken = 'Bearer ' + OauthToken['access_token']

    return OauthToken




def load_vacancie(page):
    data = page.content.decode()
    return json.loads(data)['found']


def print_vacancie(count_of_employers):
    i = 0
    vacancy_one = []
    while i < count_of_employers:
        req = requests.get(f'https://api.hh.ru/vacancies/{str(i + 1)}')
        i += 1
        data = req.content.decode()
        req.close()
        
        group_of_vacancies = json.loads(data)
        #print(group_of_vacancies)
        vacancy_one = json.dumps(group_of_vacancies)                         
        if i % 200 == 0:
            time.sleep(0.2)
    return vacancy_one


def parsing(vacanсie, experience, employment):

    token = "VADBME9N23G3LF5VS7MH1NN5VSRKF2JOSVBGLJ1R0D4E40433JEDRMR9PQJRPFEE"
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'text': vacanсie,
        'experience': experience,
        'employment': employment,
    }
    url = "https://api.hh.ru/vacancies"
    page = requests.get(url, headers=headers, params=params)
    count_of_employers = load_vacancie(page)
    vacancy_one = print_vacancie(count_of_employers)
    
    return params,vacancy_one
# A comment.
# Нету страниц json or if connected go next

def main2(vacanсie, experience, employment,vacancy_one):
  # auth()
  parsing('vacanсie', 'experience', 'employment')
  vacancy_one=parsing(vacancy_one)
  print (vacancy_one[1].text)
