from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app)


@app.route("/")
def index():
    news = mongo.db.news.find_one()
    return render_template("index.html", news=news)

@app.route("/scrape")
def scrape():
	news = mongo.db.news
	newsInfo = scrape_mars.scrape()
	news.update(
		{},
		newsInfo,
		upsert=True
	)
	return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)