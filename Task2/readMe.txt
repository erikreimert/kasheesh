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

I would like to start off by saying that I had not worked with statistical analysis for a while so my skills were rusty and I had a steep learning curve. I would like to thank you for that
because this proved to be a great learning experience. At first, I took a glance at the data to see what I was working with, I was interested to know what different columns and fields were inside
those columns as to prune and prep the data accordingly. I decided to group purchases on a daily basis as to have a net purchase per merchant code to train the data and to exclude returns.
Once I had this data, I selected the merchant code that was assigned to me and ran some tests to figure out if the data was stationary or not, this would inform the model I would select.
I ran an augmented Dickey–Fuller test and got values that suggested the data was stationary (ADF Statistic: -7.798311117160032, p-value: 7.612023769124106e-12).
I then plotted the data into scatter and line plots and visually inspected it (see figures 1 and 2, stationary test code in mainDeprecated.py under the stationaryTests function).
At this point I decided that the data was stationary and that ARIMA would be the best model to proceed with.
I then used auto arima to confirm this and find the best order to run my ARIMA model on. After I had a working model with 'mainV2' ("mainDeprecated" was a bust and I
decided to start fresh) I decided to create a third model, except that this time I would include return data, I thought that in including return data I could get predictions on net daily earnings,
which would prove valuable in tandem to raw daily purchases. I also initially only used the data corresponding to merchant_type_code = 5732 for training, but I found that using the rest of the data for
training proved to give me best results (also oddly enough, excluding the final 13 items from 5732 when using returns yielded a lower MAE and excluding the final 16 items from 5732 when testing yielded a lower MAE.
I chose to use MAE (Mean absolute error) as the data had some outlier days that would be punished to heavily by MSE, RMSE, etc…
These are the results I got (see figures 3 and 4 for net daily purchases and net daily earnings correspondingly):
net daily purchases MAE: 507.7127497987443
net daily earnings MAE: 449.96884861153814

NOTE: In a professional environment, I would have discussed the creation of a net daily earnings with my team as to see if its value is worth the time implementing it, I would also have a doc with
      my assumptions and intentions as to wage which direction would be best for the project.

** Improvements

Having a larger data set would be better, I would also be able to check for seasonality if the date range was larger than a couple of months (which in turn would lead me to use SARIMAX or maybe
even an entirely different model).

I tried implementing differentiation, but any attempt I had with it would fill my evaluations with NAN values which in turn broke MAE. It might be worth looking into this, specially given the
outliers in the data that would be compensated by this.

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