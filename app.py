import os
from flask import Flask, request, render_template, redirect
from flask import Request, Response, url_for, jsonify
from pathlib import Path
from backend.detection import predict_pill
from werkzeug.datastructures import FileStorage
import requests


app = Flask(__name__, template_folder='frontend', static_folder='frontend/static')
 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp' }
app.config['MAX_CONTENT_LENGTH']= 16*1024*1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



@app.route('/index', methods= ['GET']) 
def index():
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('re.html', content = request.args.get('content'))

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     r: Request = request
#     if 'file' not in r.files: 
#         return "No file part"
    
#     file: FileStorage = r.files['file']
#     print(file)
    
#     if file.filename == '':
#         return "No selected file"
    
#     if file:
#         filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filename)

        
#         path =os.path.join(os.getcwd(), os.listdir('uploads')[0])
#         if path:
#             data = predict_pill(path)
#             classi = data['predictions'][0]['class']
#             print(classi)
#             return jsonify({'class': classi})


@app.route('/product', methods=['GET','POST'])
def product():
    return render_template('product.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    return render_template('contactus.html')

@app.route('/model',methods=['GET','POST'])
def model():
    return render_template('model.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files')
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

def secure_filename(filename):
    return filename

if __name__ == "__main__":

    # Run the Flask app
    app.run("127.0.0.1", port=8080, debug=True)
    
