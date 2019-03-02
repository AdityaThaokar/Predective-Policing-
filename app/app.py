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
		return render_template('/index.html',district=district,day=day)

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




@app.route('/analysis')
def analysis():
    return render_template('/analysis.html')

@app.route('/predict',methods=['POST'])
def predict():
	category = request.form.get('category')
	date = request.form.get('date')
	dist = request.form.get('dist')
	lat = request.form.get('lat')
	longi = request.form.get('longi')
	# load the model from disk
	# loaded_model = pickle.load(open(filename, 'rb'))
	#code for testing
	# .
	# .
	# .
	# .
	return render_template('/ans.html',lat=lat,longi=longi)

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
