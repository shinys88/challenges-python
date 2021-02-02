from flask import Flask
from flask import render_template, request,redirect
from scrapper import get_jobs

app = Flask("SupperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("test.html")

# @app.route("/<username>")
# def contact(username):
#   return f"Hello your name is {username}"

# @app.route("/report")
# def report():
#   word = request.args.get('word')
#   return f"You are looking for a job in {word}"

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")

  return render_template("report.html", 
  searchingBy=word, 
  resultNumber=len(jobs), 
  jobs=jobs
  )


app.run(host="0.0.0.0")