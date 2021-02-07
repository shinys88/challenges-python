import requests
from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
from export import save_to_file

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

db = {}

app = Flask("Finally")

@app.route("/")
def home():
  return render_template("home.html")


@app.route("/read")
def read():

  loadjobs = []
  keyword = request.args.get("keyword").lower()

  existingItems = db.get(keyword)
  if existingItems:
    loadjobs = existingItems
  else :

    db[keyword] = []

    # stackoverflow.com
    site = "stackoverflow"
    result = requests.get(f"https://stackoverflow.com/jobs?r=true&q={keyword}")
    soup = BeautifulSoup(result.text, "html.parser")
    joblist = soup.select(".listResults .-job.js-result")

    for job in joblist:
      if job.select_one("h3.fc-black-700 span") is None:
        company = "None"
      else :
        company = job.select_one(".fc-black-700.fs-body1.mb4 span").text.strip()

      anchor = job.select_one("a.s-link.stretched-link")
      url = "https://stackoverflow.com" + anchor["href"]
      title = anchor.text

      db[keyword].append({"title":title, "company":company, "site":site, "url": url})


    #https://weworkremotely.com
    site = "weworkremotely"
    result = requests.get(f"https://weworkremotely.com/remote-jobs/search?term={keyword}")
    soup = BeautifulSoup(result.text, "html.parser")
    joblist = soup.select("#category-2 ul li")

    for job in joblist:
      anchor = job.find("a", recursive=False)

      if anchor.select_one(".company") is None:
        company = "None"
      else:
        company = anchor.select_one(".company").text


      url = "https://weworkremotely.com" + anchor["href"]

      if anchor.select_one(".title") is None:
        title ="None"
      else :
        title = anchor.select_one(".title").text
        

      db[keyword].append({"title":title, "company":company, "site":site, "url": url})


    #https://remoteok.io
    site = "remoteok"
    result = requests.get(f"https://remoteok.io/remote-dev+{keyword}-jobs", headers = headers)
    soup = BeautifulSoup(result.text, "html.parser")
    joblist = soup.select("tr.job")

    for job in joblist:
      company_td = job.select_one("td.company")
      anchor = company_td.select_one(".preventLink")
      
      company = company_td.select_one(".companyLink h3").text
      url = "https://remoteok.io" + anchor["href"]
      title = anchor.select_one("h2").text
        

      db[keyword].append({"title":title, "company":company, "site":site, "url": url})

    loadjobs = db[keyword]

  return render_template("read.html", keyword=keyword, loadjobs=loadjobs, joblen = len(loadjobs))



@app.route("/export")
def export():
  try :
    keyword = request.args.get("keyword")
    if not keyword:
      raise Exception()

    jobs = db.get(keyword)
    if not keyword:
      raise Exception()

    save_to_file(jobs)
    return send_file("jobs.csv",
      attachment_filename=f"{keyword}.csv",
      as_attachment=True)
    
  except :
    return redirect("/")



app.run(host="0.0.0.0")