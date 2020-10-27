from flask import Flask, jsonify, request, render_template, redirect
import os

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "{}".format(os.getcwd())

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return redirect(request.url)

    return render_template("upload_image.html")