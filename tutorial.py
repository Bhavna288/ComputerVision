import os
from flask import Flask, redirect, url_for, render_template, request, session
from convert import extractText, extractFromHandwritten
from werkzeug.utils import secure_filename
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.secret_key = "army_bts"

uploads_dir = os.path.join("uploads")
app.config['UPLOAD_FOLDER'] = uploads_dir

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        eType = request.form['f-type']
        session["uploaded_file"] = uploaded_file.filename
        session["e_type"] = eType
        uploaded_file.save(os.path.join(uploads_dir, secure_filename(uploaded_file.filename)))
        return redirect(url_for("extract"))
    else:
        return render_template("index.html")

@app.route("/extract")
def extract():
    if "uploaded_file" in session and "e_type" in session:
        if session["e_type"] == "handwritten":
            res = extractFromHandwritten(session["uploaded_file"])
            if res:
                session["res_str"] = res
                return redirect(url_for("result"))
            else:
                return redirect(url_for("home"))
        else:
            res = extractText(session["uploaded_file"])
            if res:
                session["res_str"] = res
                return redirect(url_for("result"))
            else:
                return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/result")
def result():
    if "res_str" in session and "uploaded_file" in session:
        res_str = session['res_str']
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], session['uploaded_file'])
        ress = {"str": res_str, "img": img_path}
        return render_template("result.html", results=ress)
    else:
        return render_template("index.html")

@app.route("/remove")
def rmfile():
    if "uploaded_file" in session:
        fname = os.path.join('uploads', session["uploaded_file"])
        if os.path.isfile(fname):
            os.remove(fname)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)