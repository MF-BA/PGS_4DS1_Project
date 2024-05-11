from flask import Flask, render_template, url_for, request,jsonify
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from orders import orders_prediction


from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
from statsmodels.tsa.statespace.sarimax import SARIMAX
from collections import defaultdict  # Import defaultdict from collections module
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


###########
def get_unique_customer_numbers():
    customer_numbers = Orders.distinct("CUSTOMER_NUMBER")
    return customer_numbers

def get_unique_product_numbers(customer_number):
    product_numbers = Orders.distinct("TERMINAL_PRODUCT_NUMBER", {"CUSTOMER_NUMBER": customer_number})
    print("Product Numbers:", product_numbers)
    return product_numbers
###########
def get_orders_data():
    orders_data = pd.DataFrame(list(Orders.find()))
    orders_data['FOLIO_NUMBER'] = pd.to_datetime(orders_data['FOLIO_NUMBER'])
    orders_data = orders_data.sort_values(by='FOLIO_NUMBER', ascending=True)
    return orders_data
def plot_orders_fn():
    orders_data = get_orders_data()
    orders_data = orders_data[orders_data['ORDERED_QUANTITY'] >= 0]
    start_date = orders_data['FOLIO_NUMBER'].min()
    end_date = orders_data['FOLIO_NUMBER'].max()
    date_range = pd.date_range(start=start_date, end=end_date, freq='W')
    interval_data = defaultdict(int)
    for index, row in orders_data.iterrows():
        for date in date_range:
            if row['FOLIO_NUMBER'] <= date:
                interval_data[date] += row['ORDERED_QUANTITY']
                break
    chart_data = [['Date', 'Ordered Quantity']]
    for date, quantity in interval_data.items():
        chart_data.append([date.strftime('%Y-%m-%d'), quantity])
    return chart_data
########

@app.route('/tahfoun')
def tahfoun():
    # Fetch unique customer numbers
    customer_numbers = get_unique_customer_numbers()
    return render_template('testi.html', customer_numbers=customer_numbers)

@app.route('/get_products/<int:customer_number>')
def get_products(customer_number):
    print(customer_number)
    product_numbers = get_unique_product_numbers(customer_number)
    return jsonify({'product_numbers': product_numbers})

@app.route('/selected_values/<int:customer_number>/<int:product_number>')
def selected_values(customer_number, product_number):
    orders_data = pd.DataFrame(list(Orders.find()))  
    future_predictions = orders_prediction(orders_data, customer_number, product_number)
    future_predictions_df = pd.DataFrame(future_predictions, columns=['Forecast'])
    future_predictions_df['Date'] = future_predictions_df.index
    return jsonify({'future_predictions': future_predictions_df.to_dict(orient='records')})


@app.route('/orders_management')
def orders_management():
    orders_data = pd.DataFrame(list(Orders.find()))  
    orders_data['FOLIO_NUMBER']= pd.to_datetime(orders_data['FOLIO_NUMBER'])
    orders_data = orders_data.sort_values(by='FOLIO_NUMBER', ascending=False)
    customer_numbers = get_unique_customer_numbers()
    
    chart_data = plot_orders_fn()
    return render_template('Orders_management.html', orders_data=orders_data, datetime=datetime,customer_numbers=customer_numbers,chart_data=chart_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
