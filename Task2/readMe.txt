ARIMA Model for Transaction Data

This code implements an ARIMA (AutoRegressive Integrated Moving Average) model to forecast transaction amounts based on historical data. The code reads transaction data from a CSV file, cleans the data, trains the ARIMA model, and generates predictions for the test set.


** Summary

Tl;DR: I determined that the data was stationary with an ADF test, employment of the Auto Arima library and visual inspections through scatter and line plots.
       ADF Statistic: -7.798311117160032
       p-value: 7.612023769124106e-12

       I assumed for mainV2 that we could discard any returns since we wanted a "raw purchase" projection,
       I grouped the data by datetime and merchantCode and summed purchases on a daily interval before running the ARIMA model on it and checking results with MAE.

       I assumed for mainV3 that we should not discard return data as we could use it to predict our earnings with it,
       which might be more valuable than raw purchases for staffing needs/budgeting. I set all return data as negative so that when I grouped by datetime and merchant code their sum would
       cancel out their purchase counterpoints. Everything else was exactly like the previous model.

I would like to start off by saying that I had not worked with statistical analysis for a while, so my skills were rusty, and I had a steep learning curve. I would like to thank you for
providing me with this opportunity because it proved to be a great learning experience.

To begin, I examined the data to understand its structure and the available columns. This allowed me to prepare and clean the data accordingly. I focused on grouping the purchases on a
daily basis to calculate the net purchase per merchant code. I excluded the returns from the analysis.

Once I obtained this daily purchase data, I selected the merchant code assigned to me and performed tests to determine if the data was stationary.
Stationarity is an important characteristic for time series analysis.
I conducted an augmented Dickey–Fuller test and obtained values suggesting that the data was indeed stationary (ADF Statistic: -7.798311117160032, p-value: 7.612023769124106e-12).
Stationary test code in mainDeprecated.py under the stationaryTests function

Next, I visually inspected the data by plotting scatter and line plots (see figures 1 and 2).
Based on the visual inspection and stationary test results, I concluded that the ARIMA model would be suitable for further analysis.

To confirm this, I used the auto_arima function which also identified the best order for the ARIMA model. Once I had a working model (implemented in 'mainV2'), I decided to incorporate return data as well.
By including return data, I aimed to predict net daily earnings, which would provide a valuable insight alongside raw daily purchases.

Initially, I only used the data corresponding to merchant_type_code = 5732 for training.
However, through experimentation, I found that including the rest of the data for training yielded better results.
Interestingly, excluding the final 13 items from merchant_type_code = 5732 when using returns resulted in a lower MAE, and excluding the final 16 items from merchant_type_code = 5732 during testing also yielded a lower MAE.

I chose to use MAE (Mean Absolute Error) as the evaluation metric because the data contained some outlier days that would be heavily penalized by metrics like MSE or RMSE.

Here are the results I obtained:

Net Daily Purchases MAE: 507.7127497987443
Net Daily Earnings MAE: 449.96884861153814

These results provide an assessment of the model's accuracy in predicting the net daily purchases and earnings.
Overall, the analysis provided valuable insights and highlighted the importance of incorporating return data for more comprehensive predictions.

NOTE: In a professional environment, I would have discussed the creation of a net daily earnings with my team as to see if its value is worth the time implementing it, I would also have a doc with
      my assumptions and intentions as to wage which direction would be best for the project.

** Improvements

Having a larger data set would be better, I would also be able to check for seasonality if the date range was larger than a couple of months (which in turn would lead me to use SARIMAX or maybe
even an entirely different model).

I tried implementing differentiation, but any attempt I had with it would fill my evaluations with NAN values which in turn broke MAE. It might be worth looking into this, specially given the
outliers in the data that would be compensated by this.

I could also combine the forecasts of several ARIMA models with different parameters (maybe even other forecasting methods) to attempt and crete a more robust model.

** File Description:
- `combined_transactions.csv`: Input CSV file containing transaction data.
- `mainDeprecated.py`: The first attempt I had at a model, I kept it to show my thinking process for this problem. I also have the code I used to determine if the data was stationary or not here.
- `mainV2.py`: The first working model I did.
- `mainV3.py`: A modified version of the mainV2, although I have some questions as to its validity. Thought I would include both for the sake of conversation.

** Dependencies:
- pandas: Data manipulation library.
- matplotlib: Data visualization library.
- pmdarima: Auto ARIMA library for selecting the optimal model order.
- scikit-learn: Machine learning library for computing the mean absolute error (MAE).
- statsmodels: Library for time series analysis and modeling.

** Usage:
1. Place the input CSV file (`combined_transactions.csv`) in the same directory as the scripts.
2. Run the `mainV*.py` script to execute the ARIMA model.
3. The script will clean the data, train the ARIMA model, generate predictions, and display the evaluation results and a plot of the test set vs predictions.

** Note:
- Make sure to install the required dependencies before running the code.
- Modify the file paths or data cleaning steps according to your dataset structure if needed.