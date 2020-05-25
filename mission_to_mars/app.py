from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/Scrape_Mars")


@app.route("/")
def home():
    latest_news = mongo.db.latest_news.find_one()

    featured_image_url = mongo.db.featured_image_url.find_one()

    mars_weather = mongo.db.mars_weather.find_one()

    mars_facts = mongo.db.mars_facts.find_one()

    hemisphere_image_url = mongo.db.hemisphere_image_url.find_one()

    return render_template("index.html", latest_news = latest_news, featured_image_url = featured_image_url, mars_weather= mars_weather, mars_facts = mars_facts, hemisphere_image_url = hemisphere_image_url)


    

@app.route("/scrape")
def scrape():

    latest_news = scrape_mars.Mars_news()
    mongo.db.latest_news.update({}, latest_news, upsert=True)

    featured_image_url = scrape_mars.featured_image()
    mongo.db.featured_image_url.update({}, featured_image_url, upsert=True)
    
    mars_weather = scrape_mars.weather()
    mongo.db.mars_weather.update({}, mars_weather, upsert=True)

    hemisphere_image_url = scrape.hemispheres()
    mongo.db.hemisphere_image_url.update({}, hemisphere_image_url, upsert=True)

    mars_facts = scrape_mars.mars_facts()
    mongo.db.mars_facts.update({}, mars_facts, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)