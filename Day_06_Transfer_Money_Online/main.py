import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency
from currencylist import get_currency_list as get_cnls

os.system("clear")
code_numbers = get_cnls()

# Print Currency List
print("Welcome to CurrencyConvert PRO 2000\n")
for i, cn in enumerate(code_numbers):
  print(f"# {i} {cn['country']}")\




print("\nWhere are you from? Choose a country by number.\n")
from_currency = ""
while True :
  try :
    input_number = int(input(str("#: ")))
    cn = code_numbers[input_number]
    print(cn['country'])
    from_currency = cn['code']
    break
  except IndexError:
    print("Choose a number from the list")
  except ValueError:
    print("That wasn't a number.")



print("\nNow choose another country.\n")
to_currency = ""
while True :
  try :
    input_number = int(input(str("#: ")))
    cn = code_numbers[input_number]
    print(cn['country'])
    to_currency = cn['code']
    break
  except IndexError:
    print("Choose a number from the list")
  except ValueError:
    print("That wasn't a number.")



from_price = 0
while True :
  print(f"\nHow many {from_currency} do you want to convert to {to_currency}?")
  try :
    from_price = float(input())
    break
  except ValueError:
    print("That wasn't a number.")



#url = f"https://transferwise.com/?sourceCurrency={from_currency}&targetCurrency={to_currency}&sourceAmount={from_price}"

url = f"https://transferwise.com/gb/currency-converter/{from_currency}-to-{to_currency}-rate?amount={from_price}"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
#to_price = soup.find("input",{"id":"tw-calculator-target"})["value"]
#to_price = soup.find("input",{"id":"cc-amount-to"})["data-hj-whitelist"]

amount = soup.find("span",{"class":"text-success"}).string
to_price = from_price * float(amount)

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""
#print(format_currency(5000, "KRW", locale="ko_KR"))

format_from_price = format_currency(from_price, from_currency, locale="ko_KR")
format_to_price = format_currency(to_price, to_currency, locale="ko_KR")
print(f"{format_from_price} is {format_to_price}")