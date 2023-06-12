import pandas as pd
from matplotlib import pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
import warnings


def cleanData(data: pd.DataFrame) -> [pd.DataFrame]:
    # Convert 'datetime' column to date if not already
    if not isinstance(data['datetime'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        data['datetime'] = pd.to_datetime(data['datetime']).dt.date

    # Change cents into dollars for purchases
    purchases = data.copy()
    purchases.loc[:, 'amount_dollars'] = purchases['amount_cents'] / 100
    purchases = purchases[purchases['transaction_type'] == 'PurchaseActivity']

    # Group by 'datetime' and 'merchant_type_code' and sum the 'amount_dollars'
    daily_purchases = purchases.groupby(['datetime', 'merchant_type_code'], as_index=False)['amount_dollars'].sum()
    daily_purchases = daily_purchases.reset_index(drop=True).set_index('datetime')

    # Get the training and testing sets
    test = daily_purchases[daily_purchases['merchant_type_code'] == 5732]
    print(test)
    train = daily_purchases[daily_purchases['merchant_type_code'] != 5732]

    return test[-13:], train


if __name__ == '__main__':
    # Read the dataset
    df = pd.read_csv("combined_transactions.csv")

    test_set, train_set = cleanData(df)
    print(test_set.shape, train_set.shape)

    # merge them to fit them in the model (wishing I could upload two datasets instead of a concatenated one)
    model_set = pd.concat([train_set, test_set], axis=0)
    # Checking the best values for the order
    stepFit = auto_arima(train_set['amount_dollars'], trace=True, suppress_warnings=True)
    stepFit.summary()

    # Select the 'amount_dollars' column for modeling
    amount_series = model_set['amount_dollars']

    # Apply differencing to make the data more stationary
    amount_series_diff = amount_series.diff().dropna()

    # Reset the index of amount_series and set it to the datetime column
    # amount_series = amount_series.reset_index(drop=True)

    # Fit the ARIMA model
    warnings.filterwarnings("ignore")
    model = ARIMA(amount_series, order=(0, 0, 2))
    model_fit = model.fit()

    # Forecast the next day
    forecast = model_fit.forecast(steps=10)
    warnings.resetwarnings()

    # Print the forecasted amount
    # print(forecast)

    # Generate predictions for the entire dataset
    predictions = model_fit.predict(start=len(train_set), end=len(train_set) + len(test_set) - 1)

    # print(predictions)

    # Create a DataFrame with actual and predicted amounts
    evaluation = pd.DataFrame({'actual_amount': test_set["amount_dollars"],
                               'predicted_amount': predictions})

    # Print the evaluation results
    print(evaluation)

    mae = mean_absolute_error(evaluation['actual_amount'], evaluation['predicted_amount'])
    print("Mean Absolute Error:", mae)

    # Plot the test set and predictions
    plt.plot(evaluation.index, evaluation['actual_amount'], label='Actual Amount')
    plt.plot(evaluation.index, evaluation['predicted_amount'], label='Predicted Amount')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Test Set vs Predictions')
    plt.legend()
    plt.show()
