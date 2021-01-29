import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
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
    code_numbers.append({'country':country,'code':code,'number':number})
  except :
    pass

#Main
print("Hello! Please choose select a country by number:")
for i, cn in enumerate(code_numbers):
  print(f"# {i} {cn['country']}")\

#Input
while True :
  try :
    input_number = int(input(str("#: ")))
    cn = code_numbers[input_number]
    print(f"You chose {cn['country']}")
    print(f"The currency code is {cn['code']}")
    break
  except IndexError:
    print("Choose a number from the list")
  except ValueError:
    print("That wasn't a number.")



