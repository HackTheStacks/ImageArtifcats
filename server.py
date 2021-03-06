import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    # Handle uploaded files
    return render_template("upload.html")

@app.route("/classify", methods=['GET', 'POST'])
def classify():

    img = request.args.get('image')
    if 'page' in request.args:
        page = request.args.get('page')
    else:
        page = 1
    cmd = ["python3", "src/run_torch.py", "static/images/%s" % img, str(page)]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out, err = p.communicate()
    return render_template("classify.html", body=out)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # Handle uploaded files
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return render_template("upload.html")
        if f: # and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            dest = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(dest)
            return redirect(url_for('classify', image=filename))

    return render_template("upload.html")

@app.route("/thanks", methods=['GET', 'POST'])
def thanks():
    return render_template("thanks.html")

if __name__ == "__main__" :
    app.run(host='10.20.40.124', port=5000)
