from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def scrape():

    # Run the scrape function
    mars_facts = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_db.replace_one({}, mars_facts, upsert=True)

    # Redirect back to home page
    return redirect("/home")

@app.route("/home")
def home():

    # Find one record of data from the mongo database
    mars_db_info = mongo.db.mars_db.find_one()

    # Return template and data
    return render_template('index.html', mars_db_info = mars_db_info)
    #  mars=mars_info)

if __name__ == "__main__":
     app.run(debug=True)