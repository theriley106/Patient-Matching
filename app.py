from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/table', methods=['GET'])
def tablePage():
	return render_template("tables.html")

# upload selected image and forward to processing page
@app.route("/myTractor", methods=["POST"])
def myTractor():
    target = os.path.join(APP_ROOT, 'static/images')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    # save file
    if (ext == ".csv"):
        print("File accepted")
    else:
        return "{} not supported".format(ext)
        #return render_template("error.html", message="The selected file is not supported"), 400
    destination = "/".join([target, 'file.csv'])
    print destination
    print("File saved to to:", destination)
    upload.save(destination)
    return "<h1>AYYYY</h1>"

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)