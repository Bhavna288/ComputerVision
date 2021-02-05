import os
from flask import Flask, redirect, url_for, render_template, request, session
from convert import extractText
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "army_bts"

uploads_dir = os.path.join("uploads")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        session["uploaded_file"] = uploaded_file.filename
        uploaded_file.save(os.path.join(uploads_dir, secure_filename(uploaded_file.filename)))
        return redirect(url_for("extract"))
    else:
        return render_template("index.html")

@app.route("/result")
def result():
    res_str = request.args['resStr']
    return render_template("result.html", result_string=res_str)

@app.route("/extract")
def extract():
    if "uploaded_file" in session:
        res = extractText(session["uploaded_file"])
        if res:
            return redirect(url_for("result", resStr=res))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

# import sys
# print(sys.path)
