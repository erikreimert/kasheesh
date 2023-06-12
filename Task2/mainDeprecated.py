from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima


def genData(merchant_type_code: int, data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate training/testing data by filtering out rows with a specific merchant_type_code and applying data cleaning.

    Args:
        merchant_type_code (int): The merchant type code to exclude from the training data.
        data (pd.DataFrame): The original merchant data.

    Returns:
        pd.DataFrame: The cleaned training data.

    """

    # Convert 'datetime' column to datetime data type. NOTE: odd that this didn't happen automatically
    data['datetime'] = pd.to_datetime(data['datetime'])

    merchant = data.loc[data['merchant_type_code'] == merchant_type_code]

    # Clean the data
    filtered_purchases: DataFrame = cleanData(merchant)
    return filtered_purchases


def stationaryTests(data: pd.DataFrame) -> None:
    """
    Performs stationary tests on the provided time series data and visualizes it.

    Args:
        data (pandas.DataFrame): The input time series data.

    Returns:
        None

    Example:
        data = pd.read_csv("time_series_data.csv")
        stationaryTests(data)

    """

    # Perform the ADF test on the 'amount_cents' column
    result = adfuller(data['amount_dollars'])

    # Extract and print the test statistics and p-value
    adf_statistic = result[0]
    p_value = result[1]
    print("ADF Statistic:", adf_statistic)
    print("p-value:", p_value)

    # Line plotting
    data.plot(x='date', y='amount_dollars')
    plt.title('Time Series Data')
    plt.xlabel('Date')
    plt.ylabel('Amount In Dollars')
    plt.show()

    # Scatter plotting
    plt.scatter(data['date'], data['amount_dollars'])
    plt.title('Scatter Plot of Time Series Data')
    plt.xlabel('Date')
    plt.ylabel('Amount In Dollars')
    plt.show()


def cleanData(merchant: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the provided DataFrame by performing various data cleaning operations.

    Args:
        merchant (pandas.DataFrame): The input DataFrame containing the data.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.

    Example:
        data = pd.read_csv("combined_transactions.csv")
        cleaned_data = cleanData(data)
        print(cleaned_data.head())
                        datetime  amount_dollars transaction_type
        0  2023-01-01 08:00:00          50.00  PurchaseActivity
        1  2023-01-01 09:30:00          35.00  PurchaseActivity
        2  2023-01-02 12:15:00          45.00  PurchaseActivity
        3  2023-01-02 18:45:00          28.00  PurchaseActivity
        4  2023-01-03 09:00:00          32.00  PurchaseActivity

    """

    # Drop rows we don't really need
    merchant = merchant.drop('user_id', axis=1)
    merchant = merchant.drop('merchant_type_code', axis=1)

    # Change cents into dollars
    merchant['amount_dollars'] = merchant['amount_cents'] / 100
    merchant.drop('amount_cents', axis=1, inplace=True)

    # Convert 'datetime' column to date if not already
    if not isinstance(merchant['datetime'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        merchant['datetime'] = pd.to_datetime(merchant['datetime']).dt.date

    # Rename the column from 'datetime' to 'date'
    merchant = merchant.rename(columns={'datetime': 'date'})

    # Separate the purchases and returns into separate DataFrames
    purchases = merchant[merchant['transaction_type'] == 'PurchaseActivity']
    returns = merchant[merchant['transaction_type'] == 'ReturnActivity']

    # Extract the date from purchases and returns
    purchase_dates = purchases['date']
    return_dates = returns['date']

    # Drop the purchase rows where the items were returned based on amounts and transaction date
    filtered_purchases = purchases[
        ~((purchases['amount_dollars'].isin(returns['amount_dollars'])) & (purchase_dates.isin(return_dates)))]

    # Reset the index
    filtered_purchases = filtered_purchases.reset_index(drop=True)

    return filtered_purchases


def arimaPrediction(df: pd.DataFrame, n_periods: int) -> pd.DataFrame:
    """
    Perform ARIMA prediction on the provided time series data.

    Args:
        df (pandas.DataFrame): The testing time series data.
        n_periods (int): The number of periods to forecast.

    Returns:
        pandas.DataFrame: A DataFrame with datetime, actual amounts, and predicted amounts.

    Example:
        train_data = pd.read_csv("train_data.csv")
        test_data = pd.read_csv("test_data.csv")
        prediction_data = arimaPrediction(train_data, test_data, n_periods=10)

    """

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # Resample the df to daily frequency
    df = df.resample('D').sum()

    # Split the data into training and testing sets
    train_data, test_data = df.iloc[:-10], df.iloc[-10:]
    # print(test_data)

    # Checking the best values for the order
    # stepFit = auto_arima(train_data['amount_dollars'], trace=True, suppress_warnings=True)
    # stepFit.summary()

    # Fit the ARIMA model
    model = ARIMA(train_data['amount_dollars'], order=(1, 0, 1))
    model_fit = model.fit()

    # Forecast the next 10 days
    forecast = model_fit.forecast(steps=10)

    # Print the forecasted amounts
    print(forecast)

    # Evaluate the model on the test set
    test_predictions = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])

    # Create a DataFrame with actual and predicted amounts
    evaluation = pd.DataFrame({'date': test_data.index, 'actual_amount': test_data['amount_dollars'],
                               'predicted_amount': test_predictions})

    # Print the evaluation results
    print(evaluation)


if __name__ == '__main__':
    df = pd.read_csv(r"combined_transactions.csv")

    # Convert 'datetime' column to date if not already
    if not isinstance(df['datetime'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        df['datetime'] = pd.to_datetime(df['datetime']).dt.date

    # Rename the column from 'datetime' to 'date'
    df = df.rename(columns={'datetime': 'date'})

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter data for merchant_type_code = 5737
    df_filtered = df[df['merchant_type_code'] == 5732]

    # Separate the purchases and returns into separate DataFrames
    purchases = df_filtered[df_filtered['transaction_type'] == 'PurchaseActivity']
    returns = df_filtered[df_filtered['transaction_type'] == 'ReturnActivity']

    # Extract the date from purchases and returns
    purchase_dates = purchases['date']
    return_dates = returns['date']

    # Drop the purchase rows where the items were returned based on amounts and transaction date
    df_filtered = purchases[
        ~((purchases['amount_cents'].isin(returns['amount_cents'])) & (purchase_dates.isin(return_dates)))]

    # Change cents into dollars
    df_filtered = df_filtered.copy()
    df_filtered.loc[:, 'amount_dollars'] = df_filtered['amount_cents'] / 100

    # Set the 'date' column as the index
    df_filtered.reset_index(drop=True, inplace=True)
    df.set_index('date', inplace=True)

    # Split the data into training and testing sets
    train_data, test_data = train_test_split(df_filtered, test_size=0.2, shuffle=False)

    # Checking the best values for the order
    stepFit = auto_arima(train_data['amount_dollars'], trace=True, suppress_warnings=True)
    stepFit.summary()

    # Fit the ARIMA model
    model = ARIMA(train_data['amount_dollars'], order=(0, 0, 0))
    model_fit = model.fit()

    # Forecast the next 10 days
    forecast = model_fit.forecast(steps=10)

    # Print the forecasted amounts
    print(forecast)

    # Evaluate the model on the test set
    test_predictions = model_fit.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1)

    # Create a DataFrame with actual and predicted amounts
    evaluation = pd.DataFrame({'date': test_data.index, 'actual_amount': test_data['amount_dollars'],
                               'predicted_amount': test_predictions})

    # Print the evaluation results
    print(evaluation)

# --------------------------------------------------------------------------------------------------------------------
    # Extract the modified merchant data
    # mod_data = genData(5732, data_csv)
    # mod_data.to_csv('cac.csv', index=False)

    # Check if stationary
    # stationaryTests(testing_data)

    # Seems like its stationary so ARIME seems like a solid choice.

    # Perform ARIMA prediction
    # print(mod_data.columns.tolist())
    # arima_data = arimaPrediction(mod_data, 10)

    # Print the predicted data
    # arima_data.to_csv('results.csv', index=False)
