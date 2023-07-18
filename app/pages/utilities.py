#  Local - page specific Data wrangling and preprocessing
#  Could be get use of app.utils functionalities as well
import pandas as pd

# read the data 
## Data file paths 
final_path = './archive order/final.csv'
order_path = './archive order/order.csv'

def load_df():
    return pd.read_csv('./data/prep_df.csv')

def load_gif():
    pass


# ============== Temporal Data Prep ==============================

## = order count Vs time =

def get_orders_over_time(df):
    cdf = df.copy()
    cdf['date'] = pd.to_datetime(cdf['date'])

    daily_order_count_series = cdf.groupby(['date'])['date'].count()
    daily_order_count_list = [(str(i).split(' ')[0], int(j)) for i,j in zip(list(daily_order_count_series.index), list(daily_order_count_series.values))]
    return daily_order_count_list

