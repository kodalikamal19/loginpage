from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# Replace the below URI with your actual Atlas connection string
app.config["MONGO_URI"] = "mongodb+srv://kamal:kamal_69@cluster0.bxsub5c.mongodb.net/loginDB?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"username": username, "password": password})

        if user:
            return render_template("welcome.html", username=username)
        else:
            return "Invalid username or password. Please try again."

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            return "Username already exists. Try another one."

        mongo.db.users.insert_one({"username": username, "password": password})
        return redirect(url_for("login"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
