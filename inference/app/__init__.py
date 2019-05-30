import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.TestingConfig')


def index():
    return render_template("public/index.html")


def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_filesize(filesize):
    if int(filesize) <= app.config["MAX_CONTENT_LENGTH"]:
        return True
    else:
        return False


@app.route("/upload_file", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_filesize(request.cookies["filesize"]):
                    return jsonify({'message': 'Too large size,400'})
            else:
                f1 = request.files["file"]
                if allowed_file(f1.filename):
                    full_filename = os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        secure_filename(
                            f1.filename))
                    f1.save(full_filename)
                    return jsonify({'message': 'Json received,200'})
                else:
                    return jsonify(
                        {'message': 'File extension not allowed,400'})
    return render_template("public/upload_file.html")
