import csv
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging , jsonify
import matplotlib.pyplot as plt
import pandas as pd


app = Flask(__name__,static_url_path='/static')
app.debug = True

@app.route('/')
def index():
		district=[]
		day=[]
		with open('Book1.csv','r') as f:
			reader = csv.reader(f,delimiter=',')
			for row in reader:
				district.append(row[8])
				day.append(row[9])
		lat = request.args.get('lat')
		longi = request.args.get('long')
		return render_template('/index.html',district=district,day=day,lat=lat,longi=longi)

@app.route('/graphs')
def graphs():
    return render_template('/graphs.html')

#FOR GRAPH PAGE
@app.route('/plot')
def plot():
	crime_type = request.args.get('crime_category')
	df = pd.read_csv('C:\\Crime_rate\\flask\\app\\chicago_crime_2016.csv')
	crime_graph1 = df[['Primary Type', 'Arrest']].groupby('Primary Type').count()['Arrest']
	crime_graph1.plot(kind = 'barh', figsize= (10,6), fontsize= 8, title = 'Arrested')
	plt.show()
	plt.savefig('/static/images/new_plot.png')
	return jsonify(result='/static/images/new_plot.png')

def normalize(data): 
    data = (data - data.min()) / (data.max() - data.min())
    return data

def parse_time(x):
    DD=datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S")
    time=DD.hour
    day=DD.day
    month=DD.month
    year=DD.year
    return time, day, month, year

@app.route('/analysis')
def analysis():
    return render_template('/analysis.html')

#actual prediction
@app.route('/predict',methods=['POST'])
def predict():
	season = request.form['season']
	date = request.form['date']
	dist = request.form['dist']
	lat = request.form['lat']
	longi = request.form['long']
	inp_list = []
	inp_list[lat] =  (lat - (-3.535613303754125)) / (2.2451860359300237 - (-3.535613303754125))
	inp_list[longi] = (longi - (-2.2236495408279686)) / (2.138911964416072 - (-2.2236495408279686))
	inp_list[time],inp_list[day],inp_list[month],inp_list[year] = parse_time(date + '03:34:23')




	return render_template('/ans.html',lat=lat,long=longi)

@app.route('/index')
def dashboard():
		district=[]
		day=[]
		with open('Book1.csv','r') as f:
			reader = csv.reader(f,delimiter=',')
			for row in reader:
				district.append(row[8])
				day.append(row[9])
		return render_template('/index.html',district=district,day=day)

if __name__ == "__main__":
    app.run()
