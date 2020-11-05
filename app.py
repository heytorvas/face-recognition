from flask import Flask, jsonify, request, render_template, redirect
from face_rec import classify_face
import os

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "{}".format(os.getcwd())

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            names = classify_face(image.filename)
            os.remove(image.filename)
            return render_template("response.html", names=names)
    return render_template("index.html")

@app.route("/response", methods=["GET", "POST"])
def response():
    return render_template("response.html")
