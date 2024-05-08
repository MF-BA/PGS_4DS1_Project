import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def orders_prediction(gainloss, customer_number, product_number):
    # Filter the DataFrame for entries with the specified customer and product number
    orders = gainloss[(gainloss['CUSTOMER_NUMBER'] == customer_number) & (gainloss['TERMINAL_PRODUCT_NUMBER'] == product_number)]

    # Convert 'FOLIO_NUMBER' to datetime if it's not already in datetime format
    orders['FOLIO_NUMBER'] = pd.to_datetime(orders['FOLIO_NUMBER'])

    # Set 'FOLIO_NUMBER' as the index
    orders.set_index('FOLIO_NUMBER', inplace=True)

    # Resample the data to weekly frequency and sum the 'ORDERED_QUANTITY' for each period
    product_data_weekly = orders['ORDERED_QUANTITY'].resample('W').sum()

    # Initial training data
    train_data = product_data_weekly

    # Create a DataFrame with the next dates
    next_dates = pd.date_range(start=product_data_weekly.index[-1] + pd.Timedelta(days=7), periods=12, freq='W')
    next_dates_df = pd.DataFrame(next_dates, columns=['Date'])
    next_dates_df.set_index('Date', inplace=True)

    # Initialize an empty dataframe to store predictions
    future_predictions = pd.DataFrame(index=next_dates_df.index, columns=['Forecast'])

    # Fitting the model and making predictions for each future date
    for end_date in next_dates_df.index:
        try:
            model = SARIMAX(train_data, order=(4,1,1), seasonal_order=(1,0,0,52))  
            model_fit = model.fit()
            pred = model_fit.forecast(steps=1)  
            future_predictions.loc[end_date] = pred[0]  
            train_data = train_data._append(pd.Series(pred[0], index=[end_date]))  
        except Exception as e:
            print("Error occurred for date:", end_date)
            print("Error details:", str(e))

    return future_predictions
