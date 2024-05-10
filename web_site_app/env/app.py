from flask import Flask, render_template, url_for, request, redirect
from equipement import cluster_injector_data,cluster_tanks_data,cluster_meter_data
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from flask import Flask, jsonify
from flask import flash
from inventory import tank_101,tank_102,tank_103,tank_104,tank_105,tank_106,tank_201,tank_202,tank_203,tank_204,tank_205,tank_206,tank_301,tank_302,tank_303,tank_305,scrape_weather_data
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'fuel_vision_Project_PGS'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/PGS"
mongo = PyMongo(app).db
client = MongoClient('mongodb://localhost:27017/')
db = client['PGS']
meter_collection = db['Meters']
injector_collection = db['Injectors']
tanks_leaks_collection = db['Leaks_Thefts']
tanks =db['Tanks']
tanks_info = db['Tanks_info']

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

@app.route('/get_injector_codes', methods=['GET'])
def get_injector_codes():
    # Retrieve unique meter codes from MongoDB
    unique_injector_codes = injector_collection.distinct("INJECTOR_CODE")

    # Return the list of unique meter codes as JSON
    return jsonify(unique_injector_codes)

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
     # Define a dictionary mapping tank codes to tank names
    tank_names = {
        'TK-101': 'Tank 101',
        'TK-102': 'Tank 102',
        'TK-103': 'Tank 103',
        'TK-104': 'Tank 104',
        'TK-105': 'Tank 105',
        'TK-106': 'Tank 106',
        'TK-201': 'Tank 201',
        'TK-202': 'Tank 202',
        'TK-203': 'Tank 203',
        'TK-204': 'Tank 204',
        'TK-205': 'Tank 205',
        'TK-206': 'Tank 206',
        'TK-301': 'Tank 301',
        'TK-302': 'Tank 302',
        'TK-303': 'Tank 303'
        # Add more tank names as needed
    }
 

    # Get the name of the selected tank
    tank_name = tank_names.get(tank_code, 'Unknown Tank')
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
    elif tank_code == 'TK-301':
        tanknb = tank_301(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-302':
        tanknb = tank_302(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-305':
        tanknb = tank_305(tanks_data)  # Assuming tank_102() takes no arguments
    elif tank_code == 'TK-303':
        tanknb = tank_303(tanks_data)  # Assuming tank_102() takes no arguments
    # Add more conditions for other tanks if needed

    # Get the SHELL_CAPACITY of the selected tank
    tank_shell_capacity = tanks_inf.loc[tanks_inf['TANK_CODE'] == tank_code, 'SHELL_CAPACITY'].values[0]
    terminal_product_number = tanks_inf.loc[tanks_inf['TANK_CODE'] == tank_code, 'NAME'].values[0]
    # Filter tanks_inf DataFrame to include only rows for the selected tank_code
    selected_tank_inf = tanks_data[tanks_data['TANK_CODE'] == tank_code]
    selected_tank_inf = selected_tank_inf.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf = selected_tank_inf.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date = sorted_tank_inf.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row = sorted_tank_inf.iloc[0]
    last_date = last_date_row['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical = last_date_row['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    
    weather_df = scrape_weather_data()
      # Filter weather_df to include only rows where bestcondition is 1
    weather_df_filtered = weather_df[weather_df['bestcondition'] == 1]
    print(weather_df)
     # Get the days from the filtered DataFrame
    days_with_best_condition = list(weather_df_filtered['date'])
    def decompose_date(date_str):
        # Split the date string into day and month parts
        day = int(date_str[3:5])
        month_name = date_str[5:].strip()  # Remove any leading or trailing spaces
        # Map the month name to its corresponding number (1 for January, 2 for February, etc.)
        month_number = datetime.strptime(month_name, "%b").month
        return day, month_number
    # Decompose each date and pass the decomposed values to the template
    decomposed_days_with_best_condition = [decompose_date(date) for date in days_with_best_condition]
    print(decomposed_days_with_best_condition)

    table_html = sorted_tank_inf.to_html(classes='table table-striped', index=False)


    # Pass the decomposed dates to the template
    return render_template('tanktest.html', tanks_inf=tanks_inf, tanknb=tanknb, shell_capacity=tank_shell_capacity,
                            product_name=terminal_product_number, tank_name=tank_name, last_date=last_date,
                            last_closing_physical=last_closing_physical, decomposed_days_with_best_condition=decomposed_days_with_best_condition,
                            tank_names=tank_names,table_html=table_html)

    #print(days_with_best_condition)

    #return render_template('tanktest.html', tanks_inf=tanks_inf, tanknb=tanknb, shell_capacity=tank_shell_capacity,product_name=terminal_product_number,tank_name=tank_name,last_date=last_date,last_closing_physical=last_closing_physical,days_with_best_condition=days_with_best_condition,tank_names=tank_names)




@app.route('/all_tanks')
def all_tanks():
     # Retrieve tanks data from MongoDB and convert it into a DataFrame
    tanks_data = pd.DataFrame(list(tanks.find()))
    tanks_inf = pd.DataFrame(list(tanks_info.find()))
    # Extract the TANK_CODE column and convert it into a dictionary of tank codes and names
    tank_name = tanks_data['TANK_CODE']

     # Define a dictionary mapping tank codes to tank names
    tank_names = {
        'TK-101': 'Tank 101',
        'TK-102': 'Tank 102',
        'TK-103': 'Tank 103',
        'TK-104': 'Tank 104',
        'TK-105': 'Tank 105',
        'TK-106': 'Tank 106',
        'TK-201': 'Tank 201',
        'TK-202': 'Tank 202',
        'TK-203': 'Tank 203',
        'TK-204': 'Tank 204',
        'TK-205': 'Tank 205',
        'TK-206': 'Tank 206',
        'TK-301': 'Tank 301',
        'TK-302': 'Tank 302',
        'TK-303': 'Tank 303'
        # Add more tank names as needed
    }
 
    weather_df = scrape_weather_data()
      # Filter weather_df to include only rows where bestcondition is 1
    weather_df_filtered = weather_df[weather_df['bestcondition'] == 1]
    print(weather_df)
     # Get the days from the filtered DataFrame
    days_with_best_condition = list(weather_df_filtered['date'])
    def decompose_date(date_str):
        # Split the date string into day and month parts
        day = int(date_str[3:5])
        month_name = date_str[5:].strip()  # Remove any leading or trailing spaces
        # Map the month name to its corresponding number (1 for January, 2 for February, etc.)
        month_number = datetime.strptime(month_name, "%b").month
        return day, month_number
    # Decompose each date and pass the decomposed values to the template
    decomposed_days_with_best_condition = [decompose_date(date) for date in days_with_best_condition]
    print(decomposed_days_with_best_condition)

    return render_template('All_tanks.html', tanks_inf=tanks_inf,tank_names=tank_names,decomposed_days_with_best_condition=decomposed_days_with_best_condition,tank_name=tank_name)


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

    # Rename the clusters for display
    renamed_counts = {
        'Operational': meter_counts.get('Cluster 0+1', 0),  # Rename combined cluster 0+1
        'Inspection': meter_counts.get('Cluster 2', 0),    # Rename cluster 2
        'Disfunction': meter_counts.get('Cluster 3', 0)    # Rename cluster 3
    }

    # Pass meter counts to the template along with other data
    return jsonify(renamed_counts)

@app.route('/get_injector_counts', methods=['GET'])
def get_injector_counts():
    # Fetch meter data and perform clustering
    injector_data = pd.DataFrame(list(injector_collection.find()))
    result_df = cluster_injector_data(injector_data)
    
    # Count the number of meters for each cluster
    injector_counts = {}
    for cluster_label in range(4):
        if cluster_label == 0 or cluster_label == 1:
            # Combine counts of clusters 0 and 1
            combined_cluster_data = result_df[result_df['cluster'].isin([0, 1])]
            injector_count = len(combined_cluster_data)
            injector_counts['Cluster 0+1'] = injector_count
        else:
            cluster_data = result_df[result_df['cluster'] == cluster_label]
            injector_count = len(cluster_data)
            injector_counts[f'Cluster {cluster_label}'] = injector_count

    # Rename the clusters for display
    renamed_counts = {
        'Operational': injector_counts.get('Cluster 0+1', 0),  # Rename combined cluster 0+1
        'Inspection': injector_counts.get('Cluster 2', 0),    # Rename cluster 2
        'Disfunction': injector_counts.get('Cluster 3', 0)    # Rename cluster 3
    }

    # Pass meter counts to the template along with other data
    return jsonify(renamed_counts)

@app.route('/get_tanks_counts', methods=['GET'])
def get_tanks_counts():
    # Fetch meter data and perform clustering
    tank_data = pd.DataFrame(list(tanks_leaks_collection.find()))
    result_df = cluster_tanks_data(tank_data)
    
    # Count the number of meters for each cluster
    tank_counts = {}
    for cluster_label in range(5):
            cluster_data = result_df[result_df['cluster'] == cluster_label]
            tank_count = len(cluster_data)
            tank_counts[f'Cluster {cluster_label}'] = tank_count

    # Rename the clusters for display
    renamed_counts = {
        'Potential Theft': tank_counts.get('Cluster 0', 0),  # Rename combined cluster 0+1
        'Normal': tank_counts.get('Cluster 1', 0),    # Rename cluster 2
        'Old Theft': tank_counts.get('Cluster 2', 0),   # Rename cluster 3
        'Potential Leak': tank_counts.get('Cluster 3', 0),
        'Old Leak': tank_counts.get('Cluster 4', 0)
    }

    # Pass meter counts to the template along with other data
    return jsonify(renamed_counts)

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

@app.route('/meter_record', methods=['POST'])
def meter_record():
    try:
        meter_code = request.form['meter_code']
        gross_unaccounted = request.form['gross_unaccounted']
        
        # Check if any of the fields are empty
        if not meter_code or not gross_unaccounted:
            flash('Please fill all the fields.', 'danger')
            return redirect(url_for('meters_monitoring'))
        
        # Get the current date
        current_date = datetime.now()
        
        # Format the date as "01/01/2024"
        formatted_date_str = current_date.strftime("%m/%d/%Y")
        
        # Create a dictionary representing the meter data
        meter_data = {
            'METER_CODE': meter_code,
            'FOLIO_NUMBER': formatted_date_str,  # Use the current date
            'GROSS_UNACCOUNTED': int(gross_unaccounted)
        }
        
        # Insert the meter data into the MongoDB collection
        meter_collection.insert_one(meter_data)
        
        flash('Meter added successfully!', 'success')
    except Exception as e:
        flash('Error: Meter not added.', 'danger')

    return redirect(url_for('meters_monitoring'))

@app.route('/injector_record', methods=['POST'])
def injector_record():
    try:
        injector_code = request.form['injector_code']
        frac_unaccounted = request.form['frac_unaccounted']
        
        # Check if any of the fields are empty
        if not injector_code or not frac_unaccounted:
            flash('Please fill all the fields.', 'danger')
            return redirect(url_for('injectors_monitoring'))
        
        # Get the current date
        current_date = datetime.now()
        
        # Format the date as "01/01/2024"
        formatted_date_str = current_date.strftime("%m/%d/%Y")
        
        # Create a dictionary representing the meter data
        injector_data = {
            'INJECTOR_CODE': injector_code,
            'FOLIO_NUMBER': formatted_date_str,  # Use the current date
            'FRAC_UNACCOUNTED': int(frac_unaccounted)
        }
        
        # Insert the meter data into the MongoDB collection
        injector_collection.insert_one(injector_data)
        
        flash('Injector added successfully!', 'success')
    except Exception as e:
        flash('Error: Injector not added.', 'danger')

    return redirect(url_for('injectors_monitoring'))

@app.route('/add_meter', methods=['POST'])
def add_meter():
    try:
        meter_code = request.form['meter_code']
        gross_unaccounted = request.form['gross_unaccounted']
        
        # Check if any of the fields are empty
        if not meter_code or not gross_unaccounted:
            flash('Please fill all the fields.', 'danger')
            return redirect(url_for('equipement_monitoring'))
        
        # Get the current date
        current_date = datetime.now()
        
        # Format the date as "01/01/2024"
        formatted_date_str = current_date.strftime("%m/%d/%Y")
        
        # Create a dictionary representing the meter data
        meter_data = {
            'METER_CODE': meter_code,
            'FOLIO_NUMBER': formatted_date_str,  # Use the current date
            'GROSS_UNACCOUNTED': int(gross_unaccounted)
        }
        
        # Insert the meter data into the MongoDB collection
        meter_collection.insert_one(meter_data)
        
        flash('Meter added successfully!', 'success')
    except Exception as e:
        flash('Error: Meter not added.', 'danger')

    return redirect(url_for('equipement_monitoring'))
    
@app.route('/add_injector', methods=['POST'])
def add_injector():
    try:
        injector_code = request.form['injector_code']
        frac_unaccounted = request.form['frac_unaccounted']
        
        # Check if any of the fields are empty
        if not injector_code or not frac_unaccounted:
            flash('Please fill all the fields.', 'danger')
            return redirect(url_for('equipement_monitoring'))
        
        # Get the current date
        current_date = datetime.now()
        
        # Format the date as "01/01/2024"
        formatted_date_str = current_date.strftime("%m/%d/%Y")
        
        # Create a dictionary representing the meter data
        injector_data = {
            'INJECTOR_CODE': injector_code,
            'FOLIO_NUMBER': formatted_date_str,  # Use the current date
            'FRAC_UNACCOUNTED': int(frac_unaccounted)
        }
        
        # Insert the meter data into the MongoDB collection
        injector_collection.insert_one(injector_data)
        
        flash('Injector added successfully!', 'success')
    except Exception as e:
        flash('Error: Injector not added.', 'danger')

    return redirect(url_for('equipement_monitoring'))


@app.route('/delivery_management')
def delivery_management():
   return render_template('Delivery_management.html')

if __name__ == "__main__":
    '''app.run(debug=True)'''
    app.run(host="0.0.0.0")