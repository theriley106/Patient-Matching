from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import os
import csv
import cleanData

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/table', methods=['GET'])
def tablePage():
	return render_template("tablesBackup.html")

@app.route('/recentupload', methods=['GET'])
def recent():
    destination = "data.csv"
    html, count1 = get_html_for_csv(destination)
    successRate = main.calc_based_on_csv(destination)
    return jsonify({"html": html, "count1": count1, "count2": successRate})


def get_html_for_csv(csvFile):
    
    with open(csvFile, "r") as f:
        reader = csv.reader(f)
        dataset = []
        for i, row in enumerate(reader):
            if i == 0:
                columns = [entry.decode("utf8").upper().replace(" ", "_") for entry in row[:-1]]
            else:
                dataset.append([cleanData.parse(entry, columns[i]) for i, entry in enumerate(row[:-1])])
    string = """
        <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
        <thead>
          <tr class="table-primary">"""
    for val in columns:
        string += "<th>{}</th>".format(val)
    string += """
      </tr>
    </thead><tbody>"""


    for val in dataset:
        string += "<tr>"
        for v in val:
            string += "<td>{}</td>".format(v)
        string += "</tr>"
    return string + "</tbody></table>", len(dataset)
    


@app.route("/weights", methods=["POST"])
def weights():
    target = os.path.join(APP_ROOT, '')

    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    filename = upload.filename
    return "True"

# upload selected image and forward to processing page
@app.route("/submit", methods=["POST"])
def myTractor():
    target = os.path.join(APP_ROOT, '')

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
    destination = target + "file.csv"
    print destination
    print("File saved to to:", destination)
    upload.save(destination)
    html, count1 = get_html_for_csv(destination)
    successRate = main.calc_based_on_csv(destination)
    return jsonify({"html": html, "count1": count1, "count2": successRate})

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)