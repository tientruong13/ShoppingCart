from flask import Flask, render_template, request
from bson.objectid import ObjectId
from bson import json_util
import bcrypt
import pymongo

app = Flask(__name__)

adapter = pymongo.MongoClient("mongodb://localhost:27017")
database = adapter['pythonShopping']

# models
productModel = database["product"]
userModel = database["user"]

@app.route("/shopping", methods=["GET"])
def shoppingRoute():
    prods = productModel.find()
    return render_template("shopping.html", items=prods)

@app.route("/addnew", methods=["GET"])
def addNewRoute():
    prods = productModel.find()
    return render_template("addprod.html", items=prods)

@app.route("/detailProd", methods=["POST"])
def detailProd():
    if "_idProd" not in request.form:
        return {"result": 0, "message": "Lack of parameters"}
    else:
        prodDetail = productModel.find_one({"_id": ObjectId(request.form["_idProd"])})
        print(ObjectId(request.form["_idProd"]))
        return {"result": 1, "message": "Ok", "prodInfo": json_util.dumps({"info":prodDetail}) }

@app.route("/removeProd", methods=["POST"])
def removeProd():
    if "_idProd" not in request.form:
        return {"result": 0, "message": "Lack of parameters"}
    else:
        productModel.delete_one({"_id": ObjectId(request.form["_idProd"])})
        print(ObjectId(request.form["_idProd"]))
        return {"result": 1, "message": "Ok"}


@app.route("/addnewprod", methods=["POST"])
def addNewProduct():
    if "Prod_Name" not in request.form or "Prod_Photo" not in request.form or "Prod_Price" not in request.form:
        return {"result": 0, "message": "Lack of parameters"}
    else:
        Prod_Name = request.form["Prod_Name"]
        Prod_Photo = request.form["Prod_Photo"]
        Prod_Price = request.form["Prod_Price"]
        productModel.insert_one({"Prod_Name": Prod_Name, "Prod_Photo": Prod_Photo, "Prod_Price": int(Prod_Price)})
    return {"result": 1, "message": "New Product has been saved"}

@app.route("/register", methods=["POST"])
def register():
    if "User_Email" not in request.form or "Password" not in request.form or "User_Name" not in request.form:
        return {"result": 0, "message": "Lack of parameters"}
    else:
        User_Email = request.form["User_Email"]
        Password = request.form["Password"]
        User_Name = request.form["User_Name"]
        if not User_Email or not Password or not User_Name:
            return {"result": 0, "message": "Fields cannot be empty"}
        else:
            userModel.insert_one({"User_Email":User_Email,"Password": Password, "User_Name":User_Name})
    return {"result": 1, "message": "Seccessful registration"}

@app.route("/signup", methods=["GET"])
def signUpRoute():
    return render_template("signup.html")

@app.route("/signin", methods=["GET"])
def signInRoute():
    return render_template("signin.html")

@app.route("/login", methods=["POST"])
def logIn():
    User_Email = request.form["User_Email"]
    Password = request.form["Password"]
    user = userModel.find_one({"User_Email":User_Email,"Password": Password})
    if user:
        return {"result": 1, "message": "Logged in", "User_Name": user["User_Name"]}
    else:
        return {"result": 0, "message": "Invalid credentials"}
