import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"



# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def main():

  url = popular
  order_by = request.args.get('order_by')

  if order_by == "new":
    url = new
  else :
    order_by = 'popular'

  # items = None

  existingItems = db.get(order_by)
  if existingItems:
    items = existingItems
  else:
    result = requests.get(url)
    result_json = result.json()
    items = result_json['hits']
    db[order_by] = items
    print("main : ",result.status_code)

  return render_template("index.html", items=items, order_by=order_by)


@app.route("/<id>")
def detail(id):
  # result_json = None
  existingItems = db.get(id)
  if existingItems:
    result_json = existingItems
  else:
    url = make_detail_url(id)
    result = requests.get(url)
    result_json = result.json()
    db[id] = result_json
    print("detail : ",result.status_code)
    


  return render_template("detail.html", result=result_json)



app.run(host="0.0.0.0")