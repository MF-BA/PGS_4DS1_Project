from flask import Flask, render_template, url_for, request
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from order import generate_predictions


from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/PGS"
mongo = PyMongo(app).db
client = MongoClient('mongodb://localhost:27017/')
db = client['PGS']
meter_collection = db['Meters']
injector_collection = db['Injectors']
Orders = db['Orders']

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/dashboard')
def dashboard():
   return render_template('Dashboard.html')

@app.route('/inventory_management')
def inventory_management():
   return render_template('Inventory_management.html')


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


@app.route('/orders_management')
def orders_management():
    orders_data = pd.DataFrame(list(Orders.find()))  
    orders_data['FOLIO_NUMBER']= pd.to_datetime(orders_data['FOLIO_NUMBER'])
    orders_data = orders_data.sort_values(by='FOLIO_NUMBER', ascending=False)
    return render_template('Orders_management.html', orders_data=orders_data, datetime=datetime)


@app.route('/customer_orders_prediction', methods=['GET', 'POST'])
def customer_orders_prediction():
    if request.method == 'POST':
        
        orders_data = pd.DataFrame(list(Orders.find())) 

        customer_number = int(request.form['customer_number'])
        orders_data['FOLIO_NUMBER']= pd.to_datetime(orders_data['FOLIO_NUMBER'])

        # Retrieve data for the selected customer number
        customer_data = orders_data[orders_data['CUSTOMER_NUMBER'] == customer_number]
        print(customer_data)

        # Create a dictionary to store xts data for each product number dynamically
        xts_data = {}
        
        # Iterate over unique terminal product numbers for the current customer
        for product_number in customer_data['TERMINAL_PRODUCT_NUMBER'].unique():
            # Filter data for the current product number
            filtered_data = customer_data[customer_data['TERMINAL_PRODUCT_NUMBER'] == product_number].drop(columns=['TERMINAL_PRODUCT_NUMBER'])
            print(filtered_data)

            # Create xts dynamically for each product number
            xts_variable_name = f"xts_data_customer_{customer_number}_product_number_{product_number}"
            xts_data[product_number] = pd.Series(filtered_data['ORDERED_QUANTITY'].values, index=filtered_data['FOLIO_NUMBER'].values)

            print("Constructed key:", xts_variable_name)

        # Perform SARIMA prediction for each product number
        plots_data = []
        for product_number, xts_series in xts_data.items():
            train_data, future_predictions = generate_predictions(xts_series, customer_number, product_number)
            plots_data.append({'product_number': product_number, 'train_data': train_data, 'future_predictions': future_predictions})

        # Render the template with the plots data
        return render_template('Customer_orders_prediction.html', customer_number=customer_number, plots_data=plots_data)

    # Render the form for user input
    return render_template('Customer_orders_input.html')

@app.route('/customer_orders_predictiontest', methods=['GET', 'POST'])
def customer_orders_prediction_test():
    if request.method == 'POST':
        
        orders_data = pd.DataFrame(list(Orders.find())) 

        customer_number = int(request.form['customer_number'])
        orders_data['FOLIO_NUMBER']= pd.to_datetime(orders_data['FOLIO_NUMBER'])
        customer_data = orders_data[orders_data['CUSTOMER_NUMBER'] == customer_number]
        print(customer_data)
        xts_data = {}
        
        filtered_data = customer_data[customer_data['TERMINAL_PRODUCT_NUMBER'] == 4].drop(columns=['TERMINAL_PRODUCT_NUMBER'])
        print(filtered_data)

        xts_variable_name = f"xts_data_customer_{customer_number}_product_number_{product_number}"
        xts_data[product_number] = pd.Series(filtered_data['ORDERED_QUANTITY'].values, index=filtered_data['FOLIO_NUMBER'].values)
        print("Constructed key:", xts_variable_name)

        # Perform SARIMA prediction for each product number
        plots_data = []
        for product_number, xts_series in xts_data.items():
            train_data, future_predictions = generate_predictions(xts_series, customer_number, product_number)
            plots_data.append({'product_number': product_number, 'train_data': train_data, 'future_predictions': future_predictions})
        # Render the template with the plots data
        return render_template('Customer_orders_prediction.html', customer_number=customer_number, plots_data=plots_data)

    # Render the form for user input
    return render_template('Customer_orders_input.html')


if __name__ == "__main__":
    app.run(debug=True)