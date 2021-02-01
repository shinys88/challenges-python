import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

result = requests.get(alba_url)
soup = BeautifulSoup(result.text, "html.parser")

boxs = soup.select("#MainSuperBrand .goodsBox .impact")

brand_list = []

# Main 브랜드 저장
for box in boxs :
  anchor = box.select_one("a")["href"]
  company = box.select_one(".company").text
  brand_list.append({'anchor':anchor, 'company':company})


company_list = {}
#기업별로 > 채용목록 가져오기.
for brand in brand_list:
  result = requests.get(brand['anchor'])
  soup = BeautifulSoup(result.text, "html.parser")

  jobs = soup.select_one("#NormalInfo > table tbody").find_all('tr',{'class',''})


  for job in jobs :

    local = job.select_one(".local").text
    title = job.select_one(".title").text
    data = job.select_one(".data").text
    pay = job.select_one(".pay").text
    regDate = job.select_one(".regDate").text
    url = job.select_one("a")["href"]

    jl = None

    try : 
      jl = company_list[str(brand['company'])]
    except :
      jl = company_list[str(brand['company'])] = []

    jl.append({
      'local':local,
      'title':title,
      'data':data,
      'pay':pay,
      'regDate':regDate,
      'url':brand['anchor'][:-1]+url
    })

#파일 저장.
for cp in company_list.items():

  file = open(f"{cp[0]}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(['local','title','data','pay','regDate','url'])
  
  for job in cp[1]:
    writer.writerow(list(job.values()))

  file.close()

print("end.")