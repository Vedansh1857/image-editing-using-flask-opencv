import os
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"The filename is : {filename} & the operation is : {operation}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename,imgProcessed)
            return newFilename

        case "webp":
            newFilename = f"static/{filename.rsplit('.')[0]}.webp"
            cv2.imwrite(newFilename,img)
            return newFilename

        case "cpng":
            newFilename = f"static/{filename.rsplit('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename

        case "cjpg":
            newFilename = f"static/{filename.rsplit('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename

@app.route("/")
def Home():
    return render_template('index.html')

@app.route("/about")
def About():
    return render_template('about.html')

@app.route("/edit", methods=["GET","POST"])
def Edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "ERROR 404"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "ERROR no selected file..."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename,operation)
            flash(f"Your image has been processed & is available <a href='/{new}' target='_blank'> here </a>")
            return render_template("index.html")
    
    return render_template('index.html')

app.run(debug=True,port=5001)