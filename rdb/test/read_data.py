## libraries
import os
import warnings
import psycopg2
import pandas as pd
from datetime import datetime

## const
DB_NAME = str(os.getenv(key = 'DB_NAME', default = 'idle'))
DB_USER = str(os.getenv(key = 'DB_USER', default = 'user'))
DB_PASS = str(os.getenv(key = 'DB_PASS', default = 'pass'))
DB_HOST = str(os.getenv(key = 'DB_HOST', default = 'localhost'))
DB_PORT = int(os.getenv(key = 'DB_PORT', default = 5432))
LOG_LEVEL = str(os.getenv(key = 'LOG_LEVEL', default = 'INFO'))

## connect to database
def db_conn():
    return psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )

## query the database
def db_read(conn):
    query = """
            SELECT *
            FROM (
                SELECT
                    agency.*,
                    events.vehicle_id,
                    events.trip_id,
                    events.route_id,
                    events.latitude,
                    events.longitude,
                    events.datetime,
                    events.duration,
                    LAG(datetime, 1) OVER (ORDER BY datetime) AS prev_datetime
                FROM agency
                INNER JOIN events ON agency.iata_id = events.iata_id
            ) t
            WHERE (prev_datetime IS NULL AND datetime IS NOT NULL)
            OR (prev_datetime IS NOT NULL AND datetime - prev_datetime <= 600)
            ORDER BY datetime;
            """

    data = pd.read_sql_query(query, conn)
    if data['datetime'].isnull().any():
        raise ValueError("NaN values found in 'datetime' column after loading.")

    return data.drop(['prev_datetime'], axis = 1)

## find 24-hour periods
def get_periods(data):
    """
    Desc:
        Divide the DataFrame into contiguous 24-hour periods with no gaps longer
        than 10 minutes.

    Args:
        data: DataFrame (default: None)
    
    Returns:
        A list of DataFrames.

    Exceptions:
        None
    """

    ## init
    periods = []
    start_time = data['datetime'].min()
    end_time = data['datetime'].max() + 86400

    ## divide into contiguous 24-hour periods with no gaps longer than 10 min
    while start_time < end_time:
        end_period = start_time + 86400
        data_period = data[
            (data['datetime'] >= start_time) & (data['datetime'] < end_period)
        ]

        ## check for gaps longer than 10 minutes within the period
        diffs = data_period['datetime'].diff()
        if (diffs > 600).any():
            gap_index = diffs[diffs > 600].index[0]
            start_time = data_period.loc[gap_index, 'datetime']
        else:
            periods.append(data_period)
            start_time = end_period

        return periods

## save csv data to disk
def to_csv(data_period, output_dir, data_index):

    ## ensure dataframe is not empty and 'datetime' column has no null vals
    if not data_period.empty and data_period['datetime'].notnull().all():
        datetime_min = data_period['datetime'].min()

        ## ensure 'datetime_min' has valid timestamp and save to disk
        if pd.notnull(datetime_min):
            date = datetime.fromtimestamp(datetime_min)
            name = f"test-data-{date.strftime('%Y-%m-%d')}.csv"
            path = os.path.join(output_dir, name)
            data_period.to_csv(path, index = False)
            print(f"Saved {path}")
        else:
            pass
    else:
        pass

## execute
def main():

    ## suppress warnings
    warnings.filterwarnings('ignore', category = UserWarning)

    ## database operations
    conn = db_conn() ## connect to database
    data = db_read(conn = conn) ## query the database
    conn.close() ## close the connection

    ## csv filepath
    dir = './rdb/test/data/'
    os.makedirs(name = dir, exist_ok = True)

    ## save csv data to disk
    periods = get_periods(data = data)
    for index, period in enumerate(periods):
        to_csv(
            data_period = period, 
            output_dir = dir, 
            data_index = index
        )

if __name__ == "__main__":
    main()