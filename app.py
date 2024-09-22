import os
from flask import Flask, request, render_template, redirect
from flask import Request, Response, url_for, jsonify
from pathlib import Path
from backend.detection import predict_pill
from backend.detection import get_drug_info
from werkzeug.datastructures import FileStorage
import requests
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd
import openpyxl

app = Flask(__name__, template_folder='frontend', static_folder='frontend/static')
 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp' }
app.config['MAX_CONTENT_LENGTH']= 16*1024*1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



@app.route('/index', methods= ['GET']) 
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


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

@app.route('/search')

def search():
    query = request.args.get('query')
    if query:
        return jsonify(get_drug_info(query))
    return jsonify({"results": []})

load_dotenv()
API_KEY = os.environ.get('ROBOFLOW_API_KEY')
print(API_KEY)


def get_drug_info(query):
    url = f"https://drugapi.p.rapidapi.com/Drug/Summary/{query}"

    headers = {
    	"x-rapidapi-key": "5d53f0c48bmsh7b773967c027048p1e9882jsn9dd54bf50d87",
    	"x-rapidapi-host": "drugapi.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        pprint(data)
    else:
        print(f"Request for drug info failed with status code {response.status_code}")


@app.route('/submit_form',methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    form_data = {
        'Name': [name],
        'Email': [email],
        'Message': [message]
    }

    write_data = pd.DataFrame(form_data)
    try:
        with pd.ExcelWriter('contact_responses.xlsx',mode='a' ,engine='openpyxl', if_sheet_exists='overlay') as writer:
            write_data.to_excel(writer,index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    except FileNotFoundError:
        write_data.to_excel('contact_responses.xlsx', index=False)
    except PermissionError:
        return "File is being used or open."
    except Exception as e:
        return f"An unknown error occued {e}"
    return "Thank You for Your response"

if __name__ == "__main__":

    # Run the Flask app
    app.run("127.0.0.1", port=8080, debug=True)
    
