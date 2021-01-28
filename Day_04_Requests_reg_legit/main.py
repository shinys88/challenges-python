import os
import requests, re

# Response Status Codes
# https://2.python-requests.org/en/master/user/quickstart/#response-status-codes


# url 검증 함수.
def legit() :
  print("Welcome to UsUtDown.py!")
  url_arr = input(str("Please write a URL or URLs you want to check. (separated by comma)\n")).split(",")

  print("----------------------------------------")

  for url in url_arr :
    
    url = url.strip().replace("\t","")
    url = re.sub(' +', '', url)
    # 정규표현식 - https://wikidocs.net/4308
    p = re.compile('^http(s)?://', re.I)
    m = p.match(url)
      
    if m == None :
      url = "http://"+url

    try :
      rq = requests.get(url)
      if rq.status_code == requests.codes.ok :
        print(f"{rq.url} is Up!")
      else :
        print(f"{rq.url} is Down!")

    except requests.exceptions.HTTPError :
      print(f'{url} is HTTPError!')
    except requests.exceptions.MissingSchema :
      print(f'{url} is MissingSchema!')
    except requests.exceptions.ConnectionError :
      print(f'{url} is ConnectionError!')
    except requests.exceptions.InvalidSchema :
      print(f'{url} is InvalidSchema!')
    except requests.exceptions.HTTPError :
      print(f'{url} is HTTPError!')


#Start Main.
yn_flag = True
while yn_flag :
  legit()
  while True :
    print("----------------------------------------")
    yn = input(str("Do you want to start over? y/n "))
    if yn == 'y':
      os.system('clear')
      # os.system('cls')
      yn_flag = True
      break
    elif yn == 'n':
      print('Bye.')
      yn_flag = False
      break
  
  
