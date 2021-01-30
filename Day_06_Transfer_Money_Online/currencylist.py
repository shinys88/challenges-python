import os
import requests
from bs4 import BeautifulSoup

def get_currency_list():

  url = "https://www.iban.com/currency-codes"

  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")

  table = soup.find("table",{"class":"table-bordered"})
  tbody = table.find("tbody")
  trs = tbody.find_all("tr")

  code_numbers = []
  for tr in trs :
    try :
      country = tr.find_all("td")[0].string
      code = tr.find_all("td")[2].string
      number = int(tr.find_all("td")[3].string)
      code_numbers.append({'country':country.capitalize(),'code':code,'number':number})
    except :
      pass

  return code_numbers