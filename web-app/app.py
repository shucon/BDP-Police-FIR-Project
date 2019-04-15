import os
import base64
import json
import requests
import pandas as pd
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="uploads",)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1", "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/')
def page():
    return render_template('index.html')

@app.route('/heatmap')
def heatmap():
    return render_template('map.html')

@app.route('/festival')
def chart3():
    label = ['Navratri', 'Diwali', 'New Year', 'Normal Days']
    value = [141, 124, 144, 115]
    return render_template('festive.html', title='Festival Analysis', max=145, labels=label, values=value)

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
    name = file.filename
    name = name.split('.')
    if name[1]!='jpg':
        im = Image.open(file)
        rgb_im = im.convert('RGB')
        rgb_im.save(UPLOAD_FOLDER+'/car.jpg')
    else:
        name[0]='car'
        name=name[0]+'.'+name[1]
        im = Image.open(file)
        im.save(UPLOAD_FOLDER+'/car.jpg')
    
    fd = open(UPLOAD_FOLDER+'/../../data.csv', 'r')
    df = pd.read_csv(fd)
    # f = os.path.join(app.config['UPLOAD_FOLDER'], 'car.jpg')
    # file.save(f)
    IMAGE_PATH = UPLOAD_FOLDER+'/car.jpg'
    SECRET_KEY = 'sk_9791a1be475cae14e87a2abf'
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    number=r.json()['results'][0]['plate'] if r.json()['results'][0]['plate'] else 'Wrong Image'
    color= r.json()['results'][0]['vehicle']['color'][0]['name'] if r.json()['results'][0]['vehicle']['color'][0]['name'] else 'Wrong Image'
    make_company=r.json()['results'][0]['vehicle']['make'][0]['name'] if r.json()['results'][0]['vehicle']['make'][0]['name'] else 'Wrong Image'
    body_type=r.json()['results'][0]['vehicle']['body_type'][0]['name'] if r.json()['results'][0]['vehicle']['body_type'][0]['name'] else 'Wrong Image'
    year=r.json()['results'][0]['vehicle']['year'][0]['name'] if r.json()['results'][0]['vehicle']['year'][0]['name'] else 'Wrong Image'
    car_name=r.json()['results'][0]['vehicle']['make_model'][0]['name'] if r.json()['results'][0]['vehicle']['make_model'][0]['name'] else 'Wrong Image'
    status='Not stolen'
    for i in range(len(df)):
        if df['Registration Number'][i]==number:
            status=df['STATUS'][i]
    value=[status, number, color, make_company, body_type, year, car_name]
    return render_template('image.html', title='Analysis of Uploaded Image', values=value)

if __name__ == '__main__':
   app.run(debug = True)