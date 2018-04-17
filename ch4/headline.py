import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib.request
import urllib

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

def get_weather(query):
    api_url="http://api.openweathermap.org/data/2.5/weather?q=" \
            "{}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
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

@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles,weather=weather)

#@app.route("/", methods=['GET','POST'])
#@app.route("/")
def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


if __name__ == "__main__":
    app.run(port=5000, debug=True)