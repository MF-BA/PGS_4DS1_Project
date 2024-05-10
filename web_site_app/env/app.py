from flask import Flask, render_template, url_for, request, redirect
from equipement import cluster_injector_data,cluster_tanks_data,cluster_meter_data
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from flask import Flask, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/PGS"
mongo = PyMongo(app).db
client = MongoClient('mongodb://localhost:27017/')
db = client['PGS']
meter_collection = db['Meters']
injector_collection = db['Injectors']
tanks_leaks_collection = db['Leaks_Thefts']

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/dashboard')
def dashboard():
   return render_template('Dashboard.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/get_meter_codes', methods=['GET'])
def get_meter_codes():
    # Retrieve unique meter codes from MongoDB
    unique_meter_codes = meter_collection.distinct("METER_CODE")

    # Return the list of unique meter codes as JSON
    return jsonify(unique_meter_codes)


@app.route('/inventory_management')
def inventory_management():
   return render_template('Inventory_management.html')

@app.route('/orders_management')
def orders_management():
   return render_template('Orders_management.html')

@app.template_filter('datetime')
def format_datetime(value, format='%d/%m/%Y'):
    """Format a datetime object."""
    return pd.to_datetime(value, format='%Y%m%d').strftime(format)
@app.route('/get_meter_counts', methods=['GET'])
def get_meter_counts():
    # Fetch meter data and perform clustering
    meter_data = pd.DataFrame(list(meter_collection.find()))
    result_df = cluster_meter_data(meter_data)
    
    # Count the number of meters for each cluster
    meter_counts = {}
    for cluster_label in range(4):
        if cluster_label == 0 or cluster_label == 1:
            # Combine counts of clusters 0 and 1
            combined_cluster_data = result_df[result_df['cluster'].isin([0, 1])]
            meter_count = len(combined_cluster_data)
            meter_counts['Cluster 0+1'] = meter_count
        else:
            cluster_data = result_df[result_df['cluster'] == cluster_label]
            meter_count = len(cluster_data)
            meter_counts[f'Cluster {cluster_label}'] = meter_count

    # Pass meter counts to the template along with other data
    return jsonify(meter_counts)


@app.route('/meters_monitoring')
def meters_monitoring():
   meter_data = pd.DataFrame(list(meter_collection.find()))
   result_df = cluster_meter_data(meter_data)
   meter_groups = {}
   for cluster_label in range(4):
      cluster_data = result_df[result_df['cluster'] == cluster_label]
      meter_codes = cluster_data['METER_CODE'].tolist()
      meter_groups[f'Cluster {cluster_label}'] = meter_codes

   return render_template('Meters_monitoring.html',meter_groups=meter_groups,meter_result = result_df,meter_data = meter_data)


@app.route('/injectors_monitoring')
def injectors_monitoring():
   injector_data = pd.DataFrame(list(injector_collection.find()))
   print(injector_data.any)
   result_df_inj = cluster_injector_data(injector_data)
   inj_groups = {}
   for cluster_label2 in range(4):
      cluster_data2 = result_df_inj[result_df_inj['cluster'] == cluster_label2]
      inj_codes = cluster_data2['INJECTOR_CODE'].tolist()
      inj_groups[f'Cluster {cluster_label2}'] = inj_codes

   return render_template('Injectors_monitoring.html',inj_groups=inj_groups,injector_result = result_df_inj,injector_data = injector_data,)

@app.route('/tanks_monitoring')
def tanks_monitoring():
   tanks_data = pd.DataFrame(list(tanks_leaks_collection.find()))
   print(tanks_data.any)
   result_df_tk_leaks = cluster_tanks_data(tanks_data)
   tk_leaks_groups = {}
   for cluster_label2 in range(5):
      cluster_data2 = result_df_tk_leaks[result_df_tk_leaks['cluster'] == cluster_label2]
      tk_codes = cluster_data2['TANK_CODE'].tolist()
      tk_leaks_groups[f'Cluster {cluster_label2}'] = tk_codes

   return render_template('Tanks_monitoring.html',tanks_groups=tk_leaks_groups,result_tanks=result_df_tk_leaks,leaks_data = tanks_data)


@app.route('/equipement_monitoring')
def equipement_monitoring():

   return render_template('Equipement_monitoring.html')

@app.route('/add_meter', methods=['POST'])
def add_meter():
    meter_code = request.form['meter_code']
    folio_number = request.form['folio_number']
    gross_unaccounted = request.form['gross_unaccounted']
    

    # Parse the original date string
    original_date = datetime.strptime(folio_number, "%Y-%m-%d")

    # Format the date as "01/01/2024"
    formatted_date_str = original_date.strftime("%m/%d/%Y")
    
    # Create a dictionary representing the meter data
    meter_data = {
        'METER_CODE': meter_code,
        'FOLIO_NUMBER': formatted_date_str,  # Use the formatted date
        'GROSS_UNACCOUNTED': int(gross_unaccounted)
    }
    
    try:
        # Insert the meter data into the MongoDB collection
        meter_collection.insert_one(meter_data)
        
        message = 'Meter added successfully!'
        #flash('Meter added successfully!', 'success')
    except Exception as e:
        message = 'error meter not added'
        #flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('equipement_monitoring', message_meter_add=message))
    
@app.route('/add_injector', methods=['POST'])
def add_injector():
    injector_code = request.form['injector_code']
    folio_number = request.form['folio_number_inj']
    frac_unaccounted = request.form['frac_unaccounted']
    

    # Parse the original date string
    original_date = datetime.strptime(folio_number, "%Y-%m-%d")

    # Format the date as "01/01/2024"
    formatted_date_str = original_date.strftime("%m/%d/%Y")
    
    # Create a dictionary representing the meter data
    injector_data = {
        'INJECTOR_CODE': injector_code,
        'FOLIO_NUMBER': formatted_date_str,  # Use the formatted date
        'FRAC_UNACCOUNTED': int(frac_unaccounted)
    }
    
    try:
        # Insert the meter data into the MongoDB collection
        injector_collection.insert_one(injector_data)
        
        message = 'Injector added successfully!'
        #flash('Meter added successfully!', 'success')
    except Exception as e:
        message = 'error injector not added'
        #flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('equipement_monitoring', message_injector_add=message))


@app.route('/delivery_management')
def delivery_management():
   return render_template('Delivery_management.html')

if __name__ == "__main__":
    '''app.run(debug=True)'''
    app.run(host="0.0.0.0")