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
def get_periods(data: pd.DataFrame) -> list:
    """
    Desc:
        Split the data into non-overlapping 24-hour segments with no single gap
        larger than 10 minutes. Once a contiguous window >= 24 hours is reached,
        it is finalized and appended to the result.

    Args:
        data (pd.DataFrame): Assumed to have at least one column named 'datetime'
                            containing Unix timestamps. Must be sorted or will
                            be sorted by 'datetime'.

    Returns:
        periods (list): A list of DataFrame segments, each covering >= 24 hours
                        with no gap > 10 minutes.
    """

    ## sort by datetime 
    data = data.sort_values('datetime', ascending = True).reset_index(drop = True)
    if data.empty:
        return []

    ## init vars
    periods = []
    chunk_start = 0  ## start index for the current 24-hour window
    min_24h = 86400  ## 24 hours in seconds
    max_gap = 600  ## 10 minutes in seconds

    ## single pass through the data
    for i in range(1, len(data)):
        gap = data.loc[i, 'datetime'] - data.loc[i - 1, 'datetime']

        ## check if a gap exceeds 10 minutes
        if gap > max_gap:
            if (data.loc[i - 1, 'datetime'] - data.loc[chunk_start, 'datetime']) >= min_24h:
                chunk_df = data.iloc[chunk_start:i]
                periods.append(chunk_df)
            chunk_start = i  ## start a new window from current row

        else:
            if (data.loc[i, 'datetime'] - data.loc[chunk_start, 'datetime']) >= min_24h:
                chunk_df = data.iloc[chunk_start:(i + 1)]
                periods.append(chunk_df)
                chunk_start = i + 1  ## next window starts from the next row after

    ## check for leftover segment at the end of 24 hours
    last_i = len(data) - 1
    if chunk_start < len(data):
        if (data.loc[last_i, 'datetime'] - data.loc[chunk_start, 'datetime']) >= min_24h:
            chunk_df = data.iloc[chunk_start:]
            periods.append(chunk_df)

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