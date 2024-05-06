from flask import Flask, render_template, url_for
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from inventory import tank_101,tank_102,tank_103,tank_104,tank_105,tank_106,tank_201,tank_202,tank_203,tank_204,tank_205,tank_206

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

@app.route('/all_tanks/tanks_information')
def tanks_information():
     # Retrieve tanks data from MongoDB and convert it into a DataFrame
    tanks_data = pd.DataFrame(list(tanks.find()))
    tanks_inf = pd.DataFrame(list(tanks_info.find()))
    print(tanks_data)
    tank101=tank_103(tanks_data)
    return render_template('tanktest.html', tanks_inf=tanks_inf,tank101=tank101)

@app.route('/all_tanks/<tank_code>')
def tank(tank_code):
    # Retrieve tanks data from MongoDB and convert it into a DataFrame
    tanks_data = pd.DataFrame(list(tanks.find()))
    tanks_inf = pd.DataFrame(list(tanks_info.find()))
    
    # Call the appropriate tank function based on the tank code
    if tank_code == 'TK-101':
        tanknb = tank_101(tanks_data)  # Assuming tank_101() takes no arguments
    elif tank_code == 'TK-102':
        tanknb = tank_102(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-103':
        tanknb = tank_103(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-104':
        tanknb = tank_104(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-105':
        tanknb = tank_105(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-106':
        tanknb = tank_106(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-201':
        tanknb = tank_201(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-202':
        tanknb = tank_202(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-203':
        tanknb = tank_203(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-204':
        tanknb = tank_204(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-205':
        tanknb = tank_205(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-206':
        tanknb = tank_206(tanks_data)  # Assuming tank_102() takes no arguments
    # Add more conditions for other tanks if needed
    
    return render_template('tanktest.html', tanks_inf=tanks_inf, tanknb=tanknb)



@app.route('/all_tanks')
def all_tanks():
     # Retrieve tanks data from MongoDB and convert it into a DataFrame
    tanks_data = pd.DataFrame(list(tanks.find()))
    tanks_inf = pd.DataFrame(list(tanks_info.find()))
    print(tanks_data)
    return render_template('All_tanks.html', tanks_inf=tanks_inf)


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