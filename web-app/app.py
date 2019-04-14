import os
import base64
import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1", "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/')
def page():
    return render_template('index.html')

@app.route('/day_analysis')
def chart():
    label = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    value = [1999, 3577, 3401, 3284, 2968, 3142, 2526]
    return render_template('day.html', title='Day Analysis Report', max=4000, labels=label, values=value,set=zip(value, label, colors))

@app.route('/vehicle_type')
def chart1():
    label = ['m-cycle/scooter', 'motor cycle', 'motor car', 'car', 'scooter', 'e-rickshaw(p)', 'goods carrier', 'scooty', 'motor cab', 'three wheeler']
    value = [7823, 4007, 2917, 1891, 1143, 653, 250, 242, 199, 184]
    return render_template('vehicle.html', title='Count of stolen vehicles', max=8000, labels=label, values=value)

@app.route('/date_analysis')
def chart2():
    label = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    value = [648, 653, 658, 735, 871, 677, 777, 733, 706, 721, 746, 658, 553, 627, 555, 547, 585, 903, 749, 628, 667, 832, 689, 725, 820, 612, 590, 606, 688, 555, 383]
    return render_template('date.html', title='Date wise Analysis', max=950, labels=label, values=value)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    IMAGE_PATH = f
    SECRET_KEY = 'sk_9791a1be475cae14e87a2abf'
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)

    #print(json.dumps(r.json(), indent=2))
    
    return render_template('index.html')
