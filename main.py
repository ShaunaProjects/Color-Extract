from colorthief import ColorThief
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
from datetime import datetime

ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("flask_key")
app.config["UPLOAD_FOLDER"] = "static/user-img/"
Bootstrap(app)

def process_colors(filename):
    file = ColorThief(filename)
    palette = file.get_palette(color_count=10)
    return palette

def allowed_file(filename):
    file = filename.split(".")[1]
    extension = f".{file}"
    if extension in ALLOWED_EXTENSIONS:
        return True

@app.context_processor
def inject_year():
    year = datetime.now().year
    return dict(year=year)

@app.route("/")
def home():
    error = ""
    return render_template("index.html", error=error)

@app.route("/colors", methods=["GET", "POST"])
def colors():
    if request.method == 'POST':
        file = request.files["file"]
        if file.filename != "" and allowed_file(file.filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
            filename = f"{app.config['UPLOAD_FOLDER']}{file.filename}"
            top_ten_colors = process_colors(filename)
            return render_template("colors.html", filename=filename, colors=top_ten_colors)
        else:
            error = "Not a valid format. Please upload a .jpg, .jpeg, or .png file."
            return render_template("index.html", error=error)




if __name__ == "__main__":
    app.run(debug=True)