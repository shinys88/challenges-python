import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")


@app.route("/")
def home():

  return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():

  getposts = []
  getreddits = []

  args = request.args

  for lang in subreddits:
    value = args.get(lang)

    if value is not None :
      getreddits.append(lang)
  

  for subreddit in getreddits :

    url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    posts = soup.select("div.rpBJOHq2PR60pnwJlUyP0 div._1oQyIsiPHYt6nx7VOmd1sz")

    for post in posts:
      title = post.select_one("h3._eYtD2XCVieq6emjKBH3m").text
      count = post.select_one("div._23h0-EcaBUorIHC-JZyh6J div._1E9mcoVn4MYnuBQSVDt1gC div._1rZYMD_4xY3gRcSS3p8ODO").text


      try :
        if count == "Vote":
          count = 0
        else :
          count = int(count)
      except :
        count = int(float(count.replace("k",""))*1000)

      post_url = "https://www.reddit.com"+post.select_one("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")['href']

      
      getposts.append({'title':title, 'count':count, 'lang':subreddit, 'url':post_url})

  getposts = sorted(getposts, key=(lambda x: x['count']), reverse=True)

  return render_template("read.html", getreddits=getreddits, getposts=getposts)


app.run(host="0.0.0.0")