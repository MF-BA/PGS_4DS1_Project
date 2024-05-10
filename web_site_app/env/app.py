from flask import Flask, render_template, url_for, request,jsonify
from equipement import cluster_meter_data
from equipement import cluster_injector_data
from orders import orders_prediction


from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from flask_pymongo import PyMongo
import folium
from delivery import TSP_Algorithm
import leafmap
import polyline
from shapely.geometry import LineString
import geopandas as gpd
import math
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/PGS"
mongo = PyMongo(app).db
client = MongoClient('mongodb://localhost:27017/')
db = client['PGS']
meter_collection = db['Meters']
injector_collection = db['Injectors']
delivery_collection = db['Delivery']
delivery_detailed_collection = db['Delivery_detailed']
destination_collection = db['Destinations']
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

@app.route('/delivery_management/<int:delivery_id>')
def delivery_display(delivery_id):
   delivery_detailed_data = pd.DataFrame(list(delivery_detailed_collection.find()))
   filtered_data = delivery_detailed_data[delivery_detailed_data['DELIVERY_ID'] == delivery_id]
   departure = [33.1521436, -8.6055754]
   mapObj = folium.Map(location=departure,
                        zoom_start=12, width=900, height=500)
   best_path,best_distance,best_consumption,best_duration,best_score,result,df,best_path_details = TSP_Algorithm(filtered_data , pd.DataFrame(list(destination_collection.find())))

   # Define a list of colors
   colors = ["red", "green", "blue", "yellow", "orange", "purple"]  # Add more colors if needed
   # Iterate through each pair of points in the best_path
   for i in range(len(best_path)-1):
      try:
         x = best_path[i]
         y = best_path[i+1]
         encoded_polyline = result.loc[(result['DEPARTURE'] == x) & (result['DESTINATION'] == y), 'ENCODED_POLYLINE'].iloc[0]
         decoded_polyline = polyline.decode(encoded_polyline, 5)
         #decoded_polyline = [(t[1], t[0]) for t in decoded_polyline]  # Swap latitudes and longitudes
         route = folium.PolyLine(locations=decoded_polyline, color=colors[i % len(colors)])
         # Add the route to the map
         route.add_to(mapObj)
      except Exception as e:
         print(f"Error processing route {i+1}: {e}")
   # Add points to the map
   geometry = gpd.GeoSeries.from_xy(df['LONGITUDE'], df['LATITUDE'], crs="EPSG:4326")
   i = 1
   for _, point in geometry.items():
      CLIENT = df[df['LATITUDE'] == point.y]
      if point.y == departure[0] and point.x == departure[1]:
         folium.Marker(location=[point.y, point.x], popup="<i>"+CLIENT['DESTINATION_NAME'].iloc[0]+"</i>", icon=folium.Icon(icon= 'home' , color='red')).add_to(mapObj)
      else:
         folium.Marker(location=[point.y, point.x], popup="<i>"+CLIENT['DESTINATION_NAME'].iloc[0]+"</i>" , icon=folium.Icon(prefix='fa', icon=f"{i}")).add_to(mapObj)
      i += 1
   print("///////////")
   print(best_path_details)
    
   # set iframe width and height
   mapObj.get_root().width = "1000px"
   mapObj.get_root().height = "500px"
   

   # derive the iframe content to be rendered in the HTML body
   iframe = mapObj.get_root()._repr_html_()
   return render_template('Delivery_dispaly.html', data=departure, iframe=iframe, best_distance=best_distance, best_consumption=best_consumption, best_duration=best_duration,best_path_details=best_path_details,)

@app.route('/delivery_management')
def delivery_management():
   delivery_data = pd.DataFrame(list(delivery_collection.find()))
   delivery_data['LAST_FOLIO_NUMBER'] = pd.to_datetime(delivery_data['LAST_FOLIO_NUMBER'], format='%Y%m%d')
   delivery_data['FIRST_FOLIO_NUMBER'] = pd.to_datetime(delivery_data['FIRST_FOLIO_NUMBER'], format='%Y%m%d')
   delivery_data = delivery_data.sort_values(by='LAST_FOLIO_NUMBER', ascending=False)
   # Pagination
   page= request.args.get('page',1,type=int)
   per_page=15
   start =(page - 1) * per_page
   end = start + per_page
   total_items = len(delivery_data)
   total_pages = math.ceil(total_items / per_page) 
   # Count deliveries for current month and year
   current_year = datetime.now().year
   current_month = datetime.now().month
   deliveries_this_month = delivery_data[(delivery_data['LAST_FOLIO_NUMBER'].dt.year == current_year) & 
                                          (delivery_data['LAST_FOLIO_NUMBER'].dt.month == current_month)].shape[0]
   items_on_page = delivery_data[start:end]
   return render_template('Delivery_management.html',delivery_data=items_on_page,total_pages=total_pages,page=page,deliveries_this_month=deliveries_this_month)


###########
def get_unique_customer_numbers():
    customer_numbers = Orders.distinct("CUSTOMER_NUMBER")
    return customer_numbers

def get_unique_product_numbers(customer_number):
    product_numbers = Orders.distinct("TERMINAL_PRODUCT_NUMBER", {"CUSTOMER_NUMBER": customer_number})
    print("Product Numbers:", product_numbers)
    return product_numbers
###########

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

    return render_template('Orders_management.html', orders_data=orders_data, datetime=datetime,customer_numbers=customer_numbers)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
