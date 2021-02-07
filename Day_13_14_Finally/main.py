import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

db = {}

app = Flask("Finally")

@app.route("/")
def home():
  return render_template("home.html")


@app.route("/read")
def read():

  loadjobs = []
  keyword = request.args.get("keyword")
  db[keyword] = []


  #stackoverflow.com
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

    db[keyword].append({"title":title, "url": url, "company":company})


  #https://weworkremotely.com
  result = requests.get(f"https://weworkremotely.com/remote-jobs/search?term={keyword}")
  soup = BeautifulSoup(result.text, "html.parser")
  joblist = soup.select("#category-2 ul li")

  for job in joblist:
    print(job)
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
      

    db[keyword].append({"title":title, "url": url, "company":company})


  #https://remoteok.io

  result = requests.get(f"https://remoteok.io/remote-dev+{keyword}-jobs")
  soup = BeautifulSoup(result.text, "html.parser")
  joblist = soup.select("#category-2 ul li")

  for job in joblist:
    print(job)
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
      

    db[keyword].append({"title":title, "url": url, "company":company})

  loadjobs = db[keyword]




  return render_template("read.html", keyword=keyword, loadjobs=loadjobs, joblen = len(loadjobs))


app.run(host="0.0.0.0")