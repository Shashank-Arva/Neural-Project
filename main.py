import h5py
from bson import ObjectId
import math
import gridfs
from flask import Flask, request,Response, render_template, session, redirect
from flask_pymongo import PyMongo
import pymongo
from Testing_model import predict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"]="1"

my_collections = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_collections['Dishcovery']
user_col = my_db['User']

app = Flask(__name__)
app.secret_key = "Dishcovery"
app.config['MONGO_URI']='mongodb://localhost:27017/Dishcovery.images'
mongo=PyMongo(app)


@app.route("/")
def userLogin():
    return render_template("/userLogin.html")


@app.route("/userLogin1", methods=['post'])
def userLogin1():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email,password)
    query = {"email": email, "password": password}
    count = user_col.count_documents(query)
    if count > 0:
        user = user_col.find_one(query)
        session['user_id'] = str(user['_id'])
        session['role'] = 'User'
        return redirect("/home")
    else:
        return render_template("userLogin.html", message="Invalid Login Details",color="red")



@app.route("/userRegister")
def userRegister():
    return render_template("/userRegister.html")


@app.route("/userRegister1", methods=['post'])
def userRegister1():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    query = {"email": email}
    count = user_col.count_documents(query)
    if count > 0:
        return render_template("userRegister.html", message="Duplicate Details!!!.....", color="red")
    query = {"FirstName": fname, "LastName": lname, "email": email, "password": password}
    result = user_col.insert_one(query)
    return render_template("userLogin.html", message="User Registered successfully", color="green")


@app.route("/home")
def userHome():
    return render_template("userHome.html")


@app.route("/fileupload", methods=['post'])
def fileupload():
    img=request.files['imageupload']
    result = predict(img).tolist()[0][0]
    print(result)
    print(type(result))
    print("in filupload")
    result=math.floor(result*100)
    return render_template("predicted.html",predict=result)


if __name__=="__main__":
    app.run(debug=True,port=5011)
