from flask import Flask, redirect, url_for, render_template, request, session
from convert import extractText
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "army_bts"

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        session["uploaded_file"] = uploaded_file.filename
        uploaded_file.save(secure_filename(uploaded_file.filename))
        return redirect(url_for("result"))
    else:
        return render_template("index.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/user")
def user():
    if "user" in session:
        return "<h1>{}</h1>".format(session["user"])
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

# import sys
# print(sys.path)
