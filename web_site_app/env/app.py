from flask import Flask, render_template, url_for
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from inventory import tank_101,tank_102,tank_103,tank_104,tank_105,tank_106,tank_201,tank_202,tank_203,tank_204,tank_205,tank_206,tank_301,tank_302,tank_303,tank_305,scrape_weather_data
from datetime import datetime

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

    # Generate HTML table with centered values
    table_html = sorted_tank_inf.to_html(classes='table table-striped', index=False, justify='center')
    ##################################################################################
    selected_tank_inf_100 = tanks_data[tanks_data['TANK_CODE'] == 'TK-100']
    selected_tank_inf_100 = selected_tank_inf_100.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_100 = selected_tank_inf_100.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_100 = sorted_tank_inf_100.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_100 = sorted_tank_inf_100.iloc[0]
    last_date_100 = last_date_row_100['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_100 = last_date_row_100['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_200 = tanks_data[tanks_data['TANK_CODE'] == 'TK-200']
    selected_tank_inf_200 = selected_tank_inf_200.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_200 = selected_tank_inf_200.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_200 = sorted_tank_inf_200.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_200 = sorted_tank_inf_200.iloc[0]
    last_date_200 = last_date_row_200['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_200 = last_date_row_200['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_300 = tanks_data[tanks_data['TANK_CODE'] == 'TK-300']
    selected_tank_inf_300 = selected_tank_inf_300.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_300 = selected_tank_inf_300.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_300 = sorted_tank_inf_300.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_300 = sorted_tank_inf_300.iloc[0]
    last_date_300 = last_date_row_300['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_300 = last_date_row_300['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_400 = tanks_data[tanks_data['TANK_CODE'] == 'TK-400']
    selected_tank_inf_400 = selected_tank_inf_400.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_400 = selected_tank_inf_400.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_400 = sorted_tank_inf_400.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_400 = sorted_tank_inf_400.iloc[0]
    last_date_400 = last_date_row_400['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_400 = last_date_row_400['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_500 = tanks_data[tanks_data['TANK_CODE'] == 'TK-500']
    selected_tank_inf_500 = selected_tank_inf_500.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_500 = selected_tank_inf_500.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_500 = sorted_tank_inf_500.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_500 = sorted_tank_inf_500.iloc[0]
    last_date_500 = last_date_row_500['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_500 = last_date_row_500['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_600 = tanks_data[tanks_data['TANK_CODE'] == 'TK-600']
    selected_tank_inf_600 = selected_tank_inf_600.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_600 = selected_tank_inf_600.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_600 = sorted_tank_inf_600.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_600 = sorted_tank_inf_600.iloc[0]
    last_date_600 = last_date_row_600['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_600 = last_date_row_600['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################





    # Pass the decomposed dates to the template
    return render_template('tanktest.html', tanks_inf=tanks_inf, tanknb=tanknb, shell_capacity=tank_shell_capacity,
                            product_name=terminal_product_number, tank_name=tank_name, last_date=last_date,
                            last_closing_physical=last_closing_physical, decomposed_days_with_best_condition=decomposed_days_with_best_condition,
                            tank_names=tank_names,table_html=table_html,last_closing_physical_100=last_closing_physical_100,last_closing_physical_200=last_closing_physical_200,last_closing_physical_300=last_closing_physical_300,
                            last_closing_physical_400=last_closing_physical_400,last_closing_physical_500=last_closing_physical_500,last_closing_physical_600=last_closing_physical_600)

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
    ##################################################################################
    selected_tank_inf_100 = tanks_data[tanks_data['TANK_CODE'] == 'TK-100']
    selected_tank_inf_100 = selected_tank_inf_100.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_100 = selected_tank_inf_100.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_100 = sorted_tank_inf_100.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_100 = sorted_tank_inf_100.iloc[0]
    last_date_100 = last_date_row_100['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_100 = last_date_row_100['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_200 = tanks_data[tanks_data['TANK_CODE'] == 'TK-200']
    selected_tank_inf_200 = selected_tank_inf_200.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_200 = selected_tank_inf_200.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_200 = sorted_tank_inf_200.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_200 = sorted_tank_inf_200.iloc[0]
    last_date_200 = last_date_row_200['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_200 = last_date_row_200['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_300 = tanks_data[tanks_data['TANK_CODE'] == 'TK-300']
    selected_tank_inf_300 = selected_tank_inf_300.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_300 = selected_tank_inf_300.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_300 = sorted_tank_inf_300.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_300 = sorted_tank_inf_300.iloc[0]
    last_date_300 = last_date_row_300['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_300 = last_date_row_300['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_400 = tanks_data[tanks_data['TANK_CODE'] == 'TK-400']
    selected_tank_inf_400 = selected_tank_inf_400.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_400 = selected_tank_inf_400.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_400 = sorted_tank_inf_400.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_400 = sorted_tank_inf_400.iloc[0]
    last_date_400 = last_date_row_400['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_400 = last_date_row_400['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_500 = tanks_data[tanks_data['TANK_CODE'] == 'TK-500']
    selected_tank_inf_500 = selected_tank_inf_500.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_500 = selected_tank_inf_500.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_500 = sorted_tank_inf_500.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_500 = sorted_tank_inf_500.iloc[0]
    last_date_500 = last_date_row_500['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_500 = last_date_row_500['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################
    selected_tank_inf_600 = tanks_data[tanks_data['TANK_CODE'] == 'TK-600']
    selected_tank_inf_600 = selected_tank_inf_600.drop(columns=['_id'])
        # Sort the filtered DataFrame by date in descending order
    sorted_tank_inf_600 = selected_tank_inf_600.sort_values(by='FOLIO_NUMBER', ascending=False)
        
        # Get the last date from the sorted DataFrame
    last_date_600 = sorted_tank_inf_600.iloc[0]['FOLIO_NUMBER'].strftime('%Y-%m-%d')
         # Get the last date from the sorted DataFrame
    last_date_row_600 = sorted_tank_inf_600.iloc[0]
    last_date_600 = last_date_row_600['FOLIO_NUMBER'].strftime('%Y-%m-%d')
    last_closing_physical_600 = last_date_row_600['CLOSING_PHYSICAL']  # Assuming 'closing_physical' is the column name
    ##################################################################################




    return render_template('All_tanks.html', tanks_inf=tanks_inf,tank_names=tank_names,decomposed_days_with_best_condition=decomposed_days_with_best_condition,tank_name=tank_name,last_closing_physical_100=last_closing_physical_100,last_closing_physical_200=last_closing_physical_200,last_closing_physical_300=last_closing_physical_300,
                            last_closing_physical_400=last_closing_physical_400,last_closing_physical_500=last_closing_physical_500,last_closing_physical_600=last_closing_physical_600)


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