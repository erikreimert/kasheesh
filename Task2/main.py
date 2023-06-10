import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA


def genTrainData(merchant_type_code: int, merchant: pd.DataFrame) -> pd.DataFrame:
    """
    Generate training data by filtering out rows with a specific merchant_type_code and applying data cleaning.

    Args:
        merchant_type_code (int): The merchant type code to exclude from the training data.
        merchant (pd.DataFrame): The original merchant data.

    Returns:
        pd.DataFrame: The cleaned training data.

    """

    merchant['datetime'] = pd.to_datetime(merchant['datetime'])
    filtered_merchant = merchant[merchant['merchant_type_code'] != merchant_type_code]
    # Convert 'datetime' column to datetime data type. NOTE: odd that this didn't happen automatically
    trainingData = cleanData(filtered_merchant)

    return trainingData


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
    result = adfuller(data['amount_cents'])

    # Extract and print the test statistics and p-value
    adf_statistic = result[0]
    p_value = result[1]
    print("ADF Statistic:", adf_statistic)
    print("p-value:", p_value)

    # Line plotting
    data.plot(x='datetime', y='amount_cents')
    plt.title('Time Series Data')
    plt.xlabel('Datetime')
    plt.ylabel('Amount In Cents')
    plt.show()

    # Scatter plotting
    plt.scatter(data['datetime'], data['amount_cents'])
    plt.title('Scatter Plot of Time Series Data')
    plt.xlabel('Datetime')
    plt.ylabel('Amount In Cents')
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
                        datetime  amount_cents transaction_type
        0  2023-01-01 08:00:00          5000  PurchaseActivity
        1  2023-01-01 09:30:00          3500  PurchaseActivity
        2  2023-01-02 12:15:00          4500  PurchaseActivity
        3  2023-01-02 18:45:00          2800  PurchaseActivity
        4  2023-01-03 09:00:00          3200  PurchaseActivity

    """

    # Drop rows we don't really need
    merchant = merchant.drop('user_id', axis=1)
    merchant = merchant.drop('merchant_type_code', axis=1)

    # Separate the purchases and returns into separate DataFrames
    purchases = merchant[merchant['transaction_type'] == 'PurchaseActivity']
    returns = merchant[merchant['transaction_type'] == 'ReturnActivity']

    # Extract the dates from purchases and returns
    purchase_dates = purchases['datetime'].dt.date
    return_dates = returns['datetime'].dt.date

    # Drop the purchase rows where the items were returned. We do this based on amounts and transaction date.
    # Really wish I had a transactionID to work with in here instead.
    filtered_purchases = purchases[
        ~((purchases['amount_cents'].isin(returns['amount_cents'])) & (purchase_dates.isin(return_dates)))]

    filtered_purchases.set_index('datetime')

    return filtered_purchases


def extractMerch(merchant_type_code: int, data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the merchant data for merchant_type_code 5732 from a CSV file and sets the ReturnActivity values as
    negative.

    Args:
    merchant_type_code (int): The merchant_type_code to be filtered by
    data (pd.DataFrame): The pd.Dataframe to be analyzed

    Returns:
        pandas.DataFrame: The extracted merchant data.

    Example:
           user_id  amount_cents             datetime  merchant_type_code
        0     1234          5000  2023-01-01 08:00:00                5732
        1     5678          3500  2023-01-01 09:30:00                5732
        2     9012          4500  2023-01-02 12:15:00                5732
        3    34567          2800  2023-01-02 18:45:00                5732
        4    89012          3200  2023-01-03 09:00:00                5732
    """
    # Convert 'datetime' column to datetime data type. NOTE: odd that this didn't happen automatically
    data['datetime'] = pd.to_datetime(data['datetime'])
    merchant = data.loc[data['merchant_type_code'] == merchant_type_code].reset_index(drop=True)

    filtered_purchases = cleanData(merchant)

    return filtered_purchases


def arimaPrediction(train_data: pd.DataFrame, test_data: pd.DataFrame, n_periods: int) -> pd.DataFrame:
    """
    Perform ARIMA prediction on the provided time series data.

    Args:
        train_data (pandas.DataFrame): The training time series data.
        test_data (pandas.DataFrame): The testing time series data.
        n_periods (int): The number of periods to forecast.

    Returns:
        pandas.DataFrame: A DataFrame with datetime, actual amounts, and predicted amounts.

    Example:
        train_data = pd.read_csv("train_data.csv")
        test_data = pd.read_csv("test_data.csv")
        prediction_data = arimaPrediction(train_data, test_data, n_periods=10)

    """
    # Reset index of train_data and test_data
    train_data = train_data.reset_index(drop=True)
    test_data = test_data.reset_index(drop=True)

    # Fit the ARIMA model using training data
    model = ARIMA(train_data['amount_cents'], order=(1, 0, 1))
    model_fit = model.fit()

    # Generate predictions for the specified number of periods
    predictions = model_fit.predict(start=len(train_data), end=len(train_data) + len(test_data) + n_periods - 1)

    # Create a DataFrame with datetime, actual amounts, and predicted amounts
    res = pd.DataFrame({'datetime': pd.concat([train_data['datetime'], test_data['datetime']], ignore_index=True),
                        'actual_amount': pd.concat([train_data['amount_cents'], test_data['amount_cents']],
                                                   ignore_index=True),
                        'predicted_amount': predictions[-(len(test_data) + n_periods):]})

    return res


if __name__ == '__main__':
    file = pd.read_csv(r"combined_transactions.csv")

    # Extract the modified merchant data
    testing_data = extractMerch(5732, file)

    # Check if stationary
    stationaryTests(testing_data)

    # Seems like its stationary so ARIME seems like a solid choice.
    training_data = genTrainData(5732, file)

    # Perform ARIMA prediction
    arima_data = arimaPrediction(training_data, testing_data, 10)

    # Print the predicted data
    print(arima_data)
