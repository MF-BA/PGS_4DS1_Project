from flask import Flask, render_template, url_for
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/PGS"
mongo = PyMongo(app).db
client = MongoClient('mongodb://localhost:27017/')
db = client['PGS']
meter_collection = db['Meters']
injector_collection = db['Injectors']
tanks =db['Tanks']
tanks_info = db['Tanks_info']

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/dashboard')
def dashboard():
   return render_template('Dashboard.html')

@app.route('/inventory_management')
def inventory_management():
   return render_template('Inventory_management.html')

@app.route('/tanks_management')
def tanks_management():
    tanks_data = pd.DataFrame(list(tanks.find()))  # Retrieve orders data from MongoDB
    return render_template('Tank_management.html', tanks_data=tanks_data)

@app.route('/tanks_information')
def tanks_information():
    tanks_inf = pd.DataFrame(list(tanks_info.find()))  # Retrieve tanks data from MongoDB
    return render_template('tanktest.html', tanks_inf=tanks_inf)



@app.route('/orders_management')
def orders_management():
   return render_template('Orders_management.html')

@app.template_filter('datetime')
def format_datetime(value, format='%d/%m/%Y'):
    """Format a datetime object."""
    return pd.to_datetime(value, format='%Y%m%d').strftime(format)


@app.route('/equipement_monitoring')
def equipement_monitoring():
   meter_data = pd.DataFrame(list(meter_collection.find()))
   result_df = cluster_meter_data(meter_data)
   meter_groups = {}
   for cluster_label in range(4):
      cluster_data = result_df[result_df['cluster'] == cluster_label]
      meter_codes = cluster_data['METER_CODE'].tolist()
      meter_groups[f'Cluster {cluster_label}'] = meter_codes

   injector_data = pd.DataFrame(list(injector_collection.find()))
   print(injector_data.any)
   result_df_inj = cluster_injector_data(injector_data)
   inj_groups = {}
   for cluster_label2 in range(4):
      cluster_data2 = result_df_inj[result_df_inj['cluster'] == cluster_label2]
      inj_codes = cluster_data2['INJECTOR_CODE'].tolist()
      inj_groups[f'Cluster {cluster_label2}'] = inj_codes
   
   return render_template('Equipement_monitoring.html',meter_groups=meter_groups,meter_result = result_df,meter_data = meter_data,inj_groups=inj_groups,injector_result = result_df_inj,injector_data = injector_data)

@app.route('/delivery_management')
def delivery_management():
   return render_template('Delivery_management.html')

if __name__ == "__main__":
    app.run(debug=True)