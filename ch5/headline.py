import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib.request
import urllib

import datetime
from flask import make_response

app = Flask(__name__)

WEATHER_URL ="http://api.openweathermap.org/data/2.5/weather?q={}" \
             "&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL ="https://openexchangerates.org/api/latest.json?app_id=cb932829eacb6a0e9ee4f38bfbf112ed"


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://rss.iol.io/iol/news'}

DEFAULTS = {'publication':'bbc',
    'city': 'London,UK'}

@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # get customised weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)

    return response

#@app.route("/", methods=['GET','POST'])
#@app.route("/")
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

if __name__ == "__main__":
    app.run(port=5000, debug=True)