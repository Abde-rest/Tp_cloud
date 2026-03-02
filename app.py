from flask import Flask, render_template, request, jsonify, session
from captcha.image import ImageCaptcha
import random
import string
import os

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/captcha")
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session["captcha"] = captcha_text

    image_path = os.path.join("static", "captcha.png")
    image.write(captcha_text, image_path)

    return jsonify({"captcha_url": "/static/captcha.png"})

@app.route("/verify", methods=["POST"])
def verify():
    user_input = request.json.get("captcha")
    if user_input == session.get("captcha"):
        return jsonify({"result": "Correct ✅"})
    else:
        return jsonify({"result": "Wrong ❌"})

if __name__ == "__main__":
    app.run()
