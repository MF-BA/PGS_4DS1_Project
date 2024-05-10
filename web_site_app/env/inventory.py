# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import timedelta
import warnings
import pmdarima as pm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima import auto_arima
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def tank_101(gainloss):

        # Filter the DataFrame for entries with tank code 'TK-101'
    tank_101_data = gainloss[gainloss['TANK_CODE'] == 'TK-101']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_101_data['FOLIO_NUMBER'] = pd.to_datetime(tank_101_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_101_data.set_index('FOLIO_NUMBER', inplace=True)

        # Resample the data to bi-weekly frequency and take the sum of 'CLOSING_PHYSICAL' for each period
    tank_101_data_monthly = tank_101_data.resample('2W')['CLOSING_PHYSICAL'].sum()
    # Extract the last date (index)
    last_date_index = tank_101_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=next_dates, columns=['Forecast'])

    # Initial training data
    train_data = tank_101_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(12, 1,1), seasonal_order=(1,0,1,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

        # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)
    
    return future_predictions_df

def tank_102(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-102'
    tank_102_data = gainloss[gainloss['TANK_CODE'] == 'TK-102']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_102_data['FOLIO_NUMBER'] = pd.to_datetime(tank_102_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_102_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_102_data_monthly = tank_102_data.resample('2W')['CLOSING_PHYSICAL'].sum()

        # Extract the last date (index)
    last_date_index = tank_102_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])


    # Initial training data
    train_data = tank_102_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

        # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_103(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-103'
    tank_103_data = gainloss[gainloss['TANK_CODE'] == 'TK-103']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_103_data['FOLIO_NUMBER'] = pd.to_datetime(tank_103_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_103_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_103_data_monthly = tank_103_data.resample('2W')['CLOSING_PHYSICAL'].sum()

        # Extract the last date (index)
    last_date_index = tank_103_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_103_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(4, 0,0), seasonal_order=(1,0,1,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_104(gainloss):

        # Filter the DataFrame for entries with tank code 'TK-104'
    tank_104_data = gainloss[gainloss['TANK_CODE'] == 'TK-104']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_104_data['FOLIO_NUMBER'] = pd.to_datetime(tank_104_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_104_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_104_data_monthly = tank_104_data.resample('2W')['CLOSING_PHYSICAL'].sum()

        # Extract the last date (index)
    last_date_index = tank_104_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_104_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(2, 0,1), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_105(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-105'
    tank_105_data = gainloss[gainloss['TANK_CODE'] == 'TK-105']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_105_data['FOLIO_NUMBER'] = pd.to_datetime(tank_105_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_105_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_105_data_monthly = tank_105_data.resample('2W')['CLOSING_PHYSICAL'].sum()

        # Extract the last date (index)
    last_date_index = tank_105_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_105_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

      # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_106(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-106'
    tank_106_data = gainloss[gainloss['TANK_CODE'] == 'TK-106']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_106_data['FOLIO_NUMBER'] = pd.to_datetime(tank_106_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_106_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_106_data_monthly = tank_106_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_106_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_106_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,1), seasonal_order=(1,1,1,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))
       # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)
   
    return future_predictions_df

def tank_201(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-201'
    tank_201_data = gainloss[gainloss['TANK_CODE'] == 'TK-201']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_201_data['FOLIO_NUMBER'] = pd.to_datetime(tank_201_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_201_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_201_data_monthly = tank_201_data.resample('2W')['CLOSING_PHYSICAL'].sum()

        # Extract the last date (index)
    last_date_index = tank_201_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_201_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,1), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))
   # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)
 
    return future_predictions_df

def tank_202(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-202'
    tank_202_data = gainloss[gainloss['TANK_CODE'] == 'TK-202']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_202_data['FOLIO_NUMBER'] = pd.to_datetime(tank_202_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_202_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_202_data_monthly = tank_202_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_202_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_202_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(16, 1,2), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

   # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_203(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-203'
    tank_203_data = gainloss[gainloss['TANK_CODE'] == 'TK-203']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_203_data['FOLIO_NUMBER'] = pd.to_datetime(tank_203_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_203_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_203_data_monthly = tank_203_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_203_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_203_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

 
    return future_predictions_df

def tank_204(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-204'
    tank_204_data = gainloss[gainloss['TANK_CODE'] == 'TK-204']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_204_data['FOLIO_NUMBER'] = pd.to_datetime(tank_204_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_204_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_204_data_monthly = tank_204_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_204_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_204_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,2), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component //order=(1, 0,0), seasonal_order=(1,0,0,26)
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

        # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

        # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

        # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

 
    return future_predictions_df

def tank_205(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-205'
    tank_205_data = gainloss[gainloss['TANK_CODE'] == 'TK-205']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_205_data['FOLIO_NUMBER'] = pd.to_datetime(tank_205_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_205_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_205_data_monthly = tank_205_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_205_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_205_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,1), seasonal_order=(1,1,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))
                
    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

            # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

            # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

            # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_206(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-206'
    tank_206_data = gainloss[gainloss['TANK_CODE'] == 'TK-206']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_206_data['FOLIO_NUMBER'] = pd.to_datetime(tank_206_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_206_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_206_data_monthly = tank_206_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_206_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_206_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(12, 1,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

            # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

            # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

            # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_301(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-302'
    tank_301_data = gainloss[gainloss['TANK_CODE'] == 'TK-301']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_301_data['FOLIO_NUMBER'] = pd.to_datetime(tank_301_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_301_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_301_data_monthly = tank_301_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_301_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_301_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

        # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

            # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

            # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

            # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_302(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-302'
    tank_302_data = gainloss[gainloss['TANK_CODE'] == 'TK-302']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_302_data['FOLIO_NUMBER'] = pd.to_datetime(tank_302_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_302_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_302_data_monthly = tank_302_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_302_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_302_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 0,0), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

            # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

            # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

            # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)
    return future_predictions_df

def tank_303(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-303'
    tank_303_data = gainloss[gainloss['TANK_CODE'] == 'TK-303']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_303_data['FOLIO_NUMBER'] = pd.to_datetime(tank_303_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_303_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_303_data_monthly = tank_303_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_303_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_303_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data,  order=(1, 0,1), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

            # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

                # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

                # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

                # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)

    return future_predictions_df

def tank_305(gainloss):
        # Filter the DataFrame for entries with tank code 'TK-305'
    tank_305_data = gainloss[gainloss['TANK_CODE'] == 'TK-305']

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    tank_305_data['FOLIO_NUMBER'] = pd.to_datetime(tank_305_data['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    tank_305_data.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to monthly frequency and take the last value of each month
    tank_305_data_monthly = tank_305_data.resample('2W')['CLOSING_PHYSICAL'].sum()
        # Extract the last date (index)
    last_date_index = tank_305_data_monthly.index[-1]

    # Convert the last date to a datetime object
    last_date_dt = pd.to_datetime(last_date_index)

    # Generate 8 dates with a 2-week step starting from the day after the last date
    next_dates = pd.date_range(start=last_date_dt + pd.DateOffset(days=14), periods=8, freq='2W')

    # Convert the next_dates to a datetime index
    next_dates = pd.to_datetime(next_dates)

    # Create a Series with future dates as the index
    future_series = pd.Series(index=next_dates)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=future_series.index, columns=['Forecast'])

    # Initial training data
    train_data = tank_305_data_monthly

    # Fitting the model and making predictions for each future date
    for end_date in future_series.index:
        try:
            model = SARIMAX(train_data, order=(1, 1,1), seasonal_order=(1,0,0,26))  # SARIMA with seasonal component
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  # Forecast one step ahead
            future_predictions.loc[end_date] = pred[0]  # Assign forecasted value to correct index
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

            # Create a DataFrame with Date index and Forecast values
    future_predictions_df = pd.DataFrame(index=next_dates, columns=['Date', 'Forecast'])

                # Fill the 'Date' column with the index values
    future_predictions_df['Date'] = next_dates

                # Fill the 'Forecast' column with the values from future_predictions
    future_predictions_df['Forecast'] = future_predictions['Forecast'].values

                # Reset the index to remove the default index and ensure 'Date' becomes a regular column
    future_predictions_df.reset_index(drop=True, inplace=True)
    print(future_predictions_df)
    return future_predictions_df


def scrape_weather_data():
    
# Filter out the specific Matplotlib warning
    warnings.filterwarnings("ignore", message="Exception ignored in:.*")
        # Scrape weather data from the website
    url = "https://www.timeanddate.com/weather/morocco/el-jadida/ext"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table", class_="zebra")

    # Extracting table rows
    rows = table.find_all("tr")

    data = []

    # Extracting data from each row
    for row in rows[1:]:  # skipping the header row
        cells = row.find_all("td")

        # Check if there are enough cells in the row
        if len(cells) >= 11:  # assuming you need at least 11 cells
            # Extracting data from each cell
            day = row.find("span").get_text(strip=True)
            date = row.find("th").get_text(strip=True)
            temperature = cells[1].get_text(strip=True)
            weather = cells[3].get_text(strip=True)
            humidity = cells[7].get_text(strip=True)
            wind = cells[4].get_text(strip=True)

            # Appending extracted data to the list
            data.append({
                "day": day,
                "date": date,
                "Weather": weather,
                "Wind": wind,
            })

    # Creating DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Clean and convert columns
    df['Weather'] = df['Weather'].astype(str)
    df['Weather'] = pd.to_numeric(df['Weather'].str.extract(r'(\d+)')[0])

    df['Wind'] = df['Wind'].astype(str)
    df['Wind'] = pd.to_numeric(df['Wind'].str.extract(r'(\d+)')[0])


    # Create 'bestcondition' based on certain conditions of 'Weather' and 'Wind':
    df['bestcondition'] = ((df['Weather'] < 23) & (df['Wind'] < 20)).astype(int)

    # Apply PCA and KMeans clustering to help in determining the clusters
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[['Weather', 'Wind', 'bestcondition']])

    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(df_pca)
    df['Cluster'] = kmeans.labels_

    return df