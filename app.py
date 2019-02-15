import os
from flask import Flask, render_template, redirect, url_for, request, session, json, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "ran1dom2string3"

app.config["MONGO_DBNAME"] = "recipeworlddb"
app.config["MONGO_URI"] = "mongodb://krivan.peter:jel123szo@ds149122.mlab.com:49122/recipeworlddb"

mongo = PyMongo(app)

@app.route("/")
@app.route("/index")
def index():
    foods=mongo.db.foods.find()
    if "username" in session:
        return render_template("index.html", foods=foods, username=session["username"])   
    return render_template("index.html", foods=foods)

@app.route("/breakfasts")
def get_breakfasts():
    foods=mongo.db.foods.find({"category_name": "breakfast"})
    return render_template("index.html", foods=foods, title="Breakfasts")

@app.route("/mains")
def get_mains():
    return render_template("index.html", 
    foods=mongo.db.foods.find({"category_name": "main"}), title="Mains")
    
@app.route("/desserts")
def get_desserts():
    return render_template("index.html", 
    foods=mongo.db.foods.find({"category_name": "dessert"}), title="Desserts")
    
@app.route("/<food_name>")
def get_food(food_name):
    return render_template("food.html", 
    food=mongo.db.foods.find_one({"name": food_name}))

@app.route("/sign_up", methods=['POST'])
def sign_up():
    exist = ""
    username =  request.form["username"];
    session["username"] = username
    email = request.form["email"];
    if mongo.db.users.find({"username": username}).count() >= 1 and mongo.db.users.find({"email": email}).count() == 0:
        exist = "username_exists"
        return exist
    elif mongo.db.users.find({"email": email}).count() >= 1 and mongo.db.users.find({"username": username}).count() == 0:
        exist = "email_exists"
        return exist
    elif mongo.db.users.find({"email": email}).count() >= 1 and mongo.db.users.find({"username": username}).count() >= 1:
        exist = "email_and_username_exist"
        return exist
    else:
        mongo.db.users.insert({ "username": username , "email": email, "favorites": "" })
        foods=mongo.db.foods.find()
        return render_template("index.html", foods=foods, username=session["username"])

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)