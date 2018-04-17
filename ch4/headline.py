import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://rss.iol.io/iol/news'}

@app.route("/", methods=['GET','POST'])
def get_news(publication="bbc"):
    #query = request.args.get("publication")
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    #first_article = feed['entries'][0]
    #return render_template("home.html",article=first_article)
    return render_template("home.html",articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)