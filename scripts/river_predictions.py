import numpy as np
import pandas as pd
from prophet import Prophet
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler


# Function to check if a year is a leap year
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# Apply sin/cos transformation
def transform_day_of_year(row):
    max_days = 366 if is_leap_year(row["year"]) else 365
    sin_val = np.sin(2 * np.pi * row["day_of_year"] / max_days)
    cos_val = np.cos(2 * np.pi * row["day_of_year"] / max_days)
    return pd.Series({"day_of_year_sin": sin_val, "day_of_year_cos": cos_val})


# Apply the transformation to the DataFrame

df = pd.read_csv("river.csv")
# Sin/Cos transformation for 'month'
df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

# Sin/Cos transformation for 'day_of_year'
df[["day_of_year_sin", "day_of_year_cos"]] = df.apply(transform_day_of_year, axis=1)

df.drop(columns=["SNWD", "month", "year", "day_of_year"], inplace=True)

# Scale columns
year = 2021
# peak_dates = []
# for year in chain(range(2000, 2012), range(2013, 2024)):
print(f"Running model for {year}")
train_df = df[df["date"] < f"{year}-04-01"]
test_df = df[(df["date"] >= f"{year}-04-01") & (df["date"] < f"{year}-08-01")]
scale_cols = ["flow_min", "PREC", "TOBS", "WTEQ", "tmin", "tmax", "oni"]
scaler = StandardScaler()
scaler.fit(train_df[scale_cols])

train_scaled = train_df.copy()
train_scaled[scale_cols] = scaler.transform(train_df[scale_cols])

test_scaled = test_df.copy()
test_scaled[scale_cols] = scaler.transform(test_df[scale_cols])


# Prophet model with regressors
train_scaled["ds"] = train_scaled["date"]
train_scaled["y"] = train_scaled["flow_max"]
test_scaled["ds"] = test_scaled["date"]
train_scaled.dropna(inplace=True)
test_scaled.dropna(inplace=True)
# test_scaled['y'] = test_scaled['flow_max']
# import ipdb; ipdb.set_trace()
# train_scaled['y'] = train_scaled['flow_max']

model = Prophet()
regressor_cols = [
    "PREC",
    "TOBS",
    "WTEQ",
    "tmin",
    "tmax",
    "oni",
    "month_sin",
    "month_cos",
    "day_of_year_sin",
    "day_of_year_cos",
]
for col in regressor_cols:
    model.add_regressor(col)
model = model.fit(df=train_scaled)

# future = model.make_future_dataframe(periods=122, freq='D')
forecast = model.predict(test_scaled)
actual_date = str(test_scaled.loc[test_scaled["flow_max"].idxmax()].ds)
peak_date = str(forecast.loc[forecast["yhat"].idxmax()].ds.date())
print(f"Actual peak date: {actual_date}")
print(f"Predict Peak date: {peak_date}")
# peak_dates.append((actual_date, peak_date))
model.plot(forecast)
# plt.title('Prophet Forecast')
plt.xlabel("Date")
plt.ylabel("y")
plt.legend(
    ["Historical Data", "Forecast (yhat)", "Uncertainty Interval"], loc="upper left"
)
plt.show()

# # Benchmark model with no regressors
# df['ds'] = df['date']
# df['y'] = df['flow_max']

# train_df = df[df['date'] < '2024-04-01']
# test_df = df[(df['date'] >= '2024-04-01') & (df['date'] < '2024-08-01')]
# import ipdb; ipdb.set_trace()
# model = Prophet()
# model = model.fit(df=train_df)
# future = model.make_future_dataframe(periods=122, freq='D')

# forecast = model.predict(future)
# model.plot(forecast)
# plt.title('Prophet Forecast')
# plt.xlabel('Date')
# plt.ylabel('y')
# plt.legend(['Historical Data', 'Forecast (yhat)', 'Uncertainty Interval'], loc='upper left')
# plt.show()

# date               2024-06-08
# flow_min               2570.0
# flow_max               3430.0
# PREC                24.666667
# TOBS                47.004167
# WTEQ                12.429167
# tmin                    46.76
# tmax                    65.12
# oni                       0.2
# month_sin                 0.0
# month_cos                -1.0
# day_of_year_sin      0.384665
# day_of_year_cos     -0.923056
# ds                 2024-06-08
# y                      3430.0
# Name: 8925, dtype: object
# print(peak_dates)
# [
#      Actual          Predicted
#     ('2000-05-30','2000-07-31'),
#     ('2001-06-02','2001-05-02'),
#     ('2002-06-01','2002-05-29'),
#     ('2003-05-30','2003-06-01'),
#     ('2004-06-08','2004-05-31'),
#     ('2005-05-24','2005-06-02'),
#     ('2006-05-23','2006-05-28'),
#     ('2007-05-20','2007-05-31'),
#     ('2008-06-03','2008-05-30'),
#     ('2009-05-19','2009-05-31'),
#     ('2010-06-06','2010-05-28'),
#     ('2011-07-08','2011-05-31'),
#     ('2013-06-10','2013-06-03'),
#     ('2014-05-30','2014-06-03'),
#     ('2015-06-17','2015-06-04'),
#     ('2016-06-11','2016-06-04'),
#     ('2017-06-09','2017-06-08'),
#     ('2018-05-26','2018-06-07'),
#     ('2019-07-01','2019-06-07'),
#     ('2020-06-02','2020-06-05'),
#     ('2021-06-05','2021-06-07'),
#     ('2022-06-12','2022-06-07'),
#     ('2023-06-09','2023-06-08')
# ]
