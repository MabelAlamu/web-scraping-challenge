# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Create an instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home(): 

    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict = mars_dict)

@app.route("/scrape")
def scrape():  
    mars_scrape = scrape_mars.scrape()
    print(mars_scrape)
    mongo.db.mars.update({}, mars_scrape, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)